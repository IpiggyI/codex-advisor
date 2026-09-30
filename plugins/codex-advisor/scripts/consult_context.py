"""Reconstruct a single qualified caller snapshot without summarizing it."""

import json
import re
from pathlib import Path


class Failure(Exception):
    def __init__(self, code, message, actual=None):
        super().__init__(message)
        self.code = code
        self.actual = actual


def require(condition, code, message):
    if not condition:
        raise Failure(code, message)


def caller_home(plugin):
    parts = plugin.parts
    require(len(parts) >= 6 and parts[-5:-1] ==
            ('plugins', 'cache', 'codex-advisor', 'codex-advisor') and
            re.fullmatch(r'\d+\.\d+\.\d+(?:[-+][\w.-]+)?', parts[-1]),
            'unsupported_layout', 'Consultation requires the versioned plugin cache layout.')
    return plugin.parents[4]


def identity(meta):
    require(isinstance(meta, dict), 'identity', 'Host MCP metadata is missing.')
    turn = meta.get('x-codex-turn-metadata')
    require(isinstance(turn, dict), 'identity', 'Host turn metadata is missing.')
    for outer, inner in [('threadId', 'thread_id'), ('sessionId', 'session_id')]:
        value = meta.get(outer)
        require(isinstance(value, str) and
                re.fullmatch(r'[0-9a-fA-F-]{36}', value) and value == turn.get(inner),
                'identity', 'Host session and thread identities are inconsistent.')
    for key in ('turn_id', 'model', 'reasoning_effort'):
        require(isinstance(turn.get(key), str) and bool(turn[key]),
                'identity', 'Host turn identity or dial is missing.')
    require(isinstance(meta.get('itemId'), str) and bool(meta['itemId']),
            'identity', 'Host consultation item identity is missing.')
    return turn


def validate_content(content, agent_message=False):
    require(isinstance(content, list), 'unsupported_content', 'Content must be an array.')
    for block in content:
        require(isinstance(block, dict), 'unsupported_content', 'Invalid content block.')
        kind = block.get('type')
        if agent_message and kind == 'encrypted_content':
            require(isinstance(block.get('encrypted_content'), str) and bool(block['encrypted_content']),
                    'unsupported_content', 'Invalid opaque agent message content.')
        elif agent_message:
            require(kind == 'input_text' and isinstance(block.get('text'), str),
                    'unsupported_content', 'Unsupported agent message content.')
        elif kind in ('input_text', 'output_text', 'summary_text'):
            require(isinstance(block.get('text'), str), 'unsupported_content', 'Invalid text block.')
        elif kind == 'input_image':
            require(isinstance(block.get('image_url'), str) and bool(block['image_url']),
                    'unsupported_content', 'An image must retain its original URL content.')
        else:
            raise Failure('unsupported_content', 'The caller has an unqualified content type.')


def validate_items(items):
    require(isinstance(items, list), 'unsupported_content', 'History must be an array.')
    pending = {}
    seen = set()
    for item in items:
        require(isinstance(item, dict), 'unsupported_content', 'Invalid history item.')
        kind = item.get('type')
        if kind == 'message':
            require(item.get('role') in ('system', 'developer', 'user', 'assistant'),
                    'unsupported_content', 'Unsupported message role.')
            validate_content(item.get('content'))
        elif kind == 'agent_message':
            require(all(isinstance(item.get(key), str) and bool(item[key])
                        for key in ('author', 'recipient')),
                    'unsupported_content', 'Agent message author or recipient is missing.')
            validate_content(item.get('content'), agent_message=True)
        elif kind == 'reasoning':
            validate_content(item.get('summary', []))
            require(item.get('encrypted_content') is None or
                    isinstance(item['encrypted_content'], str),
                    'unsupported_content', 'Invalid opaque reasoning.')
            if item.get('content') is not None:
                validate_content(item['content'])
        elif kind in ('function_call', 'custom_tool_call'):
            call = item.get('call_id')
            require(isinstance(call, str) and call and call not in seen,
                    'pairing', 'Missing or duplicate tool call identity.')
            require(isinstance(item.get('name'), str) and
                    isinstance(item.get('arguments' if kind == 'function_call' else 'input'), str),
                    'unsupported_content', 'Invalid tool call payload.')
            pending[call] = kind + '_output'
            seen.add(call)
        elif kind in ('function_call_output', 'custom_tool_call_output'):
            call = item.get('call_id')
            require(call in pending and pending[call] == kind, 'pairing',
                    'A tool result has no matching call.')
            del pending[call]
            output = item.get('output')
            if isinstance(output, list):
                validate_content(output)
            else:
                require(isinstance(output, str), 'unsupported_content', 'Invalid tool output.')
        else:
            raise Failure('unsupported_content', 'The caller has an unqualified history item.')
    require(not pending, 'pairing', 'Parallel or unfinished tool calls remain before consultation.')


