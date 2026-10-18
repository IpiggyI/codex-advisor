"""Check host upgrade policy coverage and local corpus replay boundaries."""

import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import consultation_schema_check as schema_check
import consultation_corpus_replay as corpus
from consult_context import Failure, ITEM_POLICY, comparable, validate_items
from consult_native import verify_history

THREAD = '11111111-1111-1111-1111-111111111111'


def records():
    return [
        {'type': 'session_meta', 'payload': {'id': THREAD, 'cli_version': 'test',
                                          'base_instructions': {'text': 'PRIVATE_HISTORY'}}},
        {'type': 'event_msg', 'payload': {'type': 'task_started', 'turn_id': 'turn1'}},
        {'type': 'turn_context', 'payload': {'turn_id': 'turn1', 'model': 'gpt-6-sol', 'effort': 'high'}},
        {'type': 'response_item', 'payload': {'type': 'function_call', 'name': 'tool',
                                            'arguments': '{}', 'call_id': 'call1'}},
        {'type': 'response_item', 'payload': {'type': 'function_call_output', 'call_id': 'call1',
                                            'output': 'PRIVATE_HISTORY'}},
        {'type': 'event_msg', 'payload': {'type': 'task_started', 'turn_id': 'turn2'}},
        {'type': 'turn_context', 'payload': {'turn_id': 'turn2', 'model': 'gpt-6.1-sol', 'effort': 'low'}},
        {'type': 'response_item', 'payload': {'type': 'custom_tool_call', 'id': 'second',
                                            'call_id': 'call2', 'name': 'tool', 'input': 'PRIVATE_HISTORY'}}]


class Policies(unittest.TestCase):
    def test_controls_are_excluded(self):
        for kind in ('configuration_update', 'compaction_trigger'):
            with self.subTest(kind=kind):
                self.assertEqual(ITEM_POLICY[kind]['policy'], 'control')
                self.assertEqual(validate_items([{'type': kind}]), [])
                self.assertEqual(verify_history({'input': []}, {'items': [{'type': kind}]}), -1)

    def test_preserved_variants(self):
        for kind in ('context_compaction', 'other'):
            with self.subTest(kind=kind):
                value = {'type': kind, 'payload': 'PRIVATE_HISTORY'}
                self.assertEqual(ITEM_POLICY[kind]['policy'], 'preserve')
                self.assertEqual(validate_items([value]), [value])
                self.assertEqual(comparable(value), value)
                with self.assertRaises(Failure):
                    verify_history({'input': []}, {'items': [value]})

    def test_local_shell_pair(self):
        call = {'type': 'local_shell_call', 'call_id': 'shell1', 'status': 'completed',
                'action': {'type': 'exec', 'command': ['echo', 'fixture']}}
        output = {'type': 'function_call_output', 'call_id': 'shell1', 'output': 'fixture'}
        self.assertEqual(validate_items([call, output]), [])
        verify_history({'input': []}, {'items': [call, output]})
        for values in ([call], [output], [call, {**output, 'call_id': 'different'}]):
            with self.subTest(values=values), self.assertRaises(Failure) as raised:
                validate_items(values)
            self.assertEqual(raised.exception.code, 'pairing')

        for kind in ('local_shell_call', 'function_call_output'):
            with mock.patch.dict(ITEM_POLICY[kind], policy='preserve', call_policies={}):
                with self.assertRaises(Failure) as raised:
                    validate_items([call, output])
                self.assertEqual(raised.exception.code, 'pairing')

        ordinary = {'type': 'function_call', 'call_id': 'ordinary', 'name': 'tool', 'arguments': '{}'}
        result = {**output, 'call_id': 'ordinary'}
        self.assertEqual(validate_items([ordinary, result, call, output]), [ordinary, result])
        for values in ([{**call, 'action': None}, output],
                       [{**call, 'status': None}, output],
                       [call, {**output, 'output': None}],
                       [call, {**output, 'output': [{'type': 'input_text', 'text': None}]}]):
            with self.subTest(values=values), self.assertRaises(Failure) as raised:
                validate_items(values)
            self.assertEqual(raised.exception.code, 'unsupported_content')

    def test_shell_requires_identity(self):
        call = {'type': 'local_shell_call', 'status': 'completed',
                'action': {'type': 'exec', 'command': ['echo', 'fixture']}}
        for value in (call, {**call, 'call_id': None}, {**call, 'call_id': ''}):
            with self.assertRaises(Failure) as raised:
                validate_items([value])
            self.assertEqual(raised.exception.code, 'pairing')

    def test_hosted_records_are_excluded(self):
        for kind in ('web_search_call', 'image_generation_call'):
            item = {'type': kind, 'status': 'completed'}
            self.assertEqual(ITEM_POLICY[kind]['policy'], 'hosted')
            self.assertEqual(validate_items([item]), [])
            verify_history({'input': []}, {'items': [item]})


