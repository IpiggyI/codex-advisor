"""Native authenticated App Server execution with temporary request evidence."""

import json
import os
from pathlib import Path
import queue
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time

from consult_context import Failure, require


FEATURES_OFF = ('shell_tool view_image goals request_permissions_tool '
                'default_mode_request_user_input image_generation apps code_mode '
                'code_mode_host code_mode_only sleep_tool current_time_reminder '
                'browser_use computer_use tool_suggest multi_agent_v2 plugins '
                'hooks codex_hooks plugin_hooks memories memory_tool external_agent_memory_import').split()
SCHEMA = {'type': 'object', 'properties': {
    'kind': {'type': 'string', 'enum': ['plan', 'correction', 'stop']},
    'advice': {'type': 'string'}}, 'required': ['kind', 'advice'],
    'additionalProperties': False}
GUIDANCE = (
    'You are the process consultant for the caller whose complete effective history '
    'precedes this instruction. Preserve all caller user constraints, authorizations, '
    'and reserved interfaces. You have no tools. Return exactly one concise plan '
    '(concrete next steps), correction (redirect a wrong path), or stop (halt and '
    'escalate to the user), using the output schema. This is advice to the caller, '
    'not user-facing output or independent acceptance. Do not execute the task. '
    'Advice grants no authorization, veto, or new requirement.')


class WindowsJob:
    """Own native descendants even after their original parent exits."""

    def __init__(self):
        import ctypes
        from ctypes import wintypes
        self.ctypes = ctypes
        self.api = ctypes.WinDLL('kernel32', use_last_error=True)
        signatures = {
            'CreateJobObjectW': ([ctypes.c_void_p, wintypes.LPCWSTR], wintypes.HANDLE),
            'SetInformationJobObject': ([wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD], wintypes.BOOL),
            'AssignProcessToJobObject': ([wintypes.HANDLE, wintypes.HANDLE], wintypes.BOOL),
            'TerminateJobObject': ([wintypes.HANDLE, wintypes.UINT], wintypes.BOOL),
            'QueryInformationJobObject': ([wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p,
                                          wintypes.DWORD, ctypes.c_void_p], wintypes.BOOL),
            'CloseHandle': ([wintypes.HANDLE], wintypes.BOOL),
        }
        for name, (args, result) in signatures.items():
            function = getattr(self.api, name)
            function.argtypes, function.restype = args, result
        self.handle = self.api.CreateJobObjectW(None, None)
        self.check(self.handle, 'create native process job')
        # JOBOBJECT_EXTENDED_LIMIT_INFORMATION contains two LARGE_INTEGERs,
        # flags, architecture-sized limits, six I/O counters, and memory limits.
        class Limits(ctypes.Structure):
            _fields_ = [('process_time', ctypes.c_longlong), ('job_time', ctypes.c_longlong),
                        ('flags', wintypes.DWORD), ('working_min', ctypes.c_size_t),
                        ('working_max', ctypes.c_size_t), ('active_limit', wintypes.DWORD),
                        ('affinity', ctypes.c_size_t), ('priority', wintypes.DWORD),
                        ('scheduling', wintypes.DWORD), ('io', ctypes.c_ulonglong * 6),
                        ('memory', ctypes.c_size_t * 4)]
        limits = Limits()
        limits.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.api.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            error = ctypes.get_last_error()
            self.close()
            raise Failure('cleanup', 'Cannot configure native process job (Windows error %d).' % error)

    def check(self, result, operation):
        if not result:
            raise Failure('cleanup', 'Cannot %s (Windows error %d).' %
                          (operation, self.ctypes.get_last_error()))

    def assign(self, process):
        self.check(self.api.AssignProcessToJobObject(self.handle, int(process._handle)),
                   'contain native process tree')

    def terminate(self):
        self.check(self.api.TerminateJobObject(self.handle, 1), 'terminate native process tree')
        # JOBOBJECT_BASIC_ACCOUNTING_INFORMATION: four LARGE_INTEGERs followed
        # by TotalPageFaultCount, TotalProcesses, ActiveProcesses, and terminated.
        accounting = self.ctypes.create_string_buffer(48)
        deadline = time.monotonic() + 10
        while True:
            self.check(self.api.QueryInformationJobObject(self.handle, 1, accounting, 48, None),
                       'verify native process tree cleanup')
            if int.from_bytes(accounting.raw[40:44], 'little') == 0:
                return
            require(time.monotonic() < deadline, 'cleanup', 'Native process tree did not terminate.')
            time.sleep(.01)

    def close(self):
        if self.handle:
            self.check(self.api.CloseHandle(self.handle), 'close native process job')
            self.handle = None


