#!/usr/bin/env python3
"""Exercise the installed MCP boundary with a synthetic home and native fixture."""

import copy
import base64
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent / 'plugins/codex-advisor'
THREAD = '11111111-1111-1111-1111-111111111111'
SESSION = '22222222-2222-2222-2222-222222222222'
TURN = '33333333-3333-3333-3333-333333333333'


def item(text, role='user'):
    return {'type': 'message', 'role': role, 'content': [{'type': 'input_text', 'text': text}]}


def agent_item():
    return {'type': 'agent_message', 'id': 'amsg_fixture', 'author': '/root',
            'recipient': '/root/worker', 'content': [
                {'type': 'input_text', 'text': 'Message Type: NEW_TASK\nTask name: worker'},
                {'type': 'encrypted_content', 'encrypted_content': 'opaque-agent-bytes-74813'}],
            'internal_chat_message_metadata_passthrough': {'turn_id': TURN, 'create_time': 'fixture'}}


def fixture(model='gpt-6-sol', effort='high', role=None):
    session = {'id': THREAD, 'session_id': SESSION, 'base_instructions': {'text': 'SOURCE_BASE_INSTRUCTIONS'},
               'source': 'cli', 'agent_role': role}
    if role:
        session['source'] = {'subagent': {'thread_spawn': {'agent_role': role}}}
    records = [{'type': 'session_meta', 'payload': session},
               {'type': 'event_msg', 'payload': {'type': 'task_started', 'turn_id': TURN}},
               {'type': 'turn_context', 'payload': {'turn_id': TURN, 'model': model, 'effort': effort}}]
    history = [item('EARLIEST_CONSTRAINT 保留约束')]
    if role:
        history.append(agent_item())
    history += [item('uncompacted turn ' + str(i)) for i in range(80)]
    history += [{'type': 'reasoning', 'summary': [], 'encrypted_content': 'opaque-unchanged-123'},
                {'type': 'message', 'role': 'user', 'content': [
                    {'type': 'input_image', 'image_url': 'data:image/png;base64,AAA=', 'detail': 'original'}]},
                {'type': 'custom_tool_call', 'id': 'ctc_previous', 'call_id': 'tool1', 'name': 'functions.exec',
                 'input': 'read nonce'},
                {'type': 'custom_tool_call_output', 'call_id': 'tool1',
                 'output': 'TRUNCATED: caller-visible bytes\nNONCE_74813'}]
    records += [{'type': 'response_item', 'payload': value} for value in history]
    records += [{'type': 'response_item', 'payload': {'type': 'custom_tool_call',
                 'id': 'ctc_consult', 'call_id': 'consult1', 'name': 'functions.exec', 'input': 'consult'}}]
    meta = {'threadId': THREAD, 'sessionId': SESSION, 'itemId': 'ctc_consult',
            'x-codex-turn-metadata': {'thread_id': THREAD, 'session_id': SESSION,
                                    'turn_id': TURN, 'model': model, 'reasoning_effort': effort}}
    return records, meta, history


class Boundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.windows_fixture = None
        if os.name != 'nt':
            return
        cls.windows_fixture = tempfile.TemporaryDirectory(prefix='ca-native-fixture-')
        cls.fixture_exe = Path(cls.windows_fixture.name) / 'codex.exe'
        source = r'''
using System;
using System.Diagnostics;
using System.Text;
public class CodexFixture {
    static string Quote(string value) {
        StringBuilder output = new StringBuilder("\"");
        int slashes = 0;
        foreach (char c in value) {
            if (c == '\\') { slashes++; continue; }
            output.Append('\\', c == '"' ? slashes * 2 + 1 : slashes);
            output.Append(c); slashes = 0;
        }
        output.Append('\\', slashes * 2); output.Append('"');
        return output.ToString();
    }
    public static int Main(string[] args) {
        ProcessStartInfo start = new ProcessStartInfo(Environment.GetEnvironmentVariable("CONSULT_FIXTURE_PYTHON"));
        start.Arguments = "-B " + Quote(Environment.GetEnvironmentVariable("CONSULT_FIXTURE_SCRIPT"));
        foreach (string value in args) { start.Arguments += " " + Quote(value); }
        start.UseShellExecute = false;
        Process child = Process.Start(start); child.WaitForExit(); return child.ExitCode;
    }
}
'''
        script = "Add-Type -TypeDefinition @'\n" + source + "\n'@ -OutputType ConsoleApplication -OutputAssembly '" + str(cls.fixture_exe).replace("'", "''") + "'"
        encoded = base64.b64encode(script.encode('utf-16le')).decode('ascii')
        result = subprocess.run(['powershell.exe', '-NoProfile', '-EncodedCommand', encoded],
                                capture_output=True, text=True, timeout=30)
        if result.returncode or not cls.fixture_exe.is_file():
            cls.windows_fixture.cleanup()
            raise AssertionError('Windows native fixture compilation failed: ' + result.stderr)

    @classmethod
    def tearDownClass(cls):
        if cls.windows_fixture:
            cls.windows_fixture.cleanup()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ca-consult-boundary-')
        self.root = Path(self.temp.name)
        self.home = self.root / 'home'
        self.plugin = self.home / 'plugins/cache/codex-advisor/codex-advisor/0.2.0'
        shutil.copytree(PLUGIN, self.plugin)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        target = self.bin / ('consult-codex.py' if os.name == 'nt' else 'codex')
        shutil.copy2(HERE / 'fixtures/consult-codex.py', target)
        target.chmod(0o755)
        if os.name == 'nt':
            shutil.copy2(self.fixture_exe, self.bin / 'codex.exe')
        (self.root / 'tmp').mkdir()
        self.env = dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ['PATH'],
                        CONSULT_FIXTURE_ROOT=str(self.root), TMPDIR=str(self.root / 'tmp'),
                        CODEX_HOME=str(self.home), PYTHONDONTWRITEBYTECODE='1')
        if os.name == 'nt':
            self.env.update(CONSULT_FIXTURE_PYTHON=sys.executable, CONSULT_FIXTURE_SCRIPT=str(target),
                            PATH=str(self.bin) + os.pathsep + str(Path(os.environ['SystemRoot']) / 'System32'))
        self.process = None

    def tearDown(self):
        if self.process:
            self.process.stdin.close()
            self.process.wait(timeout=10)
            self.process.stdout.close()
            self.process.stderr.close()
        self.temp.cleanup()

    def start(self, records, scenario='plan', bad_layout=False):
        sessions = self.home / 'sessions/2026/09/26'
        sessions.mkdir(parents=True, exist_ok=True)
        (sessions / ('rollout-' + THREAD + '.jsonl')).write_text(
            ''.join(json.dumps(r) + '\n' for r in records))
        self.before = {str(p.relative_to(self.home)): p.read_bytes()
                       for p in self.home.rglob('*') if p.is_file()}
        self.env['CONSULT_FIXTURE_CASE'] = scenario
        script = self.plugin / 'scripts/process-consultation.py'
        if bad_layout:
            script = PLUGIN / 'scripts/process-consultation.py'
        self.process = subprocess.Popen([sys.executable, str(script)], stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                        env=self.env, cwd=self.root)
        self.responses = queue.Queue()
        def read():
            for line in self.process.stdout:
                self.responses.put(json.loads(line))
        threading.Thread(target=read, daemon=True).start()

    def send(self, method, params, request=1):
        value = {'jsonrpc': '2.0', 'method': method, 'params': params}
        if request is not None:
            value['id'] = request
        self.process.stdin.write(json.dumps(value) + '\n')
        self.process.stdin.flush()

    def result(self):
        response = self.responses.get(timeout=15)
        self.assertEqual(response['id'], 1)
        result = response['result']
        self.assertEqual(json.loads(result['content'][0]['text']), result['structuredContent'])
        self.assertEqual(result['isError'], result['structuredContent']['status'] == 'failed')
        self.assertFalse(list((self.root / 'tmp').iterdir()), 'consultation temporary state survived')
        after = {str(p.relative_to(self.home)): p.read_bytes()
                 for p in self.home.rglob('*') if p.is_file()}
        self.assertEqual(self.before, after, 'component modified CODEX_HOME')
        return result['structuredContent']

    def call(self, records, meta, scenario='plan', arguments=None, bad_layout=False):
        self.start(records, scenario, bad_layout)
        self.send('tools/call', {'name': 'process_consultation',
                  'arguments': {} if arguments is None else arguments, '_meta': meta})
        return self.result()

    def test_schema_and_annotations(self):
        config = json.loads((self.plugin / '.mcp.json').read_text())
        self.assertEqual(config, {'mcpServers': {'codex_advisor': {
            'command': 'sh', 'args': ['./scripts/run-python.sh', './scripts/process-consultation.py'], 'cwd': '.'}}})
        manifest = json.loads((self.plugin / '.codex-plugin/plugin.json').read_text())
        self.assertEqual(manifest['mcpServers'], './.mcp.json')
        records, _, _ = fixture()
        self.start(records)
        self.send('tools/list', {})
        tool = self.responses.get(timeout=5)['result']['tools'][0]
        self.assertEqual(tool['name'], 'process_consultation')
        self.assertEqual(tool['inputSchema'], {'type': 'object', 'properties': {}, 'additionalProperties': False})
        self.assertEqual(tool['annotations'], {'readOnlyHint': True, 'destructiveHint': False, 'openWorldHint': False})

    def test_earliest_unfinished_images_reasoning_and_truncation(self):
        records, meta, history = fixture()
        result = self.call(records, meta)
        self.assertEqual(result['status'], 'succeeded', result)
        injected = json.loads((self.root / 'injected.json').read_text())
        self.assertEqual(injected[:-1], history)
        self.assertEqual(injected[-1]['role'], 'developer')
        inventory = [json.loads(line) for line in (self.root / 'inventory-calls.jsonl').read_text().splitlines()]
        self.assertTrue(all(message['method'] in ('initialize', 'initialized', 'mcpServerStatus/list') for message in inventory))

    def test_compaction_replaces_history(self):
        records, meta, _ = fixture()
        replacement = [item('COMPACTION_SUMMARY'), item('RETAINED_EARLIEST')]
        records.insert(-3, {'type': 'compacted', 'payload': {'replacement_history': replacement}})
        result = self.call(records, meta)
        self.assertEqual(result['status'], 'succeeded', result)
        injected = json.loads((self.root / 'injected.json').read_text())
        self.assertEqual(injected[:-1], replacement + [r['payload'] for r in records[-3:-1]])
        self.assertNotIn('EARLIEST_CONSTRAINT', json.dumps(injected))

    def test_native_world_state_and_attribution(self):
        records, meta, history = fixture()
        history[0]['internal_chat_message_metadata_passthrough'] = {
            'turn_id': TURN, 'create_time': '2026-09-26', 'content_item_kinds': ['user.text']}
        records.insert(3, {'type': 'world_state', 'payload': {'type': 'full', 'state': {'model': 'gpt-6-sol'}}})
        records.insert(4, {'type': 'token_usage_record', 'payload': {'thread_id': THREAD, 'turn_id': TURN}})
        result = self.call(records, meta)
        self.assertEqual(result['status'], 'succeeded', result)
        self.assertEqual(json.loads((self.root / 'injected.json').read_text())[:-1], history)

    def test_delegate_trigger_metadata(self):
        records, meta, history = fixture('gpt-6-luna', 'max', 'ca_worker_mainstay_m')
        records.insert(1, {'type': 'inter_agent_communication_metadata', 'payload': {'trigger_turn': True}})
        result = self.call(records, meta)
        self.assertEqual(result['status'], 'succeeded', result)
        self.assertEqual(json.loads((self.root / 'injected.json').read_text())[:-1], history)

    def test_delegate_encrypted_content_changed(self):
        records, meta, history = fixture('gpt-6-luna', 'max', 'ca_worker_mainstay_m')
        result = self.call(records, meta, 'changed-agent-content')
        self.assertEqual(result['status'], 'failed', result)
        self.assertEqual(result['code'], 'context', result)
        self.assertEqual(result['actual'], result['expected'])
        self.assertEqual(json.loads((self.root / 'injected.json').read_text())[:-1], history)

    def test_cancellation_terminates_tree(self):
        records, meta, _ = fixture()
        self.start(records, 'cancel')
        self.send('tools/call', {'name': 'process_consultation', 'arguments': {}, '_meta': meta})
        deadline = time.monotonic() + 10
        while not (self.root / 'child.pid').exists() and time.monotonic() < deadline:
            time.sleep(.02)
        self.assertTrue((self.root / 'child.pid').exists())
        pid = int((self.root / 'child.pid').read_text())
        self.send('notifications/cancelled', {'requestId': 1}, request=None)
        result = self.result()
        self.assertEqual(result['code'], 'cancelled', result)
        self.assert_process_ended(pid)

    def assert_process_ended(self, pid):
        if os.name == 'nt':
            import ctypes
            api = ctypes.WinDLL('kernel32', use_last_error=True)
            api.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
            api.OpenProcess.restype = ctypes.c_void_p
            api.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            api.CloseHandle.argtypes = [ctypes.c_void_p]
            handle = api.OpenProcess(0x100000, False, pid)
            if handle:
                try:
                    self.assertEqual(api.WaitForSingleObject(handle, 3000), 0)
                finally:
                    self.assertTrue(api.CloseHandle(handle))
            else:
                self.assertEqual(ctypes.get_last_error(), 87)
        else:
            state = Path('/proc') / str(pid) / 'stat'
            self.assertTrue(not state.exists() or state.read_text().split()[2] == 'Z')

    def test_parent_exit_does_not_hide_descendant(self):
        records, meta, _ = fixture()
        result = self.call(records, meta, 'orphan')
        self.assertEqual(result['status'], 'succeeded', result)
        self.assert_process_ended(int((self.root / 'child.pid').read_text()))

    def inject_cleanup_failure(self, api=None):
        # Inject an OS-boundary failure into the separate MCP process, while
        # still performing real termination/handle closure to keep tests clean.
        source = '''
import ctypes, os
if os.name == 'nt':
    original = ctypes.WinDLL
    class FailedCall:
        def __init__(self, native):
            object.__setattr__(self, 'native', native)
        def __setattr__(self, key, value):
            setattr(self.native, key, value)
        def __call__(self, *args):
            if os.environ.get('CONSULT_FIXTURE_FAIL_AFTER_START') == '1' and not os.path.isfile(os.path.join(os.environ['CONSULT_FIXTURE_ROOT'], 'cleanup-fail')):
                return self.native(*args)
            if os.environ['CONSULT_FIXTURE_FAIL_API'] != 'CreateJobObjectW':
                self.native(*args)
            ctypes.set_last_error(5)
            return 0
    def load(name, *args, **kwargs):
        library = original(name, *args, **kwargs)
        if name.lower() == 'kernel32':
            target = os.environ['CONSULT_FIXTURE_FAIL_API']
            setattr(library, target, FailedCall(getattr(library, target)))
        return library
    ctypes.WinDLL = load
else:
    original = os.killpg
    def fail(group, sig):
        if os.environ.get('CONSULT_FIXTURE_FAIL_AFTER_START') == '1' and not os.path.isfile(os.path.join(os.environ['CONSULT_FIXTURE_ROOT'], 'cleanup-fail')):
            return original(group, sig)
        try:
            original(group, sig)
        except ProcessLookupError:
            pass
        raise PermissionError('fixture cleanup error')
    os.killpg = fail
'''
        (self.bin / 'sitecustomize.py').write_text(source)
        self.env['PYTHONPATH'] = str(self.bin)
        self.env['CONSULT_FIXTURE_FAIL_API'] = api or 'TerminateJobObject'

    def test_cleanup_failure_is_explicit(self):
        self.inject_cleanup_failure()
        records, meta, _ = fixture()
        result = self.call(records, meta)
        self.assertEqual(result['status'], 'failed', result)
        self.assertEqual(result['code'], 'cleanup', result)
        self.assertIsNone(result['actual'])
        self.assertNotIn('advice', result)

    def test_cancel_cleanup_failure_retains_cause(self):
        self.inject_cleanup_failure()
        self.env['CONSULT_FIXTURE_FAIL_AFTER_START'] = '1'
        records, meta, _ = fixture()
        self.start(records, 'cancel')
        self.send('tools/call', {'name': 'process_consultation', 'arguments': {}, '_meta': meta})
        deadline = time.monotonic() + 10
        while not (self.root / 'child.pid').exists() and time.monotonic() < deadline:
            time.sleep(.02)
        self.assertTrue((self.root / 'child.pid').exists())
        (self.root / 'cleanup-fail').write_text('fail the OS cleanup boundary')
        self.send('notifications/cancelled', {'requestId': 1}, request=None)
        result = self.result()
        self.assertEqual(result['code'], 'cleanup', result)
        self.assertIn('cancelled', result['message'])
        self.assert_process_ended(int((self.root / 'child.pid').read_text()))

    @unittest.skipUnless(os.name == 'nt', 'Windows native npm lookup requires Windows')
    def test_windows_native_npm_layout(self):
        target = self.bin / 'node_modules/@openai/codex/node_modules/@openai/codex-win32-x64/vendor/x86_64-pc-windows-msvc/bin/codex.exe'
        target.parent.mkdir(parents=True)
        (self.bin / 'codex.exe').rename(target)
        (self.bin / 'codex.cmd').write_text('@exit /b 99\r\n')
        records, meta, _ = fixture()
        result = self.call(records, meta)
        self.assertEqual(result['status'], 'succeeded', result)

    @unittest.skipUnless(os.name == 'nt', 'Windows native npm lookup requires Windows')
    def test_windows_native_npm_missing(self):
        (self.bin / 'codex.exe').unlink()
        (self.bin / 'codex.cmd').write_text('@exit /b 99\r\n')
        records, meta, _ = fixture()
        result = self.call(records, meta)
        self.assertEqual(result['code'], 'executor', result)
        self.assertFalse((self.root / 'inventory-calls.jsonl').exists())

    @unittest.skipUnless(os.name == 'nt', 'Windows native npm lookup requires Windows')
    def test_windows_native_npm_ambiguous(self):
        package = self.bin / 'node_modules/@openai/codex/vendor'
        for architecture in ('first', 'second'):
            target = package / architecture / 'bin/codex.exe'
            target.parent.mkdir(parents=True)
            shutil.copy2(self.bin / 'codex.exe', target)
        (self.bin / 'codex.exe').unlink()
        (self.bin / 'codex.cmd').write_text('@exit /b 99\r\n')
        records, meta, _ = fixture()
        result = self.call(records, meta)
        self.assertEqual(result['code'], 'executor', result)
        self.assertFalse((self.root / 'inventory-calls.jsonl').exists())


