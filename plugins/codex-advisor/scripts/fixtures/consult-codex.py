#!/usr/bin/env python3
"""Deterministic native executable replacement, used only by the verifier."""

import json
import os
from pathlib import Path
import subprocess
import sys
import time
import tomllib

root = Path(os.environ['CONSULT_FIXTURE_ROOT'])
scenario = os.environ.get('CONSULT_FIXTURE_CASE', 'plan')
if sys.argv[1:] == ['debug', 'models', '--bundled']:
    print(json.dumps({'models': [{'slug': 'gpt-6-astra', 'shell_type': 'local',
          'tool_mode': 'code_mode_only',
          'apply_patch_tool_type': 'freeform', 'experimental_supported_tools': ['clock'],
          'supports_search_tool': True, 'use_tools_instructions': True}]}))
    sys.exit(0)
assert sys.argv[1] == 'app-server'
settings = {}
for index in range(2, len(sys.argv), 2):
    assert sys.argv[index] == '-c'
    parsed = tomllib.loads(sys.argv[index + 1])
    def merge(target, source):
        for key, value in source.items():
            if isinstance(value, dict):
                merge(target.setdefault(key, {}), value)
            else:
                target[key] = value
    merge(settings, parsed)
disabled = settings.get('mcp_servers', {})
stage = 'advisor' if disabled else 'inventory'
record = root / (stage + '-calls.jsonl')
names = ['ordinary', 'dots.and "quotes" \\ unicode雪']
catalog = json.loads(Path(settings['model_catalog_json']).read_text())['models'][0]
assert catalog['slug'] == settings['model']
assert 'tool_mode' not in catalog
assert catalog['shell_type'] == 'disabled' and catalog['apply_patch_tool_type'] is None
assert catalog['experimental_supported_tools'] == [] and catalog['supports_search_tool'] is False
assert catalog['use_tools_instructions'] is False
assert settings['history']['persistence'] == 'none'
assert settings['features']['skip_host_skill_discovery'] is True
assert all(v is False for k, v in settings['features'].items() if k != 'skip_host_skill_discovery')
assert settings['features']['memories'] is False
assert settings['memories'] == {'generate_memories': False, 'use_memories': False}
assert Path(settings['log_dir']).parent == Path.cwd()
assert Path(settings['sqlite_home']).parent == Path.cwd()
if stage == 'advisor':
    assert set(disabled) == set(names) and all(v['enabled'] is False for v in disabled.values())
thread = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
turn = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'


def emit(message):
    print(json.dumps(message), flush=True)


