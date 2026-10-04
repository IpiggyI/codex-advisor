#!/usr/bin/env python3
"""在一次性主目录中，用本地响应核实原生工具钩子。"""

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


class Endpoint(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.requests.append(request)
        outputs = [x for x in request.get('input', []) if x.get('type') == 'function_call_output']
        child = request.get('reasoning', {}).get('effort') == 'xhigh'
        steps = 5 if self.server.product else 4
        if self.server.inventory or child or len(outputs) >= steps:
            item = {'type': 'message', 'id': 'msg_local', 'role': 'assistant', 'status': 'completed',
                    'content': [{'type': 'output_text', 'text': 'LOCAL_COMPLETE'}]}
            delta = {'type': 'response.output_text.delta', 'item_id': item['id'],
                     'output_index': 0, 'content_index': 0, 'delta': 'LOCAL_COMPLETE'}
        else:
            index = len(outputs)
            args = ({'agent_type': 'ca_worker_crux_m', 'fork_turns': 'none',
                     'task_name': 'denied' if index == 0 else 'allowed',
                     'message': 'DENY_PACKET' if index == 0 else 'CHILD_PACKET'} if index < 2 else
                    {'target': 'allowed', 'message': 'DENY_PACKET'})
            name = 'spawn_agent' if index < 2 else 'send_message' if index == 3 else 'followup_task'
            if self.server.product and index in (1, 4):
                route = 'Route: role=worker tier=crux dial=gpt-6.1-sol[xhigh] basis=key-difficulty ref=local-probe'
                args['message'] = ('allowed\n\n' if index == 1 else '') + route + '\n\nCHILD_PACKET'
            item = {'type': 'function_call', 'id': f'fc_{index}', 'call_id': f'call_{index}',
                    'namespace': 'collaboration', 'name': name,
                    'arguments': json.dumps(args), 'status': 'completed'}
            delta = {'type': 'response.function_call_arguments.delta', 'item_id': item['id'],
                     'output_index': 0, 'delta': item['arguments']}
        events = [{'type': 'response.created', 'response': {'id': 'resp_local', 'status': 'in_progress', 'output': []}},
                  {'type': 'response.output_item.added', 'output_index': 0,
                   'item': dict(item, status='in_progress', **({'arguments': ''}
                           if item['type'] == 'function_call' else {'content': []}))}, delta,
                  {'type': 'response.output_item.done', 'output_index': 0, 'item': item},
                  {'type': 'response.completed', 'response': {'id': 'resp_local', 'status': 'completed',
                   'output': [item], 'usage': {'input_tokens': 100, 'output_tokens': 10, 'total_tokens': 110}}}]
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        for event in events:
            self.wfile.write(('data: ' + json.dumps(event) + '\n\n').encode())

    def log_message(self, *args):
        pass


def run_case(policy, inventory, allow_bypass, product):
    with tempfile.TemporaryDirectory(prefix='ca-route-host-') as directory:
        root = Path(directory)
        home = root / 'home'
        home.mkdir()
        cwd = root / 'work'
        cwd.mkdir()
        endpoint = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Endpoint)
        endpoint.requests, endpoint.inventory, endpoint.product = [], inventory, product
        listener = threading.Thread(target=endpoint.serve_forever, daemon=True)
        listener.start()
        hook = root / 'hook.py'
        events = root / 'events.jsonl'
        hook.write_text('import json,sys\nfrom pathlib import Path\n'
            'e=json.load(sys.stdin)\n'
            f'with Path({str(events)!r}).open("a") as f:f.write(json.dumps(e)+"\\n")\n'
            'if "DENY_PACKET" in json.dumps(e.get("tool_input")):\n'
            ' print(json.dumps({"hookSpecificOutput":{"hookEventName":"PreToolUse",'
            '"permissionDecision":"deny","permissionDecisionReason":"CA_PROBE_DENIED"}}))\n')
        if not product:
            (home / 'hooks.json').write_text(json.dumps({'hooks': {'PreToolUse': [{'matcher': '.*',
                'hooks': [{'type': 'command', 'command': f'python3 "{hook}"', 'timeout': 10}]}]}}))
        (home / 'config.toml').write_text('model = "gpt-6.1-sol"\nmodel_reasoning_effort = "medium"\n'
            f'approval_policy = "{policy}"\nsandbox_mode = "read-only"\nmodel_provider = "local"\n'
            '[features]\nhooks = true\nmulti_agent_v2 = true\ncode_mode = false\n'
            f'code_mode_only = false\ncode_mode_host = false\nplugins = {str(product).lower()}\n'
            '[agents]\nenabled = true\n'
            '[model_providers.local]\nname = "Local test"\n'
            f'base_url = "http://127.0.0.1:{endpoint.server_port}/v1"\n'
            'wire_api = "responses"\nrequires_openai_auth = false\n'
            'request_max_retries = 0\nstream_max_retries = 0\n')
        env = dict(os.environ, CODEX_HOME=str(home))
        subprocess.run(['sh', str(REPO / 'plugins/codex-advisor/scripts/install-agents.sh'),
                        '--target-dir', str(home / 'agents')], env=env, cwd=cwd, text=True,
                       capture_output=True, timeout=30, check=True)
        installed_hashes = {}
        if product:
            source = root / 'source'
            (source / '.agents/plugins').mkdir(parents=True)
            shutil.copy2(REPO / '.agents/plugins/marketplace.json', source / '.agents/plugins')
            shutil.copytree(REPO / 'plugins/codex-advisor', source / 'plugins/codex-advisor')
            # 只测钩子，避免启动与本探针无关的咨询服务。
            (source / 'plugins/codex-advisor/.mcp.json').unlink()
            for arguments in (['plugin', 'marketplace', 'add', str(source)],
                              ['plugin', 'add', 'codex-advisor@codex-advisor']):
                installed = subprocess.run(['codex', *arguments, '--json'], env=env, cwd=cwd, text=True,
                                           capture_output=True, timeout=30)
                if installed.returncode:
                    raise RuntimeError(installed.stderr + installed.stdout)
            version = json.loads((source / 'plugins/codex-advisor/.codex-plugin/plugin.json').read_text())['version']
            cache = home / 'plugins/cache/codex-advisor/codex-advisor' / version
            for name in ('hooks/hooks.json', 'scripts/advisor-hooks.py', 'scripts/run-python.sh'):
                content = (cache / name).read_bytes()
                assert content == (REPO / 'plugins/codex-advisor' / name).read_bytes(), name
                installed_hashes[name] = hashlib.sha256(content).hexdigest()
        command = ['codex', 'exec', '--skip-git-repo-check', '--json', '-C', str(cwd)]
        if allow_bypass:
            command.append('--dangerously-bypass-hook-trust')
        command.append('LOCAL_PARENT')
        try:
            result = subprocess.run(command, env=env, text=True, capture_output=True, timeout=45)
            observed = [json.loads(x) for x in events.read_text().splitlines()] if events.exists() else []
            children = []
            for path in (home / 'sessions').rglob('*.jsonl'):
                rows = [json.loads(line) for line in path.read_text().splitlines()]
                meta = rows[0].get('payload', {})
                if meta.get('parent_thread_id'):
                    children.append({'meta': {k: meta.get(k) for k in ('id', 'session_id', 'parent_thread_id',
                                     'timestamp', 'cwd', 'cli_version', 'agent_path', 'agent_role')},
                                     'turns': sum(x.get('type') == 'turn_context' for x in rows),
                                     'dials': [{'model': x['payload'].get('model'), 'effort': x['payload'].get('effort')}
                                               for x in rows if x.get('type') == 'turn_context'],
                                     'activity': [{'timestamp': x.get('timestamp'), 'type': x.get('type'),
                                                   'event': x.get('payload', {}).get('type')}
                                                  for x in rows if x.get('type') in ('event_msg', 'turn_context')]})
            evidence = {'approval': policy, 'exit': result.returncode, 'installedHashes': installed_hashes, 'hooks': observed,
                        'children': children, 'stdout': result.stdout, 'stderr': result.stderr}
            if inventory:
                evidence['inventory'] = [{k: r.get(k) for k in ('tools', 'input')} for r in endpoint.requests]
            else:
                evidence['outputs'] = list({x['call_id']: x for r in endpoint.requests
                    if r.get('reasoning', {}).get('effort') != 'xhigh'
                    for x in r.get('input', []) if x.get('type') == 'function_call_output'}.values())
                if policy != 'untrusted':
                    assert result.returncode == 0, result.stderr
                    mapped = {x['call_id']: x['output'] for x in evidence['outputs']}
                    for index in (0, 2, 3):
                        assert 'Tool call blocked by PreToolUse hook:' in mapped[f'call_{index}'], mapped
                    assert json.loads(mapped['call_1'])['task_name'] == '/root/allowed', mapped
                    assert len(children) == 1 and children[0]['meta']['agent_path'] == '/root/allowed', children
                    if product:
                        assert 'blocked' not in mapped['call_4'].lower(), mapped
                        assert children[0]['turns'] == 2, children
                        assert children[0]['dials'] == [{'model': 'gpt-6.1-sol', 'effort': 'xhigh'}] * 2, children
                    else:
                        assert children[0]['turns'] == 1, children
                    evidence['verified'] = True
            return evidence
        finally:
            endpoint.shutdown()
            endpoint.server_close()
            listener.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', action='store_true')
    parser.add_argument('--allow-hook-trust-bypass', action='store_true')
    parser.add_argument('--product', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not args.inventory and not args.allow_hook_trust_bypass:
        parser.error('执行钩子探针需要本轮用户授权 --allow-hook-trust-bypass。')
    policies = ['never'] if args.inventory else ['never', 'on-request', 'on-failure']
    if not args.product and not args.inventory:
        policies.append('untrusted')
    result = []
    for policy in policies:
        result.append(run_case(policy, args.inventory, args.allow_hook_trust_bypass, args.product))
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps([{k: r[k] for k in ('approval', 'exit')} for r in result]))
