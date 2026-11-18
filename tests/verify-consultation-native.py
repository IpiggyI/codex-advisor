#!/usr/bin/env python3
"""Check bounded native I/O, completion gates, and complete request instructions."""

import copy
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import threading
import time
import types
import unittest
from unittest import mock

sys.dont_write_bytecode = True
PLUGIN = Path(__file__).resolve().parent.parent / 'plugins/codex-advisor'
sys.path.insert(0, str(PLUGIN / 'scripts'))
import consult_native as native
from consult_context import Failure, ITEM_POLICY, CONTENT_POLICY, validate_items, reconstruct

EXPECTED = {'model': 'gpt-6.2-sol', 'effort': 'xhigh'}
CALLER = {'base': 'BASE_CONSTRAINT', 'thread': 'caller', 'items': [
    {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'FIRST_CONSTRAINT'}]},
    {'type': 'message', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': 'LAST_SOURCE'}]}]}
ADVICE = {'kind': 'plan', 'advice': 'Keep the complete context.'}


def message(text, role='developer'):
    return {'type': 'message', 'role': role, 'content': [{'type': 'input_text', 'text': text}]}


def completed():
    return [{'method': 'item/completed', 'params': {'threadId': 'advisor', 'turnId': 'turn',
             'item': {'type': 'agentMessage', 'phase': 'final_answer', 'text': json.dumps(ADVICE)}}},
            {'method': 'turn/completed', 'params': {'threadId': 'advisor', 'turnId': 'turn',
             'turn': {'id': 'turn', 'status': 'completed'}}}]


class HistoryPolicy(unittest.TestCase):
    def test_named_function_outputs_without_calls_are_preserved(self):
        for identity in ({}, {'call_id': None}):
            item = {'type': 'function_call_output', 'name': 'codex_apps_open_page',
                    'namespace': 'agent', 'output': 'PAGE_CONTEXT', **identity}
            with self.subTest(identity=identity):
                self.assertEqual(validate_items([item]), [item])
                native.verify_history({'input': [item]}, {'items': [item]})
                for changed in ([], [{**item, 'output': 'CHANGED'}],
                                [{**item, 'name': 'different'}], [{**item, 'namespace': 'different'}]):
                    with self.assertRaises(Failure):
                        native.verify_history({'input': changed}, {'items': [item]})

    def test_named_outputs_do_not_hide_incomplete_or_invalid_pairs(self):
        output = {'type': 'function_call_output', 'name': 'page', 'namespace': 'agent', 'output': ''}
        call = {'type': 'function_call', 'call_id': 'pending', 'name': 'page', 'arguments': '{}'}
        for items in ([call, output], [{**output, 'call_id': 'missing'}],
                      [{**output, 'call_id': ''}], [{**output, 'name': ''}],
                      [{**output, 'name': None}], [{**output, 'namespace': 1}],
                      [{'type': 'function_call_output', 'output': ''}],
                      [{**output, 'type': 'custom_tool_call_output'}]):
            with self.subTest(items=items), self.assertRaises(Failure) as raised:
                validate_items(items)
            self.assertEqual(raised.exception.code, 'pairing')

    def test_web_search_optional_fields_are_excluded(self):
        for item in (
                {'type': 'web_search_call', 'status': 'completed', 'action': {'type': 'search'}},
                {'type': 'web_search_call', 'id': 'web', 'status': 'completed',
                 'action': {'type': 'search'}, 'internal_chat_message_metadata_passthrough': {}},
                {'type': 'web_search_call', 'status': 'completed'},
                {'type': 'web_search_call'}):
            with self.subTest(keys=list(item)):
                self.assertEqual(validate_items([item]), [])
                native.verify_history({'input': []}, {'items': [item]})

    def test_protocol_required_fields_and_pairing(self):
        for item in (message(''), {'type': 'message', 'role': 'future_role', 'content': []},
                     {'type': 'agent_message', 'author': '', 'recipient': '', 'content': []},
                     {'type': 'reasoning', 'summary': []},
                     {'type': 'message', 'role': 'user', 'content': [{'type': 'input_image'}]}):
            self.assertEqual(validate_items([item]), [item])
        call = {'type': 'tool_search_call', 'execution': 'server', 'arguments': None}
        result = {'type': 'tool_search_output', 'execution': 'server', 'status': 'completed', 'tools': []}
        self.assertEqual(validate_items([call, result]), [])
        for index, field in ((0, 'arguments'), (0, 'execution'), (1, 'execution'), (1, 'status'), (1, 'tools')):
            pair = copy.deepcopy([call, result])
            del pair[index][field]
            with self.assertRaises(Failure):
                validate_items(pair)
        for item in ({'type': 'reasoning'}, {'type': 'additional_tools', 'tools': []}):
            with self.assertRaises(Failure):
                validate_items([item])

    def test_policy_controls_injection_and_comparison(self):
        item = {'type': 'web_search_call', 'id': 'web', 'status': 'completed',
                'action': {'type': 'search', 'query': 'PRIVATE_QUERY'}}
        self.assertEqual(validate_items([item]), [])
        self.assertEqual(native.verify_history({'input': []}, {'items': [item]}), -1)
        with mock.patch.dict(ITEM_POLICY['web_search_call'], policy='preserve'):
            self.assertEqual(validate_items([item]), [item])
            with self.assertRaises(Failure):
                native.verify_history({'input': []}, {'items': [item]})
        with mock.patch.dict(ITEM_POLICY['web_search_call'], policy='reject'):
            with self.assertRaises(Failure):
                validate_items([item])

    def test_unknown_items_and_blocks_remain_exact(self):
        items = [{'type': 'future_item', 'id': 'KEEP_ID', 'nullable': None, 'text': 'PRIVATE_TEXT'},
                 message('PRIVATE_MESSAGE'),
                 {'type': 'message', 'role': 'user', 'content': [
                     {'type': 'future_block', 'id': 'KEEP_BLOCK', 'text': 'PRIVATE_BLOCK'}]}]
        self.assertEqual(validate_items(items), items)
        self.assertEqual(native.comparable(items[0]), {'type': 'future_item', 'text': 'PRIVATE_TEXT'})
        native.verify_history({'input': items}, {'items': items})
        for index in range(len(items)):
            for change in ('drop', 'rewrite'):
                request = copy.deepcopy(items)
                if change == 'drop':
                    request.pop(index)
                elif index == 0:
                    request[index]['text'] = 'CHANGED_PRIVATE'
                else:
                    request[index]['content'][0]['text'] = 'CHANGED_PRIVATE'
                with self.assertRaises(Failure) as raised:
                    native.verify_history({'input': request}, {'items': items, 'hostVersion': 'test-host'})
                error = raised.exception
                self.assertEqual(error.code, 'context')
                self.assertEqual(error.details['stage'], 'request')
                self.assertEqual(error.details['hostVersion'], 'test-host')
                self.assertIn('path', error.details)
                self.assertNotIn('PRIVATE', str(error) + json.dumps(error.details))
        request = copy.deepcopy(items)
        request[1]['content'][0]['text'] = 'CHANGED_PRIVATE'
        with self.assertRaises(Failure) as raised:
            native.verify_history({'input': request}, {'items': items})
        self.assertEqual(raised.exception.details['path'], 'content[0].text')

    def test_undeclared_items_normalize_only_transport_fields(self):
        item = {'type': 'future_generation_call', 'status': 'completed', 'result': 'PRIVATE_RESULT'}
        transported = dict(item, id='image_synthetic', nullable=None,
                           internal_chat_message_metadata_passthrough={'turn_id': 'synthetic'})
        self.assertNotIn(item['type'], ITEM_POLICY)
        self.assertEqual(validate_items([transported]), [transported])
        self.assertEqual(native.comparable(transported), item)
        for source, request in ((item, transported), (transported, item)):
            native.verify_history({'input': [request]}, {'items': [source]})
            changed = dict(request, result='CHANGED_PRIVATE_RESULT')
            with self.assertRaises(Failure) as raised:
                native.verify_history({'input': [changed]}, {'items': [source]})
            self.assertEqual(raised.exception.code, 'context')
            self.assertEqual(raised.exception.details['path'], 'result')
            self.assertNotIn('PRIVATE', str(raised.exception) + json.dumps(raised.exception.details))

    def test_capability_pairs_are_validated_before_exclusion(self):
        call = {'type': 'tool_search_call', 'call_id': 'search', 'execution': 'client', 'arguments': {'query': 'tools'}}
        result = {'type': 'tool_search_output', 'call_id': 'search', 'execution': 'client', 'status': 'completed', 'tools': [{'name': 'tool'}]}
        self.assertEqual(validate_items([{'type': 'additional_tools', 'role': 'developer', 'tools': []}, call, result]), [])
        for items in ([call], [result], [result, call], [call, call, result]):
            with self.assertRaises(Failure) as raised:
                validate_items(items)
            self.assertEqual(raised.exception.code, 'pairing')
            self.assertIn('historyIndex', raised.exception.details)
        with mock.patch.dict(ITEM_POLICY['tool_search_output'], policy='preserve'):
            with self.assertRaises(Failure) as raised:
                validate_items([call, result])
            self.assertEqual(raised.exception.code, 'pairing')

    def test_content_policy_controls_both_paths(self):
        item = message('PRIVATE')
        with mock.patch.dict(CONTENT_POLICY['input_text'], policy='capability'):
            expected = dict(item, content=[])
            self.assertEqual(validate_items([item]), [expected])
            self.assertEqual(native.comparable(item), expected)

    def test_content_diagnostics(self):
        with self.assertRaises(Failure) as raised:
            validate_items([message(None)])
        self.assertEqual(raised.exception.details, {'stage': 'content', 'type': 'input_text',
                                                  'historyIndex': 0, 'contentIndex': 0})


class NativeLifecycle(unittest.TestCase):
    def test_windows_uses_npm_executor_when_first_catalog_lacks_exact_model(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            desktop = str(root / 'desktop' / 'codex.exe')
            shim = root / 'npm' / 'codex.cmd'
            npm = shim.parent / 'node_modules/@openai/codex/vendor/target/bin/codex.exe'
            npm.parent.mkdir(parents=True)
            npm.touch()
            resolve = {'codex.exe': desktop, 'codex.cmd': str(shim)}
            catalogs = {desktop: [{'slug': 'gpt-6.1-sol'}],
                        str(npm): [{'slug': EXPECTED['model'], 'use_responses_lite': True}]}

            def bundled(command, env, cwd):
                self.assertEqual(command[1:], ['debug', 'models', '--bundled'])
                process = mock.Mock(returncode=0)
                executable = desktop if command[0] == 'codex' else command[0]
                process.communicate.return_value = (json.dumps({'models': catalogs[executable]}), None)
                return process

            def discovery(env, root, values, cancel, deadline, executable):
                entry, = json.loads(Path(values['model_catalog_json']).read_text(encoding='utf-8'))['models']
                self.assertEqual(entry['slug'], EXPECTED['model'])
                self.assertTrue(entry['use_responses_lite'])
                self.assertEqual(entry['shell_type'], 'disabled')
                self.assertEqual(executable, str(npm))
                return set()

            server = mock.Mock()
            server.call.return_value = {'thread': {'id': 'advisor'}, 'turn': {'id': 'turn'}}
            with mock.patch.object(native, 'os', types.SimpleNamespace(name='nt', environ={})), \
                    mock.patch.object(native.shutil, 'which', side_effect=lambda name, path: resolve.get(name)), \
                    mock.patch.object(native, 'launch', side_effect=bundled) as launch, \
                    mock.patch.object(native, 'terminate'), \
                    mock.patch.object(native, 'server_names', side_effect=discovery), \
                    mock.patch.object(native, 'Server', return_value=server) as start, \
                    mock.patch.object(native, 'verify_isolation'), \
                    mock.patch.object(native, 'completion', return_value=ADVICE), \
                    mock.patch.object(native, 'verify_requests', return_value=EXPECTED):
                result = native.execute(root, CALLER, EXPECTED, threading.Event())
            self.assertEqual(result['actual'], EXPECTED)
            self.assertEqual([call.args[0][0] for call in launch.call_args_list], [desktop, str(npm)])
            self.assertEqual(start.call_args.args[-1], str(npm))

    def test_diagnostics_keep_only_bounded_event_metadata(self):
        clock = [10.0]
        with mock.patch.object(native.time, 'monotonic', side_effect=lambda: clock[0]):
            diagnostics = native.Diagnostics()
            with diagnostics.phase('completion'):
                clock[0] = 11.0
                diagnostics.observe({'method': 'item/agentMessage/delta', 'params': {'delta': 'PRIVATE_TEXT'}})
                clock[0] = 12.0
                diagnostics.observe({'method': 'error', 'params': {
                    'willRetry': True, 'error': {'message': 'PRIVATE_TOKEN',
                        'codexErrorInfo': {'responseStreamDisconnected': {'httpStatusCode': 503}}}}})
                clock[0] = 13.0
                diagnostics.observe({'method': 'PRIVATE_METHOD', 'params': {'secret': 'PRIVATE_VALUE'}})
                result = diagnostics.snapshot()
            self.assertEqual(result['phase'], 'completion')
            self.assertEqual(result['elapsedMs'], 3000)
            self.assertEqual(result['firstOutputMs'], 1000)
            self.assertEqual(result['lastEvent'], 'other')
            self.assertEqual(result['lastEventMs'], 3000)
            self.assertEqual(result['retryCount'], 1)
            self.assertEqual(result['lastRetry'], {'nativeCode': 'responseStreamDisconnected', 'httpStatusCode': 503})
            self.assertEqual(diagnostics.snapshot()['phaseTimingsMs'], {'completion': 3000})
            self.assertNotIn('PRIVATE', json.dumps(result))

    def test_startup_timeout_reports_phase_before_any_request(self):
        with mock.patch.object(native, 'catalog', side_effect=Failure('timeout', 'Expired.')):
            with self.assertRaises(Failure) as raised:
                native.execute(Path('unused'), CALLER, EXPECTED, threading.Event())
        self.assertEqual(raised.exception.details['nativeExecution']['phase'], 'catalog')

    def test_receive_tracks_retry_and_terminal_event_without_output_text(self):
        server = native.Server.__new__(native.Server)
        server.cancel, server.deadline = threading.Event(), time.monotonic() + 5
        server.pending, server.messages = [], native.queue.Queue()
        server.diagnostics = native.Diagnostics()
        server.messages.put({'method': 'error', 'params': {
            'threadId': 'advisor', 'turnId': 'turn', 'willRetry': True,
            'error': {'message': 'PRIVATE_ERROR', 'codexErrorInfo': 'serverOverloaded'}}})
        for event in completed():
            server.messages.put(event)
        self.assertEqual(native.completion(server, 'advisor', 'turn'), ADVICE)
        result = server.diagnostics.snapshot()
        self.assertEqual(result['retryCount'], 1)
        self.assertEqual(result['lastEvent'], 'turn/completed')
        self.assertEqual(result['lastRetry'], {'nativeCode': 'serverOverloaded'})
        self.assertNotIn(ADVICE['advice'], json.dumps(result))
        self.assertNotIn('PRIVATE', json.dumps(result))

    def test_cleanup_does_not_replace_completion_timeout_phase(self):
        server = types.SimpleNamespace(initialize=lambda: None, close=lambda: None,
                                      call=lambda *args: {'thread': {'id': 'advisor'}, 'turn': {'id': 'turn'}})
        with mock.patch.object(native, 'catalog', return_value=(Path('models.json'), 'codex')), \
                mock.patch.object(native, 'server_names', return_value=set()), \
                mock.patch.object(native, 'Server', return_value=server), \
                mock.patch.object(native, 'verify_isolation'), \
                mock.patch.object(native, 'completion', side_effect=Failure('timeout', 'Expired.')), \
                mock.patch.object(native, 'verify_requests', return_value=EXPECTED):
            with self.assertRaises(Failure) as raised:
                native.execute(Path('unused'), CALLER, EXPECTED, threading.Event())
        self.assertEqual(raised.exception.details['nativeExecution']['phase'], 'completion')
        self.assertEqual(raised.exception.actual, EXPECTED)

    def launch_idle(self, root):
        with mock.patch.object(native, 'windows_codex', return_value=sys.executable):
            return native.launch([sys.executable, '-B', '-c',
                                  'import time; print(\'{"ready": true}\', flush=True); time.sleep(30)'],
                                 dict(os.environ), root)

    def force_end(self, process):
        if os.name == 'nt':
            process._consult_job.terminate()
        else:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        process.wait(timeout=5)

    def check_blocked_send(self, cancellation):
        with tempfile.TemporaryDirectory(prefix='ca-native-pipe-') as directory:
            cancel = threading.Event()
            process = self.launch_idle(Path(directory))
            with mock.patch.object(native, 'launch', return_value=process):
                server = native.Server({}, Path(directory), {}, cancel, time.monotonic() + 5)
            self.assertEqual(server.receive(), {'ready': True})
            server.deadline = time.monotonic() + (.2 if not cancellation else 5)
            errors = []
            def send_and_close():
                try:
                    server.send({'context': 'x' * 1024 * 1024})
                except Failure as error:
                    errors.append(error.code)
                finally:
                    try:
                        server.close()
                    except Failure as error:
                        errors.append(error.code)
            sender = threading.Thread(target=send_and_close, daemon=True)
            sender.start()
            try:
                time.sleep(.05)
                self.assertTrue(sender.is_alive(), 'real pipe write did not block')
                if cancellation:
                    cancel.set()
                sender.join(timeout=1.5)
                self.assertFalse(sender.is_alive(), 'blocked write ignored cancellation or deadline')
                self.assertEqual(errors, ['cancelled' if cancellation else 'timeout'])
                self.assertIsNotNone(process.poll(), 'native child survived cancelled send')
                self.assertTrue(process.stdin.closed)
                self.assertTrue(process.stdout.closed)
            finally:
                if sender.is_alive() or process.poll() is None:
                    self.force_end(process)
                sender.join(timeout=5)
                if not process.stdin.closed or not process.stdout.closed:
                    server.close()

    def test_real_pipe_cancellation_terminates_before_stream_close(self):
        self.check_blocked_send(True)

    def test_real_pipe_deadline_terminates_before_stream_close(self):
        self.check_blocked_send(False)

    def test_reader_start_failure_closes_native_process_and_pipes(self):
        with tempfile.TemporaryDirectory(prefix='ca-native-reader-') as directory:
            process = self.launch_idle(Path(directory))
            try:
                with mock.patch.object(native, 'launch', return_value=process), \
                        mock.patch.object(threading.Thread, 'start', side_effect=RuntimeError('thread unavailable')):
                    with self.assertRaises(RuntimeError):
                        native.Server({}, Path(directory), {}, threading.Event(), time.monotonic() + 5)
                self.assertIsNotNone(process.poll(), 'constructor leaked its native process')
                self.assertTrue(process.stdin.closed)
                self.assertTrue(process.stdout.closed)
            finally:
                if process.poll() is None:
                    self.force_end(process)
                for stream in (process.stdin, process.stdout):
                    stream.close()

    def pending_server(self, cancel=None, deadline=None):
        return types.SimpleNamespace(cancel=cancel or threading.Event(),
                                     deadline=time.monotonic() + 5 if deadline is None else deadline,
                                     pending=completed(), receive=lambda: self.fail('pending result was lost'))

    def test_pending_completion_rejects_existing_cancellation(self):
        cancel = threading.Event()
        cancel.set()
        with self.assertRaises(Failure) as raised:
            native.completion(self.pending_server(cancel), 'advisor', 'turn')
        self.assertEqual(raised.exception.code, 'cancelled')

    def test_pending_completion_rejects_expired_deadline(self):
        with self.assertRaises(Failure) as raised:
            native.completion(self.pending_server(deadline=time.monotonic() - 1), 'advisor', 'turn')
        self.assertEqual(raised.exception.code, 'timeout')

    def test_completion_checks_cancellation_after_consuming_terminal_message(self):
        server = self.pending_server()
        class CancelAtTerminal(list):
            def pop(self, index):
                value = super().pop(index)
                if value['method'] == 'turn/completed':
                    server.cancel.set()
                return value
        server.pending = CancelAtTerminal(server.pending)
        with self.assertRaises(Failure) as raised:
            native.completion(server, 'advisor', 'turn')
        self.assertEqual(raised.exception.code, 'cancelled')

    def test_pending_completion_keeps_retry_and_identity_validation(self):
        server = self.pending_server()
        server.pending.insert(1, {'method': 'error', 'params': {
            'threadId': 'advisor', 'turnId': 'turn', 'willRetry': True}})
        server.pending[2:2] = completed()[:1]
        self.assertEqual(native.completion(server, 'advisor', 'turn'), ADVICE)
        server = self.pending_server()
        server.pending[-1]['params']['turn']['id'] = 'wrong-turn'
        with self.assertRaises(Failure) as raised:
            native.completion(server, 'advisor', 'turn')
        self.assertEqual(raised.exception.code, 'executor')

    def check_success_publication(self, expires):
        cancel, clock = threading.Event(), [10.0]
        server = types.SimpleNamespace(initialize=lambda: None, close=lambda: None,
                                      call=lambda *args: {'thread': {'id': 'advisor'}, 'turn': {'id': 'turn'}})
        def verify(*args):
            if expires:
                clock[0] = 200.0
            else:
                cancel.set()
            return EXPECTED
        with tempfile.TemporaryDirectory(prefix='ca-native-publish-') as directory, \
                mock.patch.object(native, 'catalog', return_value=(Path(directory) / 'models.json', 'codex')), \
                mock.patch.object(native, 'server_names', return_value=set()), \
                mock.patch.object(native, 'Server', return_value=server), \
                mock.patch.object(native, 'verify_isolation'), \
                mock.patch.object(native, 'completion', return_value=ADVICE), \
                mock.patch.object(native, 'verify_requests', side_effect=verify), \
                mock.patch.object(native.time, 'monotonic', side_effect=lambda: clock[0]):
            with self.assertRaises(Failure) as raised:
                native.execute(Path(directory), CALLER, EXPECTED, cancel)
        self.assertEqual(raised.exception.code, 'timeout' if expires else 'cancelled')
        self.assertEqual(raised.exception.details['nativeExecution']['phase'], 'publish')

    def test_success_publication_rejects_cancellation_during_verification(self):
        self.check_success_publication(False)

    def test_success_publication_rejects_deadline_during_verification(self):
        self.check_success_publication(True)


class NativeRequest(unittest.TestCase):
    def request(self, lite=True):
        request = {'model': EXPECTED['model'], 'reasoning': {'effort': EXPECTED['effort']},
                   'input': [{'type': 'additional_tools', 'role': 'developer', 'tools': []}]}
        if lite:
            request['input'].append(message(CALLER['base']))
        else:
            request['instructions'] = CALLER['base']
        request['input'] += [message('HOST_SKILLS'), message('HOST_ENVIRONMENT', 'user')]
        request['input'] += copy.deepcopy(CALLER['items']) + [
            message(native.GUIDANCE), message('Return process consultation for the caller now.', 'user')]
        return request

    def verify(self, request, lite=True):
        with tempfile.TemporaryDirectory(prefix='ca-native-request-') as directory:
            root = Path(directory)
            (root / 'models.json').write_text(json.dumps({'models': [{'use_responses_lite': lite}]}))
            trace = root / 'trace/rollout'
            trace.mkdir(parents=True)
            (trace / 'request.json').write_text(json.dumps(request))
            (trace / 'events.jsonl').write_text(json.dumps({'thread_id': 'advisor', 'payload': {
                'type': 'inference_started', 'request_payload': {'path': 'request.json'}}}) + '\n')
            return native.verify_requests(root, 'advisor', EXPECTED, CALLER)

    def reject(self, request, lite=True, source_index=None):
        with self.assertRaises(Failure) as raised:
            self.verify(request, lite)
        self.assertEqual(raised.exception.code, 'context')
        self.assertEqual(raised.exception.actual, EXPECTED)
        if source_index is not None:
            self.assertEqual(raised.exception.details['sourceIndex'], source_index)
        self.assertNotIn('BASE_CONSTRAINT', json.dumps(raised.exception.details))
        self.assertNotIn('FIRST_CONSTRAINT', json.dumps(raised.exception.details))

    def test_exact_base_and_guidance_accept_both_qualified_representations(self):
        for lite in (True, False):
            with self.subTest(lite=lite):
                self.assertEqual(self.verify(self.request(lite), lite), EXPECTED)

    def test_lite_empty_tools_may_omit_both_inventories(self):
        request = self.request()
        request['input'].pop(0)
        self.assertEqual(self.verify(request), EXPECTED)

    def test_nonlite_requires_an_explicit_empty_inventory(self):
        request = self.request(False)
        request['input'].pop(0)
        with self.assertRaises(Failure) as raised:
            self.verify(request, False)
        self.assertEqual(raised.exception.code, 'tools')

    def test_nonlite_unknown_empty_inventory_is_not_proof(self):
        request = self.request(False)
        request['input'][0]['type'] = 'future_inventory'
        with self.assertRaises(Failure) as raised:
            self.verify(request, False)
        self.assertEqual(raised.exception.code, 'tools')

    def test_explicit_empty_top_level_tools_accept_both_catalog_modes(self):
        for lite in (True, False):
            with self.subTest(lite=lite):
                request = self.request(lite)
                request['input'].pop(0)
                request['tools'] = []
                self.assertEqual(self.verify(request, lite), EXPECTED)

    def test_nonempty_or_malformed_tools_fail_in_both_locations(self):
        for lite in (True, False):
            for value in (None, {}, '', [{'name': 'shell'}]):
                for location in ('top', 'additional', 'both', 'omitted_additional'):
                    with self.subTest(lite=lite, value=value, location=location):
                        request = self.request(lite)
                        if location in ('top', 'both', 'omitted_additional'):
                            request['tools'] = value
                        if location in ('additional', 'both'):
                            request['input'][0]['tools'] = value
                        if location == 'omitted_additional':
                            request['input'].pop(0)
                        with self.assertRaises(Failure) as raised:
                            self.verify(request, lite)
                        self.assertEqual(raised.exception.code, 'tools')
                        self.assertEqual(raised.exception.actual, EXPECTED)

    def test_additional_inventory_requires_tools_and_checks_every_item(self):
        for lite in (True, False):
            for change in ('missing', 'second_nonempty'):
                with self.subTest(lite=lite, change=change):
                    request = self.request(lite)
                    request['tools'] = []
                    if change == 'missing':
                        request['input'][0].pop('tools')
                    else:
                        request['input'].append({'type': 'additional_tools', 'role': 'developer',
                                                 'tools': [{'name': 'shell'}]})
                    if change == 'missing':
                        self.assertEqual(self.verify(request, lite), EXPECTED)
                    else:
                        with self.assertRaises(Failure) as raised:
                            self.verify(request, lite)
                        self.assertEqual(raised.exception.code, 'tools')

    def test_unknown_input_type_cannot_grant_tools(self):
        request = self.request()
        request['input'].append({'type': 'future_inventory', 'tools': [{'name': 'shell'}]})
        with self.assertRaises(Failure) as raised:
            self.verify(request)
        self.assertEqual(raised.exception.code, 'tools')

    def test_lite_base_is_required_in_exact_developer_prefix(self):
        for change in ('missing', 'content', 'role', 'position', 'substring', 'top_level'):
            with self.subTest(change=change):
                request = self.request()
                if change == 'missing':
                    request['input'].pop(1)
                elif change == 'content':
                    request['input'][1]['content'][0]['text'] = 'CHANGED_BASE'
                elif change == 'role':
                    request['input'][1]['role'] = 'user'
                elif change == 'position':
                    request['input'].insert(3, request['input'].pop(1))
                elif change == 'substring':
                    request['input'][1]['content'][0]['text'] += '\nEXTRA_BASE'
                else:
                    request['instructions'] = CALLER['base']
                    request['input'].pop(1)
                self.reject(request)

    def test_nonlite_base_is_required_as_exact_top_level_instructions(self):
        for change in ('missing', 'content', 'substring', 'message'):
            with self.subTest(change=change):
                request = self.request(False)
                if change == 'missing':
                    request.pop('instructions')
                elif change == 'content':
                    request['instructions'] = 'CHANGED_BASE'
                elif change == 'substring':
                    request['instructions'] += '\nEXTRA_BASE'
                else:
                    request.pop('instructions')
                    request['input'].insert(1, message(CALLER['base']))
                self.reject(request, False)

    def test_guidance_must_follow_complete_history_with_exact_role_and_content(self):
        for lite in (True, False):
            for change in ('missing', 'content', 'role', 'position', 'substring'):
                with self.subTest(lite=lite, change=change):
                    request = self.request(lite)
                    if change == 'missing':
                        request['input'].pop(-2)
                    elif change == 'content':
                        request['input'][-2]['content'][0]['text'] = 'CHANGED_GUIDANCE'
                    elif change == 'role':
                        request['input'][-2]['role'] = 'user'
                    elif change == 'position':
                        request['input'].insert(-3, request['input'].pop(-2))
                    else:
                        request['input'][-2]['content'][0]['text'] += '\nEXTRA_GUIDANCE'
                    self.reject(request, lite)

    def test_history_error_keeps_source_item_index(self):
        request = self.request()
        request['input'][-3]['content'][0]['text'] = 'CHANGED_SOURCE'
        self.reject(request, source_index=1)

    def test_fixed_invocation_has_exact_content_role_and_position(self):
        for lite in (True, False):
            for change in ('missing', 'content', 'role', 'position'):
                with self.subTest(lite=lite, change=change):
                    request = self.request(lite)
                    if change == 'missing':
                        request['input'].pop()
                    elif change == 'content':
                        request['input'][-1]['content'][0]['text'] = 'CHANGED_INVOCATION'
                    elif change == 'role':
                        request['input'][-1]['role'] = 'developer'
                    else:
                        request['input'].insert(-2, request['input'].pop())
                    self.reject(request, lite)

    def test_native_retry_suffix_keeps_the_fixed_invocation_before_assistant_message(self):
        for lite in (True, False):
            with self.subTest(lite=lite):
                request = self.request(lite)
                request['input'].append({'type': 'message', 'role': 'assistant', 'content': [
                    {'type': 'output_text', 'text': json.dumps(ADVICE)}]})
                self.assertEqual(self.verify(request, lite), EXPECTED)


if __name__ == '__main__':
    unittest.main(verbosity=2)
