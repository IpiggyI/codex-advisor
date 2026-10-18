"""Check real-history selection, safe diagnostics, and native normalization sensitivity."""

import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True
import consultation_native_corpus as corpus
from consult_context import Failure
from test_consultation_upgrade import records, THREAD

LITE = {'use_responses_lite': True, 'advisorModels': sorted(['gpt-6.1-sol', 'gpt-6-astra'])}
FULL = {'use_responses_lite': False, 'advisorModels': ['gpt-6-astra']}


class Selection(unittest.TestCase):
    def test_cli_rejects_mutation_option_before_running_checks(self):
        output, errors = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, 'argv', [corpus.__file__, '--mutation', 'transport-fields']), \
                mock.patch.object(corpus, 'check') as check, \
                contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            with self.assertRaises(SystemExit) as raised:
                corpus.main()
        self.assertEqual(raised.exception.code, 2)
        check.assert_not_called()
        self.assertEqual(output.getvalue(), '')
        self.assertIn('unrecognized arguments: --mutation transport-fields', errors.getvalue())

    def test_smallest_sequential_history_and_excluded_type(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            large = records()
            large[3:3] = [{'type': 'response_item', 'payload': {
                'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'PRIVATE' * 100}]}}]
            small = records()
            small[3:3] = [
                {'type': 'response_item', 'payload': {'type': 'additional_tools', 'role': 'developer', 'tools': []}},
                {'type': 'response_item', 'payload': {'type': 'message', 'role': 'user',
                    'content': [{'type': 'input_text', 'text': 'PRIVATE'}]}}]
            parallel = copy.deepcopy(small[5])
            parallel['payload']['call_id'] = 'parallel'
            small[6:6] = [parallel, {'type': 'response_item', 'payload': {
                'type': 'function_call_output', 'call_id': 'parallel', 'output': ''}}]
            for name, values in [('large', large), ('small', small)]:
                (root / (name + '-' + THREAD + '.jsonl')).write_text(
                    ''.join(json.dumps(v) + '\n' for v in values), encoding='utf-8')
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            samples = corpus.select_samples([root])
            self.assertEqual(samples.failures, [])
            self.assertIn('additional_tools', samples.present)
            sample = samples.best['additional_tools']
            self.assertEqual(sample['sampleKind'], 'excluded')
            self.assertIn('additional_tools', sample['rawExcludedTypes'])
            self.assertFalse(any(i['type'] == 'additional_tools' for i in sample['caller']['items']))
            self.assertEqual(samples.best['message']['file'], 'small-' + THREAD + '.jsonl')
            self.assertEqual(samples.best['message']['boundaryIndex'], 5)
            self.assertEqual(samples.counts['parallelSkipped'], 1)
            for sample in samples.best.values():
                self.assertEqual(sample['size'], len(corpus.encoded({
                    'base': sample['caller']['base'], 'items': sample['caller']['items']})))
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})

    def test_dual_modes_and_cli_failure_diagnostics(self):
        caller = {'base': 'PRIVATE', 'items': [{'type': 'message'}]}
        samples = corpus.Samples()
        samples.present.add('message')
        samples.best['message'] = {'file': 'fixture.jsonl', 'boundaryIndex': 3, 'caller': caller,
                                   'size': 1, 'sampleKind': 'preserved'}
        error = Failure('context', 'Normalization mismatch.', details={
            'stage': 'request', 'type': 'message', 'path': 'id'})
        output = io.StringIO()
        with mock.patch.object(corpus, 'select_samples', return_value=samples), \
                mock.patch.object(corpus, 'discover_request_modes', return_value=([LITE, FULL], [])), \
                mock.patch.object(corpus, 'run_mode', side_effect=[None, error]) as run, \
                mock.patch.object(sys, 'argv', [corpus.__file__]), contextlib.redirect_stdout(output):
            self.assertEqual(corpus.main(), 1)
        self.assertEqual([call.args[1]['use_responses_lite'] for call in run.call_args_list], [True, False])
        self.assertNotIn('PRIVATE', output.getvalue())
        report = json.loads(output.getvalue())
        self.assertEqual(report['counts']['passed'], 1)
        self.assertEqual(report['counts']['failed'], 1)
        self.assertEqual(report['verdicts'][1]['failure'], {
            'stage': 'request', 'type': 'message', 'code': 'context', 'path': 'id',
            'message': 'Normalization mismatch.'})

    def test_only_used_modes_run_and_excluded_coverage_passes(self):
        samples = corpus.Samples()
        samples.present.add('additional_tools')
        samples.best['additional_tools'] = {'file': 'fixture.jsonl', 'boundaryIndex': 4,
            'caller': {'base': 'PRIVATE', 'items': []}, 'size': 1, 'sampleKind': 'excluded',
            'rawExcludedTypes': ['additional_tools']}
        missing = [{'use_responses_lite': False, 'reason': 'No advisor model uses this request mode.'}]
        output = io.StringIO()
        with mock.patch.object(corpus, 'select_samples', return_value=samples), \
                mock.patch.object(corpus, 'discover_request_modes', return_value=([LITE], missing)), \
                mock.patch.object(corpus, 'run_mode') as run, \
                mock.patch.object(sys, 'argv', [corpus.__file__]), contextlib.redirect_stdout(output):
            self.assertEqual(corpus.main(), 0)
        report = json.loads(output.getvalue())
        self.assertEqual(run.call_count, 1)
        self.assertEqual(run.call_args.args[1], LITE)
        self.assertEqual(report['notCovered'], missing)
        self.assertEqual(report['uncoveredTypes'], [])
        self.assertEqual(report['counts']['excludedTypes'], 1)
        self.assertEqual(report['verdicts'][0]['sampleKind'], 'excluded')


class RequestModes(unittest.TestCase):
    def test_modes_come_only_from_advisor_rows_and_host_catalog(self):
        profile = corpus.load_profile(corpus.PLUGIN)
        models = [{'slug': 'gpt-6.1-sol', 'use_responses_lite': True},
                  {'slug': 'gpt-6-astra', 'use_responses_lite': True},
                  {'slug': 'gpt-6-luna', 'use_responses_lite': False}]
        modes, missing = corpus.modes_from_catalog(profile, models)
        self.assertEqual(len(modes), 1)
        self.assertEqual(modes[0], LITE)
        self.assertEqual([m['use_responses_lite'] for m in missing], [False])
        models[1]['use_responses_lite'] = False
        modes, missing = corpus.modes_from_catalog(profile, models)
        self.assertEqual([m['use_responses_lite'] for m in modes], [True, False])
        self.assertEqual(missing, [])
        self.assertEqual(corpus.expected_dial({'model': 'gpt-6.1-sol', 'effort': 'high'}, modes[1])['model'],
                         'gpt-6-astra')
        with self.assertRaises(Failure):
            corpus.modes_from_catalog(profile, models[:1])

    def test_excluded_items_and_tools_cannot_pass_request_assertions(self):
        corpus.verify_excluded_requests([{'input': [], 'tools': []}])
        for request, code in (({'tools': [{'name': 'inert'}]}, 'tools'),
                              ({'input': [{'type': 'future_item', 'tools': [{}]}]}, 'tools'),
                              ({'input': [{'type': 'additional_tools', 'tools': []}]}, 'context'),
                              ({'input': [{'type': 'web_search_call'}]}, 'context'),
                              ({'input': [{'type': 'image_generation_call'}]}, 'context'),
                              ({'input': [{'type': 'local_shell_call'}]}, 'context'),
                              ({'input': [{'type': 'compaction_trigger'}]}, 'context')):
            with self.subTest(request=request), self.assertRaises(Failure) as raised:
                corpus.verify_excluded_requests([request])
            self.assertEqual(raised.exception.code, code)
            self.assertEqual(raised.exception.details['stage'], 'request')


class NativeMutation(unittest.TestCase):
    def test_transport_normalization_mutation_fails_with_type_and_path(self):
        caller = {'base': 'Preserve the synthetic history.', 'thread': 'synthetic',
                  'model': 'gpt-6.1-sol', 'effort': 'high', 'items': [{
                      'type': 'message', 'id': 'source-id', 'role': 'user',
                      'content': [{'type': 'input_text', 'text': 'PRIVATE_MUTATION_FIXTURE'}]}]}
        corpus.run_mode(caller, LITE)
        with self.assertRaises(Failure) as raised:
            corpus.run_mode(caller, LITE, 'transport-fields')
        error = raised.exception
        self.assertEqual(error.code, 'context')
        self.assertEqual(error.details['stage'], 'request')
        self.assertEqual(error.details['type'], 'message')
        self.assertIsInstance(error.details['path'], str)
        self.assertTrue(error.details['path'])
        self.assertNotIn('PRIVATE_MUTATION_FIXTURE', json.dumps(corpus.diagnostics(error)))
        print('PASS: transport mutation rejected; stage=request type=message code=context path=' + error.details['path'])

    def test_raw_excluded_types_pass_through_reconstruction_and_native_chain(self):
        excluded = [
            {'type': 'additional_tools', 'role': 'developer', 'tools': [{'type': 'function',
                'name': 'inert_probe', 'parameters': {'type': 'object', 'properties': {}}}]},
            {'type': 'tool_search_call', 'execution': 'server', 'arguments': None},
            {'type': 'tool_search_output', 'execution': 'server', 'status': 'completed', 'tools': []},
            {'type': 'configuration_update'}, {'type': 'compaction_trigger'},
            {'type': 'web_search_call'}, {'type': 'image_generation_call'},
            {'type': 'local_shell_call', 'call_id': 'shell', 'status': 'completed', 'action': {}},
            {'type': 'function_call_output', 'call_id': 'shell', 'output': 'PRIVATE_SHELL_RESULT'}]
        with tempfile.TemporaryDirectory() as directory:
            values = records()
            values[3:3] = [{'type': 'response_item', 'payload': {'type': 'message', 'role': 'user',
                'content': [{'type': 'input_text', 'text': 'Retain the synthetic constraint.'}]}}] + [
                    {'type': 'response_item', 'payload': i} for i in excluded]
            path = Path(directory) / ('rollout-' + THREAD + '.jsonl')
            path.write_text(''.join(json.dumps(v) + '\n' for v in values), encoding='utf-8')
            samples = corpus.select_samples([Path(directory)])
        self.assertEqual(samples.failures, [])
        for item in excluded:
            if item['type'] == 'function_call_output':
                continue
            sample = samples.best[item['type']]
            self.assertEqual(sample['sampleKind'], 'excluded')
            self.assertIn(item['type'], sample['rawExcludedTypes'])
            self.assertEqual(sample['boundaryIndex'], 9 + 4)
            self.assertFalse(any(i['type'] in {v['type'] for v in excluded[:-1]}
                                 or i.get('call_id') == 'shell' for i in sample['caller']['items']))
        corpus.run_mode(samples.best['additional_tools']['caller'], LITE)
        print('PASS: raw capability, control and hosted samples excluded; native request has no tools or excluded items')


if __name__ == '__main__':
    unittest.main()
