#!/bin/sh
# Exercise the public installer with disposable destinations.
set -eu
script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd)
case "${1-}" in ''|--installation|--runtime) ;; *) printf '%s\n' 'Unknown verification group' >&2; exit 2 ;; esac
if [ "${1-}" != --runtime ]; then
python3 - "$script_dir" <<'PY'
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib

scripts = Path(sys.argv[1])
plugin = scripts.parent
repo = plugin.parent.parent
manifest = json.loads((plugin / '.codex-plugin/plugin.json').read_text())
market = json.loads((repo / '.agents/plugins/marketplace.json').read_text())
assert manifest['name'] == market['name'] == 'codex-advisor'
assert market['plugins'][0]['name'] == 'codex-advisor'
assert market['plugins'][0]['source']['path'] == './plugins/codex-advisor'
templates = {p.name: p.read_bytes() for p in (plugin / 'agents').glob('*.toml')}
assert templates
for filename, content in templates.items():
    data = tomllib.loads(content.decode())
    assert filename.startswith('ca-'), filename
    assert data['name'].startswith('ca_'), data['name']
    assert data['description'] and data['developer_instructions']
stems = {name[3:-5]: name for name in templates}
assert stems
sample_name = sorted(stems.values())[0]
sample_stem = sample_name[3:-5]
other_name = sorted(stems.values())[1]
other_stem = other_name[3:-5]
worker_name = next(name for name in sorted(templates) if name.startswith('ca-worker-'))
# Same-role developer_instructions must be byte-identical (role = second
# segment of name).
by_role = {}
for filename, content in templates.items():
    data = tomllib.loads(content.decode())
    role = data['name'].split('_')[1]
    by_role.setdefault(role, []).append(data['developer_instructions'])
for role, bodies in by_role.items():
    assert bodies and all(b == bodies[0] for b in bodies), role
# Pin model_reasoning_effort exactly when the routing profile marks a single
# bare effort. Source: plugins/codex-advisor/skills/orchestration/references/routing-profile.md
profile = (plugin / 'skills/orchestration/references/routing-profile.md').read_text()
name_re = re.compile(r'`(ca_[a-z0-9_]+)`')
dial_re = re.compile(r'`(ca_[a-z0-9_]+)`\s+(gpt-[^\s\[]+)\[([^\]]+)\]')
table_names = []
table_dials = {}
for line in profile.splitlines():
    if not line.lstrip().startswith('|'):
        continue
    table_names.extend(name_re.findall(line))
    for match in dial_re.finditer(line):
        table_dials[match.group(1)] = (match.group(2), match.group(3).strip())
profile_set = set(table_names)
expected_entries = len(profile_set)
shipped = {}
for filename, content in templates.items():
    data = tomllib.loads(content.decode())
    shipped[data['name']] = data
assert len(shipped) == expected_entries, sorted(shipped)
shipped_set = set(shipped)
mismatch = profile_set ^ shipped_set
assert not mismatch, ', '.join(sorted(mismatch))
assert set(table_dials) == shipped_set, ', '.join(sorted(set(table_dials) ^ shipped_set))
for name, (model, inner) in table_dials.items():
    data = shipped[name]
    assert data['model'] == model, name
    is_pinned = '*' not in inner and ',' not in inner
    assert ('model_reasoning_effort' in data) == is_pinned, name
    if is_pinned:
        assert data['model_reasoning_effort'] == inner, name
installer = scripts / 'install-agents.sh'

def snapshot(root):
    return sorted((str(p.relative_to(root)), 'link', str(p.readlink())) if p.is_symlink()
                  else (str(p.relative_to(root)), 'file', p.read_bytes()) if p.is_file()
                  else (str(p.relative_to(root)), 'other', '')
                  for p in root.rglob('*'))

