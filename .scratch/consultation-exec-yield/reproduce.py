"""Replay a real rollout at a consultation boundary with a chosen read point.
usage: reproduce.py <rollout> <boundaryIndex> <lastIndexVisible>"""
import json, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'plugins/codex-advisor/scripts'))
from consult_context import reconstruct, Failure
src, boundary, last = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
lines = [l for l in src.read_text(encoding='utf-8').splitlines() if l.strip()]
recs = [json.loads(l) for l in lines]
session = recs[0]['payload']
turn = next(r['payload'] for r in reversed(recs[:boundary]) if r['type'] == 'turn_context')
item = recs[boundary]['payload']
with tempfile.TemporaryDirectory() as home:
    (Path(home) / 'sessions').mkdir()
    (Path(home) / 'sessions' / src.name).write_text('\n'.join(lines[:last + 1]) + '\n', encoding='utf-8')
    meta = {'threadId': session['id'], 'sessionId': session.get('session_id', session['id']), 'itemId': item['id'],
            'x-codex-turn-metadata': {'thread_id': session['id'], 'session_id': session.get('session_id', session['id']),
                                      'turn_id': turn['turn_id'], 'model': turn['model'], 'reasoning_effort': turn['effort']}}
    try:
        caller = reconstruct(Path(home), meta)
        print('OK items=%d' % len(caller['items']))
    except Failure as e:
        print('FAIL', e.code, str(e), json.dumps(e.details))
