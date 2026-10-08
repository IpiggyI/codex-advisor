#!/usr/bin/env python3
"""Verify native route admission and opaque packet delivery using a loopback provider."""

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

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / 'plugins/codex-advisor'


def scenario(name, tool, target, declaration=True, advisor=False):
    role = 'advisor' if advisor else 'worker'
    route = (f'Route: tool={tool} target={target} role={role} tier=crux dial=gpt-6.1-sol[xhigh] '
             f'basis={"acceptance-mapping" if advisor else "key-difficulty"} ref=local-probe')
    arguments = {'message': 'gAAAA-native-fixture-' + name}
    if tool == 'spawn_agent':
        arguments.update(task_name=target, agent_type=f'ca_{role}_crux_m', fork_turns='none')
        if advisor:
            arguments['reasoning_effort'] = 'xhigh'
    else:
        arguments['target'] = target
    return {'id': name, 'tool': tool, 'arguments': arguments,
            'declaration': route if declaration else None, 'allowed': declaration}


def scenarios():
    cases = [scenario('missing_spawn', 'spawn_agent', 'missing', False),
             scenario('wrong_spawn', 'spawn_agent', 'wrong'),
             scenario('advisor', 'spawn_agent', 'advisor', advisor=True),
             scenario('worker', 'spawn_agent', 'worker')]
    cases[1]['declaration'] = cases[1]['declaration'].replace('[xhigh]', '[high]')
    cases[1]['allowed'] = False
    for tool in ('followup_task', 'send_message'):
        cases.append(scenario('missing_' + tool, tool, 'worker', False))
        wrong = scenario('wrong_' + tool, tool, 'worker')
        wrong['declaration'] = wrong['declaration'].replace('target=worker', 'target=other')
        wrong['allowed'] = False
        cases.extend([wrong, scenario('allowed_' + tool, tool, 'worker')])
    cases.append(scenario('drain_messages', 'followup_task', 'worker'))
    return cases


def message(text, identity):
    return {'type': 'message', 'id': identity, 'role': 'assistant', 'channel': 'commentary',
            'status': 'completed', 'content': [{'type': 'output_text', 'text': text}]}


def response_items(request, cases):
    outputs = [x for x in request.get('input', []) if x.get('type') == 'function_call_output']
    if request.get('reasoning', {}).get('effort') == 'xhigh' or len(outputs) >= len(cases):
        return [message('LOCAL_COMPLETE', 'msg_complete')]
    case = cases[len(outputs)]
    items = [message(case['declaration'], 'msg_' + case['id'])] if case['declaration'] else []
    items.append({'type': 'function_call', 'id': 'fc_' + case['id'], 'call_id': case['id'],
                  'namespace': 'collaboration', 'name': case['tool'],
                  'arguments': json.dumps(case['arguments']), 'status': 'completed'})
    return items


def response_events(items):
    events = [{'type': 'response.created', 'response': {'id': 'resp_local', 'status': 'in_progress', 'output': []}}]
    for index, item in enumerate(items):
        call = item['type'] == 'function_call'
        events.append({'type': 'response.output_item.added', 'output_index': index,
                       'item': dict(item, status='in_progress', **({'arguments': ''} if call else {'content': []}))})
        delta = {'type': 'response.function_call_arguments.delta' if call else 'response.output_text.delta',
                 'item_id': item['id'], 'output_index': index,
                 'delta': item['arguments'] if call else item['content'][0]['text']}
        if not call:
            delta['content_index'] = 0
        events.extend([delta, {'type': 'response.output_item.done', 'output_index': index, 'item': item}])
    events.append({'type': 'response.completed', 'response': {'id': 'resp_local', 'status': 'completed',
                   'output': items, 'usage': {'input_tokens': 100, 'output_tokens': 10, 'total_tokens': 110}}})
    return events


