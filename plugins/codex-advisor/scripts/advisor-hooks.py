#!/usr/bin/env python3
"""Inject posture, check routing before calls, and verify native dispatches."""

from datetime import datetime, timezone
import json
from pathlib import Path
import posixpath
import re
import sys
import time
import tomllib

sys.dont_write_bytecode = True
from consult_context import Failure, advisor_dial, load_profile

PLUGIN = Path(__file__).resolve().parent.parent
REFERENCES = PLUGIN / 'skills/orchestration/references'
WAIT_SECONDS = 2
REUSE_SECONDS = 30 * 60
SPAWN = 'collaborationspawn_agent'
CONTINUE = {'collaborationfollowup_task', 'collaborationsend_message'}


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
    profile = load_profile(PLUGIN)
    require(isinstance(event.get('model'), str) and event['model'], 'The session model is missing.')
    # Session start supplies no effort, so the advisor model must be the same at every effort.
    models = {advisor_dial(profile, event['model'], effort)[0] for effort in profile[2]}
    require(len(models) == 1, 'Advisor model selection depends on an effort that session start does not supply.')
    variant = 'reduced' if event['model'] == models.pop() else 'full'
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
    return (f'Codex Advisor: {role} identity, model, and effort match the host record at {model}[{effort}]; '
            'working directory and permissions were not checked.')


def route_line(message, task=None):
    require(isinstance(message, str), 'A route declaration is required in message.')
    lines = message.splitlines()
    if task is not None:
        require(len(lines) >= 3 and lines[0] == task and not lines[1],
                'Start message with task_name, a blank line, then Route:.')
        lines = lines[2:]
    match = re.fullmatch(r'Route: role=(worker|explorer|advisor) tier=(mainstay|crux|rescue) '
                        r'dial=(gpt-[\w.-]+)\[([a-z]+)\]'
                        r'(?: basis=([a-z-]+) ref=(\S[^\r\n]*))?', lines[0] if lines else '')
    require(match is not None, 'A canonical Route: role=... tier=... dial=... line is required.')
    return match.groups()


def check_route(route, entry, dial):
    role, tier, model, effort, basis, reference = route
    require(entry.split('_')[1:3] == [role, tier], 'Route role or tier conflicts with the native entry.')
    rows = load_profile(PLUGIN)[0]
    require(entry in rows and rows[entry][0] == model and effort in rows[entry][1],
            'The declared dial is outside this entry in the routing profile.')
    require((model, effort) == dial, 'The declared dial conflicts with native settings or host evidence.')
    if tier == 'mainstay':
        require(basis is None, 'Mainstay routes omit basis and ref.')
        return
    allowed = ({'acceptance-mapping', 'user-declaration'} if role == 'advisor' else
               {'failure', 'user-declaration'} | ({'key-difficulty'} if tier == 'crux' else set()))
    require(basis in allowed and reference and reference.strip(),
            'This role and tier require an allowed basis and nonempty ref: ' + ', '.join(sorted(allowed)) + '.')


def target_thread(event, target):
    require(isinstance(target, str) and target.strip(), 'A native target is required.')
    path, meta = parent(event)
    roots = [p for p in path.parents if p.name == 'sessions']
    require(len(roots) == 1, 'The host transcript is outside the qualified sessions layout.')
    caller_path = child_path(meta) or '/root'
    task = posixpath.normpath(target if target.startswith('/') else caller_path + '/' + target)
    matches = []
    for candidate in roots[0].rglob('*.jsonl'):
        try:
            child = header(candidate)
        except (OSError, ValueError, Pending):
            continue
        if child.get('session_id', child.get('id')) != event.get('session_id'):
            continue
        if child.get('id') == target or (child_path(child) or '/root') == task:
            matches.append((candidate, child))
    require(len(matches) == 1, 'The target must resolve to exactly one thread in this host session.')
    return matches[0]


def check_window(path, now=None):
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    activity = [row for row in rows if row.get('type') in ('response_item', 'event_msg', 'turn_context')]
    require(activity, 'Target activity time is unknown; start a fresh thread at the same tier and dial.')
    timestamp = activity[-1].get('timestamp')
    require(isinstance(timestamp, str), 'Target activity time is missing; start a fresh thread.')
    try:
        latest = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    except ValueError:
        raise Pending('Target activity time is invalid; start a fresh thread.') from None
    require(latest.tzinfo is not None, 'Target activity time has no timezone; start a fresh thread.')
    age = ((now or datetime.now(timezone.utc)) - latest).total_seconds()
    require(0 <= age <= REUSE_SECONDS,
            'Target activity is outside the 30-minute reuse window; start a fresh thread at the same tier and dial.')


def target_entry(meta):
    entry = meta.get('agent_role')
    source = meta.get('source')
    if meta.get('parent_thread_id') or isinstance(source, dict):
        require(isinstance(entry, str) and entry, 'Target entry identity is missing.')
        require(isinstance(source, dict), 'Target source identity is missing.')
        spawn = source.get('subagent', {}).get('thread_spawn', {})
        require(spawn.get('agent_role', entry) == entry, 'Target entry and source identity conflict.')
    return entry if isinstance(entry, str) else ''


def route_gate(event):
    arguments = event.get('tool_input')
    require(isinstance(arguments, dict), 'Native tool arguments are unavailable.')
    if event['tool_name'] == SPAWN:
        entry = arguments.get('agent_type', '')
        if not isinstance(entry, str) or not entry.startswith('ca_'):
            return None
        require(isinstance(arguments.get('task_name'), str) and arguments['task_name'].strip(),
                'A nonempty native task_name is required.')
        route = route_line(arguments.get('message'), arguments.get('task_name'))
        require(arguments.get('fork_turns') == 'none', 'Native entries require fork_turns: none.')
        dial = expected(arguments)
    else:
        path, meta = target_thread(event, arguments.get('target'))
        entry = target_entry(meta)
        if not entry.startswith('ca_'):
            return None
        require(entry.startswith('ca_worker_'), 'Explorer calls and independent acceptance require fresh threads.')
        route = route_line(arguments.get('message'))
        dial = actual(path, entry, meta.get('parent_thread_id'), event['session_id'], child_path(meta))
        check_window(path)
    check_route(route, entry, dial)
    return ('Codex Advisor: route declaration checked for ' + entry + '; '
            'basis truth, task fit, and user authorization remain the caller\'s responsibility.')


def main():
    event = json.load(sys.stdin)
    kind = event.get('hook_event_name')
    if kind not in ('SessionStart', 'PostToolUse', 'PreToolUse'):
        return
    if kind == 'PostToolUse' and event.get('tool_name') != SPAWN:
        return
    if kind == 'PreToolUse' and event.get('tool_name') not in {SPAWN, *CONTINUE}:
        return
    try:
        context = (posture(event) if kind == 'SessionStart' else
                   route_gate(event) if kind == 'PreToolUse' else dispatch(event))
    except (Pending, Failure, OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        reason = (str(error) if isinstance(error, (Pending, Failure))
                  else 'Hook input or runtime evidence could not be read.')
        if kind == 'PreToolUse':
            print(json.dumps({'hookSpecificOutput': {'hookEventName': kind, 'permissionDecision': 'deny',
                              'permissionDecisionReason': 'Codex Advisor route check: ' + reason}}))
            return
        context = 'Codex Advisor: affected work remains pending. ' + reason
    if context:
        print(json.dumps({'hookSpecificOutput': {'hookEventName': kind, 'additionalContext': context}}))


if __name__ == '__main__':
    main()
