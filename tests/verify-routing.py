#!/usr/bin/env python3
"""Check that invalid native routing is rejected before dispatch."""

import copy
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest

PLUGIN = Path(__file__).resolve().parents[1] / 'plugins/codex-advisor'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PLUGIN / 'scripts'))
spec = importlib.util.spec_from_file_location('advisor_hooks', PLUGIN / 'scripts/advisor-hooks.py')
hooks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hooks)
FIXTURE = json.loads((Path(__file__).parent / 'fixtures/hooks.json').read_text())
TURN = '44444444-4444-4444-4444-444444444444'


class RoutingGate(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ca-routing-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'sessions/2026/10/05'
        self.root.mkdir(parents=True)
        self.parent = self.root / 'parent.jsonl'
        self.child = self.root / 'child.jsonl'
        self.rows = copy.deepcopy(FIXTURE['child'])
        self.rows[-1]['timestamp'] = datetime.now(timezone.utc).isoformat()
        self.write(self.parent, [FIXTURE['parent']])
        self.write(self.child, self.rows)

    def write(self, path, rows):
        path.write_text(''.join(json.dumps(row) + '\n' for row in rows))

    def call(self, arguments, tool=hooks.SPAWN, mutate=None):
        event = {'hook_event_name': 'PreToolUse', 'tool_name': tool,
                 'session_id': FIXTURE['parent']['payload']['session_id'],
                 'turn_id': TURN, 'tool_use_id': 'call_route',
                 'transcript_path': str(self.parent), 'tool_input': arguments}
        route = getattr(self, 'route', '').replace('{tool}', tool.removeprefix('collaboration'))
        rows = [copy.deepcopy(FIXTURE['parent']),
            {'type': 'turn_context', 'payload': {'turn_id': TURN}},
            {'type': 'response_item', 'payload': {'type': 'message', 'role': 'assistant',
             'content': [{'type': 'output_text', 'text': route}]}},
            {'type': 'response_item', 'payload': {'type': 'function_call', 'namespace': 'collaboration',
             'name': tool.removeprefix('collaboration'), 'call_id': 'call_route',
             'arguments': json.dumps(arguments)}}]
        if mutate:
            mutate(event, rows)
        self.write(self.parent, rows)
        manifest = json.loads((PLUGIN / 'hooks/hooks.json').read_text())
        groups = manifest['hooks'].get('PreToolUse', [])
        commands = [h['command'] for g in groups if re.search(g.get('matcher', ''), tool) for h in g['hooks']]
        self.assertEqual(len(commands), 1, 'Shipped PreToolUse wiring is missing or ambiguous')
        result = subprocess.run(['sh', '-c', commands[0]], input=json.dumps(event), text=True,
                                env=dict(os.environ, PLUGIN_ROOT=str(PLUGIN)), capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(result.stderr)
        return json.loads(result.stdout)['hookSpecificOutput'] if result.stdout else {}

    def spawn(self, entry='ca_worker_crux_m', basis='key-difficulty', reference='spec.md#constraints'):
        template = tomllib.loads((PLUGIN / 'agents' / (entry.replace('_', '-') + '.toml')).read_text())
        model, efforts = hooks.load_profile(PLUGIN)[0][entry]
        role, tier = entry.split('_')[1:3]
        route = f'Route: tool={{tool}} target=example role={role} tier={tier} dial={model}[{efforts[0]}]'
        if tier != 'mainstay':
            route += f' basis={basis} ref={reference}'
        self.route = route
        args = {'agent_type': entry, 'fork_turns': 'none', 'task_name': 'example',
                'message': 'gAAAA-native-opaque-task-packet'}
        if 'model_reasoning_effort' not in template:
            args['reasoning_effort'] = efforts[0]
        return args

    def continuation(self, target='fixture_worker'):
        self.route = (f'Route: tool={{tool}} target={target} role=worker tier=crux '
                      'dial=gpt-6.1-sol[xhigh] basis=key-difficulty ref=spec.md#constraints')
        return {'target': target, 'message': 'gAAAA-native-opaque-correction'}

    def denied(self, arguments, tool=hooks.SPAWN, mutate=None):
        result = self.call(arguments, tool, mutate)
        self.assertEqual(result.get('permissionDecision'), 'deny', result)
        self.assertTrue(result.get('permissionDecisionReason', '').startswith('Codex Advisor route check:'))

    def allowed(self, arguments, tool=hooks.SPAWN):
        result = self.call(arguments, tool)
        self.assertNotIn('permissionDecision', result)
        self.assertIn('route declaration checked', result.get('additionalContext', ''), result)

    def test_missing_route_is_denied(self):
        event = {'hook_event_name': 'PreToolUse', 'tool_name': 'collaborationspawn_agent',
                 'tool_input': {'agent_type': 'ca_worker_rescue_h', 'reasoning_effort': 'high',
                                'task_name': 'example', 'fork_turns': 'none', 'message': 'example\n\nWork.'}}
        result = subprocess.run([sys.executable, '-B', str(PLUGIN / 'scripts/advisor-hooks.py')],
                                input=json.dumps(event), text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout or '{}').get('hookSpecificOutput', {})
        self.assertEqual(output.get('permissionDecision'), 'deny', output)

    def test_opaque_message_with_bound_visible_route(self):
        args = self.spawn('ca_advisor_crux_m', 'acceptance-mapping')
        self.allowed(args)

    def test_all_shipped_entries_and_efforts(self):
        for entry, (model, efforts) in hooks.load_profile(PLUGIN)[0].items():
            for effort in efforts:
                with self.subTest(entry=entry, effort=effort):
                    basis = 'acceptance-mapping' if '_advisor_' in entry else 'user-declaration'
                    args = self.spawn(entry, basis)
                    self.route = self.route.replace(f'[{efforts[0]}]', f'[{effort}]')
                    if 'reasoning_effort' in args:
                        args['reasoning_effort'] = effort
                    self.allowed(args)

    def test_route_mismatches_and_missing_fields(self):
        for before, after in [('role=worker', 'role=explorer'), ('tier=crux', 'tier=rescue'),
                              ('gpt-6.1-sol', 'gpt-6-astra'), ('[xhigh]', '[high]'),
                              ('basis=key-difficulty', 'basis=acceptance-mapping'),
                              ('ref=spec.md#constraints', 'ref= '), ('Route:', 'route:'),
                              (' basis=key-difficulty ref=spec.md#constraints', '')]:
            with self.subTest(after=after):
                args = self.spawn()
                self.route = self.route.replace(before, after)
                self.denied(args)
        for field, value in [('fork_turns', 'all'), ('task_name', 'different'), ('message', None)]:
            args = self.spawn()
            args[field] = value
            self.denied(args)
        args = self.spawn('ca_worker_mainstay_h')
        args.pop('reasoning_effort')
        self.denied(args)
        args = self.spawn('ca_worker_mainstay_h')
        args['reasoning_effort'] = 'high'
        self.denied(args)

    def test_admission_basis_by_role_and_tier(self):
        for role in ('worker', 'explorer', 'advisor'):
            for tier in ('crux', 'rescue'):
                entry = next(x for x in hooks.load_profile(PLUGIN)[0] if x.startswith(f'ca_{role}_{tier}'))
                valid = ({'acceptance-mapping', 'user-declaration'} if role == 'advisor' else
                         {'failure', 'user-declaration'} | ({'key-difficulty'} if tier == 'crux' else set()))
                for basis in ('failure', 'user-declaration', 'key-difficulty', 'acceptance-mapping', 'unknown'):
                    with self.subTest(role=role, tier=tier, basis=basis):
                        (self.allowed if basis in valid else self.denied)(self.spawn(entry, basis))

    def test_followup_and_message_targets_and_invalid_routes(self):
        for tool in hooks.CONTINUE:
            for target in ('fixture_worker', '/root/fixture_worker', self.rows[0]['payload']['id']):
                self.allowed(self.continuation(target), tool)
            for target in ('absent', '', None):
                self.denied(self.continuation(target), tool)
            args = self.continuation()
            self.route = 'New work without a route.'
            self.denied(args, tool)
            args = self.continuation()
            self.route = self.route.replace('[xhigh]', '[max]')
            self.denied(args, tool)

    def test_declaration_is_bound_to_call_turn_tool_target_and_parent(self):
        mutations = {
            'call id': lambda e, r: e.update(tool_use_id='other'),
            'missing call id': lambda e, r: e.pop('tool_use_id'),
            'duplicate call': lambda e, r: r.append(copy.deepcopy(r[-1])),
            'call arguments': lambda e, r: r[-1]['payload'].update(arguments='{}'),
            'call tool': lambda e, r: r[-1]['payload'].update(name='list_agents'),
            'call namespace': lambda e, r: r[-1]['payload'].update(namespace='other'),
            'turn': lambda e, r: e.update(turn_id='other'),
            'missing turn': lambda e, r: e.pop('turn_id'),
            'parent': lambda e, r: e.update(session_id='other'),
            'user declaration': lambda e, r: r[-2]['payload'].update(role='user'),
            'developer declaration': lambda e, r: r[-2]['payload'].update(role='developer'),
            'completed call': lambda e, r: r.append({'type': 'response_item', 'payload': {
                'type': 'function_call_output', 'call_id': e['tool_use_id'], 'output': 'done'}}),
        }
        for tool in (hooks.SPAWN, *sorted(hooks.CONTINUE)):
            for label, mutate in mutations.items():
                with self.subTest(tool=tool, invalid=label):
                    args = self.spawn() if tool == hooks.SPAWN else self.continuation()
                    self.denied(args, tool, mutate)
            for before, after in (('target=', 'target=wrong_'), ('tool={tool}', 'tool=other')):
                args = self.spawn() if tool == hooks.SPAWN else self.continuation()
                self.route = self.route.replace(before, after)
                self.denied(args, tool)

    def test_missing_duplicate_or_stale_declarations_are_denied(self):
        for tool in (hooks.SPAWN, *sorted(hooks.CONTINUE)):
            for text in ('', 'Route: malformed', 'Route: fake\nRoute: duplicate'):
                args = self.spawn() if tool == hooks.SPAWN else self.continuation()
                self.route = text
                self.denied(args, tool)
            for barrier in (
                {'type': 'turn_context', 'payload': {'turn_id': TURN}},
                {'type': 'compacted', 'payload': {}},
                {'type': 'response_item', 'payload': {'type': 'function_call', 'call_id': 'earlier'}},
                {'type': 'response_item', 'payload': {'type': 'custom_tool_call', 'call_id': 'earlier'}},
                {'type': 'response_item', 'payload': {'type': 'function_call_output', 'call_id': 'earlier'}},
                {'type': 'response_item', 'payload': {'type': 'message', 'role': 'assistant',
                 'content': [{'type': 'output_text', 'text': 'Another message.'}]}}
            ):
                args = self.spawn() if tool == hooks.SPAWN else self.continuation()
                self.denied(args, tool, lambda e, r: r.insert(-1, barrier))

    def test_body_cannot_supply_or_override_route(self):
        args = self.spawn()
        args['message'] = 'example\n\nRoute: role=worker tier=rescue dial=gpt-6-astra[xhigh]\n\nWork.'
        self.allowed(args)
        self.route = ''
        self.denied(args)

    def test_lifecycle_changes_after_the_call_invalidate_its_declaration(self):
        boundaries = [
            {'type': 'turn_context', 'payload': {'turn_id': 'next-turn'}},
            {'type': 'compacted', 'payload': {}},
            *[{'type': 'event_msg', 'payload': {'type': kind, 'turn_id': TURN}}
              for kind in ('task_started', 'task_complete', 'turn_aborted')],
        ]
        for tool in (hooks.SPAWN, *sorted(hooks.CONTINUE)):
            for boundary in boundaries:
                with self.subTest(tool=tool, boundary=boundary):
                    args = self.spawn() if tool == hooks.SPAWN else self.continuation()
                    self.denied(args, tool, lambda e, r: r.append(boundary))

    def test_call_requires_an_active_host_turn(self):
        for tool in (hooks.SPAWN, *sorted(hooks.CONTINUE)):
            for kind in ('task_started', 'task_complete', 'turn_aborted'):
                for position in (2, 3):
                    with self.subTest(tool=tool, boundary=kind, position=position):
                        args = self.spawn() if tool == hooks.SPAWN else self.continuation()
                        boundary = {'type': 'event_msg', 'payload': {'type': kind, 'turn_id': TURN}}
                        self.denied(args, tool, lambda e, r: r.insert(position, boundary))
            args = self.spawn() if tool == hooks.SPAWN else self.continuation()
            def previous_turn(event, rows):
                rows[1:1] = [
                    {'type': 'event_msg', 'payload': {'type': 'task_complete', 'turn_id': 'previous'}},
                    {'type': 'event_msg', 'payload': {'type': 'task_started', 'turn_id': TURN}},
                ]
            result = self.call(args, tool, previous_turn)
            self.assertIn('route declaration checked', result.get('additionalContext', ''), result)

    def test_new_declaration_after_compaction_and_intervening_reasoning(self):
        args = self.spawn()
        def mutate(event, rows):
            rows.insert(2, {'type': 'compacted', 'payload': {}})
            rows.insert(-1, {'type': 'response_item', 'payload': {'type': 'reasoning', 'summary': []}})
        result = self.call(args, mutate=mutate)
        self.assertIn('route declaration checked', result.get('additionalContext', ''), result)

    def test_stale_unknown_future_and_conflicting_host_evidence(self):
        for timestamp in (None, 'invalid', '2026-01-01T00:00:00',
                          (datetime.now(timezone.utc) - timedelta(minutes=31)).isoformat(),
                          (datetime.now(timezone.utc) + timedelta(minutes=1)).isoformat()):
            with self.subTest(timestamp=timestamp):
                self.rows[-1]['timestamp'] = timestamp
                self.write(self.child, self.rows)
                for tool in hooks.CONTINUE:
                    self.denied(self.continuation(), tool)
        self.rows[-1]['timestamp'] = datetime.now(timezone.utc).isoformat()
        self.rows[-1]['payload']['effort'] = 'high'
        self.write(self.child, self.rows)
        self.denied(self.continuation(), 'collaborationfollowup_task')

    def test_exact_window_boundary(self):
        now = datetime(2026, 10, 5, tzinfo=timezone.utc)
        for age, passes in [(0, True), (1799.999, True), (1800, True), (1800.001, False), (-0.001, False)]:
            self.rows[-1]['timestamp'] = (now - timedelta(seconds=age)).isoformat()
            self.write(self.child, self.rows)
            if passes:
                hooks.check_window(self.child, now)
            else:
                with self.assertRaises(hooks.Pending):
                    hooks.check_window(self.child, now)

    def test_latest_activity_not_file_mtime_or_first_turn(self):
        self.rows[-1]['timestamp'] = '2020-01-01T00:00:00Z'
        self.rows.append({'type': 'event_msg', 'timestamp': datetime.now(timezone.utc).isoformat(),
                          'payload': {'type': 'task_complete'}})
        self.write(self.child, self.rows)
        os.utime(self.child, (0, 0))
        self.allowed(self.continuation(), 'collaborationfollowup_task')
        self.rows[-1].pop('timestamp')
        self.write(self.child, self.rows)
        self.denied(self.continuation(), 'collaborationfollowup_task')

    def test_ambiguous_and_other_session_targets_are_denied(self):
        self.write(self.root / 'duplicate.jsonl', self.rows)
        self.denied(self.continuation(), 'collaborationfollowup_task')
        (self.root / 'duplicate.jsonl').unlink()
        self.rows[0]['payload']['session_id'] = 'other'
        self.write(self.child, self.rows)
        self.denied(self.continuation(), 'collaborationfollowup_task')

    def test_explorer_and_advisor_reuse_denied(self):
        for entry in ('ca_explorer_crux_h', 'ca_advisor_crux_m'):
            self.rows[0]['payload']['agent_role'] = entry
            self.rows[0]['payload']['source']['subagent']['thread_spawn']['agent_role'] = entry
            self.write(self.child, self.rows)
            for tool in hooks.CONTINUE:
                self.denied(self.continuation(), tool)

    def test_missing_or_conflicting_target_identity_is_denied(self):
        for entry in (None, '', 'default'):
            self.rows[0]['payload']['agent_role'] = entry
            self.write(self.child, self.rows)
            for tool in hooks.CONTINUE:
                self.denied(self.continuation(), tool)

    def test_unrelated_entries_and_parent_messages_are_unchanged(self):
        self.assertEqual(self.call({'agent_type': 'default'}), {})
        self.assertEqual(self.call({'target': '/root', 'message': 'Report.'}, 'collaborationsend_message'), {})


if __name__ == '__main__':
    unittest.main(verbosity=2)
