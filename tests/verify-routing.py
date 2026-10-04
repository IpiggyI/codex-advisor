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

    def call(self, arguments, tool=hooks.SPAWN):
        event = {'hook_event_name': 'PreToolUse', 'tool_name': tool,
                 'session_id': FIXTURE['parent']['payload']['session_id'],
                 'transcript_path': str(self.parent), 'tool_input': arguments}
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
        route = f'Route: role={role} tier={tier} dial={model}[{efforts[0]}]'
        if tier != 'mainstay':
            route += f' basis={basis} ref={reference}'
        args = {'agent_type': entry, 'fork_turns': 'none', 'task_name': 'example',
                'message': 'example\n\n' + route + '\n\nWork.'}
        if 'model_reasoning_effort' not in template:
            args['reasoning_effort'] = efforts[0]
        return args

    def continuation(self, target='fixture_worker'):
        return {'target': target, 'message': 'Route: role=worker tier=crux '
                'dial=gpt-6.1-sol[xhigh] basis=key-difficulty ref=spec.md#constraints\n\nRework.'}

    def denied(self, arguments, tool=hooks.SPAWN):
        result = self.call(arguments, tool)
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

    def test_all_shipped_entries_and_efforts(self):
        for entry, (model, efforts) in hooks.load_profile(PLUGIN)[0].items():
            for effort in efforts:
                with self.subTest(entry=entry, effort=effort):
                    basis = 'acceptance-mapping' if '_advisor_' in entry else 'user-declaration'
                    args = self.spawn(entry, basis)
                    args['message'] = args['message'].replace(f'[{efforts[0]}]', f'[{effort}]')
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
                args['message'] = args['message'].replace(before, after)
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
            args['message'] = 'New work without a route.'
            self.denied(args, tool)
            args = self.continuation()
            args['message'] = args['message'].replace('[xhigh]', '[max]')
            self.denied(args, tool)

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