def run_install(script, target, *args, ok=True, env=None, cwd=None):
    cmd = ['sh', str(script), '--target-dir', str(target), *args]
    result = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=cwd)
    assert (result.returncode == 0) == ok, (args, result.stdout, result.stderr)
    if not ok:
        assert 'ERROR:' in result.stderr, result.stderr
    return result

def install(target, *args, ok=True):
    return run_install(installer, target, *args, ok=ok)

with tempfile.TemporaryDirectory(prefix='codex-advisor-verify.') as tmp:
    root = Path(tmp)
    target = root / 'agents'
    install(target, '--check', ok=False)
    assert not target.exists()
    target.mkdir()
    (root / 'config.toml').write_text('model = "user-choice"\n')
    (target / 'sol-advisor-luna.toml').write_text('upstream installation\n')
    (target / 'unrelated.toml').write_text('unrelated agent\n')
    preserved = snapshot(root)
    missing_check = install(target, '--check', ok=False)
    assert snapshot(root) == preserved
    for filename in templates:
        assert str(target / filename) in missing_check.stderr
    first = install(target)
    assert first.stdout.count('INSTALLED:') == len(templates)
    assert 'UNCHANGED:' not in first.stdout
    for filename, content in templates.items():
        assert f'INSTALLED: {target / filename}' in first.stdout
        assert (target / filename).read_bytes() == content
    assert not list(target.glob('*.bak'))
    installed = snapshot(root)
    for state in preserved:
        assert state in installed
    repeat = install(target)
    assert repeat.stdout.count('UNCHANGED:') == len(templates)
    assert 'INSTALLED:' not in repeat.stdout
    assert 'REMOVED:' not in repeat.stdout
    matched = install(target, '--check')
    assert 'CHECK PASSED' in matched.stdout
    assert snapshot(root) == installed
    (target / sample_name).write_bytes(templates[sample_name] + b'changed\n')
    before = snapshot(root)
    drift = install(target, '--check', ok=False)
    assert str(target / sample_name) in drift.stderr
    assert snapshot(root) == before
    over = install(target)
    assert f'INSTALLED: {target / sample_name}' in over.stdout
    assert (target / sample_name).read_bytes() == templates[sample_name]
    for filename in templates:
        if filename != sample_name:
            assert f'UNCHANGED: {target / filename}' in over.stdout
    install(target, '--check')
    (target / sample_name).write_bytes(templates[sample_name] + b'x\n')
    (target / other_name).unlink()
    before = snapshot(root)
    listed = install(target, '--check', ok=False)
    assert str(target / sample_name) in listed.stderr
    assert str(target / other_name) in listed.stderr
    assert snapshot(root) == before
    install(target)
    (target / sample_name).write_bytes(templates[sample_name] + b'x\n')
    before = snapshot(root)
    install(target, '--check-role', other_stem)
    install(target, '--check-role', sample_stem, ok=False)
    install(target, '--check-role', sample_stem, '--check-role', sample_stem, ok=False)
    assert snapshot(root) == before
    install(target)
    installed = snapshot(root)
    for stem in stems:
        install(target, '--check-role', stem)
    for args in [('--check-role',), ('--check-role', 'unknown')]:
        install(target, *args, ok=False)
        assert snapshot(root) == installed
    copy = root / 'plugin-copy'
    (copy / 'scripts').mkdir(parents=True)
    (copy / 'agents').mkdir()
    shutil.copy2(installer, copy / 'scripts')
    for path in (plugin / 'agents').iterdir():
        if path.is_file() and not path.is_symlink():
            shutil.copy2(path, copy / 'agents')
    extra_name = 'codex-advisor-extra.toml'
    (copy / 'agents' / extra_name).write_text('name = "extra"\n')
    (copy / 'agents' / 'retire.txt').write_text('retired-agent.toml\nlegacy-extra.toml\n')
    copied = copy / 'scripts' / 'install-agents.sh'
    residue_target = root / 'residue-agents'
    residue_target.mkdir()
    copied_first = run_install(copied, residue_target)
    assert f'INSTALLED: {residue_target / extra_name}' in copied_first.stdout
    (residue_target / 'retired-agent.toml').write_text('old\n')
    (residue_target / 'legacy-extra.toml').write_text('old2\n')
    (residue_target / 'unrelated.toml').write_text('keep\n')
    before = snapshot(residue_target)
    residue_check = run_install(copied, residue_target, '--check', ok=False)
    assert str(residue_target / 'retired-agent.toml') in residue_check.stderr
    assert str(residue_target / 'legacy-extra.toml') in residue_check.stderr
    assert snapshot(residue_target) == before
    selective = run_install(copied, residue_target, '--check-role', sample_stem)
    assert 'CHECK PASSED' in selective.stdout
    assert snapshot(residue_target) == before
    removed = run_install(copied, residue_target)
    assert f'REMOVED: {residue_target / "retired-agent.toml"}' in removed.stdout
    assert f'REMOVED: {residue_target / "legacy-extra.toml"}' in removed.stdout
    assert not (residue_target / 'retired-agent.toml').exists()
    assert not (residue_target / 'legacy-extra.toml').exists()
    assert (residue_target / 'unrelated.toml').read_text() == 'keep\n'
    assert (residue_target / extra_name).read_text() == 'name = "extra"\n'
    run_install(copied, residue_target, '--check')
    default_home = root / 'default-home'
    default_home.mkdir()
    (default_home / 'config.toml').write_text('model = "user-choice"\n')
    result = subprocess.run(['sh', str(installer)],
                            env=dict(os.environ, CODEX_HOME=str(default_home)),
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (default_home / 'agents' / sample_name).read_bytes() == templates[sample_name]
    assert (default_home / 'config.toml').read_text() == 'model = "user-choice"\n'
    result = subprocess.run(['sh', str(installer), '--target-dir', 'relative'],
                            cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (root / 'relative' / sample_name).read_bytes() == templates[sample_name]
    for kind in ('symlink', 'directory', 'fifo'):
        unsafe = root / kind
        unsafe.mkdir()
        destination = unsafe / sample_name
        if kind == 'symlink':
            destination.symlink_to(root / 'absent')
        elif kind == 'directory':
            destination.mkdir()
        else:
            os.mkfifo(destination)
        before = snapshot(root)
        install(unsafe, ok=False)
        assert snapshot(root) == before
    mixed = root / 'mixed'
    mixed.mkdir()
    os.mkfifo(mixed / sample_name)
    before = snapshot(root)
    install(mixed, ok=False)
    assert snapshot(root) == before
    previous_install = root / 'previous-worker-install'
    previous_install.mkdir()
    (previous_install / worker_name).write_text('old worker\n')
    upgraded = install(previous_install)
    assert f'INSTALLED: {previous_install / worker_name}' in upgraded.stdout
    assert (previous_install / worker_name).read_bytes() == templates[worker_name]
    retire_names = [
        line.strip()
        for line in (plugin / 'agents' / 'retire.txt').read_text().splitlines()
        if line.strip() and not line.startswith('#')
    ]
    new_entries = sorted(templates)
    assert len(retire_names) == 8, retire_names
    assert len(new_entries) == expected_entries, new_entries
    assert all(name.startswith('ca-') and name.endswith('.toml') for name in new_entries)
    legacy_target = root / 'legacy-010'
    legacy_target.mkdir()
    for name in retire_names:
        (legacy_target / name).write_text('old\n')
    (legacy_target / 'unrelated-legacy.toml').write_text('keep\n')
    legacy_run = install(legacy_target)
    assert legacy_run.stdout.count('INSTALLED:') == expected_entries
    assert legacy_run.stdout.count('REMOVED:') == 8
    for name in new_entries:
        assert f'INSTALLED: {legacy_target / name}' in legacy_run.stdout
        assert (legacy_target / name).read_bytes() == templates[name]
    for name in retire_names:
        assert f'REMOVED: {legacy_target / name}' in legacy_run.stdout
        assert not (legacy_target / name).exists()
    leftover = sorted(p.name for p in legacy_target.iterdir())
    assert leftover == sorted(new_entries + ['unrelated-legacy.toml'])
    assert (legacy_target / 'unrelated-legacy.toml').read_text() == 'keep\n'
    install(legacy_target, '--check')
    retired_link_target = root / 'retired-symlink'
    retired_link_target.mkdir()
    retired_link_name = retire_names[0]
    (retired_link_target / retired_link_name).symlink_to(root / 'absent')
    before = snapshot(retired_link_target)
    retired_link = install(retired_link_target, ok=False)
    assert f'unsafe destination: {retired_link_target / retired_link_name}' in retired_link.stderr
    assert snapshot(retired_link_target) == before
    retired_link_check = install(retired_link_target, '--check', ok=False)
    assert f'residue: {retired_link_target / retired_link_name}' in retired_link_check.stderr
    assert snapshot(retired_link_target) == before
    link = root / 'linked-target'
    link.symlink_to(target, target_is_directory=True)
    before = snapshot(root)
    install(link, ok=False)
    install(link / 'nested', ok=False)
    install(root / 'config.toml' / 'nested', ok=False)
    install('/', ok=False)
    install('//', ok=False)
    install('///', ok=False)
    install(str(target) + '/./', ok=False)
    install(str(target) + '/../agents', ok=False)
    assert snapshot(root) == before
    missing_flag = subprocess.run(['sh', str(installer), '--target-dir'],
                                  capture_output=True, text=True)
    assert missing_flag.returncode != 0 and 'ERROR:' in missing_flag.stderr
print('PASS: fork metadata, overwrite, unchanged, retire, check drift/residue, preservation, refusals')
PY
fi
if [ "${1-}" != --installation ]; then
python3 - "$script_dir" <<'PY'
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib

scripts = Path(sys.argv[1])
plugin = scripts.parent
manifest = json.loads((plugin / '.codex-plugin/plugin.json').read_text())
inspector = scripts / 'inspect-agent-runtime.sh'
thread = '11111111-1111-7111-8111-111111111111'
parent = '00000000-0000-7000-8000-000000000000'
secret = 'DO_NOT_LEAK_PROMPT_OR_CREDENTIAL'
ALLOWLIST = {
    'thread_id', 'parent_thread_id', 'agent_role', 'agent_path',
    'model_provider', 'model', 'effort', 'sandbox_policy_type',
    'permission_profile_type', 'cwd',
}
RETIRED_AGENT_OPTIONS = (
    '--luna', '--sol-effort', '--astra-effort', '--explorer-effort',
    '--sol-explorer-effort', '--astra-explorer-effort', '--advisor-effort',
    '--reviewer-effort',
)
READONLY_TOKENS = ('explorer', 'advisor')

file_prefix = manifest['name'] + '-'
templates = []
for path in sorted((plugin / 'agents').glob('*.toml')):
    data = tomllib.loads(path.read_text())
    assert data['name'].startswith('ca_'), path.name
    role_part = path.name
    if role_part.startswith(file_prefix) and role_part.endswith('.toml'):
        role_part = role_part[len(file_prefix):-len('.toml')]
    if any(token in role_part for token in READONLY_TOKENS):
        assert data.get('sandbox_mode') == 'read-only', path.name
    templates.append((path, data))
assert templates

def dump(obj):
    return json.loads(json.dumps(obj))

def session_for(name):
    return {'type': 'session_meta', 'payload': {
        'id': thread, 'agent_role': name,
        'parent_thread_id': parent, 'model_provider': 'openai',
        'agent_path': '/root/agent', 'secret': secret}}

def turn_for(model, effort, sandbox='read-only', permission='legacy', cwd='/fixture'):
    return {'type': 'turn_context', 'payload': {
        'model': model, 'effort': effort,
        'sandbox_policy': {'type': sandbox},
        'permission_profile': {'type': permission},
        'cwd': cwd, 'prompt': secret}}

def role_args(name, effort=None):
    args = ['--agent', name]
    if effort is not None:
        args.extend(['--effort', effort])
    return args

with tempfile.TemporaryDirectory(prefix='codex-advisor-runtime-test.') as tmp:
    root = Path(tmp)
    rollout = root / f'rollout-fixture-{thread}.jsonl'

    def write(records):
        rollout.write_text('\n'.join(json.dumps(r) for r in records) + '\n')

    def run_inspect(*args, thread_id=thread, sessions=True):
        cmd = ['sh', str(inspector)]
        if sessions:
            cmd.extend(['--sessions-dir', str(root)])
        cmd.extend(args)
        if thread_id is not None:
            cmd.append(thread_id)
        return subprocess.run(cmd, capture_output=True, text=True)

    def inspect(*args, ok=True, reason=''):
        result = run_inspect(*args)
        blob = result.stdout + result.stderr
        assert secret not in blob, (reason, blob)
        assert (result.returncode == 0) == ok, (reason or args, result.stdout, result.stderr)
        if not ok:
            assert not result.stdout and 'ERROR:' in result.stderr, (reason, result.stdout, result.stderr)
            return result
        evidence = json.loads(result.stdout)
        assert set(evidence) == ALLOWLIST, (reason, evidence)
        return evidence

    for option in RETIRED_AGENT_OPTIONS:
        result = run_inspect(option)
        assert result.returncode != 0 and not result.stdout
        assert 'ERROR:' in result.stderr and '--agent' in result.stderr, result.stderr
        assert secret not in result.stdout + result.stderr
    for option in ('--review-primary-effort', '--select-review-effort'):
        result = run_inspect(option)
        assert result.returncode != 0 and not result.stdout
        assert 'retired' in result.stderr and '--agent' in result.stderr, result.stderr

    names = [data['name'] for _, data in templates]
    for path, data in templates:
        name = data['name']
        model = data['model']
        pinned = data.get('model_reasoning_effort')
        expected_effort = pinned if pinned else 'high'
        cli_effort = None if pinned else expected_effort
        other = next(n for n in names if n != name)
        session = session_for(name)
        turn = turn_for(model, expected_effort)
        write([session, turn, {'type': 'response_item', 'payload': {'text': secret}}])
        evidence = inspect(*role_args(name, cli_effort), reason=f'accepted {name}')
        assert evidence['model'] == model and evidence['effort'] == expected_effort
        assert evidence['agent_role'] == name
        assert evidence['sandbox_policy_type'] == 'read-only'
        if pinned:
            evidence = inspect(*role_args(name, pinned), reason=f'equal pin {name}')
            assert evidence['effort'] == pinned
            pin_mismatch = 'high' if pinned != 'high' else 'low'
            inspect(*role_args(name, pin_mismatch), ok=False, reason=f'effort pin mismatch {name}')
        else:
            inspect(*role_args(name), ok=False, reason=f'missing effort {name}')
            write([session, turn_for(model, 'ultra')])
            evidence = inspect(*role_args(name, 'ultra'), reason=f'any effort {name}')
            assert evidence['effort'] == 'ultra'
        bad = dump(turn)
        bad['payload']['model'] = 'not-the-expected-model'
        write([session, bad])
        inspect(*role_args(name, cli_effort), ok=False,
                reason=f'mismatched model must be rejected for {name}')
        bad = dump(turn)
        bad['payload']['effort'] = 'not-the-expected-effort'
        write([session, bad])
        inspect(*role_args(name, cli_effort), ok=False,
                reason=f'mismatched effort must be rejected for {name}')
        bad_session = dump(session)
        bad_session['payload']['agent_role'] = other
        write([bad_session, turn])
        inspect(*role_args(name, cli_effort), ok=False,
                reason=f'mismatched agent role must be rejected for {name}')
        missing = dump(turn)
        del missing['payload']['sandbox_policy']
        write([session, missing])
        inspect(*role_args(name, cli_effort), ok=False, reason=f'missing sandbox {name}')
        conflict = dump(turn)
        conflict['payload']['sandbox_policy'] = {'type': 'workspace-write'}
        write([session, turn, conflict])
        inspect(*role_args(name, cli_effort), ok=False, reason=f'conflicting sandbox {name}')
        missing = dump(turn)
        del missing['payload']['permission_profile']
        write([session, missing])
        inspect(*role_args(name, cli_effort), ok=False, reason=f'missing permission {name}')
        conflict = dump(turn)
        conflict['payload']['permission_profile'] = {'type': 'disabled'}
        write([session, turn, conflict])
        inspect(*role_args(name, cli_effort), ok=False, reason=f'conflicting permission {name}')
        for value in (None, '', 'not-a-thread'):
            missing_parent = dump(session)
            missing_parent['payload']['parent_thread_id'] = value
            write([missing_parent, turn])
            inspect(*role_args(name, cli_effort), ok=False,
                    reason=f'invalid parent {name} {value!r}')
        missing = dump(turn)
        del missing['payload']['cwd']
        write([session, missing])
        inspect(*role_args(name, cli_effort), ok=False, reason=f'missing cwd {name}')
        observed = dump(turn)
        observed['payload']['sandbox_policy'] = {'type': 'danger-full-access'}
        observed['payload']['permission_profile'] = {'type': 'disabled'}
        write([session, observed])
        evidence = inspect(*role_args(name, cli_effort), reason=f'echo sandbox {name}')
        assert evidence['sandbox_policy_type'] == 'danger-full-access'
        assert evidence['permission_profile_type'] == 'disabled'

    generic_session = session_for('unrelated-role')
    generic_turn = turn_for('some-model', 'low')
    write([generic_session, generic_turn])
    evidence = inspect(reason='generic evidence')
    assert evidence['agent_role'] == 'unrelated-role'
    assert evidence['model'] == 'some-model' and evidence['effort'] == 'low'
    inspect('--effort', 'high', ok=False, reason='effort without agent')
    sample = templates[0][1]
    inspect('--agent', sample['name'], '--effort', '', ok=False, reason='empty effort')
    inspect('--agent', sample['name'], '--effort', '--high', ok=False, reason='effort starts with --')
    inspect('--agent', 'nonexistent', ok=False, reason='unknown agent')

    sample = templates[0][1]
    sample_name = sample['name']
    pinned = sample.get('model_reasoning_effort')
    sample_effort = pinned if pinned else 'high'
    sample_args = role_args(sample_name, None if pinned else sample_effort)
    session = session_for(sample_name)
    turn = turn_for(sample['model'], sample_effort)
    for records in ([], [session], [turn], [session, session, turn]):
        write(records)
        inspect(*sample_args, ok=False, reason='malformed records')
    rollout.write_text('{"prompt":"' + secret + '",broken')
    inspect(ok=False, reason='malformed json')
    write([session, turn])
    duplicate = root / f'rollout-other-{thread}.jsonl'
    duplicate.write_bytes(rollout.read_bytes())
    inspect(ok=False, reason='two rollouts')
    duplicate.unlink()
    rollout.unlink()
    inspect(ok=False, reason='missing rollout')
    bad = subprocess.run(['sh', str(inspector), '../invalid'],
                         capture_output=True, text=True)
    assert bad.returncode != 0 and not bad.stdout
print('PASS: generic inspector, table-driven templates, retired options, payload filtering')
PY
fi
for script in "$script_dir"/*.sh; do sh -n "$script"; done
printf '%s\n' 'VERIFY PASSED: selected deterministic checks (no live routing claim)'
