#!/usr/bin/env python3
"""Exercise the shipped hook commands using pinned native event shapes."""

import copy
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import threading
import time
import tomllib

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent / 'plugins/codex-advisor'
FIXTURE = json.loads((HERE / 'fixtures/hooks.json').read_text())
MANIFEST = json.loads((PLUGIN / 'hooks/hooks.json').read_text())
REFERENCES = PLUGIN / 'skills/orchestration/references'
CANONICAL = (REFERENCES / 'consult-posture.md').read_text()
PROFILE = (REFERENCES / 'routing-profile.md').read_text()
ADVISORS = set(re.findall(r'`ca_advisor_[a-z0-9_]+`\s+([^\s\[]+)\[', PROFILE))
assert len(ADVISORS) == 1
ADVISOR = next(iter(ADVISORS))
assert set(MANIFEST['hooks']) == {'SessionStart', 'PostToolUse'}


def run(event, disabled=False, plugin=PLUGIN):
    groups = MANIFEST['hooks'][event['hook_event_name']]
    commands = [hook['command'] for group in groups for hook in group['hooks']
                if re.search(group.get('matcher', ''), event.get('tool_name', event.get('source', '')))]
    assert len(commands) == 1
    result = subprocess.run(['sh', '-c', ':' if disabled else commands[0]],
                            input=json.dumps(event), text=True, encoding='utf-8', capture_output=True,
                            env={**os.environ, 'PLUGIN_ROOT': str(plugin)}, timeout=12)
    assert result.returncode == 0 and not result.stderr, (result.returncode, result.stderr)
    if not result.stdout:
        return None
    output = json.loads(result.stdout)['hookSpecificOutput']
    assert output['hookEventName'] == event['hook_event_name']
    return output['additionalContext']


def pending(event, plugin=PLUGIN):
    def require_pending(value):
        assert value and 'affected work remains pending' in value, value
    require_pending(run(event, plugin=plugin))
    try:
        require_pending(run(event, disabled=True, plugin=plugin))
    except AssertionError:
        pass
    else:
        raise AssertionError('Surfacing assertion accepted a disabled hook')


def confirmed(event, model, effort):
    line = (f"Codex Advisor: {event['tool_input']['agent_type']} identity, model, and effort match the host "
            f"record at {model}[{effort}]; working directory and permissions were not checked.")
    def require_confirmed(value):
        assert value == line, value
    require_confirmed(run(event))
    try:
        require_confirmed(run(event, disabled=True))
    except AssertionError:
        pass
    else:
        raise AssertionError('Confirmation assertion accepted a disabled hook')


def block(name):
    return re.search(r'<!-- consult-posture:' + name + r':start -->.*?<!-- consult-posture:' +
                     name + r':end -->', CANONICAL, re.S)[0]


def write(path, rows):
    path.write_text(''.join(json.dumps(row) + '\n' for row in rows))


def check_launcher(root):
    if os.name == 'nt':
        return
    commands = root / 'interpreters'
    commands.mkdir()
    probe = commands / 'python3'
    probe.write_text('#!/bin/sh\nexit 1\n')
    probe.chmod(0o700)
    fallback = commands / 'python'
    fallback.write_text('#!/bin/sh\nexec ' + shlex.quote(sys.executable) + ' "$@"\n')
    fallback.chmod(0o700)
    command = ['/bin/sh', str(PLUGIN / 'scripts/run-python.sh'), '-c',
               'import json,sys; print(json.dumps([sys.argv[1],sys.stdin.read(),sys.dont_write_bytecode,sys.stdout.encoding]))',
               'spaces and 中文']
    result = subprocess.run(command, input='request body', text=True, encoding='utf-8',
                            capture_output=True, env={**os.environ, 'PATH': str(commands)}, timeout=5)
    assert result.returncode == 0 and not result.stderr, result.stderr
    assert json.loads(result.stdout) == ['spaces and 中文', 'request body', True, 'utf-8']
    fallback.unlink()
    result = subprocess.run(command, text=True, capture_output=True,
                            env={**os.environ, 'PATH': str(commands)}, timeout=5)
    assert result.returncode == 127 and not result.stdout and 'Python 3.11' in result.stderr
    probe.unlink()
    commands.rmdir()
    print('PASS: launcher skips unusable interpreter, preserves arguments/stdin, disables bytecode, fails without Python')


