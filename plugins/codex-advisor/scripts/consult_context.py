"""Reconstruct a single qualified caller snapshot without summarizing it."""

import json
import re
from pathlib import Path


class Failure(Exception):
    def __init__(self, code, message, actual=None, details=None):
        super().__init__(message)
        self.code = code
        self.actual = actual
        self.details = details or {}


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


# Type-specific normalization follows the declared item and content policies.
ITEM_POLICY = {
    'message': {'policy': 'preserve', 'shape': 'message', 'blocks': ('content',)},
    'agent_message': {'policy': 'preserve', 'shape': 'agent', 'blocks': ('content',)},
    'reasoning': {'policy': 'preserve', 'shape': 'reasoning', 'blocks': ('summary', 'content')},
    'compaction': {'policy': 'preserve', 'shape': 'opaque'},
    'web_search_call': {'policy': 'hosted'},
    'additional_tools': {'policy': 'capability', 'shape': 'inventory'},
    'configuration_update': {'policy': 'control'},
    'compaction_trigger': {'policy': 'control'},
    'local_shell_call': {'policy': 'hosted', 'shape': 'call',
                         'pair': 'function_call_output', 'shell': True},
    'image_generation_call': {'policy': 'hosted'},
    'context_compaction': {'policy': 'preserve'},
    'other': {'policy': 'preserve'},
}
for call, result, policy, argument in (
        ('function_call', 'function_call_output', 'preserve', 'arguments'),
        ('custom_tool_call', 'custom_tool_call_output', 'preserve', 'input'),
        ('tool_search_call', 'tool_search_output', 'capability', 'arguments')):
    ITEM_POLICY[call] = {'policy': policy, 'shape': 'call', 'pair': result, 'argument': argument,
                         'search': policy == 'capability'}
    ITEM_POLICY[result] = {'policy': policy, 'shape': 'result', 'pair': call,
                           'blocks': ('output',), 'empty_text': True, 'search': policy == 'capability'}
ITEM_POLICY['function_call_output']['call_policies'] = {'local_shell_call': 'hosted'}
ITEM_POLICY['function_call_output']['named_output'] = True

CONTENT_POLICY = {
    'input_text': {'policy': 'preserve', 'field': 'text', 'agent': True, 'empty_tool_text': True},
    'output_text': {'policy': 'preserve', 'field': 'text'},
    'summary_text': {'policy': 'preserve', 'field': 'text'},
    'input_image': {'policy': 'preserve', 'field': 'image_url', 'optional': True,
                    'lite_detail': ('auto', 'high', 'original')},
    'encrypted_content': {'policy': 'preserve', 'field': 'encrypted_content', 'nonempty': True,
                          'agent': True, 'agent_only': True},
}


def diagnostic(error, stage, kind, **location):
    error.details = {'stage': stage, 'type': kind, **location, **error.details}
    return error


def validate_content(content, agent_message=False):
    if not isinstance(content, list):
        raise Failure('unsupported_content', 'Content must be an array.',
                      details={'stage': 'content', 'type': None, 'contentIndex': 0})
    retained = []
    for index, block in enumerate(content):
        kind = block.get('type') if isinstance(block, dict) else None
        try:
            require(isinstance(kind, str), 'unsupported_content', 'Invalid content block.')
            policy = CONTENT_POLICY.get(kind, {})
            require(policy.get('policy') != 'reject', 'unsupported_content', 'Rejected content type.')
            require(not policy or (not agent_message or policy.get('agent')) and
                    (agent_message or not policy.get('agent_only')),
                    'unsupported_content', 'Content type is invalid for this item.')
            field = policy.get('field')
            if field and (not policy.get('optional') or field in block):
                require(isinstance(block.get(field), str) and
                        (not policy.get('nonempty') or bool(block[field])),
                        'unsupported_content', 'Invalid content payload.')
            if policy.get('policy') != 'capability':
                retained.append(block)
        except Failure as error:
            raise diagnostic(error, 'content', kind, contentIndex=index)
    return retained