def cleanup_case(api):
    @unittest.skipUnless(os.name == 'nt', 'Windows Job Object API boundary requires Windows')
    def test(self):
        self.inject_cleanup_failure(api)
        records, meta, _ = fixture()
        result = self.call(records, meta)
        self.assertEqual(result['status'], 'failed', result)
        self.assertEqual(result['code'], 'cleanup', result)
    return test


for api in ('CreateJobObjectW', 'SetInformationJobObject', 'AssignProcessToJobObject',
            'QueryInformationJobObject', 'CloseHandle'):
    setattr(Boundary, 'test_windows_cleanup_' + api, cleanup_case(api))


def route_case(model, effort, role, expected):
    def test(self):
        records, meta, _ = fixture(model, effort, role)
        result = self.call(records, meta)
        self.assertEqual(result['status'], 'succeeded', result)
        self.assertEqual(result['actual'], dict(zip(('model', 'effort'), expected)))
        self.assertEqual(result['expected'], result['actual'])
    return test


for name, values in {
    'mainstay': ('gpt-6-luna', 'max', 'ca_worker_mainstay_m', ('gpt-6.1-sol', 'medium')),
    'mainstay_sol_6_1': ('gpt-6.1-sol', 'high', 'ca_worker_mainstay_h', ('gpt-6.1-sol', 'high')),
    'crux': ('gpt-6.1-sol', 'xhigh', 'ca_explorer_crux_h', ('gpt-6.1-sol', 'xhigh')),
    'crux_astra': ('gpt-6-astra', 'low', 'ca_worker_crux_h', ('gpt-6-astra', 'high')),
    'rescue': ('gpt-6-astra', 'high', 'ca_worker_rescue_h', ('gpt-6-astra', 'xhigh')),
    'rescue_sol_6_1': ('gpt-6.1-sol', 'max', 'ca_worker_rescue_m', ('gpt-6.1-sol', 'max')),
    'primary_astra': ('gpt-6-astra', 'xhigh', None, ('gpt-6-astra', 'xhigh')),
    'primary_astra_max': ('gpt-6-astra', 'max', None, ('gpt-6-astra', 'xhigh')),
    'primary_sol': ('gpt-6-sol', 'high', None, ('gpt-6.1-sol', 'xhigh')),
    'primary_sol_6_1': ('gpt-6.1-sol', 'high', None, ('gpt-6.1-sol', 'high')),
    'primary_sol_6_1_max': ('gpt-6.1-sol', 'max', None, ('gpt-6.1-sol', 'max')),
    'primary_unknown': ('gpt-5.6-terra', 'high', None, ('gpt-6.1-sol', 'xhigh')),
    'primary_medium': ('gpt-6-astra', 'medium', None, ('gpt-6-astra', 'medium')),
}.items():
    setattr(Boundary, 'test_route_' + name, route_case(*values))