with tempfile.TemporaryDirectory(prefix='codex-advisor-hooks-test-') as directory:
    root = Path(directory)
    check_launcher(root)
    sessions = root / 'sessions/2026/09/26'
    sessions.mkdir(parents=True)
    parent = sessions / 'rollout-parent.jsonl'
    child = sessions / 'rollout-child.jsonl'
    write(parent, [FIXTURE['parent']])
    session = {**FIXTURE['session'], 'transcript_path': str(parent)}
    dispatch = {**FIXTURE['dispatch'], 'transcript_path': str(parent)}
    for model in (ADVISOR, 'gpt-6-sol', 'gpt-5.6-terra'):
        variant = 'reduced' if model == ADVISOR else 'full'
        for source in ('startup', 'resume', 'compact', 'clear'):
            event = {**session, 'model': model, 'source': source}
            assert run(event) == block(variant) + '\n\n' + block('adoption')
    assert run({**session, 'agent_id': 'child'}) is None
    write(parent, [FIXTURE['child'][0]])
    assert run({**session, 'session_id': FIXTURE['child'][0]['payload']['session_id']}) is None
    write(parent, [FIXTURE['parent']])
    pending({**session, 'model': ''})
    pending({**session, 'session_id': 'wrong'})
    pending({**session, 'transcript_path': str(sessions / 'absent.jsonl')})
    copy_plugin = root / 'plugin'
    (copy_plugin / 'scripts').mkdir(parents=True)
    copy_refs = copy_plugin / 'skills/orchestration/references'
    copy_refs.mkdir(parents=True)
    (copy_plugin / 'scripts/advisor-hooks.py').write_bytes((PLUGIN / 'scripts/advisor-hooks.py').read_bytes())
    (copy_plugin / 'scripts/run-python.sh').write_bytes((PLUGIN / 'scripts/run-python.sh').read_bytes())
    (copy_refs / 'routing-profile.md').write_text(PROFILE.replace(
        '`ca_advisor_rescue` ' + ADVISOR, '`ca_advisor_rescue` fixture-other-model'))
    (copy_refs / 'consult-posture.md').write_text(CANONICAL)
    pending(session, plugin=copy_plugin)
    (copy_refs / 'routing-profile.md').write_text(PROFILE)
    (copy_refs / 'consult-posture.md').write_text('missing canonical blocks')
    pending(session, plugin=copy_plugin)
    print('PASS: exact canonical full/reduced/adoption, unknown model, resume, delegate exclusion')

    templates = [tomllib.loads(path.read_text()) for path in (PLUGIN / 'agents').glob('*.toml')]
    for template in templates:
        role = template['name']
        options = re.search(r'`' + role + r'`\s+[^\s\[]+\[([^\]]+)\]', PROFILE)[1]
        effort = template.get('model_reasoning_effort', options.split(',')[0].strip().rstrip('*'))
        event = copy.deepcopy(dispatch)
        event['tool_input']['agent_type'] = role
        if 'model_reasoning_effort' in template:
            event['tool_input'].pop('reasoning_effort')
        else:
            event['tool_input']['reasoning_effort'] = effort
        rows = copy.deepcopy(FIXTURE['child'])
        rows[0]['payload']['agent_role'] = role
        rows[0]['payload']['source']['subagent']['thread_spawn']['agent_role'] = role
        rows[1]['payload'] = {'model': template['model'], 'effort': effort}
        write(child, rows)
        confirmed(event, template['model'], effort)
        if 'model_reasoning_effort' in template:
            overridden = copy.deepcopy(event)
            overridden['tool_input']['reasoning_effort'] = 'low' if effort != 'low' else 'high'
            confirmed(overridden, template['model'], effort)
        for key in ('model', 'effort'):
            bad = copy.deepcopy(rows)
            bad[1]['payload'][key] = 'wrong'
            write(child, bad)
            pending(event)
        write(child, rows)
        if 'model_reasoning_effort' not in template:
            missing = copy.deepcopy(event)
            del missing['tool_input']['reasoning_effort']
            pending(missing)
    print('PASS: all 13 entries, confirmation line on match, wrong model/effort, omitted caller effort; disabled negatives')

    write(child, FIXTURE['child'])
    fixture_turn = FIXTURE['child'][1]['payload']
    confirmed(dispatch, fixture_turn['model'], fixture_turn['effort'])
    for mutation in ('missing-turn', 'missing-effort', 'conflicting-turn', 'wrong-parent',
                     'wrong-path', 'wrong-role', 'wrong-session', 'source-parent', 'source-role',
                     'duplicate-header'):
        rows = copy.deepcopy(FIXTURE['child'])
        if mutation == 'missing-turn':
            rows.pop()
        elif mutation == 'missing-effort':
            del rows[1]['payload']['effort']
        elif mutation == 'conflicting-turn':
            rows.append({'type': 'turn_context', 'payload': {'model': 'wrong', 'effort': 'high'}})
        elif mutation == 'wrong-parent':
            rows[0]['payload']['parent_thread_id'] = 'unrelated'
        elif mutation == 'wrong-path':
            rows[0]['payload']['source']['subagent']['thread_spawn']['agent_path'] = '/other/task'
        elif mutation == 'wrong-role':
            rows[0]['payload']['agent_role'] = 'ca_explorer_mainstay_m'
        elif mutation == 'wrong-session':
            rows[0]['payload']['session_id'] = 'unrelated'
        elif mutation == 'source-parent':
            rows[0]['payload']['source']['subagent']['thread_spawn']['parent_thread_id'] = 'unrelated'
        elif mutation == 'source-role':
            rows[0]['payload']['source']['subagent']['thread_spawn']['agent_role'] = 'unrelated'
        else:
            rows.append(rows[0])
        write(child, rows)
        pending(dispatch)
    write(child, FIXTURE['child'])
    duplicate = sessions / 'rollout-duplicate.jsonl'
    write(duplicate, FIXTURE['child'])
    pending(dispatch)
    duplicate.unlink()
    for response in ('not json', '{}', '{"task_name":"/root/other"}'):
        pending({**dispatch, 'tool_response': response})
    pending({**dispatch, 'tool_input': None})
    pending({**dispatch, 'tool_input': {'agent_type': 'ca_unknown'}})
    pending({**dispatch, 'session_id': 'wrong'})
    child.unlink()
    pending(dispatch)
    writer = threading.Thread(target=lambda: (time.sleep(0.3), write(child, FIXTURE['child'])))
    writer.start()
    confirmed(dispatch, fixture_turn['model'], fixture_turn['effort'])
    writer.join()
    assert run({**dispatch, 'tool_input': {'agent_type': 'default'}}) is None
    assert sorted(p.name for p in sessions.iterdir()) == ['rollout-child.jsonl', 'rollout-parent.jsonl']
    assert sorted(p.name for p in root.iterdir()) == ['plugin', 'sessions']
    assert not list(copy_plugin.rglob('__pycache__'))
    print('PASS: native response/path/header join, bounded race, missing/ambiguous/conflicting evidence; disabled negatives')

print('PASS: hooks are stateless; no primary Stop or SubagentStop enforcement in this scoped group')
