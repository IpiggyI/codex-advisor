#!/usr/bin/env python3
"""在隔离宿主中比对响应参数、钩子输入、会话记录和子线程消息。"""

import argparse
import hashlib
import http.server
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading

REPO = Path(__file__).resolve().parents[2]
PLUGIN = REPO / 'plugins/codex-advisor'
TRACE = Path('/home/hyy/.codex/sessions/2026/10/08/rollout-2026-10-08T15-45-10-01a11a79-27f4-7dd0-bf3c-0dd0cd50322f.jsonl')
CALLS = {'call_1117c8d44c7f418c85dcacfd8979acb5', 'call_30a8146b049244ee82b0205d113d651e',
         'call_85e8ad584a624f3ca147bf1f48e5735c'}


def shape(message):
    return {'chars': len(message), 'lines': len(message.splitlines()),
            'sha256': hashlib.sha256(message.encode()).hexdigest(),
            'opaque_prefix': message.startswith('gAAAA'), 'has_route': 'Route:' in message}


def cases():
    found = []
    for line in TRACE.open():
        item = json.loads(line).get('payload', {})
        if item.get('type') == 'function_call' and item.get('call_id') in CALLS:
            found.append({'id': item['call_id'], 'arguments': json.loads(item['arguments']), 'allowed': False})
    assert len(found) == len(CALLS)
    route = 'Route: role=advisor tier=crux dial=gpt-6.1-sol[xhigh] basis=acceptance-mapping ref=local-probe'
    for index in range(3):
        task = f'plain_{index}'
        args = dict(found[index]['arguments'], task_name=task, message=task + '\n\n' + route + '\n\nLOCAL_CHILD')
        found.append({'id': f'plain_{index}', 'arguments': args, 'allowed': True})
    bad = dict(found[-1]['arguments'], task_name='malformed', message='malformed\n\nRoute: invalid\n\nLOCAL_CHILD')
    found.append({'id': 'malformed', 'arguments': bad, 'allowed': False})
    native = dict(found[0]['arguments'], task_name='native_opaque', agent_type='default', model='gpt-6.1-sol')
    found.append({'id': 'native_opaque', 'arguments': native, 'allowed': True})
    return found


class Endpoint(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.requests.append(request)
        outputs = [x for x in request.get('input', []) if x.get('type') == 'function_call_output']
        index = len(outputs)
        if request.get('reasoning', {}).get('effort') == 'xhigh' or index >= len(self.server.cases):
            item = {'type': 'message', 'id': 'msg_local', 'role': 'assistant', 'status': 'completed',
                    'content': [{'type': 'output_text', 'text': 'LOCAL_COMPLETE'}]}
            delta = {'type': 'response.output_text.delta', 'item_id': item['id'],
                     'output_index': 0, 'content_index': 0, 'delta': 'LOCAL_COMPLETE'}
        else:
            case = self.server.cases[index]
            item = {'type': 'function_call', 'id': f'fc_{index}', 'call_id': case['id'],
                    'namespace': 'collaboration', 'name': 'spawn_agent',
                    'arguments': json.dumps(case['arguments']), 'status': 'completed'}
            delta = {'type': 'response.function_call_arguments.delta', 'item_id': item['id'],
                     'output_index': 0, 'delta': item['arguments']}
        events = [{'type': 'response.created', 'response': {'id': 'resp_local', 'status': 'in_progress', 'output': []}},
                  {'type': 'response.output_item.added', 'output_index': 0,
                   'item': dict(item, status='in_progress', **({'arguments': ''}
                           if item['type'] == 'function_call' else {'content': []}))}, delta,
                  {'type': 'response.output_item.done', 'output_index': 0, 'item': item},
                  {'type': 'response.completed', 'response': {'id': 'resp_local', 'status': 'completed',
                   'output': [item], 'usage': {'input_tokens': 100, 'output_tokens': 10, 'total_tokens': 110}}}]
        if item['type'] == 'function_call' and item['call_id'] == 'plain_0':
            text = ('Route: tool=spawn_agent target=plain_0 role=advisor tier=crux '
                    'dial=gpt-6.1-sol[xhigh] basis=acceptance-mapping ref=local-probe')
            message = {'type': 'message', 'id': 'msg_route', 'role': 'assistant', 'channel': 'commentary',
                       'status': 'completed', 'content': [{'type': 'output_text', 'text': text}]}
            for event in events:
                if 'output_index' in event:
                    event['output_index'] = 1
            events[1:1] = [
                {'type': 'response.output_item.added', 'output_index': 0,
                 'item': dict(message, status='in_progress', content=[])},
                {'type': 'response.output_text.delta', 'item_id': message['id'],
                 'output_index': 0, 'content_index': 0, 'delta': text},
                {'type': 'response.output_item.done', 'output_index': 0, 'item': message}]
            events[-1]['response']['output'] = [message, item]
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        for event in events:
            self.wfile.write(('data: ' + json.dumps(event) + '\n\n').encode())

    def log_message(self, *args):
        pass


def run():
    with tempfile.TemporaryDirectory(prefix='ca-message-boundary-') as directory:
        root = Path(directory)
        home, cwd = root / 'home', root / 'work'
        home.mkdir()
        cwd.mkdir()
        endpoint = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Endpoint)
        endpoint.requests, endpoint.cases = [], cases()
        listener = threading.Thread(target=endpoint.serve_forever, daemon=True)
        listener.start()
        try:
            return run_host(root, home, cwd, endpoint)
        finally:
            endpoint.shutdown()
            endpoint.server_close()
            listener.join()


