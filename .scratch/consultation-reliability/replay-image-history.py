#!/usr/bin/env python3
"""Replay consultation boundaries through the native host and a local endpoint."""

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import threading

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('host_check', REPO / 'tests/verify-consultation-host.py')
host = importlib.util.module_from_spec(spec)
spec.loader.exec_module(host)
from consult_context import reconstruct


def replay_boundary(path, snapshot, turn):
    session, payload = snapshot[0]['payload'], snapshot[-1]['payload']
    thread = session['id']
    root_session = session.get('session_id', thread)
    meta = {'threadId': thread, 'sessionId': root_session, 'itemId': payload['id'],
            'x-codex-turn-metadata': {'thread_id': thread, 'session_id': root_session,
                                    'turn_id': turn['turn_id'], 'model': turn['model'],
                                    'reasoning_effort': turn['effort']}}
    check = host.NativeHistory()
    check.setUp()
    try:
        (check.home / 'sessions').mkdir()
        (check.home / 'sessions' / path.name).write_text(
            '\n'.join(json.dumps(value) for value in snapshot), encoding='utf-8')
        caller = reconstruct(check.home, meta)
        expected = {'model': turn['model'], 'effort': turn['effort']}
        result = host.execute(check.home, caller, expected, threading.Event())
        assert result['status'] == 'succeeded' and result['actual'] == expected
        return {'boundaryLine': len(snapshot), 'sourceItems': len(caller['items']),
                'requestItems': len(check.endpoint.requests[0]['input']),
                'status': result['status'], 'actual': result['actual']}
    finally:
        check.tearDown()


def replay(path):
    raw = path.read_bytes()
    records = [json.loads(line) for line in raw.splitlines() if line.strip()]
    turn, results = None, []
    for index, record in enumerate(records):
        payload = record['payload']
        if record['type'] == 'turn_context':
            turn = payload
        if (record['type'] == 'response_item' and payload.get('type') == 'custom_tool_call' and
                'process_consultation' in payload.get('input', '')):
            results.append(replay_boundary(path, records[:index + 1], turn))
    assert results, 'No consultation boundaries found.'
    return {'thread': records[0]['payload']['id'],
            'rolloutSha256': hashlib.sha256(raw).hexdigest(), 'results': results}


if __name__ == '__main__':
    print(json.dumps(replay(Path(sys.argv[1])), ensure_ascii=False, indent=2))