def terminate(process):
    prior = sys.exc_info()[1]
    job = getattr(process, '_consult_job', None)
    try:
        try:
            terminate_tree(process, job)
        finally:
            if job:
                job.close()
    except (Failure, OSError, subprocess.SubprocessError) as error:
        message = str(error) if isinstance(error, Failure) else 'Native process cleanup failed.'
        if isinstance(prior, Failure):
            message += ' Previous consultation failure: ' + prior.code + '.'
        raise Failure('cleanup', message, getattr(prior, 'actual', None)) from None


def terminate_tree(process, job):
    if process.stdin and not process.stdin.closed:
        try:
            process.stdin.close()
        except BrokenPipeError:
            pass
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        pass
    if job:
        job.terminate()
    elif os.name == 'nt':
        raise Failure('cleanup', 'Native process has no containment job; tree cleanup cannot be proven.')
    else:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            pass
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=10)


def windows_codex(env):
    executable = shutil.which('codex.exe', path=env.get('PATH'))
    if executable:
        return executable
    shim = shutil.which('codex', path=env.get('PATH'))
    require(shim is not None, 'executor', 'The native Codex executable is not available on PATH.')
    package = Path(shim).parent / 'node_modules/@openai/codex'
    matches = {path.resolve() for pattern in (
        'node_modules/@openai/codex-win32-*/vendor/*/bin/codex.exe',
        'vendor/*/bin/codex.exe') for path in package.glob(pattern) if path.is_file()}
    require(len(matches) == 1, 'executor',
            'Exactly one native codex.exe is required in the qualified npm package layout.')
    return str(matches.pop())


def launch(command, env, cwd):
    if os.name == 'nt':
        command = [windows_codex(env), *command[1:]]
    job = WindowsJob() if os.name == 'nt' else None
    if job:
        command = [sys.executable, '-B', str(Path(__file__).resolve()), '--job-child', *command]
    process = None
    try:
        process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                   text=True, encoding='utf-8', start_new_session=os.name != 'nt',
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0)
        if job:
            job.assign(process)
            process._consult_job = job
            process.stdin.write('G')
            process.stdin.flush()
        return process
    except BaseException:
        try:
            if process:
                process.kill()
                process.wait(timeout=10)
        finally:
            try:
                if job:
                    job.close()
            finally:
                if process:
                    process.stdin.close()
                    process.stdout.close()
        raise


def check_cancel(cancel, deadline):
    require(not cancel.is_set(), 'cancelled', 'Consultation was cancelled; no advice was accepted.')
    require(time.monotonic() < deadline, 'timeout', 'The native consultation deadline expired.')


def catalog(env, root, cancel, deadline, model):
    process = launch(['codex', 'debug', 'models', '--bundled'], env, root)
    try:
        while True:
            check_cancel(cancel, deadline)
            try:
                output, _ = process.communicate(timeout=.1)
                break
            except subprocess.TimeoutExpired:
                continue
        require(process.returncode == 0, 'catalog', 'Native bundled model discovery failed.')
        data = json.loads(output)
        selected = [entry for entry in data['models'] if entry.get('slug') == model]
        require(len(selected) == 1, 'catalog', 'The exact advisor model is absent from the bundled catalog.')
        entry = selected[0]
        entry.pop('tool_mode', None)
        entry.update(shell_type='disabled', apply_patch_tool_type=None,
                     experimental_supported_tools=[], supports_search_tool=False)
        for key in entry:
            if 'instruction' in key and isinstance(entry[key], bool):
                entry[key] = False
        target = root / 'models.json'
        target.write_text(json.dumps({'models': selected}), encoding='utf-8')
        return target
    finally:
        terminate(process)


def configuration(root, expected):
    values = {f'features.{name}': False for name in FEATURES_OFF}
    values.update({'agents.enabled': False, 'tools.update_plan.enabled': False,
                   'tools.experimental_request_user_input.enabled': False,
                   'web_search': 'disabled', 'features.skip_host_skill_discovery': True,
                   'memories.generate_memories': False, 'memories.use_memories': False,
                   'history.persistence': 'none', 'log_dir': str(root / 'logs'),
                   'sqlite_home': str(root / 'sqlite'), 'model': expected['model'],
                   'model_reasoning_effort': expected['effort']})
    return values