for line in sys.stdin:
    message = json.loads(line)
    method, params = message['method'], message.get('params', {})
    with record.open('a') as stream:
        stream.write(json.dumps(message) + '\n')
    if 'id' not in message:
        continue
    result = {}
    if method == 'initialize':
        result = {'userAgent': 'fixture'}
    elif method == 'mcpServerStatus/list':
        page = 0 if params.get('cursor') is None else 1
        entry = {'name': names[page], 'tools': {} if stage == 'advisor' else {'private': {}},
                 'resources': [], 'resourceTemplates': []}
        if scenario == 'mcp-leak' and stage == 'advisor':
            entry['tools'] = {'leaked': {}}
        result = {'data': [entry], 'nextCursor': 'page2' if page == 0 else None}
    elif method == 'hooks/list':
        result = {'data': [{'cwd': str(Path.cwd()), 'hooks': [] if scenario != 'hook-leak' else [{}],
                           'warnings': [], 'errors': []}]}
    elif method == 'thread/start':
        assert stage == 'advisor' and params['ephemeral'] is True
        assert params['baseInstructions'] == 'SOURCE_BASE_INSTRUCTIONS'
        assert params['developerInstructions'] == ''
        result = {'thread': {'id': thread}, 'model': settings['model'],
                  'reasoningEffort': settings['model_reasoning_effort']}
    elif method == 'thread/inject_items':
        assert params['threadId'] == thread
        (root / 'injected.json').write_text(json.dumps(params['items']))
    elif method == 'turn/start':
        assert params['threadId'] == thread
        assert params['outputSchema']['additionalProperties'] is False
        assert params['outputSchema']['properties']['kind']['enum'] == ['plan', 'correction', 'stop']
        if scenario == 'cancel':
            child = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(90)'])
            (root / 'child.pid').write_text(str(child.pid))
            time.sleep(90)
        if scenario == 'error':
            emit({'id': message['id'], 'error': {'code': -1, 'message': 'fixture error'}})
            continue
        result = {'turn': {'id': turn}}
        emit({'id': message['id'], 'result': result})
        trace = Path(os.environ['CODEX_ROLLOUT_TRACE_ROOT']) / 'rollout'
        trace.mkdir(parents=True, exist_ok=True)
        (trace / 'payloads').mkdir()
        request = {'model': params['model'], 'reasoning': {'effort': params['effort']},
                   'input': [{'type': 'additional_tools', 'role': 'developer', 'tools': []}] +
                            json.loads((root / 'injected.json').read_text())}
        if scenario == 'lost-context':
            request['input'].pop(1)
        if scenario == 'changed-context':
            request['input'][1]['role'] = 'assistant'
        if scenario == 'changed-text':
            request['input'][1]['content'][0]['text'] = 'constraint silently rewritten'
        if scenario == 'changed-agent-content':
            agent = next(value for value in request['input'] if value['type'] == 'agent_message')
            agent['content'][1]['encrypted_content'] = 'modified-opaque-bytes'
        for value in request['input']:
            value.pop('internal_chat_message_metadata_passthrough', None)
        if scenario == 'wrong-model':
            request['model'] = 'wrong-model'
        if scenario == 'wrong-effort':
            request['reasoning']['effort'] = 'max'
        if scenario == 'tools':
            request['input'][0]['tools'] = [{'name': 'shell'}]
        if scenario == 'top-tools':
            request['tools'] = []
            request['input'].pop(0)
        if scenario == 'nonempty-top-tools':
            request['tools'] = [{'name': 'shell'}]
        if scenario == 'missing-inventory':
            request['input'] = []
        (trace / 'payloads/1.json').write_text(json.dumps(request, ensure_ascii=False), encoding='utf-8')
        event = {'thread_id': thread, 'payload': {'type': 'inference_started',
                 'request_payload': {'path': 'payloads/1.json'}}}
        if scenario != 'no-trace':
            (trace / 'events.jsonl').write_text(json.dumps(event) + '\n')
        if scenario == 'earlier-mismatch':
            request['reasoning']['effort'] = 'max'
            (trace / 'payloads/1.json').write_text(json.dumps(request, ensure_ascii=False), encoding='utf-8')
            request['reasoning']['effort'] = params['effort']
            (trace / 'payloads/2.json').write_text(json.dumps(request, ensure_ascii=False), encoding='utf-8')
            event['payload']['request_payload']['path'] = 'payloads/2.json'
            with (trace / 'events.jsonl').open('a') as stream:
                stream.write(json.dumps(event) + '\n')
        advice = {'kind': scenario if scenario in ('plan', 'correction', 'stop') else 'plan',
                  'advice': 'Keep the earliest constraint and apply the next bounded change.'}
        text = json.dumps(advice)
        if scenario == 'empty':
            text = ''
        if scenario == 'bad-output':
            text = json.dumps({'kind': 'plan', 'advice': 'a', 'other': 'b'})
        emit({'method': 'item/completed', 'params': {'threadId': thread, 'turnId': turn,
              'item': {'type': 'agentMessage', 'phase': 'final_answer', 'text': text}}})
        if scenario == 'tool-request':
            emit({'id': 991, 'method': 'item/tool/call', 'params': {}})
        if scenario == 'orphan':
            child = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(90)'])
            (root / 'child.pid').write_text(str(child.pid))
        emit({'method': 'turn/completed', 'params': {'threadId': thread,
              'turn': {'id': turn, 'status': 'interrupted' if scenario == 'abort' else
                       'failed' if scenario == 'overflow' else 'completed',
                       'error': {'message': 'context overflow'} if scenario == 'overflow' else None}}})
        if scenario == 'orphan':
            sys.exit(0)
        continue
    else:
        raise AssertionError(method)
    emit({'id': message['id'], 'result': result})
