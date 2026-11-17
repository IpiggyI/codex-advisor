"""Replay one original consultation through the current source and native provider."""

import importlib.util
import json
import os
from pathlib import Path
import sys
import threading
from unittest import mock

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'plugins/codex-advisor/scripts'))
import consult_native as native
from consult_limits import failure_count

home = Path(os.environ['CODEX_HOME'])
thread = os.environ['CODEX_THREAD_ID']
plugin = home / 'plugins/cache/codex-advisor/codex-advisor/0.3.8'
process = Path('/proc/1040126')
if process.joinpath('cwd').resolve() != plugin or failure_count(home, thread) != 2:
    raise SystemExit('Original MCP process or failure-count precondition changed; no consultation started.')
environment = dict(entry.split('=', 1) for entry in process.joinpath('environ').read_bytes().decode().split('\0')
                   if '=' in entry)
path, = (home / 'sessions').rglob('*' + thread + '*.jsonl')
rows = [json.loads(line) for line in path.read_bytes().splitlines() if line.strip()]
boundary = 31
item = rows[boundary]['payload']
if item.get('call_id') != 'call_988aac2b794a4654943ad8a981de6533':
    raise SystemExit('Original consultation boundary changed; no consultation started.')
current = next(row['payload'] for row in reversed(rows[:boundary]) if row['type'] == 'turn_context')
session = rows[0]['payload']
meta = {'threadId': thread, 'sessionId': session.get('session_id', thread), 'itemId': item['id'],
        'x-codex-turn-metadata': {'thread_id': thread, 'session_id': session.get('session_id', thread),
                                'turn_id': current['turn_id'], 'model': current['model'],
                                'reasoning_effort': current['effort']}}
snapshot = b'\n'.join(json.dumps(row).encode('utf-8') for row in rows[:boundary + 1])
read_bytes = Path.read_bytes
spec = importlib.util.spec_from_file_location('consultation', REPO / 'plugins/codex-advisor/scripts/process-consultation.py')
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)
mcp = server.MCP()
mcp.plugin = plugin
diagnostics = native.Diagnostics()
with mock.patch.dict(os.environ, environment, clear=True), \
        mock.patch.object(Path, 'read_bytes', autospec=True,
                          side_effect=lambda target: snapshot if target == path else read_bytes(target)), \
        mock.patch.object(native, 'Diagnostics', return_value=diagnostics):
    response = mcp.consultation({'id': 1, 'params': {
        'name': 'process_consultation', 'arguments': {}, '_meta': meta}}, threading.Event())['result']
result = {'sourceBoundary': boundary, 'sourceHost': session.get('cli_version'),
          'outcome': response['structuredContent'], 'finalTiming': diagnostics.snapshot()}
evidence = Path(__file__).with_name('evidence')
evidence.mkdir(exist_ok=True)
evidence.joinpath('real-consultation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False), flush=True)
