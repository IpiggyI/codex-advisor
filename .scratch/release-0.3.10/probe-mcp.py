"""Check a fresh installed MCP launcher without requesting consultation."""

import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--home', type=Path, required=True)
args = parser.parse_args()
plugin = args.home / 'plugins/cache/codex-advisor/codex-advisor/0.3.10'
shell = r'C:\Program Files\Git\bin\sh.exe' if os.name == 'nt' else 'sh'
requests = [
    {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
        'protocolVersion': '2024-11-05', 'capabilities': {},
        'clientInfo': {'name': 'release-startup-check', 'version': '1'}}},
    {'jsonrpc': '2.0', 'method': 'notifications/initialized', 'params': {}},
    {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list', 'params': {}}]
result = subprocess.run([shell, './scripts/run-python.sh', './scripts/process-consultation.py'],
    cwd=plugin, env=dict(os.environ, CODEX_HOME=str(args.home), PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1'),
    input=''.join(json.dumps(value) + '\n' for value in requests),
    capture_output=True, text=True, encoding='utf-8', timeout=30)
if result.returncode:
    raise SystemExit('Installed MCP launcher failed; exit code ' + str(result.returncode))
responses = {value['id']: value for line in result.stdout.splitlines()
             if (value := json.loads(line)).get('id') in (1, 2)}
assert all('result' in responses[key] for key in (1, 2)), 'MCP initialization or inventory failed.'
tools = responses[2]['result']['tools']
assert len(tools) == 1 and tools[0]['name'] == 'process_consultation'
print(json.dumps({'version': '0.3.10', 'initialize': 'passed', 'toolInventory': 'passed',
                  'consultationRequested': False, 'processExitCode': result.returncode}))
