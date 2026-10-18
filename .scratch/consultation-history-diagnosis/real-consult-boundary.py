#!/usr/bin/env python3
"""对一个真实咨询边界用真实认证做一次咨询，只输出结构化结果，不输出历史或建议正文。"""

import argparse
import json
from pathlib import Path
import sys
import tempfile
import threading

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('rollout', type=Path)
parser.add_argument('line', type=int)
parser.add_argument('--scripts', type=Path, default=Path(__file__).resolve().parents[2] / 'plugins/codex-advisor/scripts')
args = parser.parse_args()
sys.path.insert(0, str(args.scripts))
from consult_context import Failure, reconstruct, route  # noqa: E402
from consult_native import execute  # noqa: E402

records = [json.loads(line) for line in args.rollout.read_text(encoding='utf-8').splitlines() if line.strip()][:args.line]
session = records[0]['payload']
turn = next(row['payload'] for row in reversed(records) if row['type'] == 'turn_context')
boundary = records[-1]['payload']
assert 'process_consultation' in str(boundary), '边界必须是实际咨询调用'
meta = {'threadId': session['id'], 'sessionId': session.get('session_id', session['id']), 'itemId': boundary['id'],
        'x-codex-turn-metadata': {'thread_id': session['id'], 'session_id': session.get('session_id', session['id']),
                                  'turn_id': turn['turn_id'], 'model': turn['model'], 'reasoning_effort': turn['effort']}}
raw = sorted({row['payload'].get('type') for row in records[:-1] if row['type'] == 'response_item'})
entry = {'rollout': args.rollout.name, 'callLine': args.line, 'hostVersion': session.get('cli_version'), 'rawTypes': raw}
try:
    with tempfile.TemporaryDirectory(prefix='ca-real-consult-') as directory:
        home = Path(directory)
        (home / 'sessions').mkdir()
        (home / 'sessions' / (session['id'] + '.jsonl')).write_text(
            '\n'.join(json.dumps(row) for row in records), encoding='utf-8')
        caller = reconstruct(home, meta)
    entry.update(injectedTypes=sorted({item['type'] for item in caller['items']}), injectedItems=len(caller['items']),
                 caller={'model': caller['model'], 'effort': caller['effort']})
    expected = route(args.scripts.parent, caller)
    result = execute(Path.home() / '.codex', caller, expected, threading.Event())
    entry.update(status=result['status'], kind=result['kind'], adviceChars=len(result['advice']),
                 expected=result['expected'], actual=result['actual'], advisorThreadId=result['advisorThreadId'])
except Failure as error:
    entry.update(status='failed', code=error.code, message=str(error), details=error.details, actual=error.actual)
print(json.dumps(entry, ensure_ascii=False, indent=2))