def reconstruct(home, meta):
    turn = identity(meta)
    paths = list((home / 'sessions').rglob('*' + meta['threadId'] + '*.jsonl'))
    require(len(paths) == 1, 'identity', 'Exactly one caller rollout must match the host identity.')
    try:
        snapshot = paths[0].read_bytes()
        records = [json.loads(line) for line in snapshot.splitlines() if line.strip()]
    except (OSError, ValueError):
        raise Failure('snapshot', 'The caller rollout snapshot cannot be decoded.') from None
    require(records and records[0].get('type') == 'session_meta',
            'identity', 'The caller session header is missing.')
    session = records[0]['payload']
    require(session.get('id') == meta['threadId'], 'identity', 'Caller rollout identity mismatch.')
    require(session.get('session_id', session['id']) == meta['sessionId'],
            'identity', 'Caller session root identity mismatch.')
    base = session.get('base_instructions', {}).get('text')
    require(isinstance(base, str) and bool(base), 'context', 'Source base instructions are missing.')
    items, current, started = [], None, None
    boundary = False
    for index, record in enumerate(records[1:], 1):
        kind, payload = record.get('type'), record.get('payload')
        require(isinstance(payload, dict), 'snapshot', 'Invalid rollout payload.')
        if kind == 'turn_context':
            current = payload
        elif kind == 'event_msg':
            event = payload.get('type')
            require(event != 'thread_rolled_back', 'rollback', 'Rollback reconstruction is not qualified.')
            if event == 'task_started':
                started = payload.get('turn_id')
            if event in ('task_complete', 'turn_aborted') and payload.get('turn_id') == turn['turn_id']:
                raise Failure('identity', 'The consultation turn is no longer active.')
        elif kind == 'compacted':
            replacement = payload.get('replacement_history')
            require(isinstance(replacement, list), 'compaction', 'Compaction replacement history is missing.')
            items = replacement.copy()
        elif kind == 'inter_agent_communication_metadata':
            require(set(payload) == {'trigger_turn'} and isinstance(payload['trigger_turn'], bool),
                    'snapshot', 'Unqualified delegate communication metadata.')
        elif kind == 'response_item':
            if payload.get('id') == meta['itemId']:
                require(payload.get('type') in ('function_call', 'custom_tool_call'),
                        'identity', 'Consultation boundary is not a tool call.')
                require(not any(later.get('type') == 'response_item' for later in records[index + 1:]),
                        'pairing', 'History changed beyond the unfinished consultation boundary.')
                boundary = True
                break
            items.append(payload)
        else:
            require(kind != 'rollback', 'rollback', 'Rollback reconstruction is not qualified.')
            require(kind in ('session_meta', 'world_state', 'token_usage_record'),
                    'snapshot', 'Unqualified rollout event type.')
    require(boundary and current is not None, 'identity', 'The active consultation boundary is missing.')
    require(current.get('turn_id') == turn['turn_id'] and started == turn['turn_id'],
            'identity', 'The consultation item does not belong to the host active turn.')
    require(current.get('model') == turn['model'] and
            current.get('effort') == turn['reasoning_effort'],
            'identity', 'Caller dial differs from host turn metadata.')
    validate_items(items)
    return {'items': items, 'base': base, 'model': turn['model'],
            'effort': turn['reasoning_effort'], 'role': session.get('agent_role'),
            'source': session.get('source'), 'thread': meta['threadId']}


def load_profile(plugin):
    profile = (plugin / 'skills/orchestration/references/routing-profile.md').read_text(encoding='utf-8')
    rows = dict((name, (model, [e.strip().rstrip('*') for e in efforts.split(',')]))
                for name, model, efforts in re.findall(
                    r'`(ca_[a-z0-9_]+)`\s+(gpt-[^\s\[]+)\[([^\]]+)\]', profile))
    ordering = re.search(r'compare model first:\s*([^\n]+)\. Compare effort second:\s*([^\n]+)\.', profile)
    require(ordering is not None, 'profile', 'Routing profile ordering is unavailable.')
    models = ordering[1].split(' < ')
    require(all(model in models for model, _ in rows.values()),
            'profile', 'A routing profile model is missing from the ordering.')
    unknown = re.search(r'absent\s+from\s+this\s+profile\s+uses\s+(gpt-[^\s\[]+)\[([a-z]+)\]', profile)
    advisors = {(model, effort) for name, (model, allowed) in rows.items()
                if name.startswith('ca_advisor_') for effort in allowed}
    require(unknown is not None and (unknown[1], unknown[2]) in advisors,
            'profile', 'Routing profile fallback for an unknown model is not an Advisor dial.')
    return rows, models, ordering[2].split(' < '), (unknown[1], unknown[2])


def advisor_dial(profile, model, effort, tier=None):
    # The lowest Advisor dial not weaker than the caller, else the strongest; a tier limits it to one cell.
    # Only a primary can carry a model absent from the ordering; it takes the profile's declared fallback.
    rows, models, efforts, unknown = profile
    dials = [(candidate, level) for name, (candidate, allowed) in rows.items()
             if name.startswith('ca_advisor_') and tier in (None, name.split('_')[2]) for level in allowed]
    require(bool(dials), 'profile', 'No advisor dials are configured.')
    dials.sort(key=lambda d: (models.index(d[0]), efforts.index(d[1])))
    if model not in models:
        return unknown
    rank = (models.index(model), efforts.index(effort))
    return next((d for d in dials if (models.index(d[0]), efforts.index(d[1])) >= rank), dials[-1])


def route(plugin, caller):
    profile = load_profile(plugin)
    rows, _, efforts, _ = profile
    role = caller['role']
    if role:
        require(role in rows and role.startswith(('ca_worker_', 'ca_explorer_')),
                'route', 'Caller role is not a supported consultation entry.')
        require(caller['model'] == rows[role][0] and caller['effort'] in rows[role][1],
                'route', 'Caller entry actual dial is outside its routing profile.')
        chosen = advisor_dial(profile, caller['model'], caller['effort'], role.split('_')[2])
    else:
        require(not isinstance(caller['source'], dict), 'route', 'A delegate is missing its entry identity.')
        require(caller['effort'] in efforts, 'route', 'Caller effort is not in the qualified ordering.')
        chosen = advisor_dial(profile, caller['model'], caller['effort'])
    return dict(zip(('model', 'effort'), chosen))