class Schema(unittest.TestCase):
    def schema(self, union='anyOf'):
        return {'definitions': {'ResponseItem': {union: [
            {'properties': {'type': {'enum': [kind]}}} for kind in ITEM_POLICY]}}}

    def test_union_forms(self):
        for union in ('anyOf', 'oneOf'):
            self.assertEqual(schema_check.missing_types(self.schema(union), ITEM_POLICY),
                             ([], len(ITEM_POLICY)))

    def test_removed_policy_fails_command(self):
        host_schema = self.schema()
        policy = dict(ITEM_POLICY)
        del policy['local_shell_call']

        def generate(command, **kwargs):
            Path(command[-1], 'protocol.json').write_text(json.dumps(host_schema), encoding='utf-8')
            return subprocess.CompletedProcess(command, 0)

        output = io.StringIO()
        with mock.patch.object(schema_check, 'ITEM_POLICY', policy), \
                mock.patch.object(schema_check.subprocess, 'run', side_effect=generate), \
                contextlib.redirect_stdout(output):
            self.assertEqual(schema_check.main(), 1)
        self.assertEqual(json.loads(output.getvalue())['missingTypes'], ['local_shell_call'])


class Corpus(unittest.TestCase):
    def run_replay(self, values, extra=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / ('rollout-' + THREAD + '.jsonl')
            path.write_text(''.join(json.dumps(value) + '\n' for value in values), encoding='utf-8')
            if extra:
                (root / 'legacy.jsonl').write_text(json.dumps(extra) + '\n', encoding='utf-8')
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            temporary = []
            original = tempfile.TemporaryDirectory

            def track(*args, **kwargs):
                result = original(*args, **kwargs)
                temporary.append(Path(result.name))
                return result

            with mock.patch.object(corpus.tempfile, 'TemporaryDirectory', side_effect=track):
                report = corpus.replay([root])
            self.assertTrue(temporary)
            self.assertTrue(all(not p.exists() for p in temporary))
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})
            self.assertNotIn('PRIVATE_HISTORY', json.dumps(report))
            return report

    def test_every_boundary_and_latest_context(self):
        observed = []
        original = corpus.reconstruct

        def reconstruct(home, meta):
            observed.append(copy.deepcopy(meta))
            return original(home, meta)

        with mock.patch.object(corpus, 'reconstruct', side_effect=reconstruct):
            report = self.run_replay(records())
        self.assertEqual(report['counts']['replayed'], 2)
        self.assertEqual(report['counts']['passed'], 2)
        self.assertEqual(report['failures'], [])
        self.assertEqual([m['x-codex-turn-metadata']['model'] for m in observed],
                         ['gpt-6-sol', 'gpt-6.1-sol'])

    def test_skip_counts(self):
        values = records()
        values[1:1] = [
            {'type': 'response_item', 'payload': {**values[3]['payload'], 'call_id': 'early'}},
            {'type': 'response_item', 'payload': {**values[4]['payload'], 'call_id': 'early'}}]
        report = self.run_replay(values, extra={'type': 'message', 'content': 'PRIVATE_HISTORY'})
        self.assertEqual(report['counts']['legacyFilesSkipped'], 1)
        self.assertEqual(report['counts']['boundariesSkipped'], 1)
        self.assertEqual(report['counts']['beforeTurnContext'], 1)
        self.assertEqual(report['counts']['beforeTaskStarted'], 1)

    def test_parallel_positions_are_skipped(self):
        values = records()
        values[4:4] = [copy.deepcopy(values[-1]),
                       {'type': 'response_item', 'payload': {'type': 'custom_tool_call_output',
                                                           'call_id': 'call2', 'output': 'PRIVATE_HISTORY'}}]
        values[-1]['payload'].update(id='third', call_id='call3')
        observed = []
        original = corpus.reconstruct

        def reconstruct(home, meta):
            observed.append(meta['itemId'])
            return original(home, meta)

        with mock.patch.object(corpus, 'reconstruct', side_effect=reconstruct):
            report = self.run_replay(values)
        self.assertEqual(report['counts']['boundaries'], 3)
        self.assertEqual(report['counts']['parallelSkipped'], 1)
        self.assertEqual(report['counts']['boundariesSkipped'], 1)
        self.assertEqual(report['counts']['replayed'], 2)
        self.assertEqual(report['counts']['passed'], 2)
        self.assertEqual(report['failures'], [])
        self.assertEqual(len(observed), 2)
        self.assertNotIn('second', observed)
        self.assertEqual(observed[-1], 'third')

    def test_rollback_location_and_no_history_output(self):
        values = records()
        values.insert(3, {'type': 'rollback', 'payload': {'text': 'PRIVATE_HISTORY'}})
        report = self.run_replay(values)
        self.assertEqual(report['counts']['failures'], 0)
        self.assertEqual(report['failures'], [])
        self.assertEqual(report['counts']['designRejections'], {'rollback': 2})
        self.assertEqual(report['designRejections'][0], {
            'file': 'rollout-' + THREAD + '.jsonl', 'boundaryIndex': 4, 'recordIndex': 3,
            'stage': 'record', 'type': 'rollback', 'code': 'rollback',
            'message': 'Rollback reconstruction is not qualified.'})

    def test_declared_pairs_determine_parallel_positions(self):
        for call, output in (
                ({'type': 'local_shell_call', 'call_id': 'shell', 'status': 'completed', 'action': {}},
                 {'type': 'function_call_output', 'call_id': 'shell', 'output': ''}),
                ({'type': 'tool_search_call', 'execution': 'server', 'arguments': None},
                 {'type': 'tool_search_output', 'execution': 'server', 'status': 'completed', 'tools': []})):
            with self.subTest(kind=call['type']):
                values = records()[:3] + [
                    {'type': 'response_item', 'payload': call}, copy.deepcopy(records()[-1]),
                    {'type': 'response_item', 'payload': output},
                    {'type': 'response_item', 'payload': {'type': 'custom_tool_call_output',
                                                        'call_id': 'call2', 'output': ''}},
                    {**records()[-1], 'payload': {**records()[-1]['payload'], 'id': 'third', 'call_id': 'call3'}}]
                report = self.run_replay(values)
                self.assertEqual(report['counts']['parallelSkipped'], 1)
                self.assertEqual(report['counts']['passed'], 1)
                self.assertEqual(report['failures'], [])

    def test_unpaired_shell_reaches_pairing_validation(self):
        values = records()[:3] + [{'type': 'response_item', 'payload': {
            'type': 'local_shell_call', 'status': 'completed', 'action': {}}}, records()[-1]]
        report = self.run_replay(values)
        self.assertEqual(report['counts']['parallelSkipped'], 0)
        self.assertEqual(report['counts']['failures'], 1)
        self.assertEqual(report['failures'][0]['code'], 'pairing')

    def test_compaction_replaces_pending_calls(self):
        values = records()[:4] + [{'type': 'compacted', 'payload': {'replacement_history': []}}, records()[-1]]
        report = self.run_replay(values)
        self.assertEqual(report['counts']['parallelSkipped'], 0)
        self.assertEqual(report['counts']['passed'], 2)
        values[4]['payload']['replacement_history'] = [records()[3]['payload']]
        report = self.run_replay(values)
        self.assertEqual(report['counts']['parallelSkipped'], 1)
        self.assertEqual(report['counts']['passed'], 1)

    def test_wrong_result_does_not_hide_pairing_failure(self):
        values = records()
        values[4]['payload']['type'] = 'custom_tool_call_output'
        report = self.run_replay(values)
        self.assertEqual(report['counts']['parallelSkipped'], 0)
        self.assertEqual(report['counts']['failures'], 1)
        self.assertEqual(report['failures'][0]['code'], 'pairing')

    def run_cli(self, event):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ('rollout-' + THREAD + '.jsonl')
            values = records()
            values.insert(3, event)
            path.write_text(''.join(json.dumps(v) + '\n' for v in values), encoding='utf-8')
            result = subprocess.run([sys.executable, '-B', corpus.__file__, '--root', directory],
                                    capture_output=True, text=True)
            self.assertEqual(result.stderr, '')
            self.assertNotIn('PRIVATE_HISTORY', result.stdout)
            return result.returncode, json.loads(result.stdout)

    def test_rollback_does_not_fail_exit_status(self):
        code, report = self.run_cli({'type': 'event_msg', 'payload': {'type': 'thread_rolled_back'}})
        self.assertEqual(code, 0)
        self.assertEqual(report['counts']['designRejections'], {'rollback': 2})
        self.assertEqual(len(report['designRejections']), 2)
        self.assertEqual(report['counts']['failures'], 0)

    def test_unknown_record_still_fails_exit_status(self):
        code, report = self.run_cli({'type': 'future_record', 'payload': {'text': 'PRIVATE_HISTORY'}})
        self.assertEqual(code, 1)
        self.assertEqual(report['counts']['designRejections'], {})
        self.assertEqual(report['designRejections'], [])
        self.assertEqual(report['counts']['failures'], 2)
        self.assertEqual(report['failures'][0]['stage'], 'record')
        self.assertEqual(report['failures'][0]['type'], 'future_record')
        self.assertEqual(report['failures'][0]['code'], 'snapshot')


if __name__ == '__main__':
    unittest.main()