def segment_case(mutation, expected=None):
    def test(self):
        path = self.plugin / 'skills/orchestration/references/routing-profile.md'
        original = path.read_text()
        changed = mutation(original)
        self.assertNotEqual(original, changed)
        path.write_text(changed)
        records, meta, _ = fixture('gpt-6-luna', 'max')
        result = self.call(records, meta)
        if expected is None:
            self.assertEqual(result['status'], 'failed', result)
            self.assertEqual(result['code'], 'profile', result)
            self.assertNotIn('advice', result)
            self.assertFalse((self.root / 'injected.json').exists())
        else:
            self.assertEqual(result['status'], 'succeeded', result)
            self.assertEqual(result['actual'], dict(zip(('model', 'effort'), expected)))
    return test


SEGMENT_ROWS = ('| `gpt-6-luna` | `starter` |\n'
                '| — | `midrange` |\n'
                '| `gpt-6.1-sol` | `premium` |\n'
                '| `gpt-6-astra` | `flagship` |\n')
for name, mutation, expected in [
    ('missing_table', lambda p: p.replace(SEGMENT_ROWS, ''), None),
    ('missing_model', lambda p: p.replace('| `gpt-6-luna` | `starter` |\n', ''), None),
    ('duplicate_model', lambda p: p.replace(SEGMENT_ROWS, SEGMENT_ROWS + '| `gpt-6-luna` | `premium` |\n'), None),
    ('unknown_segment', lambda p: p.replace('| `gpt-6-luna` | `starter` |', '| `gpt-6-luna` | `unknown` |'), None),
    ('row_order', lambda p: p.replace(SEGMENT_ROWS, ''.join(reversed(SEGMENT_ROWS.splitlines(keepends=True)))),
     ('gpt-6.1-sol', 'medium')),
    ('same_segment', lambda p: p.replace('| `gpt-6.1-sol` | `premium` |', '| `gpt-6.1-sol` | `starter` |'),
     ('gpt-6.1-sol', 'max')),
    ('changed_segment', lambda p: p.replace('| `gpt-6-luna` | `starter` |', '| `gpt-6-luna` | `flagship` |'),
     ('gpt-6-astra', 'xhigh')),
]:
    setattr(Boundary, 'test_segments_' + name, segment_case(mutation, expected))


