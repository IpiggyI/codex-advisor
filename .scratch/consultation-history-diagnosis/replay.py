#!/usr/bin/env python3
"""离线重放指定咨询边界，只输出结构，不输出历史正文。"""

import argparse
import importlib.util
import json
from pathlib import Path
import tempfile


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('rollout', type=Path)
parser.add_argument('line', type=int)
parser.add_argument('--scripts', type=Path, default=Path(__file__).resolve().parents[2] / 'plugins/codex-advisor/scripts')
args = parser.parse_args()
spec = importlib.util.spec_from_file_location('context', args.scripts / 'consult_context.py')
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)
records = [json.loads(line) for line in args.rollout.read_text(encoding='utf-8').splitlines() if line.strip()][:args.line]
session = records[0]['payload']
turn = next(row['payload'] for row in reversed(records) if row['type'] == 'turn_context')
boundary = records[-1]['payload']
assert 'process_consultation' in str(boundary), '边界必须是实际咨询调用'
meta = {'threadId': session['id'], 'sessionId': session.get('session_id', session['id']),
        'itemId': boundary['id']}
meta['x-codex-turn-metadata'] = {'thread_id': meta['threadId'], 'session_id': meta['sessionId'],
                                'turn_id': turn['turn_id'], 'model': turn['model'],
                                'reasoning_effort': turn['effort']}
history = []
origins = []
for number, row in enumerate(records[:-1], 1):
    if row['type'] == 'compacted':
        history = row['payload']['replacement_history'].copy()
        origins = [number] * len(history)
    elif row['type'] == 'response_item':
        history.append(row['payload'])
        origins.append(number)


def verdict(items):
    try:
        context.validate_items(items)
        return 'PASS'
    except context.Failure as error:
        return error.code + ': ' + str(error)


with tempfile.TemporaryDirectory(prefix='ca-history-diagnosis-') as directory:
    home = Path(directory)
    (home / 'sessions').mkdir()
    (home / 'sessions' / (session['id'] + '.jsonl')).write_text(
        '\n'.join(json.dumps(row) for row in records), encoding='utf-8')
    try:
        context.reconstruct(home, meta)
        result = 'PASS'
    except context.Failure as error:
        result = error.code + ': ' + str(error)
print(json.dumps({'rollout': str(args.rollout), 'callLine': args.line,
                  'hostVersion': session.get('cli_version'), 'items': len(history),
                  'reconstruct': result}, ensure_ascii=False))
known = {'message', 'agent_message', 'reasoning', 'compaction', 'function_call',
         'custom_tool_call', 'function_call_output', 'custom_tool_call_output'}
unknown = [(i, item) for i, item in enumerate(history) if item.get('type') not in known]
for index, item in unknown:
    minimized = verdict([item])
    assert minimized == 'unsupported_content: The caller has an unqualified history item.'
    print(json.dumps({'index': index, 'sourceLine': origins[index], 'type': item.get('type'),
                      'keys': list(item), 'singleItem': minimized,
                      'withoutThisItem': verdict(history[:index] + history[index + 1:])}, ensure_ascii=False))
if unknown:
    assert result == 'unsupported_content: The caller has an unqualified history item.'
    assert verdict([]) == 'PASS'
    print('已复现并缩减到单个未知历史条目。删除条目仅用于离线因果验证，不是修复方案。')
