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
from consult_context import Failure

EXPECTED = {'model': 'gpt-6.1-sol', 'effort': 'xhigh'}
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


class NativeLifecycle(unittest.TestCase):
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
                mock.patch.object(native, 'catalog', return_value=Path(directory) / 'models.json'), \
                mock.patch.object(native, 'server_names', return_value=set()), \
                mock.patch.object(native, 'Server', return_value=server), \
                mock.patch.object(native, 'verify_isolation'), \
                mock.patch.object(native, 'completion', return_value=ADVICE), \
                mock.patch.object(native, 'verify_requests', side_effect=verify), \
                mock.patch.object(native.time, 'monotonic', side_effect=lambda: clock[0]):
            with self.assertRaises(Failure) as raised:
                native.execute(Path(directory), CALLER, EXPECTED, cancel)
        self.assertEqual(raised.exception.code, 'timeout' if expires else 'cancelled')

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