class Server:
    def __init__(self, env, root, values, cancel, deadline):
        command = ['codex', 'app-server']
        for key, value in values.items():
            encoded = ('{' + ','.join(json.dumps(name, ensure_ascii=False) + '={enabled=false}'
                       for name in value) + '}') if key == 'mcp_servers' else json.dumps(value)
            command.extend(['-c', key + '=' + encoded])
        self.process = launch(command, env, root)
        self.cancel, self.deadline = cancel, deadline
        self.messages, self.pending = queue.Queue(), []
        self.sequence = 0
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()

    def _read(self):
        try:
            for line in self.process.stdout:
                try:
                    self.messages.put(json.loads(line))
                except ValueError:
                    self.messages.put(None)
        finally:
            self.messages.put(None)

    def send(self, payload):
        try:
            self.process.stdin.write(json.dumps(payload) + '\n')
            self.process.stdin.flush()
        except (BrokenPipeError, OSError):
            raise Failure('executor', 'Native App Server closed its input.') from None

    def receive(self):
        while True:
            check_cancel(self.cancel, self.deadline)
            try:
                result = self.messages.get(timeout=.1)
                require(isinstance(result, dict), 'executor', 'Native App Server ended or emitted invalid JSON.')
                if 'method' in result and 'id' in result:
                    self.send({'id': result['id'], 'error': {'code': -32601,
                               'message': 'Consultation accepts no tool or approval requests.'}})
                    raise Failure('tools', 'Native consultation attempted a tool or approval request.')
                return result
            except queue.Empty:
                continue

    def call(self, method, params):
        self.sequence += 1
        request = self.sequence
        self.send({'id': request, 'method': method, 'params': params})
        while True:
            message = self.receive()
            if message.get('id') == request:
                require('error' not in message, 'executor', 'Native App Server rejected ' + method + '.')
                require('result' in message, 'executor', 'Native App Server omitted a result.')
                return message['result']
            self.pending.append(message)

    def initialize(self):
        self.call('initialize', {'clientInfo': {'name': 'codex-advisor-consult',
                  'version': '1'}, 'capabilities': {'experimentalApi': True}})
        self.send({'method': 'initialized', 'params': {}})

    def close(self):
        try:
            terminate(self.process)
        finally:
            self.reader.join(timeout=2)
            if not self.reader.is_alive():
                for stream in (self.process.stdin, self.process.stdout):
                    stream.close()


def server_names(env, root, values, cancel, deadline):
    server = Server(env, root, values, cancel, deadline)
    names, cursors, cursor = set(), set(), None
    try:
        server.initialize()
        while True:
            page = server.call('mcpServerStatus/list', {'cursor': cursor})
            require(isinstance(page.get('data'), list), 'inventory', 'MCP inventory is unavailable.')
            for entry in page['data']:
                name = entry.get('name')
                require(isinstance(name, str) and bool(name), 'inventory', 'MCP server identity is missing.')
                names.add(name)
            cursor = page.get('nextCursor')
            if cursor is None:
                return names
            require(isinstance(cursor, str) and cursor not in cursors,
                    'inventory', 'MCP inventory pagination is inconsistent.')
            cursors.add(cursor)
    finally:
        server.close()


def verify_isolation(server, root, names):
    cursor, cursors = None, set()
    while True:
        page = server.call('mcpServerStatus/list', {'cursor': cursor})
        require(isinstance(page.get('data'), list), 'isolation', 'Disabled MCP inventory is unavailable.')
        for entry in page['data']:
            require(entry.get('name') in names and entry.get('tools') == {} and
                    entry.get('resources') == [] and entry.get('resourceTemplates', []) == [],
                    'isolation', 'An MCP capability remains available to the advisor process.')
        cursor = page.get('nextCursor')
        if cursor is None:
            break
        require(isinstance(cursor, str) and cursor not in cursors,
                'isolation', 'Disabled MCP inventory pagination is inconsistent.')
        cursors.add(cursor)
    response = server.call('hooks/list', {'cwds': [str(root)]})
    data = response.get('data')
    require(isinstance(data, list) and len(data) == 1 and
            data[0].get('cwd') == str(root) and data[0].get('hooks') == [] and
            data[0].get('errors') == [] and data[0].get('warnings') == [],
            'isolation', 'Native hooks could not be proven disabled.')


def completion(server, thread, turn):
    finals = []
    while True:
        message = server.pending.pop(0) if server.pending else server.receive()
        method, params = message.get('method'), message.get('params', {})
        if method == 'error':
            raise Failure('executor', 'Native consultation reported an inference error.')
        if method in ('item/completed', 'turn/completed'):
            require(params.get('threadId') == thread and params.get('turnId', turn) == turn,
                    'executor', 'Native completion identity mismatch.')
        if method == 'item/completed':
            item = params.get('item', {})
            if item.get('type') == 'agentMessage' and item.get('phase') in (None, 'final_answer'):
                finals.append(item.get('text', ''))
        if method == 'turn/completed':
            result = params.get('turn', {})
            require(result.get('id') == turn and result.get('status') == 'completed' and not result.get('error'),
                    'executor', 'Native consultation aborted or failed, including possible context overflow.')
            require(len(finals) == 1 and isinstance(finals[0], str) and finals[0].strip(),
                    'empty', 'Consultation must return exactly one nonempty final message.')
            try:
                advice = json.loads(finals[0])
            except ValueError:
                raise Failure('output', 'Consultation output is not valid structured advice.') from None
            require(isinstance(advice, dict) and set(advice) == {'kind', 'advice'} and
                    advice['kind'] in ('plan', 'correction', 'stop') and
                    isinstance(advice['advice'], str) and bool(advice['advice'].strip()),
                    'output', 'Consultation output violates the plan/correction/stop contract.')
            return advice


