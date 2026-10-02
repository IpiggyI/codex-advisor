#!/usr/bin/env python3
"""Check real native request construction against a local, unauthenticated endpoint."""

import http.server
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest

sys.dont_write_bytecode = True
PLUGIN = Path(__file__).resolve().parent.parent / 'plugins/codex-advisor'
sys.path.insert(0, str(PLUGIN / 'scripts'))
from consult_native import execute

ADVICE = '保留全部上下文。'
EXPECTED = {'model': 'gpt-6.1-sol', 'effort': 'xhigh'}


class Endpoint(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        self.server.requests.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
        interrupted = self.server.disconnect_first and len(self.server.requests) == 1
        text = json.dumps({'kind': 'plan', 'advice': '过期建议。' if interrupted else ADVICE}, ensure_ascii=False)
        item = {'type': 'message', 'id': 'msg_local', 'role': 'assistant', 'status': 'completed',
                'content': [{'type': 'output_text', 'text': text}]}
        events = [
            {'type': 'response.created', 'response': {'id': 'resp_local', 'status': 'in_progress', 'output': []}},
            {'type': 'response.output_item.added', 'output_index': 0,
             'item': dict(item, status='in_progress', content=[])},
            {'type': 'response.output_text.delta', 'item_id': 'msg_local', 'output_index': 0,
             'content_index': 0, 'delta': text},
            {'type': 'response.output_item.done', 'output_index': 0, 'item': item},
            {'type': 'response.completed', 'response': {'id': 'resp_local', 'status': 'completed',
             'output': [item], 'usage': {'input_tokens': 100, 'output_tokens': 10, 'total_tokens': 110}}}]
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        for event in events[:-1] if interrupted else events:
            self.wfile.write(('data: ' + json.dumps(event, ensure_ascii=False) + '\n\n').encode('utf-8'))
        self.wfile.flush()

    def log_message(self, *args):
        pass


class NativeHistory(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ca-native-history-')
        self.home = Path(self.temp.name)
        self.endpoint = http.server.HTTPServer(('127.0.0.1', 0), Endpoint)
        self.endpoint.requests = []
        self.endpoint.disconnect_first = False
        self.listener = threading.Thread(target=self.endpoint.serve_forever, daemon=True)
        self.listener.start()
        (self.home / 'config.toml').write_text(
            'model_provider = "diagnostic"\n'
            '[model_providers.diagnostic]\nname = "Local diagnostic"\n'
            f'base_url = "http://127.0.0.1:{self.endpoint.server_port}/v1"\n'
            'wire_api = "responses"\nrequires_openai_auth = false\n'
            'request_max_retries = 0\nstream_max_retries = 0\n', encoding='utf-8')

    def tearDown(self):
        self.endpoint.shutdown()
        self.endpoint.server_close()
        self.listener.join()
        self.temp.cleanup()

    def consult(self, output, tool_type='custom_tool_call', request_count=1):
        caller = {'base': 'Keep the caller history intact.', 'thread': 'local-test', 'items': [
            {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'EARLIEST_CONSTRAINT'}]},
            {'type': tool_type, 'name': 'fixture', 'call_id': 'call_local',
             ('input' if tool_type == 'custom_tool_call' else 'arguments'): '{}'},
            {'type': tool_type + '_output', 'call_id': 'call_local', 'output': output}]}
        result = execute(self.home, caller, EXPECTED, threading.Event())
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(result['actual'], EXPECTED)
        self.assertEqual(result['advice'], ADVICE)
        self.assertEqual(len(self.endpoint.requests), request_count)
        request = self.endpoint.requests[-1]
        return next(item['output'] for item in request['input'] if item.get('type') == tool_type + '_output')

    def test_long_tool_output_is_not_truncated(self):
        output = [{'type': 'input_text', 'text': 'BEGIN\n' + 'row 中文 ' * 20000 + '\nEND'}]
        self.assertEqual(self.consult(output), output)

    def test_empty_tool_text_block_is_lossless(self):
        output = [{'type': 'input_text', 'text': 'NONEMPTY'}, {'type': 'input_text', 'text': ''}]
        self.assertEqual(self.consult(output), output[:1])

    def test_function_output_is_not_truncated(self):
        output = 'BEGIN\n' + 'line ' * 20000 + '\nEND'
        self.assertEqual(self.consult(output, 'function_call'), output)

    def test_retry_discards_answer_from_interrupted_stream(self):
        self.endpoint.disconnect_first = True
        config = self.home / 'config.toml'
        config.write_text(config.read_text(encoding='utf-8').replace(
            'stream_max_retries = 0', 'stream_max_retries = 1'), encoding='utf-8')
        self.assertEqual(self.consult('RETAINED_OUTPUT', request_count=2), 'RETAINED_OUTPUT')


if __name__ == '__main__':
    unittest.main(verbosity=2)
