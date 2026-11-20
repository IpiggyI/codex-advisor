#!/usr/bin/env python3
"""Replay local tool boundaries without emitting history or contacting a server."""

import argparse
from contextlib import ExitStack
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'plugins/codex-advisor/scripts'))
from consult_context import Failure, ITEM_POLICY, pair_identity, reconstruct, standalone_output


def default_roots():
    return [Path.home() / '.codex/sessions',
            *sorted(Path('/mnt/c/Users').glob('*/.codex/sessions'))]


def failure(path, boundary, error):
    return {'file': path.name, 'boundaryIndex': boundary,
            'recordIndex': error.details.get('recordIndex', boundary),
            'stage': error.details.get('stage', 'record'), 'type': error.details.get('type'),
            'code': error.code, 'message': str(error),
            **({'withLaterRecords': True} if error.details.get('withLaterRecords') else {})}


class CallBatch:
    def __init__(self):
        self.pending = {}
        self.invalid = False

    def track(self, item):
        if not isinstance(item, dict):
            return
        kind = item.get('type')
        policy = ITEM_POLICY.get(kind, {}) if isinstance(kind, str) else {}
        shape = policy.get('shape')
        if shape not in ('call', 'result'):
            return
        if standalone_output(item, policy):
            return
        try:
            call = pair_identity(item, policy)
        except Failure:
            self.invalid = True
            return
        if call is None:
            self.invalid = True
        elif shape == 'call':
            self.invalid |= call in self.pending
            self.pending[call] = (policy['pair'], policy['policy'], kind)
        elif (call in self.pending and self.pending[call][:2] ==
              (kind, policy.get('call_policies', {}).get(self.pending[call][2], policy['policy']))):
            del self.pending[call]
        else:
            self.invalid = True

    def observe(self, record):
        if not isinstance(record, dict):
            return
        if record.get('type') == 'response_item':
            self.track(record.get('payload'))
        elif record.get('type') == 'compacted':
            self.pending.clear()
            self.invalid = False
            payload = record.get('payload')
            history = payload.get('replacement_history') if isinstance(payload, dict) else None
            if isinstance(history, list):
                for item in history:
                    self.track(item)
            else:
                self.invalid = True


def compare_with_later_records(home, target, source, meta, expected):
    offset = source.tell()
    try:
        shutil.copyfileobj(source, target)
    finally:
        source.seek(offset)
    target.flush()
    try:
        actual = reconstruct(home, meta)
        if actual != expected:
            raise Failure('post_boundary', 'Later records changed the reconstructed context.')
    except Failure as error:
        error.details['withLaterRecords'] = True
        raise


def replay_boundary(home, target, record, session, current, *, source=None):
    offset = target.tell()
    payload = record['payload']
    # The boundary is excluded from history; a temporary id selects id-less host calls.
    marker = payload.get('id') or 'corpus-boundary-' + str(offset)
    selected = {**record, 'payload': {**payload, 'id': marker}}
    target.write(json.dumps(selected).encode('utf-8') + b'\n')
    target.flush()
    meta = {'threadId': session.get('id'), 'sessionId': session.get('session_id', session.get('id')),
            'itemId': marker, 'x-codex-turn-metadata': {
                'thread_id': session.get('id'),
                'session_id': session.get('session_id', session.get('id')),
                'turn_id': current.get('turn_id'), 'model': current.get('model'),
                'reasoning_effort': current.get('effort')}}
    try:
        expected = reconstruct(home, meta)
        if source is not None and source.peek(1):
            compare_with_later_records(home, target, source, meta, expected)
        return expected
    finally:
        target.seek(offset)
        target.truncate()


def replay_file(path, home, counts, failures, design_rejections):
    target = None
    current, started = None, False
    batch = CallBatch()
    with ExitStack() as stack:
        source = stack.enter_context(path.open('rb'))
        for index, line in enumerate(source):
            if not line.strip():
                if target:
                    target.write(line)
                continue
            try:
                record = json.loads(line)
            except (ValueError, UnicodeError):
                failures.append(failure(path, index, Failure('snapshot', 'Rollout record cannot be decoded.')))
                return
            if target is None:
                if not isinstance(record, dict) or record.get('type') != 'session_meta':
                    counts['legacyFilesSkipped'] += 1
                    return
                session = record.get('payload')
                session = session if isinstance(session, dict) else {}
                thread = session.get('id') if isinstance(session, dict) else None
                name = thread if isinstance(thread, str) and re.fullmatch(r'[0-9a-fA-F-]{36}', thread) else 'invalid'
                target = stack.enter_context((home / 'sessions' / ('rollout-' + name + '.jsonl')).open('wb'))
            kind = record.get('type') if isinstance(record, dict) else None
            payload = record.get('payload', {}) if isinstance(record, dict) else {}
            if kind == 'turn_context':
                current = payload if isinstance(payload, dict) else {}
            if kind == 'event_msg' and isinstance(payload, dict) and payload.get('type') == 'task_started':
                started = True
            boundary = kind == 'response_item' and isinstance(payload, dict) and payload.get('type') in (
                'function_call', 'custom_tool_call')
            if boundary:
                counts['boundaries'] += 1
                if current is None or not started:
                    counts['boundariesSkipped'] += 1
                    counts['beforeTurnContext'] += int(current is None)
                    counts['beforeTaskStarted'] += int(not started)
                elif batch.pending and not batch.invalid:
                    counts['boundariesSkipped'] += 1
                    counts['parallelSkipped'] += 1
                else:
                    counts['replayed'] += 1
                    try:
                        replay_boundary(home, target, record, session, current, source=source)
                        counts['passed'] += 1
                    except Failure as error:
                        diagnostics = (design_rejections if error.code == 'rollback'
                                       and not error.details.get('withLaterRecords') else failures)
                        diagnostics.append(failure(path, index, error))
            target.write(line)
            batch.observe(record)


def replay(roots):
    counts = dict(files=0, legacyFilesSkipped=0, boundaries=0, boundariesSkipped=0,
                  beforeTurnContext=0, beforeTaskStarted=0, parallelSkipped=0, replayed=0, passed=0)
    failures, design_rejections = [], []
    paths = sorted({path.resolve() for root in roots for path in root.rglob('*.jsonl')})
    for path in paths:
        counts['files'] += 1
        with tempfile.TemporaryDirectory(prefix='ca-corpus-') as directory:
            home = Path(directory)
            (home / 'sessions').mkdir()
            try:
                replay_file(path, home, counts, failures, design_rejections)
            except OSError:
                failures.append(failure(path, None, Failure('snapshot', 'Rollout replay I/O failed.')))
    by_code = {}
    for rejection in design_rejections:
        code = rejection['code']
        by_code[code] = by_code.get(code, 0) + 1
    return {'counts': {**counts, 'failures': len(failures), 'designRejections': by_code},
            'failures': failures, 'designRejections': design_rejections}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', action='append', type=Path,
                        help='Session root; repeat to replace the default roots.')
    args = parser.parse_args()
    roots = args.root if args.root is not None else default_roots()
    if args.root and any(not root.is_dir() for root in roots):
        print(json.dumps({'counts': {'failures': 1}, 'failures': [
            {'file': None, 'recordIndex': None, 'stage': 'record', 'type': None,
             'code': 'root', 'message': 'An explicit session root is not a directory.'}]}))
        return 1
    report = replay(roots)
    print(json.dumps(report))
    return int(bool(report['failures']))


if __name__ == '__main__':
    sys.exit(main())
