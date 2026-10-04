#!/usr/bin/env python3
"""Replay a saved consultation boundary; retain only bounded diagnostic metadata."""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import threading

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'plugins/codex-advisor/scripts'))
import consult_native as native
from consult_context import reconstruct, route

parser = argparse.ArgumentParser()
parser.add_argument('rollout', type=Path)
parser.add_argument('--line', type=int, required=True)
parser.add_argument('--live-home', type=Path)
args = parser.parse_args()
raw = args.rollout.read_bytes()
records = [json.loads(line) for line in raw.splitlines()]
turn = None
for index, record in enumerate(records):
    payload = record['payload']
    if record['type'] == 'turn_context':
        turn = payload
    if record['type'] != 'response_item' or payload.get('type') not in ('function_call', 'custom_tool_call'):
        continue
    if args.line and index + 1 != args.line:
        continue
    if 'process_consultation' not in json.dumps(payload):
        continue
    break
else:
    raise SystemExit('No matching consultation boundary.')

header = records[0]['payload']
thread = header['id']
session = header.get('session_id', thread)
meta = {'threadId': thread, 'sessionId': session, 'itemId': payload['id'],
        'x-codex-turn-metadata': {'thread_id': thread, 'session_id': session,
                                'turn_id': turn['turn_id'], 'model': turn['model'],
                                'reasoning_effort': turn['effort']}}
summary = {'thread': thread, 'sourceSha256': hashlib.sha256(raw).hexdigest(),
           'boundaryLine': index + 1, 'nativeErrors': [], 'platform': os.name}
original = native.native_failure


def capture(error, message):
    content = json.dumps(error, ensure_ascii=False)
    terms = ('Missing environment variable', 'S2A_API_KEY', 'API key', 'authentication',
             'image', '401', '403', '429', 'timeout', 'certificate', 'proxy', 'keyring',
             'Access is denied', 'os error', 'No such file', 'invalid', 'decrypt')
    summary['nativeErrors'].append({'keys': list(error) if isinstance(error, dict) else [],
                                    'length': len(content),
                                    'terms': [term for term in terms if term in content]})
    text = error.get('message', '') if isinstance(error, dict) else ''
    if text.startswith('Missing environment variable'):
        import re
        summary['nativeErrors'][-1]['messageShape'] = re.sub(r'[A-Za-z_]+', 'WORD', text)
    return original(error, message)


native.native_failure = capture
with tempfile.TemporaryDirectory(prefix='ca-history-replay-') as temporary:
    snapshot = Path(temporary)
    (snapshot / 'sessions').mkdir()
    (snapshot / 'sessions' / args.rollout.name).write_text(
        '\n'.join(json.dumps(record) for record in records[:index + 1]), encoding='utf-8')
    caller = reconstruct(snapshot, meta)
    expected = route(REPO / 'plugins/codex-advisor', caller)
    summary.update(sourceItems=len(caller['items']), expected=expected)
    check = None
    if args.live_home:
        home = args.live_home
    else:
        spec = importlib.util.spec_from_file_location('host_check', REPO / 'tests/verify-consultation-host.py')
        host = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(host)
        check = host.NativeHistory()
        check.setUp()
        home = check.home
    try:
        result = native.execute(home, caller, expected, threading.Event())
        summary.update(status=result['status'], actual=result['actual'])
    except native.Failure as error:
        summary.update(status='failed', code=error.code, message=str(error),
                       details=error.details, actual=error.actual)
    finally:
        if check:
            summary['requestCount'] = len(check.endpoint.requests)
            check.tearDown()
print(json.dumps(summary, ensure_ascii=False, indent=2))
sys.exit(0 if summary['status'] == 'succeeded' else 1)
