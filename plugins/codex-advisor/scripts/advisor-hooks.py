#!/usr/bin/env python3
"""Inject canonical posture and verify native dispatches without writing state."""

import json
from pathlib import Path
import re
import sys
import time
import tomllib

sys.dont_write_bytecode = True

PLUGIN = Path(__file__).resolve().parent.parent
REFERENCES = PLUGIN / 'skills/orchestration/references'
WAIT_SECONDS = 2


class Pending(Exception):
    pass


def require(condition, reason):
    if not condition:
        raise Pending(reason)


def header(path):
    with path.open(encoding='utf-8') as stream:
        row = json.loads(stream.readline())
    require(row.get('type') == 'session_meta' and isinstance(row.get('payload'), dict),
            'Session identity evidence is missing.')
    return row['payload']


def parent(event):
    path = Path(event.get('transcript_path', ''))
    require(path.is_absolute(), 'The host transcript path is missing.')
    meta = header(path)
    require(meta.get('id') and meta.get('session_id', meta['id']) == event.get('session_id'),
            'The host session identity conflicts with its transcript.')
    return path, meta


def posture(event):
    if event.get('agent_id') or event.get('agent_type'):
        return None
    _, meta = parent(event)
    if meta.get('parent_thread_id') or meta.get('agent_role') or isinstance(meta.get('source'), dict):
        return None
    profile = (REFERENCES / 'routing-profile.md').read_text(encoding='utf-8')
    models = set(re.findall(r'`ca_advisor_[a-z0-9_]+`\s+([^\s\[]+)\[', profile))
    require(len(models) == 1, 'Advisor model selection needs evidence unavailable at session start.')
    require(isinstance(event.get('model'), str) and event['model'], 'The session model is missing.')
    variant = 'reduced' if event['model'] == next(iter(models)) else 'full'
    canonical = (REFERENCES / 'consult-posture.md').read_text(encoding='utf-8')
    blocks = []
    for name in (variant, 'adoption'):
        matches = re.findall(r'<!-- consult-posture:' + name + r':start -->.*?<!-- consult-posture:' +
                             name + r':end -->', canonical, re.S)
        require(len(matches) == 1, 'The canonical posture block is missing or ambiguous.')
        blocks.append(matches[0])
    return '\n\n'.join(blocks)


def expected(arguments):
    entries = [tomllib.loads(path.read_text(encoding='utf-8')) for path in (PLUGIN / 'agents').glob('*.toml')]
    entries = [entry for entry in entries if entry.get('name') == arguments['agent_type']]
    require(len(entries) == 1, 'The requested entry is missing or ambiguous in shipped templates.')
    entry = entries[0]
    effort = entry.get('model_reasoning_effort') or arguments.get('reasoning_effort')
    require(isinstance(effort, str) and effort, 'A caller-effort entry was spawned without reasoning_effort.')
    return entry['model'], effort


def child_path(meta):
    source = meta.get('source')
    if not isinstance(source, dict):
        return None
    return source.get('subagent', {}).get('thread_spawn', {}).get('agent_path')


def find_child(root, parent_id, task):
    matches = []
    for path in root.rglob('*.jsonl'):
        try:
            meta = header(path)
        except (OSError, ValueError, Pending):
            continue
        if meta.get('parent_thread_id') == parent_id and child_path(meta) == task:
            matches.append(path)
    require(len(matches) <= 1, 'Child session evidence is ambiguous for this parent and task path.')
    require(matches, 'Child session evidence is not yet available for this parent and task path.')
    return matches[0]


def actual(path, role, parent_id, session_id, task):
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    headers = [row['payload'] for row in rows if row.get('type') == 'session_meta']
    require(len(headers) == 1 and headers[0].get('agent_role') == role and headers[0].get('id'),
            'Child entry identity is missing or conflicting.')
    meta = headers[0]
    require(meta.get('parent_thread_id') == parent_id and meta.get('session_id') == session_id and
            child_path(meta) == task, 'Child parent, session, or task identity conflicts.')
    spawn = meta['source']['subagent']['thread_spawn']
    require(spawn.get('parent_thread_id', parent_id) == parent_id and
            spawn.get('agent_role', role) == role, 'Child source identity conflicts with its header.')
    turns = [row['payload'] for row in rows if row.get('type') == 'turn_context']
    require(turns, 'Child model and effort evidence is not yet available.')
    models, efforts = set(), set()
    for turn in turns:
        require(isinstance(turn.get('model'), str) and turn['model'] and
                isinstance(turn.get('effort'), str) and turn['effort'],
                'Child model or effort evidence is missing.')
        models.add(turn['model'])
        efforts.add(turn['effort'])
    require(len(models) == len(efforts) == 1, 'Child model or effort evidence conflicts across turns.')
    return next(iter(models)), next(iter(efforts))


def observe(root, parent_id, task, role, session_id):
    deadline = time.monotonic() + WAIT_SECONDS
    while True:
        try:
            return actual(find_child(root, parent_id, task), role, parent_id, session_id, task)
        except (Pending, OSError, ValueError):
            if time.monotonic() >= deadline:
                raise
            time.sleep(0.1)


def dispatch(event):
    arguments = event.get('tool_input')
    require(isinstance(arguments, dict), 'Native spawn arguments are unavailable.')
    role = arguments.get('agent_type', '')
    if not isinstance(role, str) or not role.startswith('ca_'):
        return None
    model, effort = expected(arguments)
    response = event.get('tool_response')
    if isinstance(response, str):
        response = json.loads(response)
    require(isinstance(response, dict), 'Native spawn response is unavailable.')
    task = response.get('task_name')
    require(isinstance(task, str) and task.startswith('/') and
            task.rsplit('/', 1)[-1] == arguments.get('task_name'),
            'Native spawn response does not identify the requested task path.')
    path, meta = parent(event)
    roots = [p for p in path.parents if p.name == 'sessions']
    require(len(roots) == 1, 'The host transcript is outside the qualified sessions layout.')
    observed = observe(roots[0], meta['id'], task, role, event['session_id'])
    require(observed == (model, effort),
            f'Native dispatch {role} expected {model}[{effort}] but observed {observed[0]}[{observed[1]}].')
    return None


def main():
    event = json.load(sys.stdin)
    kind = event.get('hook_event_name')
    if kind not in ('SessionStart', 'PostToolUse'):
        return
    if kind == 'PostToolUse' and event.get('tool_name') != 'collaborationspawn_agent':
        return
    try:
        context = posture(event) if kind == 'SessionStart' else dispatch(event)
    except (Pending, OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        reason = str(error) if isinstance(error, Pending) else 'Hook input or runtime evidence could not be read.'
        context = 'Codex Advisor: affected work remains pending. ' + reason
    if context:
        print(json.dumps({'hookSpecificOutput': {'hookEventName': kind, 'additionalContext': context}}))


if __name__ == '__main__':
    main()
