#!/usr/bin/env python3
"""Check real caller histories through the native chain and a loopback provider."""

import argparse
from collections import Counter
from contextlib import ExitStack
import json
import os
from pathlib import Path
import re
import sys
import subprocess
import tempfile
import threading
from unittest import mock

sys.dont_write_bytecode = True
from consultation_corpus_replay import CallBatch, default_roots, replay_boundary
from consultation_loopback import local_home
import consult_native as native
from consult_context import Failure, ITEM_POLICY, load_profile, advisor_dial

PLUGIN = Path(__file__).resolve().parents[1] / 'plugins/codex-advisor'


def encoded(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def diagnostics(error):
    return {'stage': error.details.get('stage', 'record'), 'type': error.details.get('type'),
            'code': error.code, 'path': error.details.get('path'), 'message': str(error)}


class HistorySize:
    def __init__(self, base):
        self.size = len(encoded({'base': base, 'items': []}))
        self.types = Counter()
        self.excluded = Counter()
        self.length = 0
        self.hosted_calls = set()

    def add(self, item):
        if not isinstance(item, dict) or not isinstance(item.get('type'), str):
            return
        kind = item['type']
        policy = ITEM_POLICY.get(kind, {})
        if policy.get('policy') == 'hosted' and policy.get('shape') == 'call':
            self.hosted_calls.add(item.get('call_id'))
        if (policy.get('policy') in ('capability', 'control', 'hosted') or
                kind == 'function_call_output' and item.get('call_id') in self.hosted_calls):
            self.excluded[kind] += 1
            return
        self.size += len(encoded(item)) + int(self.length > 0)
        self.length += 1
        self.types[kind] += 1


class Samples:
    def __init__(self):
        self.best, self.present, self.failures = {}, set(), []
        self.counts = dict(files=0, legacyFilesSkipped=0, boundaries=0, parallelSkipped=0,
                           beforeContextSkipped=0, reconstructionRejections=0)

    def consider(self, location, size, reconstruct):
        if not any(kind not in self.best or size.size < self.best[kind]['size']
                   for kind in size.types.keys() | size.excluded.keys()):
            return
        try:
            caller = reconstruct()
        except Failure as error:
            if error.code == 'rollback':
                self.counts['reconstructionRejections'] += 1
            else:
                self.failures.append({'sample': location, 'failure': diagnostics(error)})
            return
        actual_size = len(encoded({'base': caller['base'], 'items': caller['items']}))
        retained_types = {item['type'] for item in caller['items']}
        for kind in retained_types | size.excluded.keys():
            if kind not in self.best or actual_size < self.best[kind]['size']:
                sample_kind = 'preserved' if kind in retained_types else 'excluded'
                self.best[kind] = {**location, 'caller': caller, 'size': actual_size,
                                   'sampleKind': sample_kind, 'rawExcludedTypes': sorted(size.excluded)}


def scan_file(path, home, samples):
    target, current, started, size = None, None, False, None
    batch = CallBatch()
    with ExitStack() as stack:
        source = stack.enter_context(path.open('rb'))
        for index, line in enumerate(source):
            if not line.strip():
                if target:
                    target.write(line)
                continue
            record = json.loads(line)
            if target is None:
                if not isinstance(record, dict) or record.get('type') != 'session_meta':
                    samples.counts['legacyFilesSkipped'] += 1
                    return
                session = record.get('payload', {})
                thread = session.get('id', '')
                name = thread if isinstance(thread, str) and re.fullmatch(r'[0-9a-fA-F-]{36}', thread) else 'invalid'
                target = stack.enter_context((home / 'sessions' / ('rollout-' + name + '.jsonl')).open('wb'))
                instructions = session.get('base_instructions', {})
                base = instructions.get('text', '') if isinstance(instructions, dict) else ''
                size = HistorySize(base)
            kind = record.get('type') if isinstance(record, dict) else None
            payload = record.get('payload', {}) if isinstance(record, dict) else {}
            if kind == 'turn_context':
                current = payload
            if kind == 'event_msg' and isinstance(payload, dict) and payload.get('type') == 'task_started':
                started = True
            boundary = kind == 'response_item' and isinstance(payload, dict) and payload.get('type') in (
                'function_call', 'custom_tool_call')
            if boundary:
                samples.counts['boundaries'] += 1
                if current is None or not started:
                    samples.counts['beforeContextSkipped'] += 1
                elif batch.pending and not batch.invalid:
                    samples.counts['parallelSkipped'] += 1
                else:
                    samples.consider({'file': path.name, 'boundaryIndex': index}, size,
                        lambda: replay_boundary(home, target, record, session, current))
            target.write(line)
            batch.observe(record)
            if kind == 'compacted' and isinstance(payload, dict):
                size = HistorySize(base)
                items = payload.get('replacement_history', [])
            else:
                items = [payload] if kind == 'response_item' else []
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and isinstance(item.get('type'), str):
                        samples.present.add(item['type'])
                    size.add(item)


def select_samples(roots):
    samples = Samples()
    paths = sorted({p.resolve() for root in roots for p in root.rglob('*.jsonl')})
    for path in paths:
        samples.counts['files'] += 1
        with tempfile.TemporaryDirectory(prefix='ca-corpus-select-') as directory:
            home = Path(directory)
            (home / 'sessions').mkdir()
            try:
                scan_file(path, home, samples)
            except (OSError, ValueError, TypeError, AttributeError):
                error = Failure('snapshot', 'Corpus sample selection could not read a rollout.')
                samples.failures.append({'sample': {'file': path.name, 'boundaryIndex': None},
                                         'failure': diagnostics(error)})
    return samples


def modes_from_catalog(profile, models):
    advisors = {model for name, (model, _) in profile[0].items() if name.startswith('ca_advisor_')}
    if not advisors:
        raise Failure('catalog', 'The routing profile declares no advisor models.')
    modes = {True: [], False: []}
    for model in sorted(advisors):
        entries = [entry for entry in models if entry.get('slug') == model]
        if len(entries) != 1:
            raise Failure('catalog', 'An advisor model is missing or duplicated in the host catalog.')
        modes[entries[0].get('use_responses_lite') is True].append(model)
    return ([{'use_responses_lite': lite, 'advisorModels': names} for lite, names in modes.items() if names],
            [{'use_responses_lite': lite, 'reason': 'No advisor model uses this request mode.'}
             for lite, names in modes.items() if not names])


def discover_request_modes():
    with local_home() as (home, _):
        process = native.launch(['codex', 'debug', 'models', '--bundled'], dict(os.environ), home)
        try:
            output, _ = process.communicate(timeout=30)
            if process.returncode != 0:
                raise Failure('catalog', 'Host bundled catalog discovery failed.')
            models = json.loads(output)['models']
        finally:
            native.terminate(process)
    return modes_from_catalog(load_profile(PLUGIN), models)


def expected_dial(caller, mode):
    profile = load_profile(PLUGIN)
    model, effort = advisor_dial(profile, caller['model'], caller['effort'])
    if model not in mode['advisorModels']:
        model, efforts = next((model, efforts) for name, (model, efforts) in profile[0].items()
                              if name.startswith('ca_advisor_') and model in mode['advisorModels'])
        effort = efforts[0]
    return {'model': model, 'effort': effort}


def verify_excluded_requests(requests):
    excluded = {kind for kind, policy in ITEM_POLICY.items()
                if policy['policy'] in ('capability', 'control', 'hosted')}
    for request in requests:
        if request.get('tools', []) != []:
            raise Failure('tools', 'The loopback request carries tools.',
                          details={'stage': 'request', 'type': 'request', 'path': 'tools'})
        for index, item in enumerate(request.get('input', [])):
            if item.get('tools', []) != []:
                raise Failure('tools', 'The loopback request item carries tools.', details={
                    'stage': 'request', 'type': item.get('type'), 'path': f'input[{index}].tools'})
            if item.get('type') in excluded:
                raise Failure('context', 'An excluded caller item reached the loopback request.', details={
                    'stage': 'request', 'type': item['type'], 'path': f'input[{index}].type'})


def run_mode(caller, mode, mutation=None):
    catalog = native.catalog

    def checked_catalog(*args):
        path, executable = catalog(*args)
        data = json.loads(path.read_text(encoding='utf-8'))
        if (data['models'][0].get('use_responses_lite') is True) != mode['use_responses_lite']:
            raise Failure('catalog', 'The advisor request mode changed after catalog discovery.')
        return path, executable

    with local_home() as (home, endpoint), ExitStack() as stack:
        stack.enter_context(mock.patch.object(native, 'catalog', side_effect=checked_catalog))
        if mutation == 'transport-fields':
            comparable = native.comparable
            source_ids = {item['id'] for item in caller['items'] if isinstance(item.get('id'), str)}

            def broken(item, omit_image_detail=False):
                value = comparable(item, omit_image_detail)
                if isinstance(item.get('id'), str) and item['id'] in source_ids:
                    value['id'] = item['id']
                return value

            stack.enter_context(mock.patch.object(native, 'comparable', side_effect=broken))
        expected = expected_dial(caller, mode)
        result = native.execute(home, caller, expected, threading.Event())
        if not endpoint.requests or result['status'] != 'succeeded':
            raise Failure('trace', 'The native check did not produce a verified loopback request.')
        verify_excluded_requests(endpoint.requests)


def check(roots):
    modes, not_covered = discover_request_modes()
    samples = select_samples(roots)
    verdicts = []
    for kind, sample in sorted(samples.best.items()):
        for mode in modes:
            verdict = {'type': kind, 'sample': {key: sample[key] for key in ('file', 'boundaryIndex')},
                       'sampleKind': sample['sampleKind'],
                       'use_responses_lite': mode['use_responses_lite']}
            try:
                run_mode(sample['caller'], mode)
                verdict['status'] = 'passed'
            except Failure as error:
                verdict.update(status='failed', failure=diagnostics(error))
            verdicts.append(verdict)
    uncovered = sorted(samples.present - samples.best.keys())
    return {'counts': {**samples.counts, 'presentTypes': len(samples.present),
                      'sampledTypes': len(samples.best), 'runs': len(verdicts),
                      'preservedTypes': sum(s['sampleKind'] == 'preserved' for s in samples.best.values()),
                      'excludedTypes': sum(s['sampleKind'] == 'excluded' for s in samples.best.values()),
                      'passed': sum(v['status'] == 'passed' for v in verdicts),
                      'failed': sum(v['status'] == 'failed' for v in verdicts)},
            'requestModes': modes, 'notCovered': not_covered,
            'uncoveredTypes': uncovered, 'samplingFailures': samples.failures, 'verdicts': verdicts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', action='append', type=Path)
    args = parser.parse_args()
    roots = args.root if args.root is not None else default_roots()
    if args.root and any(not root.is_dir() for root in roots):
        print(json.dumps({'failure': diagnostics(Failure('root', 'An explicit session root is not a directory.'))}))
        return 1
    try:
        report = check(roots)
    except Failure as error:
        print(json.dumps({'failure': diagnostics(error)}))
        return 1
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired):
        print(json.dumps({'failure': diagnostics(Failure('catalog', 'Host request mode discovery failed.'))}))
        return 1
    print(json.dumps(report))
    return int(bool(report['counts']['failed'] or report['samplingFailures'] or report['uncoveredTypes']))


if __name__ == '__main__':
    sys.exit(main())
