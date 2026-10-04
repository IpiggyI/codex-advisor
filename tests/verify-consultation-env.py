#!/usr/bin/env python3
"""Check the installed plugin's environment through actual native MCP startup."""

import http.server
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parent.parent
PLUGIN = REPO / 'plugins/codex-advisor'
sys.path.insert(0, str(PLUGIN / 'scripts'))
from consult_native import Server, catalog, configuration, windows_codex

EXPECTED = {'model': 'gpt-6.1-sol', 'effort': 'xhigh'}
ADVICE = 'Preserve the caller history and continue the authorized test.'

PROBE = '''import json, os, pathlib, sys
pathlib.Path(sys.argv[1]).write_text(json.dumps({
    "providerPresent": os.environ.get("S2A_API_KEY") == "inert-provider-marker",
    "unrelatedPresent": "CA_UNRELATED_SECRET" in os.environ
}), encoding="utf-8")
for line in sys.stdin:
    request = json.loads(line)
    if "id" not in request:
        continue
    result = {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
              "serverInfo": {"name": "env-probe", "version": "1"}}
    if request["method"] == "tools/list":
        result = {"tools": []}
    print(json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}), flush=True)
'''


class ConsultationEndpoint(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.requests.append(request)
        self.server.provider_headers.append(self.headers.get('Authorization') == 'Bearer inert-provider-marker')
        if request.get('text', {}).get('format', {}).get('type') == 'json_schema':
            self.server.consultation_temp_active = any((path / 'models.json').is_file()
                for path in self.server.consult_temp.glob('codex-advisor-consult-*'))
        item, deltas = self.response_item(request)
        events = [{'type': 'response.created', 'response': {'id': 'resp_local',
                   'status': 'in_progress', 'output': []}},
                  {'type': 'response.output_item.added', 'output_index': 0,
                   'item': dict(item, status='in_progress', **({'arguments': ''}
                           if item['type'] == 'function_call' else {'content': []}))},
                  *deltas, {'type': 'response.output_item.done', 'output_index': 0, 'item': item},
                  {'type': 'response.completed', 'response': {'id': 'resp_local', 'status': 'completed',
                   'output': [item], 'usage': {'input_tokens': 100, 'output_tokens': 10, 'total_tokens': 110}}}]
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        for event in events:
            self.wfile.write(('data: ' + json.dumps(event) + '\n\n').encode('utf-8'))
        self.wfile.flush()

    def response_item(self, request):
        inner = request.get('text', {}).get('format', {}).get('type') == 'json_schema'
        if len(self.server.requests) == 1:
            item = {'type': 'function_call', 'id': 'fc_consult', 'call_id': 'call_consult',
                    'namespace': 'mcp__codex_advisor', 'name': 'process_consultation',
                    'arguments': '{}', 'status': 'completed'}
            deltas = [{'type': 'response.function_call_arguments.delta', 'item_id': item['id'],
                       'output_index': 0, 'delta': '{}'}]
        else:
            text = json.dumps({'kind': 'plan', 'advice': ADVICE}) if inner else 'OUTER_COMPLETE'
            item = {'type': 'message', 'id': 'msg_local', 'role': 'assistant', 'status': 'completed',
                    'content': [{'type': 'output_text', 'text': text}]}
            deltas = [{'type': 'response.output_text.delta', 'item_id': item['id'],
                       'output_index': 0, 'content_index': 0, 'delta': text}]
        return item, deltas

    def log_message(self, *args):
        pass


class NativeEnvironment(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ca-mcp-environment-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        marketplace = self.source / '.agents/plugins'
        marketplace.mkdir(parents=True)
        shutil.copy2(REPO / '.agents/plugins/marketplace.json', marketplace)
        self.plugin = self.source / 'plugins/codex-advisor'
        shutil.copytree(PLUGIN, self.plugin)
        self.script = self.root / 'probe.py'
        self.script.write_text(PROBE, encoding='utf-8')
        self.observed = self.root / 'observed.json'
        self.home = self.root / 'home'
        self.home.mkdir()
        self.env = dict(os.environ, CODEX_HOME=str(self.home), S2A_API_KEY='inert-provider-marker',
                        CA_UNRELATED_SECRET='must-not-be-forwarded')

    def probe(self, forward):
        manifest = json.loads((self.plugin / '.mcp.json').read_text(encoding='utf-8'))
        config = manifest['mcpServers']['codex_advisor']
        config['args'] = [config['args'][0], str(self.script), str(self.observed)]
        if not forward:
            config.pop('env_vars', None)
        (self.plugin / '.mcp.json').write_text(json.dumps(manifest), encoding='utf-8')
        self.install()
        self.check_started_environment(forward)

    def install(self):
        executable = windows_codex(self.env) if os.name == 'nt' else shutil.which('codex')
        for arguments in (['plugin', 'marketplace', 'add', str(self.source)],
                          ['plugin', 'add', 'codex-advisor@codex-advisor']):
            result = subprocess.run([executable, *arguments, '--json'], env=self.env,
                                    cwd=self.root, capture_output=True, text=True,
                                    encoding='utf-8', timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)

    def check_started_environment(self, forward):
        server = Server(self.env, self.root, {'features.hooks': False, 'features.plugins': True,
                        'features.codex_hooks': False, 'features.plugin_hooks': False},
                        threading.Event(), time.monotonic() + 30)
        try:
            server.initialize()
            page = server.call('mcpServerStatus/list', {})
            self.assertIn('codex_advisor', [item['name'] for item in page['data']])
            self.assertTrue(self.observed.is_file(), 'The native host did not start the MCP probe.')
            self.assertEqual(json.loads(self.observed.read_text(encoding='utf-8')),
                             {'providerPresent': forward, 'unrelatedPresent': False})
        finally:
            server.close()

    def test_host_filters_undeclared_provider_environment(self):
        self.probe(False)

    def test_shipped_manifest_forwards_only_declared_provider_environment(self):
        self.probe(True)

    def start_endpoint(self):
        endpoint = http.server.ThreadingHTTPServer(('127.0.0.1', 0), ConsultationEndpoint)
        endpoint.requests = []
        endpoint.provider_headers = []
        listener = threading.Thread(target=endpoint.serve_forever, daemon=True)
        listener.start()
        def cleanup():
            endpoint.shutdown()
            endpoint.server_close()
            listener.join()
        self.addCleanup(cleanup)
        (self.home / 'config.toml').write_text(
            'model_provider = "diagnostic"\n[model_providers.diagnostic]\nname = "Local diagnostic"\n'
            f'base_url = "http://127.0.0.1:{endpoint.server_port}/v1"\n'
            'wire_api = "responses"\nrequires_openai_auth = false\nenv_key = "S2A_API_KEY"\n'
            'request_max_retries = 0\nstream_max_retries = 0\n', encoding='utf-8')
        self.consult_temp = self.root / 'consult-temp'
        self.consult_temp.mkdir()
        endpoint.consult_temp = self.consult_temp
        endpoint.consultation_temp_active = False
        manifest_path = self.plugin / '.mcp.json'
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        manifest['mcpServers']['codex_advisor']['env'] = {
            name: str(self.consult_temp) for name in ('TMPDIR', 'TEMP', 'TMP')}
        manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
        return endpoint

    def run_outer_turn(self, timeout=60):
        values = configuration(self.root, EXPECTED)
        values['features.plugins'] = True
        # Reserve outer tool-output capacity for the complete MCP result.
        budget = {'items': [{'type': 'function_call_output', 'output': 'x' * 4096}]}
        values['model_catalog_json'] = str(catalog(self.env, self.root, threading.Event(),
                time.monotonic() + 30, (EXPECTED['model'], budget)))
        server = Server(self.env, self.root, values, threading.Event(), time.monotonic() + timeout)
        try:
            server.initialize()
            started = server.call('thread/start', {'model': EXPECTED['model'], 'cwd': str(self.root),
                                 'ephemeral': False, 'approvalPolicy': 'never', 'sandbox': 'read-only',
                                 'baseInstructions': 'Consult before completing the test.', 'developerInstructions': ''})
            thread = started['thread']['id']
            server.call('turn/start', {'threadId': thread, 'model': EXPECTED['model'],
                              'effort': EXPECTED['effort'],
                              'input': [{'type': 'text', 'text': 'CHAIN_EARLIEST_CONSTRAINT'}]})
            completed = []
            while True:
                event = server.pending.pop(0) if server.pending else server.receive()
                if event.get('method') == 'item/completed':
                    completed.append(event['params']['item'])
                if event.get('method') == 'turn/completed':
                    self.assertEqual(event['params']['turn']['status'], 'completed', event)
                    return thread, completed
        finally:
            server.close()

    def test_shipped_plugin_completes_native_consultation_chain(self):
        endpoint = self.start_endpoint()
        self.install()
        thread, completed = self.run_outer_turn()
        consultation = next(item for item in completed if item['type'] == 'mcpToolCall')
        result = consultation['result']['structuredContent']
        print('Native consultation result:', json.dumps(result), flush=True)
        self.assertEqual(result['status'], 'succeeded', result)
        self.assertEqual(consultation['status'], 'completed')
        self.assertIsNone(consultation['error'])
        self.assertEqual(result['actual'], EXPECTED)
        self.assertEqual(result['expected'], EXPECTED)
        self.assertEqual(result['callerThreadId'], thread)
        self.assertEqual(result['advice'], ADVICE)
        self.assertEqual(result['failureCount'], 0)
        self.assertFalse(result['consultationDisabled'])
        self.assertEqual(completed[-1]['text'], 'OUTER_COMPLETE')
        self.assertEqual(len(endpoint.requests), 3)
        self.assertTrue(all(endpoint.provider_headers))
        self.check_inner_request(endpoint.requests[1])
        returned = next(item for item in endpoint.requests[2]['input'] if item.get('call_id') == 'call_consult'
                        and item['type'] == 'function_call_output')
        self.assertIn(ADVICE, returned['output'])
        self.assertRegex(returned['output'], r'"status"\s*:\s*"succeeded"')
        self.assertTrue(endpoint.consultation_temp_active, 'The test did not observe native temporary output.')
        self.assertEqual(list(self.consult_temp.iterdir()), [], 'Consultation temporary output survived.')

    def check_inner_request(self, request):
        self.assertEqual(request['model'], EXPECTED['model'])
        self.assertEqual(request['reasoning']['effort'], EXPECTED['effort'])
        self.assertTrue(any(item.get('role') == 'user' and any(
            block.get('text') == 'CHAIN_EARLIEST_CONSTRAINT' for block in item.get('content', []))
            for item in request['input']))
        inventories = [item for item in request['input'] if item['type'] == 'additional_tools']
        self.assertTrue(inventories or request.get('tools') == [])
        self.assertTrue(all(item['tools'] == [] for item in inventories))
        self.assertFalse(request.get('tools'))
        self.assertEqual(len(list((self.home / 'sessions').rglob('*.jsonl'))), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