def pair_identity(item, policy):
    call = item.get('call_id')
    if policy.get('search'):
        require(isinstance(item.get('execution'), str), 'unsupported_content', 'Invalid tool search execution.')
        if call is None:
            return ('search', item['execution'])
    require(call is None or isinstance(call, str), 'pairing', 'Invalid tool call identity.')
    return call or None


def standalone_output(item, policy):
    return (policy.get('named_output') and item.get('call_id') is None and
            isinstance(item.get('name'), str) and bool(item['name']) and
            (item.get('namespace') is None or isinstance(item['namespace'], str)))


def validate_items(items):
    require(isinstance(items, list), 'unsupported_content', 'History must be an array.')
    pending, seen, retained = {}, set(), []
    for index, item in enumerate(items):
        kind = item.get('type') if isinstance(item, dict) else None
        try:
            require(isinstance(kind, str), 'unsupported_content', 'Invalid history item.')
            policy = ITEM_POLICY.get(kind, {})
            disposition = policy.get('policy')
            require(policy.get('policy') != 'reject', 'unsupported_content', 'Rejected history type.')
            shape = policy.get('shape')
            if shape == 'call':
                call = pair_identity(item, policy)
                require((call is not None and call not in pending and
                         (isinstance(call, tuple) or call not in seen)),
                        'pairing', 'Missing or duplicate tool call identity.')
                pending[call] = (policy['pair'], index, kind, policy['policy'])
                seen.add(call)
            elif shape == 'result':
                call = pair_identity(item, policy)
                if call in pending:
                    disposition = policy.get('call_policies', {}).get(pending[call][2], disposition)
                if not standalone_output(item, policy):
                    require(call is not None and call in pending and pending[call][0] == kind and
                            pending[call][3] == disposition, 'pairing', 'A tool result has no matching call.')
                    del pending[call]

            if disposition in ('capability', 'control', 'hosted'):
                continue
            if shape == 'message':
                require(isinstance(item.get('role'), str),
                        'unsupported_content', 'Unsupported message role.')
            elif shape == 'agent':
                require(all(isinstance(item.get(key), str) for key in ('author', 'recipient')),
                        'unsupported_content', 'Agent message author or recipient is missing.')
            elif shape == 'reasoning':
                require(item.get('encrypted_content') is None or isinstance(item['encrypted_content'], str),
                        'unsupported_content', 'Invalid opaque reasoning.')
            elif shape == 'opaque':
                require(isinstance(item.get('encrypted_content'), str) and bool(item['encrypted_content']),
                        'unsupported_content', 'Invalid opaque compaction content.')
            elif shape == 'inventory':
                require(isinstance(item.get('role'), str) and isinstance(item.get('tools'), list),
                        'unsupported_content', 'Invalid tool inventory.')
            elif shape == 'call':
                if policy.get('shell'):
                    require(isinstance(item.get('action'), dict) and isinstance(item.get('status'), str),
                            'unsupported_content', 'Invalid local shell call payload.')
                else:
                    require((policy.get('search') and policy['argument'] in item) or
                            (isinstance(item.get(policy['argument']), str) and isinstance(item.get('name'), str)),
                            'unsupported_content', 'Invalid tool call payload.')
            elif shape == 'result':
                if policy.get('search'):
                    require(isinstance(item.get('status'), str) and isinstance(item.get('tools'), list),
                            'unsupported_content', 'Invalid tool inventory.')
                else:
                    require(isinstance(item.get('output'), (str, list)),
                            'unsupported_content', 'Invalid tool output.')
            value = dict(item)
            for field in policy.get('blocks', ()):
                if field == 'output' and not isinstance(item.get(field), list):
                    continue
                if shape == 'reasoning' and field == 'content' and item.get(field) is None:
                    continue
                value[field] = validate_content(item.get(field), agent_message=shape == 'agent')
            retained.append(value)
        except Failure as error:
            raise diagnostic(error, 'item', kind, historyIndex=index)
    if pending:
        _, index, kind, _ = next(iter(pending.values()))
        raise Failure('pairing', 'Parallel or unfinished tool calls remain before consultation.',
                      details={'stage': 'item', 'type': kind, 'historyIndex': index})
    return retained