def outcome_case(scenario, code):
    def test(self):
        records, meta, _ = fixture()
        result = self.call(records, meta, scenario)
        if code is None:
            self.assertEqual(result['status'], 'succeeded', result)
            self.assertEqual(result['kind'], scenario if scenario in ('plan', 'correction', 'stop') else 'plan')
        else:
            self.assertEqual(result['status'], 'failed', result)
            self.assertEqual(result['code'], code, result)
            self.assertNotIn('advice', result)
            if code == 'mismatch':
                self.assertIsNotNone(result['actual'])
                self.assertNotEqual(result['expected'], result['actual'])
            if scenario in ('tools', 'nonempty-top-tools', 'missing-inventory',
                            'lost-context', 'changed-context', 'changed-text'):
                self.assertEqual(result['actual'], result['expected'])
    return test


for scenario, code in {'correction': None, 'stop': None, 'error': 'executor', 'abort': 'executor',
                       'overflow': 'executor', 'empty': 'empty', 'bad-output': 'output',
                       'wrong-model': 'mismatch', 'wrong-effort': 'mismatch', 'earlier-mismatch': 'mismatch',
                       'tools': 'tools', 'top-tools': None, 'nonempty-top-tools': 'tools', 'missing-inventory': 'tools',
                       'no-trace': 'trace', 'tool-request': 'tools',
                       'lost-context': 'context', 'changed-context': 'context', 'changed-text': 'context',
                       'mcp-leak': 'isolation', 'hook-leak': 'isolation'}.items():
    setattr(Boundary, 'test_outcome_' + scenario.replace('-', '_'), outcome_case(scenario, code))


