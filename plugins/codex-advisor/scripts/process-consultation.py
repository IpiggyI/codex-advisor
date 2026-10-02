#!/usr/bin/env python3
"""Zero-argument, newline JSON-RPC MCP consultation server."""

import json
from pathlib import Path
import signal
import sys
import threading

sys.dont_write_bytecode = True
from consult_context import Failure, caller_home, identity, reconstruct, route
from consult_limits import FAILURE_LIMIT, STOP_CALLING, failure_count, limit_result
from consult_native import execute

TOOL = {'name': 'process_consultation',
        'description': 'Consult on your current effective context automatically. Takes no arguments. '
                       'Returns a plan, correction, or stop with verified advisor model and effort; '
                       'an explicit failure leaves the work pending. '
                       'On failure, state it in your next visible reply; do not present it as advice '
                       'or declare consultation complete. When consultationDisabled is true, stop calling '
                       'in this thread and continue authorized work with consultation marked unavailable.',
        'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False},
        'annotations': {'readOnlyHint': False, 'destructiveHint': False, 'openWorldHint': False}}


def result_text(result):
    if result['status'] == 'succeeded':
        actual = result['actual']
        return (result['advice'].strip() + '\n\n' + result['kind'] + ' | ' +
                actual['model'] + '[' + actual['effort'] + ']')
    text = 'Consultation failed: ' + result['message'] + '\nCode: ' + result['code']
    if result.get('details'):
        text += '\nDetails: ' + json.dumps(result['details'], ensure_ascii=False)
    return text


class MCP:
    def __init__(self):
        self.output_lock = threading.Lock()
        self.calls = {}
        self.plugin = Path(__file__).resolve().parent.parent

    def send(self, message):
        with self.output_lock:
            try:
                print(json.dumps({'jsonrpc': '2.0', **message}, ensure_ascii=False), flush=True)
            except BrokenPipeError:
                self.cancel_all()

    def cancel_all(self):
        for cancel, _ in list(self.calls.values()):
            cancel.set()

    def consultation(self, request, cancel):
        expected = home = thread = None
        try:
            params = request.get('params', {})
            home = caller_home(self.plugin)
            identity(params.get('_meta'))
            thread = params['_meta']['threadId']
            if failure_count(home, thread) >= FAILURE_LIMIT:
                raise Failure('disabled', 'Consultation is disabled after four failed calls. ' + STOP_CALLING)
            if params.get('name') != TOOL['name'] or params.get('arguments', {}) != {}:
                raise Failure('arguments', 'Process consultation accepts only an empty argument object.')
            caller = reconstruct(home, params.get('_meta'))
            expected = route(self.plugin, caller)
            result = execute(home, caller, expected, cancel)
        except Failure as error:
            result = {'status': 'failed', 'code': error.code, 'message': str(error),
                      'expected': expected, 'actual': error.actual}
            if error.details:
                result['details'] = error.details
        except Exception:
            # Native output and source history may contain sensitive content.
            result = {'status': 'failed', 'code': 'internal',
                      'message': 'Consultation encountered an unsupported host response or local I/O failure.',
                      'expected': expected, 'actual': None}
        result = limit_result(result, home, thread)
        self.send({'id': request['id'], 'result': {'isError': result['status'] == 'failed',
                   'structuredContent': result, 'content': [{'type': 'text', 'text': result_text(result)}]}})

    def dispatch(self, request):
        method, request_id = request.get('method'), request.get('id')
        if method == 'notifications/cancelled':
            active = self.calls.get(request.get('params', {}).get('requestId'))
            if active:
                active[0].set()
            return
        if request_id is None:
            return
        if method == 'initialize':
            self.send({'id': request_id, 'result': {'protocolVersion': '2024-11-05',
                       'capabilities': {'tools': {}},
                       'serverInfo': {'name': 'codex-advisor-consult', 'version': '1'}}})
        elif method == 'tools/list':
            self.send({'id': request_id, 'result': {'tools': [TOOL]}})
        elif method == 'ping':
            self.send({'id': request_id, 'result': {}})
        elif method == 'tools/call':
            if request_id in self.calls:
                self.send({'id': request_id, 'error': {'code': -32600, 'message': 'Duplicate request identity.'}})
                return
            cancel = threading.Event()
            thread = threading.Thread(target=self.consultation, args=(request, cancel))
            self.calls[request_id] = (cancel, thread)
            thread.start()
        else:
            self.send({'id': request_id, 'error': {'code': -32601, 'message': 'Unknown MCP method.'}})

    def run(self):
        def stop(_signal, _frame):
            self.cancel_all()
            raise SystemExit(0)
        signal.signal(signal.SIGTERM, stop)
        signal.signal(signal.SIGINT, stop)
        try:
            for line in sys.stdin:
                try:
                    request = json.loads(line)
                    if not isinstance(request, dict):
                        raise ValueError()
                    self.dispatch(request)
                except (ValueError, TypeError):
                    self.send({'id': None, 'error': {'code': -32700, 'message': 'Invalid JSON-RPC input.'}})
        finally:
            self.cancel_all()
            for _, thread in list(self.calls.values()):
                thread.join()


if __name__ == '__main__':
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    MCP().run()