class Endpoint(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.requests.append(request)
        events = response_events(response_items(request, self.server.cases))
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        for event in events:
            self.wfile.write(('data: ' + json.dumps(event) + '\n\n').encode())

    def log_message(self, *args):
        pass


def command(arguments, env, cwd):
    return subprocess.run(arguments, env=env, cwd=cwd, text=True, capture_output=True, timeout=90, check=True)


def install(root, home, env, cwd, plugin):
    source = root / 'source'
    (source / '.agents/plugins').mkdir(parents=True)
    shutil.copy2(REPO / '.agents/plugins/marketplace.json', source / '.agents/plugins')
    copied = source / 'plugins/codex-advisor'
    shutil.copytree(plugin, copied)
    (copied / '.mcp.json').unlink()
    command(['codex', 'plugin', 'marketplace', 'add', str(source), '--json'], env, cwd)
    command(['codex', 'plugin', 'add', 'codex-advisor@codex-advisor', '--json'], env, cwd)
    version = json.loads((plugin / '.codex-plugin/plugin.json').read_text())['version']
    cache = home / 'plugins/cache/codex-advisor/codex-advisor' / version
    command(['sh', str(cache / 'scripts/install-agents.sh'), '--target-dir', str(home / 'agents')], env, cwd)
    hashes = {}
    for name in ('scripts/advisor-hooks.py', 'hooks/hooks.json', 'scripts/run-python.sh'):
        assert (cache / name).read_bytes() == (plugin / name).read_bytes(), name
        hashes[name] = hashlib.sha256((cache / name).read_bytes()).hexdigest()
    return hashes


def configure(home, port):
    (home / 'config.toml').write_text('model = "gpt-6.1-sol"\nmodel_reasoning_effort = "medium"\n'
        'approval_policy = "never"\nsandbox_mode = "read-only"\nmodel_provider = "local"\n'
        '[features]\nhooks = true\nmulti_agent_v2 = true\ncode_mode = false\n'
        'code_mode_only = false\ncode_mode_host = false\nplugins = true\n'
        '[agents]\nenabled = true\n'
        '[model_providers.local]\nname = "Local test"\n'
        f'base_url = "http://127.0.0.1:{port}/v1"\n'
        'wire_api = "responses"\nrequires_openai_auth = false\n'
        'request_max_retries = 0\nstream_max_retries = 0\n')


def child_evidence(home):
    children = []
    for path in (home / 'sessions').rglob('*.jsonl'):
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        meta = rows[0]['payload']
        if not meta.get('parent_thread_id'):
            continue
        packets = [part['encrypted_content'] for row in rows if row['type'] == 'response_item'
                   and row['payload'].get('type') == 'agent_message'
                   for part in row['payload'].get('content', []) if part.get('type') == 'encrypted_content']
        turns = [row['payload'] for row in rows if row['type'] == 'turn_context']
        children.append({'task': meta['source']['subagent']['thread_spawn']['agent_path'],
                         'id': meta['id'], 'role': meta['agent_role'],
                         'dials': [{'model': t['model'], 'effort': t['effort']} for t in turns],
                         'packet_sha256': [hashlib.sha256(p.encode()).hexdigest() for p in packets]})
    return children


def verify(endpoint, children):
    outputs = {item['call_id']: item['output'] for request in endpoint.requests
               if request.get('reasoning', {}).get('effort') != 'xhigh'
               for item in request.get('input', []) if item.get('type') == 'function_call_output'}
    spawned = {'/root/' + c['arguments']['task_name']: c['arguments']['agent_type']
               for c in endpoint.cases if c['tool'] == 'spawn_agent' and c['allowed']}
    expected_packets = {target: [] for target in spawned}
    results = []
    for case in endpoint.cases:
        output = outputs[case['id']]
        denied = output.startswith('Tool call blocked by PreToolUse hook: Codex Advisor route check:')
        assert denied != case['allowed'], (case['id'], output)
        if case['allowed']:
            target = '/root/' + case['arguments'].get('task_name', 'worker')
            if case['tool'] == 'spawn_agent':
                assert json.loads(output)['task_name'] == target, output
            else:
                assert output == '', (case['id'], output)
            packet = case['arguments']['message']
            expected_packets[target].append(hashlib.sha256(packet.encode()).hexdigest())
        results.append({'call': case['id'], 'tool': case['tool'], 'allowed': not denied})
    assert {child['task'] for child in children} == set(expected_packets), children
    for child in children:
        assert child['role'] == spawned[child['task']] and child['dials'], child
        assert all(d == {'model': 'gpt-6.1-sol', 'effort': 'xhigh'} for d in child['dials']), child
        assert sorted(child['packet_sha256']) == sorted(expected_packets[child['task']]), child
    return results


def run(plugin=PLUGIN):
    with tempfile.TemporaryDirectory(prefix='ca-native-routing-') as directory:
        root = Path(directory)
        home, cwd = root / 'home', root / 'work'
        home.mkdir()
        cwd.mkdir()
        endpoint = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Endpoint)
        endpoint.requests, endpoint.cases = [], scenarios()
        listener = threading.Thread(target=endpoint.serve_forever, daemon=True)
        listener.start()
        try:
            configure(home, endpoint.server_port)
            env = dict(os.environ, CODEX_HOME=str(home))
            hashes = install(root, home, env, cwd, plugin)
            command(['codex', 'exec', '--skip-git-repo-check', '--json', '-C', str(cwd),
                     '--dangerously-bypass-hook-trust', 'LOCAL_PARENT'], env, cwd)
            children = child_evidence(home)
            results = verify(endpoint, children)
            return {'host': subprocess.check_output(['codex', '--version'], text=True).strip(),
                    'installed_hashes': hashes, 'cases': results, 'children': children, 'verified': True}
        finally:
            endpoint.shutdown()
            endpoint.server_close()
            listener.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-hook-trust-bypass', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not args.allow_hook_trust_bypass:
        parser.error('User authorization is required for the disposable-home hook trust bypass.')
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