def comparable(item, omit_image_detail=False):
    policy = ITEM_POLICY.get(item.get('type'), {})
    value = {key: data for key, data in item.items()
             if key not in ('id', 'internal_chat_message_metadata_passthrough') and data is not None}
    for field in policy.get('blocks', ()):
        if not isinstance(value.get(field), list):
            continue
        blocks = []
        for block in value[field]:
            rule = CONTENT_POLICY.get(block.get('type'), {})
            if rule.get('policy') == 'capability':
                continue
            if policy.get('empty_text') and rule.get('empty_tool_text') and block == {
                    'type': block['type'], rule['field']: ''}:
                continue
            if omit_image_detail and block.get('detail') in rule.get('lite_detail', ()):
                block = {key: data for key, data in block.items() if key != 'detail'}
            blocks.append(block)
        value[field] = blocks
    return value


def validate_retained(payload):
    # These host-owned events are model-invisible; answers remain in tool results.
    kind = payload.get('type')
    require(isinstance(payload.get('turn_id'), str), 'snapshot', 'Retained event turn identity is missing.')
    if kind == 'verified_answer':
        require(isinstance(payload.get('call_id'), str) and isinstance(payload.get('questions'), list),
                'snapshot', 'Invalid retained answer identity or questions.')
        require(all(isinstance(question, dict) and
                    all(isinstance(question.get(key), str) for key in ('question', 'answer'))
                    for question in payload['questions']), 'snapshot', 'Invalid retained question or answer.')
    elif kind == 'delivered_assistant_message':
        require(isinstance(payload.get('text'), str) and isinstance(payload.get('complete'), bool),
                'snapshot', 'Invalid retained assistant message.')
    else:
        raise Failure('snapshot', 'Unqualified retained context event.', details={'eventType': kind})


def read_rollout(path, location):
    location.update(type='session_meta', recordIndex=0)
    location.pop('hostVersion', None)
    try:
        snapshot = path.read_bytes()
        records = []
        lines = snapshot.splitlines(keepends=True)
        for index, line in enumerate(lines):
            location['recordIndex'] = index
            if line.strip():
                try:
                    records.append(json.loads(line))
                except ValueError:
                    if index == len(lines) - 1 and not line.endswith((b'\n', b'\r')):
                        break
                    raise
                if len(records) == 1 and isinstance(records[0], dict):
                    header = records[0].get('payload')
                    if isinstance(header, dict) and 'cli_version' in header:
                        location['hostVersion'] = header['cli_version']
        location['recordIndex'] = 0
    except (OSError, ValueError):
        raise Failure('snapshot', 'The caller rollout snapshot cannot be decoded.') from None
    return records


def matches_call(records, meta):
    if not records or not isinstance(records[0], dict) or records[0].get('type') != 'session_meta':
        return False
    session = records[0].get('payload')
    if not isinstance(session, dict) or session.get('id') != meta['threadId'] or \
            session.get('session_id', session.get('id')) != meta['sessionId']:
        return False
    current = None
    for record in records[1:]:
        if not isinstance(record, dict) or not isinstance(record.get('payload'), dict):
            continue
        payload = record['payload']
        if record.get('type') == 'turn_context':
            current = payload.get('turn_id')
        elif record.get('type') == 'response_item' and payload.get('id') == meta['itemId'] and \
                current == meta['x-codex-turn-metadata']['turn_id']:
            return True
    return False


