"""Credential-free loopback provider for production native-chain checks."""

from contextlib import contextmanager
import http.server
import json
import os
from pathlib import Path
import tempfile
import threading
from unittest import mock


class Endpoint(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        self.server.requests.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
        interrupted = self.server.disconnect_first and len(self.server.requests) == 1
        text = json.dumps({'kind': 'plan', 'advice': 'Retry the local check.' if interrupted else self.server.advice})
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


@contextmanager
def local_home():
    with tempfile.TemporaryDirectory(prefix='ca-corpus-native-') as directory:
        home = Path(directory)
        endpoint = http.server.HTTPServer(('127.0.0.1', 0), Endpoint)
        endpoint.requests, endpoint.disconnect_first = [], False
        endpoint.advice = 'Preserve the caller history and continue the local check.'
        listener = threading.Thread(target=endpoint.serve_forever, daemon=True)
        listener.start()
        (home / 'config.toml').write_text(
            'model_provider = "diagnostic"\n'
            '[model_providers.diagnostic]\nname = "Local diagnostic"\n'
            f'base_url = "http://127.0.0.1:{endpoint.server_port}/v1"\n'
            'wire_api = "responses"\nrequires_openai_auth = false\n'
            'request_max_retries = 0\nstream_max_retries = 0\n', encoding='utf-8')
        # Native children receive process essentials and no provider credentials or user homes.
        env = {key: value for key, value in os.environ.items() if key in (
            'PATH', 'SYSTEMROOT', 'SystemRoot', 'WINDIR', 'COMSPEC', 'PATHEXT', 'LANG', 'LC_ALL')}
        env.update(HOME=str(home), USERPROFILE=str(home), CODEX_HOME=str(home),
                   XDG_CONFIG_HOME=str(home / 'config'), XDG_DATA_HOME=str(home / 'data'),
                   TMPDIR=str(home), TEMP=str(home), TMP=str(home))
        try:
            with mock.patch.dict(os.environ, env, clear=True):
                yield home, endpoint
        finally:
            endpoint.shutdown()
            endpoint.server_close()
            listener.join()
            endpoint.requests.clear()
