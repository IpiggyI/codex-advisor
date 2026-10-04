#!/usr/bin/env python3
"""Check MCP request lifetimes independently of native inference."""

import importlib.util
import io
import json
from contextlib import ExitStack
from pathlib import Path
import queue
import sys
import threading
import unittest
from unittest import mock

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parent.parent / 'plugins/codex-advisor/scripts'
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('consultation_mcp', SCRIPTS / 'process-consultation.py')
mcp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mcp)


class RequestLifetime(unittest.TestCase):
    def setUp(self):
        self.server = mcp.MCP()
        self.responses = queue.Queue()
        self.server.send = self.responses.put
        self.release = threading.Event()
        self.started = threading.Event()

        def execute(home, caller, expected, cancel):
            self.started.set()
            self.release.wait(2)
            if cancel.is_set():
                raise mcp.Failure('cancelled', 'Consultation was cancelled.')
            return {'status': 'succeeded', 'kind': 'plan', 'advice': 'Complete.', 'actual': expected}

        patches = ExitStack()
        self.addCleanup(patches.close)
        for name, value in [('caller_home', lambda _: Path('/unused')),
                            ('identity', lambda _: None), ('failure_count', lambda *_: 0),
                            ('reconstruct', lambda *_: {}), ('route', lambda *_: {'model': 'm', 'effort': 'high'}),
                            ('limit_result', lambda result, *_: result), ('execute', execute)]:
            patches.enter_context(mock.patch.object(mcp, name, value))

    def tearDown(self):
        self.release.set()
        self.server.cancel_all()

    def call(self):
        self.server.dispatch({'id': 'call-1', 'method': 'tools/call', 'params': {
            'name': 'process_consultation', '_meta': {'threadId': 'fixture'}}})
        self.assertTrue(self.started.wait(1))

    def test_finished_request_is_released_and_id_can_be_reused(self):
        self.call()
        worker = self.server.calls['call-1'][1]
        self.release.set()
        worker.join(2)
        self.assertFalse(worker.is_alive())
        self.assertEqual(self.responses.get(timeout=1)['id'], 'call-1')
        self.assertEqual(self.server.calls, {})
        self.started.clear()
        self.call()
        self.assertIn('result', self.responses.get(timeout=1))

    def test_duplicate_active_request_preserves_original_cancellation(self):
        self.call()
        original = self.server.calls['call-1']
        self.server.dispatch({'id': 'call-1', 'method': 'tools/call', 'params': {}})
        self.assertEqual(self.responses.get(timeout=1)['error']['code'], -32600)
        self.assertIs(self.server.calls['call-1'], original)
        self.server.dispatch({'method': 'notifications/cancelled', 'params': {'requestId': 'call-1'}})
        self.release.set()
        self.assertEqual(self.responses.get(timeout=1)['result']['structuredContent']['code'], 'cancelled')
        original[1].join(2)

    def test_invalid_cancellation_does_not_terminate_server(self):
        requests = [{'method': 'notifications/cancelled', 'params': None},
                    {'method': 'notifications/cancelled', 'params': {'requestId': []}},
                    {'id': 'alive', 'method': 'ping'}]
        stream = io.StringIO('\n'.join(json.dumps(request) for request in requests))
        with mock.patch.object(sys, 'stdin', stream), mock.patch.object(mcp.signal, 'signal'):
            self.server.run()
        self.assertEqual(self.responses.get(timeout=1)['error']['code'], -32700)
        self.assertEqual(self.responses.get(timeout=1)['error']['code'], -32700)
        self.assertEqual(self.responses.get(timeout=1), {'id': 'alive', 'result': {}})

    def test_failed_request_thread_start_releases_request(self):
        with mock.patch.object(threading.Thread, 'start', side_effect=RuntimeError('cannot start new thread')):
            with self.assertRaises(RuntimeError):
                self.server.dispatch({'id': 'call-1', 'method': 'tools/call', 'params': {}})
        self.assertEqual(self.server.calls, {})


if __name__ == '__main__':
    unittest.main(verbosity=2)