def caller_records(home, meta, location):
    paths = list((home / 'sessions').rglob('*' + meta['threadId'] + '*.jsonl'))
    if len(paths) == 1:
        return read_rollout(paths[0], location)
    matches = []
    for path in paths:
        records = read_rollout(path, location)
        if matches_call(records, meta):
            matches.append(records)
    location.pop('hostVersion', None)
    if len(matches) != 1:
        raise Failure('identity', 'Exactly one caller rollout must match the active consultation identity.',
                      details={'candidateCount': len(paths), 'matchingCount': len(matches)})
    return matches[0]


def _reconstruct(home, meta, location):
    turn = identity(meta)
    records = caller_records(home, meta, location)
    require(records and isinstance(records[0], dict) and records[0].get('type') == 'session_meta',
            'identity', 'The caller session header is missing.')
    session = records[0].get('payload')
    require(isinstance(session, dict), 'snapshot', 'Invalid session header.')
    location['hostVersion'] = session.get('cli_version')
    require(session.get('id') == meta['threadId'], 'identity', 'Caller rollout identity mismatch.')
    require(session.get('session_id', session['id']) == meta['sessionId'],
            'identity', 'Caller session root identity mismatch.')
    instructions = session.get('base_instructions')
    base = instructions.get('text') if isinstance(instructions, dict) else None
    require(isinstance(base, str) and bool(base), 'context', 'Source base instructions are missing.')
    items, current, started = [], None, None
    positions = []
    boundary = False
    for index, record in enumerate(records[1:], 1):
        location.update(recordIndex=index, type=None)
        require(isinstance(record, dict), 'snapshot', 'Invalid rollout record.')
        kind, payload = record.get('type'), record.get('payload')
        location.update(recordIndex=index, type=kind)
        if kind in ('retained_context', 'event_msg') and isinstance(payload, dict):
            location['type'] = payload.get('type')
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
            positions = [index] * len(items)
        elif kind == 'inter_agent_communication_metadata':
            require(set(payload) == {'trigger_turn'} and isinstance(payload['trigger_turn'], bool),
                    'snapshot', 'Unqualified delegate communication metadata.')
        elif kind == 'retained_context':
            validate_retained(payload)
        elif kind == 'response_item':
            if payload.get('id') == meta['itemId']:
                require(payload.get('type') in ('function_call', 'custom_tool_call'),
                        'identity', 'Consultation boundary is not a tool call.')
                boundary = True
                break
            items.append(payload)
            positions.append(index)
        else:
            require(kind != 'rollback', 'rollback', 'Rollback reconstruction is not qualified.')
            if kind not in ('session_meta', 'world_state', 'token_usage_record'):
                raise Failure('snapshot', 'Unqualified rollout event type.',
                              details={'recordIndex': index, 'recordType': kind})
    require(boundary and current is not None, 'identity', 'The active consultation boundary is missing.')
    require(current.get('turn_id') == turn['turn_id'] and started == turn['turn_id'],
            'identity', 'The consultation item does not belong to the host active turn.')
    require(current.get('model') == turn['model'] and
            current.get('effort') == turn['reasoning_effort'],
            'identity', 'Caller dial differs from host turn metadata.')
    try:
        items = validate_items(items)
    except Failure as error:
        if 'historyIndex' in error.details:
            error.details['recordIndex'] = positions[error.details['historyIndex']]
        raise
    return {'items': items, 'base': base, 'model': turn['model'],
            'effort': turn['reasoning_effort'], 'role': session.get('agent_role'),
            'source': session.get('source'), 'thread': meta['threadId'],
            'hostVersion': session.get('cli_version')}


def reconstruct(home, meta):
    location = {'stage': 'record', 'type': 'session_meta', 'recordIndex': 0}
    try:
        return _reconstruct(home, meta, location)
    except Failure as error:
        error.details = {**location, **error.details}
        raise