def comparable(item):
    # The host removes item IDs, attribution metadata, and optional nulls from
    # requests. Tool call_id, roles, content, and encrypted reasoning stay exact.
    return {key: value for key, value in item.items()
            if key not in ('id', 'internal_chat_message_metadata_passthrough') and value is not None}


def verify_history(request, caller):
    source = iter(caller['items'])
    wanted = next(source, None)
    for item in request.get('input', []):
        if wanted is not None and comparable(item) == comparable(wanted):
            wanted = next(source, None)
    require(wanted is None, 'context',
            'Actual advisor request omitted or changed effective caller history, including possible automatic compaction.')


def verify_requests(root, thread, expected, caller):
    observed = []
    for trace in sorted((root / 'trace').rglob('*.jsonl')):
        for line in trace.read_text(encoding='utf-8').splitlines():
            event = json.loads(line)
            payload = event.get('payload', {})
            if payload.get('type') != 'inference_started':
                continue
            require(event.get('thread_id') == thread, 'trace', 'Unexpected inference thread in consultation trace.')
            relative = payload.get('request_payload', {}).get('path')
            require(isinstance(relative, str), 'trace', 'Actual inference request path is missing.')
            path = (trace.parent / relative).resolve()
            require(path.is_relative_to((root / 'trace').resolve()) and path.is_file(),
                    'trace', 'Actual inference request payload is unavailable.')
            request = json.loads(path.read_text(encoding='utf-8'))
            actual = {'model': request.get('model'), 'effort': request.get('reasoning', {}).get('effort')}
            if actual != expected:
                raise Failure('mismatch', 'Actual consultation model or effort differs from its expected dial.', actual)
            inventories = [item for item in request.get('input', []) if item.get('type') == 'additional_tools']
            try:
                require(('tools' not in request or request['tools'] == []) and
                        (inventories or request.get('tools') == []) and
                        all(item.get('tools') == [] for item in inventories),
                        'tools', 'Actual consultation request did not prove an empty tool set.')
                verify_history(request, caller)
            except Failure as error:
                error.actual = actual
                raise
            observed.append(actual)
    require(bool(observed), 'trace', 'No actual inference request trace was recorded.')
    return observed[-1]


def execute(home, caller, expected, cancel):
    deadline = time.monotonic() + 180
    with tempfile.TemporaryDirectory(prefix='codex-advisor-consult-') as directory:
        root = Path(directory)
        env = dict(os.environ, CODEX_HOME=str(home), CODEX_ROLLOUT_TRACE_ROOT=str(root / 'trace'))
        values = configuration(root, expected)
        values['model_catalog_json'] = str(catalog(env, root, cancel, deadline, expected['model']))
        names = server_names(env, root, values, cancel, deadline)
        values['mcp_servers'] = sorted(names)
        server = Server(env, root, values, cancel, deadline)
        try:
            server.initialize()
            verify_isolation(server, root, names)
            started = server.call('thread/start', {'model': expected['model'], 'cwd': str(root),
                                  'ephemeral': True, 'approvalPolicy': 'never', 'sandbox': 'read-only',
                                  'baseInstructions': caller['base'], 'developerInstructions': ''})
            thread = started['thread']['id']
            server.call('thread/inject_items', {'threadId': thread, 'items': caller['items'] + [
                {'type': 'message', 'role': 'developer', 'content': [{'type': 'input_text', 'text': GUIDANCE}]}]})
            started_turn = server.call('turn/start', {'threadId': thread, 'model': expected['model'],
                                       'effort': expected['effort'], 'outputSchema': SCHEMA,
                                       'input': [{'type': 'text', 'text': 'Return process consultation for the caller now.'}]})
            advice = completion(server, thread, started_turn['turn']['id'])
        finally:
            server.close()
        actual = verify_requests(root, thread, expected, caller)
        return {'status': 'succeeded', **advice, 'actual': actual, 'expected': expected,
                'advisorThreadId': thread, 'callerThreadId': caller['thread']}


if __name__ == '__main__':
    # The parent assigns this blocked helper to a job before native code can
    # spawn descendants. One unbuffered byte leaves JSON-RPC stdin untouched.
    if len(sys.argv) < 3 or sys.argv[1] != '--job-child' or os.read(0, 1) != b'G':
        sys.exit(2)
    child = subprocess.Popen(sys.argv[2:], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    sys.exit(child.wait())
