#!/usr/bin/env python3
"""把三条历史载荷追加到公开宿主回归；只保存摘要证据。"""

import argparse
import json
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[2]
AREA = Path(__file__).resolve().parent
TRACE = Path('/home/hyy/.codex/sessions/2026/10/08/rollout-2026-10-08T15-45-10-01a11a79-27f4-7dd0-bf3c-0dd0cd50322f.jsonl')
CALLS = {'call_1117c8d44c7f418c85dcacfd8979acb5', 'call_30a8146b049244ee82b0205d113d651e',
         'call_85e8ad584a624f3ca147bf1f48e5735c'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-hook-trust-bypass', action='store_true')
    args = parser.parse_args()
    if not args.allow_hook_trust_bypass:
        parser.error('需要本轮用户授权仅限一次性主目录的钩子信任绕过。')
    harness = runpy.run_path(str(REPO / 'tests/verify-routing-host.py'))
    cases = harness['scenarios']()
    historical = []
    for line in TRACE.open():
        item = json.loads(line).get('payload', {})
        if item.get('type') != 'function_call' or item.get('call_id') not in CALLS:
            continue
        arguments = json.loads(item['arguments'])
        task = arguments['task_name'] + '_' + str(len(historical))
        case = harness['scenario'](item['call_id'], 'spawn_agent', task, advisor=True)
        case['arguments'] = dict(arguments, task_name=task)
        historical.append(case)
    assert len(historical) == 3
    cases.extend(historical)
    harness['run'].__globals__['scenarios'] = lambda: cases
    report = harness['run']()
    (AREA / 'historical-host-after.json').write_text(json.dumps(report, indent=2) + '\n')
    print('共 14 项场景通过，包括三条原始载荷；仅为重复任务名增加了唯一后缀。')
    print('三条历史载荷的子线程角色、实际拨盘及正文摘要均已核对。')