def model_segments(profile):
    segments = ('starter', 'midrange', 'premium', 'flagship')
    placements = re.findall(r'^\|\s*`(gpt-[^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*$', profile, re.M)
    require(bool(placements), 'profile', 'Routing profile model segments are unavailable.')
    models = {}
    for model, segment in placements:
        require(segment in segments, 'profile', 'Routing profile model segment is unknown.')
        require(model not in models, 'profile', 'A routing profile model has duplicate segments.')
        models[model] = segments.index(segment)
    return models


def load_profile(plugin):
    profile = (plugin / 'skills/orchestration/references/routing-profile.md').read_text(encoding='utf-8')
    rows = dict((name, (model, [e.strip().rstrip('*') for e in efforts.split(',')]))
                for name, model, efforts in re.findall(
                    r'`(ca_[a-z0-9_]+)`\s+(gpt-[^\s\[]+)\[([^\]]+)\]', profile))
    models = model_segments(profile)
    ordering = re.search(r'Compare effort second:\s*([^\n]+)\.', profile)
    require(ordering is not None, 'profile', 'Routing profile effort ordering is unavailable.')
    require(all(model in models for model, _ in rows.values()),
            'profile', 'A routing profile model is missing from the segment table.')
    unknown = re.search(r'absent\s+from\s+this\s+profile\s+uses\s+(gpt-[^\s\[]+)\[([a-z]+)\]', profile)
    advisors = {(model, effort) for name, (model, allowed) in rows.items()
                if name.startswith('ca_advisor_') for effort in allowed}
    require(unknown is not None and (unknown[1], unknown[2]) in advisors,
            'profile', 'Routing profile fallback for an unknown model is not an Advisor dial.')
    efforts = ordering[1].split(' < ')
    aliases = dict(re.findall(r'^\|\s*`([a-z]+)`\s*\|\s*`([a-z]+)`\s*\|\s*$', profile, re.M))
    require(all(alias not in efforts and value in efforts for alias, value in aliases.items()),
            'profile', 'Routing profile host effort mapping is invalid.')
    return rows, models, efforts, (unknown[1], unknown[2]), aliases


def advisor_dial(profile, model, effort, tier=None):
    # The lowest Advisor dial not weaker than the caller, else the strongest; a tier limits it to one cell.
    # Only a primary can carry a model absent from the segment table; it takes the fallback dial.
    rows, models, efforts, unknown, aliases = profile
    effort = aliases.get(effort, effort)
    dials = [(candidate, level) for name, (candidate, allowed) in rows.items()
             if name.startswith('ca_advisor_') and tier in (None, name.split('_')[2]) for level in allowed]
    require(bool(dials), 'profile', 'No advisor dials are configured.')
    dials.sort(key=lambda d: (models[d[0]], efforts.index(d[1])))
    if model not in models:
        return unknown
    rank = (models[model], efforts.index(effort))
    return next((d for d in dials if (models[d[0]], efforts.index(d[1])) >= rank), dials[-1])


def route(plugin, caller):
    profile = load_profile(plugin)
    rows, _, efforts, _, aliases = profile
    role = caller['role']
    if role:
        require(role in rows and role.startswith(('ca_worker_', 'ca_explorer_')),
                'route', 'Caller role is not a supported consultation entry.')
        require(caller['model'] == rows[role][0] and caller['effort'] in rows[role][1],
                'route', 'Caller entry actual dial is outside its routing profile.')
        chosen = advisor_dial(profile, caller['model'], caller['effort'], role.split('_')[2])
    else:
        require(not isinstance(caller['source'], dict), 'route', 'A delegate is missing its entry identity.')
        if caller['effort'] not in efforts and caller['effort'] not in aliases:
            raise Failure('route', 'Caller effort is not in the qualified ordering.',
                          details={'caller': {'model': caller['model'], 'effort': caller['effort']},
                                   'allowedEfforts': efforts + list(aliases)})
        chosen = advisor_dial(profile, caller['model'], caller['effort'])
    return dict(zip(('model', 'effort'), chosen))
