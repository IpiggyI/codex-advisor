#!/usr/bin/env python3
"""用真实认证对指定类型的最小真实历史各做一次咨询，只输出结构化结果，不输出历史或建议正文。"""

import json
from pathlib import Path
import sys
import threading

repo = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo / 'plugins/codex-advisor/scripts'))
sys.path.insert(0, str(repo / 'tests'))
from consult_context import Failure, route  # noqa: E402
from consult_native import execute  # noqa: E402
from consultation_corpus_replay import default_roots  # noqa: E402
from consultation_native_corpus import select_samples  # noqa: E402

WANTED = ('web_search_call', 'additional_tools', 'tool_search_output')
samples = select_samples(default_roots())
results = []
for kind in WANTED:
    sample = samples.best.get(kind)
    if sample is None:
        results.append({'type': kind, 'status': 'no_sample'})
        continue
    caller = sample['caller']
    entry = {'type': kind, 'sampleKind': sample['sampleKind'], 'file': sample['file'],
             'boundaryIndex': sample['boundaryIndex'], 'rawExcludedTypes': sample['rawExcludedTypes'],
             'injectedTypes': sorted({item['type'] for item in caller['items']}),
             'injectedItems': len(caller['items']), 'hostVersion': caller.get('hostVersion'),
             'caller': {'model': caller['model'], 'effort': caller['effort']}}
    try:
        expected = route(repo / 'plugins/codex-advisor', caller)
        result = execute(Path.home() / '.codex', caller, expected, threading.Event())
        entry.update(status=result['status'], kind=result['kind'], adviceChars=len(result['advice']),
                     expected=result['expected'], actual=result['actual'],
                     advisorThreadId=result['advisorThreadId'])
    except Failure as error:
        entry.update(status='failed', code=error.code, message=str(error), details=error.details,
                     actual=error.actual)
    results.append(entry)
    print(json.dumps(entry, ensure_ascii=False), file=sys.stderr, flush=True)
print(json.dumps({'results': results}, ensure_ascii=False, indent=2))