def rejection_case(mutation, code):
    def test(self):
        records, meta, _ = fixture()
        options = mutation(records, meta) or {}
        result = self.call(records, meta, **options)
        self.assertEqual(result['status'], 'failed', result)
        self.assertEqual(result['code'], code, result)
        self.assertFalse((self.root / 'injected.json').exists())
    return test


for name, mutation, code in [
    ('arguments', lambda r, m: {'arguments': {'summary': 'caller packet'}}, 'arguments'),
    ('layout', lambda r, m: {'bad_layout': True}, 'unsupported_layout'),
    ('identity', lambda r, m: m.update(threadId=SESSION), 'identity'),
    ('missing_meta', lambda r, m: m.clear(), 'identity'),
    ('boundary', lambda r, m: m.update(itemId='missing'), 'identity'),
    ('wrong_turn', lambda r, m: r[2]['payload'].update(turn_id='other'), 'identity'),
    ('wrong_dial', lambda r, m: r[2]['payload'].update(model='other'), 'identity'),
    ('compaction', lambda r, m: r.insert(-1, {'type': 'compacted', 'payload': {}}), 'compaction'),
    ('rollback', lambda r, m: r.insert(-1, {'type': 'event_msg', 'payload': {'type': 'thread_rolled_back'}}), 'rollback'),
    ('parallel', lambda r, m: (r.pop(-2), None)[1], 'pairing'),
    ('unsupported', lambda r, m: r.insert(-1, {'type': 'response_item', 'payload': {'type': 'audio'}}), 'unsupported_content'),
    ('audio', lambda r, m: r[3]['payload']['content'].append({'type': 'input_audio'}), 'unsupported_content'),
    ('agent_author', lambda r, m: r.insert(-1, {'type': 'response_item', 'payload': dict(agent_item(), author='')}), 'unsupported_content'),
    ('agent_recipient', lambda r, m: r.insert(-1, {'type': 'response_item', 'payload': dict(agent_item(), recipient=None)}), 'unsupported_content'),
    ('agent_encrypted', lambda r, m: r.insert(-1, {'type': 'response_item', 'payload': dict(agent_item(), content=[{'type': 'encrypted_content', 'encrypted_content': ''}])}), 'unsupported_content'),
]:
    setattr(Boundary, 'test_reject_' + name, rejection_case(mutation, code))


if __name__ == '__main__':
    unittest.main(verbosity=2)
