#!/usr/bin/env python3
"""统计本机全部会话记录中各封闭清单的类型、次数和最早宿主版本，只输出类型名，不输出正文。"""

import collections
import json
from pathlib import Path

ROOTS = [Path('/home/hyy/.codex/sessions'), Path('/mnt/c/Users/Shy/.codex/sessions')]
# 与 consult_context.py 当前显式分支一致。
QUALIFIED = {
    'record': {'session_meta', 'turn_context', 'event_msg', 'compacted', 'retained_context',
               'inter_agent_communication_metadata', 'response_item', 'world_state', 'token_usage_record'},
    'retained': {'verified_answer', 'delivered_assistant_message'},
    'item': {'message', 'agent_message', 'reasoning', 'compaction', 'function_call',
             'custom_tool_call', 'function_call_output', 'custom_tool_call_output'},
    'role': {'system', 'developer', 'user', 'assistant'},
    'event': set(),
}


def version_key(version):
    try:
        return tuple(int(part) for part in version.split('-')[0].split('.'))
    except (AttributeError, ValueError):
        return (999,)


count, files, first = collections.Counter(), collections.Counter(), {}
total = 0
for root in ROOTS:
    for path in root.rglob('*.jsonl'):
        total += 1
        version, seen = None, set()

        def note(stage, kind):
            key = (stage, kind)
            count[key] += 1
            seen.add(key)
            if version and (key not in first or version_key(version) < version_key(first[key])):
                first[key] = version

        for line in path.open(encoding='utf-8', errors='replace'):
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if not isinstance(record, dict):
                continue
            kind, payload = record.get('type'), record.get('payload')
            if kind == 'session_meta' and isinstance(payload, dict) and version is None:
                version = payload.get('cli_version')
            # 早于 session_meta 的旧格式记录没有宿主版本，不属于当前支持范围。
            if version is None:
                continue
            note('record', kind)
            if not isinstance(payload, dict):
                continue
            if kind == 'retained_context':
                note('retained', payload.get('type'))
            if kind == 'event_msg' and payload.get('type') == 'thread_rolled_back':
                note('event', payload.get('type'))
            items = [payload] if kind == 'response_item' else (
                payload.get('replacement_history') or [] if kind == 'compacted' else [])
            for item in items:
                if isinstance(item, dict):
                    note('item', item.get('type'))
                    if item.get('type') == 'message':
                        note('role', item.get('role'))
        for key in seen:
            files[key] += 1

rows = [{'stage': stage, 'type': kind, 'count': count[(stage, kind)], 'files': files[(stage, kind)],
         'earliestHeaderVersion': first.get((stage, kind)), 'qualified': kind in QUALIFIED[stage]}
        for stage, kind in sorted(count, key=lambda key: (key[0], str(key[1])))]
print(json.dumps({'rolloutFiles': total, 'roots': [str(root) for root in ROOTS], 'rows': rows,
                  'boundary': '最早版本取包含该类型的文件头版本；续接会话的文件头可能早于写入该条目的宿主版本。'
                              'thread_rolled_back 是有意拒绝的回滚，不是遗漏。'},
                 ensure_ascii=False, indent=2))