def run_host(root, home, cwd, endpoint):
    source = root / 'source'
    (source / '.agents/plugins').mkdir(parents=True)
    shutil.copy2(REPO / '.agents/plugins/marketplace.json', source / '.agents/plugins')
    copied = source / 'plugins/codex-advisor'
    shutil.copytree(PLUGIN, copied)
    (copied / '.mcp.json').unlink()
    events = root / 'hook-events.jsonl'
    # 包装器只记录形态，再将未改动的输入交给产品脚本。
    (copied / 'scripts/message-probe.py').write_text(
        'import hashlib,io,json,runpy,sys\nfrom pathlib import Path\n'
        'raw=sys.stdin.read()\ne=json.loads(raw)\na=e.get("tool_input",{})\nm=a.get("message","")\n'
        'record={"kind":e.get("hook_event_name"),"tool":e.get("tool_name"),"task":a.get("task_name"),'
        '"shape":{"chars":len(m),"lines":len(m.splitlines()),"sha256":hashlib.sha256(m.encode()).hexdigest(),'
        '"opaque_prefix":m.startswith("gAAAA"),"has_route":"Route:" in m}}\n'
        'rows=[json.loads(line) for line in Path(e["transcript_path"]).read_text().splitlines()]\n'
        'record["turn_id"]=e.get("turn_id")\nrecord["tool_use_id"]=e.get("tool_use_id")\n'
        'record["tail"]=[{k:r["payload"].get(k) for k in ("type","role","channel","call_id","turn_id")} '
        'for r in rows if r.get("type") in ("response_item","turn_context")][-6:]\n'
        f'with Path({str(events)!r}).open("a") as f:f.write(json.dumps(record)+"\\n")\n'
        'sys.stdin=io.StringIO(raw)\nrunpy.run_path(str(Path(__file__).with_name("advisor-hooks.py")),run_name="__main__")\n')
    manifest = copied / 'hooks/hooks.json'
    manifest.write_text(manifest.read_text().replace('scripts/advisor-hooks.py', 'scripts/message-probe.py'))
    (home / 'config.toml').write_text('model = "gpt-6.1-sol"\nmodel_reasoning_effort = "medium"\n'
        'approval_policy = "never"\nsandbox_mode = "read-only"\nmodel_provider = "local"\n'
        '[features]\nhooks = true\nmulti_agent_v2 = true\ncode_mode = false\n'
        'code_mode_only = false\ncode_mode_host = false\nplugins = true\n'
        '[agents]\nenabled = true\n'
        '[model_providers.local]\nname = "Local test"\n'
        f'base_url = "http://127.0.0.1:{endpoint.server_port}/v1"\n'
        'wire_api = "responses"\nrequires_openai_auth = false\n'
        'request_max_retries = 0\nstream_max_retries = 0\n')
    env = dict(os.environ, CODEX_HOME=str(home))
    for command in (['sh', str(PLUGIN / 'scripts/install-agents.sh'), '--target-dir', str(home / 'agents')],
                    ['codex', 'plugin', 'marketplace', 'add', str(source), '--json'],
                    ['codex', 'plugin', 'add', 'codex-advisor@codex-advisor', '--json']):
        subprocess.run(command, env=env, cwd=cwd, text=True, capture_output=True, timeout=30, check=True)
    version = json.loads((PLUGIN / '.codex-plugin/plugin.json').read_text())['version']
    installed = home / 'plugins/cache/codex-advisor/codex-advisor' / version
    for name in ('scripts/advisor-hooks.py', 'scripts/run-python.sh'):
        assert (installed / name).read_bytes() == (PLUGIN / name).read_bytes()
    result = subprocess.run(['codex', 'exec', '--skip-git-repo-check', '--json', '-C', str(cwd),
                             '--dangerously-bypass-hook-trust', 'LOCAL_PARENT'],
                            env=env, text=True, capture_output=True, timeout=90)
    assert result.returncode == 0, result.stderr
    hooks = [json.loads(line) for line in events.read_text().splitlines()]
    calls, children = {}, []
    for path in (home / 'sessions').rglob('*.jsonl'):
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        meta = rows[0]['payload']
        if meta.get('parent_thread_id'):
            texts = [part.get('text', '') for row in rows if row['type'] == 'response_item'
                     and row['payload'].get('type') in ('message', 'agent_message')
                     for part in row['payload'].get('content', []) if isinstance(part, dict)]
            turns = [row['payload'] for row in rows if row['type'] == 'turn_context']
            opaque = [shape(part['encrypted_content']) for row in rows if row['type'] == 'response_item'
                      and row['payload'].get('type') == 'agent_message'
                      for part in row['payload'].get('content', []) if part.get('type') == 'encrypted_content']
            children.append({'role': meta.get('agent_role'), 'id': meta['id'],
                             'task': meta['source']['subagent']['thread_spawn']['agent_path'],
                             'dials': [{'model': t.get('model'), 'effort': t.get('effort')} for t in turns],
                             'received_plain_packet': any('\n\nRoute:' in t and 'LOCAL_CHILD' in t for t in texts),
                             'opaque': opaque})
        else:
            for row in rows:
                item = row.get('payload', {})
                if item.get('type') == 'function_call' and item.get('call_id') in {c['id'] for c in endpoint.cases}:
                    calls[item['call_id']] = shape(json.loads(item['arguments'])['message'])
    outputs = {item['call_id']: item['output'] for request in endpoint.requests
               if request.get('reasoning', {}).get('effort') != 'xhigh'
               for item in request.get('input', []) if item.get('type') == 'function_call_output'}
    reports = []
    pre = [event for event in hooks if event['kind'] == 'PreToolUse' and event['tool'] == 'collaborationspawn_agent']
    assert len(pre) == len(endpoint.cases), pre
    for case, event in zip(endpoint.cases, pre):
        sent = shape(case['arguments']['message'])
        assert event['shape'] == sent == calls[case['id']], case['id']
        output = outputs[case['id']]
        allowed = 'Tool call blocked by PreToolUse hook:' not in output
        assert allowed == case['allowed'], case['id']
        reports.append({'call_id': case['id'], 'task': case['arguments']['task_name'],
                        'response': sent, 'hook': event['shape'], 'rollout': calls[case['id']],
                        'allowed': allowed, 'result': json.loads(output) if allowed else output})
    assert len(children) == 4, children
    for child in children:
        if child['task'] == '/root/native_opaque':
            assert child['opaque'] == [shape(endpoint.cases[0]['arguments']['message'])], child
        else:
            case = next(c for c in endpoint.cases if '/root/' + c['arguments']['task_name'] == child['task'])
            assert child['role'] == 'ca_advisor_crux_m', child
            assert child['opaque'] == [shape(case['arguments']['message'])], child
        assert child['dials'] == [{'model': 'gpt-6.1-sol', 'effort': 'xhigh'}], child
    return {'host': subprocess.check_output(['codex', '--version'], text=True).strip(),
            'hook_sha256': hashlib.sha256((PLUGIN / 'scripts/advisor-hooks.py').read_bytes()).hexdigest(),
            'cases': reports, 'children': children, 'hook_boundaries': pre, 'verified': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-hook-trust-bypass', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not args.allow_hook_trust_bypass:
        parser.error('需要用户授权仅限一次性主目录的钩子信任绕过。')
    report = run()
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'verified': report['verified'], 'cases': len(report['cases']), 'children': len(report['children'])}))
