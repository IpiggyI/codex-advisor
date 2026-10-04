#!/bin/sh
# Exercise the public installer with disposable destinations.
set -eu
script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd)
repo_root=$(CDPATH= cd "$script_dir/.." && pwd)
plugin_scripts="$repo_root/plugins/codex-advisor/scripts"
case "${1-}" in ''|--installation|--runtime|--consultation|--hooks) ;; *) printf '%s\n' 'Unknown verification group' >&2; exit 2 ;; esac
if [ -z "${1-}" ] || [ "${1-}" = --installation ]; then
sh "$plugin_scripts/run-python.sh" - "$plugin_scripts" <<'PY'
import json
import os
from pathlib import Path
import re
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
shipped = {}
for filename, content in templates.items():
    data = tomllib.loads(content.decode())
    shipped[data['name']] = data

# Pin model_reasoning_effort exactly when the routing profile marks a single
# bare effort. Source: plugins/codex-advisor/skills/orchestration/references/routing-profile.md
profile = (plugin / 'skills/orchestration/references/routing-profile.md').read_text()
name_re = re.compile(r'`(ca_[a-z0-9_]+)`')
dial_re = re.compile(r'`(ca_[a-z0-9_]+)`\s+(gpt-[^\s\[]+)\[([^\]]+)\]')

def parse_profile(text):
    table_names = []
    table_dials = {}
    for line in text.splitlines():
        if not line.lstrip().startswith('|'):
            continue
        table_names.extend(name_re.findall(line))
        for match in dial_re.finditer(line):
            name = match.group(1)
            assert name not in table_dials, name
            table_dials[name] = (match.group(2), match.group(3).strip())
    assert len(table_names) == len(set(table_names)), table_names
    return set(table_names), table_dials

def require_profile_templates(profile_text, template_data):
    profile_set, table_dials = parse_profile(profile_text)
    shipped_set = set(template_data)
    assert len(profile_set) == 17, sorted(profile_set)
    assert profile_set == shipped_set, sorted(profile_set ^ shipped_set)
    assert set(table_dials) == shipped_set, sorted(set(table_dials) ^ shipped_set)
    for name, (model, inner) in table_dials.items():
        data = template_data[name]
        assert data['model'] == model, name
        is_pinned = '*' not in inner and ',' not in inner
        assert ('model_reasoning_effort' in data) == is_pinned, name
        if is_pinned:
            assert data['model_reasoning_effort'] == inner, name

require_profile_templates(profile, shipped)
profile_set, table_dials = parse_profile(profile)
expected_entries = len(profile_set)
sys.path.insert(0, str(scripts))
from consult_context import advisor_dial, load_profile
routing = load_profile(plugin)

def assigned_advisor(name):
    # The advisor model an Explorer or Worker entry consults at every effort its cell allows.
    model, inner = table_dials[name]
    advisors = {advisor_dial(routing, model, effort.strip().rstrip('*'), name.split('_')[2])[0]
                for effort in inner.split(',')}
    assert len(advisors) == 1, name
    return advisors.pop()

canonical = (plugin / 'skills/orchestration/references/consult-posture.md').read_text()
section_re = re.compile(r'\n<!-- process-consultation:start -->\n.*?\n<!-- process-consultation:end -->\n', re.S)

def posture_block(variant):
    return re.search(r'<!-- consult-posture:' + variant + r':start -->.*?<!-- consult-posture:' + variant + r':end -->', canonical, re.S)[0]

def require_postures(entries):
    by_role = {}
    for name, data in entries.items():
        role = name.split('_')[1]
        body = data['developer_instructions']
        sections = section_re.findall(body)
        if role == 'advisor':
            assert not sections and 'consult-posture:' not in body, name
        else:
            variant = 'reduced' if data['model'] == assigned_advisor(name) else 'full'
            expected = ('\n<!-- process-consultation:start -->\n' + posture_block(variant) +
                        '\n\n' + posture_block('adoption') + '\n<!-- process-consultation:end -->\n')
            assert sections == [expected], name
        outside = section_re.sub('', body)
        assert 'consult-posture:' not in outside and 'process-consultation:' not in outside, name
        by_role.setdefault(role, []).append(outside)
    for role, bodies in by_role.items():
        assert all(body == bodies[0] for body in bodies), role

require_postures(shipped)
full_name = next(name for name, data in shipped.items() if name.startswith('ca_worker_') and
                 data['model'] != assigned_advisor(name))
advisor_name = next(name for name in shipped if name.startswith('ca_advisor_'))
for mutation in ('one-character', 'wrong-variant', 'advisor-section'):
    changed = {name: dict(data) for name, data in shipped.items()}
    body = changed[full_name]['developer_instructions']
    if mutation == 'one-character':
        changed[full_name]['developer_instructions'] = body.replace(posture_block('full'), posture_block('full') + 'x')
    elif mutation == 'wrong-variant':
        changed[full_name]['developer_instructions'] = body.replace(posture_block('full'), posture_block('reduced'))
    else:
        changed[advisor_name]['developer_instructions'] += section_re.findall(body)[0]
    try:
        require_postures(changed)
    except AssertionError:
        pass
    else:
        raise AssertionError('posture check accepted ' + mutation)
print('PASS: canonical posture, advisor exclusion, outside-section identity, three negative posture fixtures')
canonical = (repo / 'docs/zh/skills/orchestration/references/consult-posture.md').read_text()
twins = {data['name']: data for path in (repo / 'docs/zh/agents').glob('*.toml')
         for data in [tomllib.loads(path.read_text())]}
require_postures(twins)

mutated_shipped = {name: dict(data) for name, data in shipped.items()}
mutated_name = sorted(mutated_shipped)[0]
mutated_shipped[mutated_name]['model'] = 'fixture-wrong-model'
try:
    require_profile_templates(profile, mutated_shipped)
except AssertionError:
    pass
else:
    raise AssertionError('profile check accepted a template with the wrong model')
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
    former_target = root / 'former-entries'
    former_target.mkdir()
    for name in ('codex-advisor-luna-explorer.toml', 'ca-worker-light.toml'):
        (former_target / name).write_text('old\n')
    (former_target / 'ca-advisor-senior.toml').symlink_to(root / 'absent')
    (former_target / 'unrelated-legacy.toml').write_text('keep\n')
    kept = snapshot(former_target)
    former_run = install(former_target)
    assert former_run.stdout.count('INSTALLED:') == expected_entries
    assert 'REMOVED:' not in former_run.stdout
    assert [state for state in snapshot(former_target) if state[0] not in templates] == kept
    install(former_target, '--check')
    assert sorted(p.name for p in (plugin / 'agents').iterdir()) == sorted(templates)
    usage = subprocess.run(['sh', str(installer), '--help'], capture_output=True, text=True)
    assert usage.returncode == 0, usage.stderr
    assert ("overwrite this plugin's own files and leave everything else untouched."
            in ' '.join(usage.stdout.split())), usage.stdout
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
print('PASS: profile/template equality, negative model fixture')
print('PASS: fork metadata, overwrite, unchanged, check drift, former names and unrelated files untouched, refusals')
PY
fi
if [ -z "${1-}" ] || [ "${1-}" = --runtime ]; then
sh "$plugin_scripts/run-python.sh" - "$plugin_scripts" <<'PY'
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
FORMER_OPTIONS = (
    '--luna', '--sol-effort', '--astra-effort', '--explorer-effort',
    '--sol-explorer-effort', '--astra-explorer-effort', '--advisor-effort',
    '--reviewer-effort', '--review-primary-effort', '--select-review-effort',
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

    for option in FORMER_OPTIONS:
        result = run_inspect(option)
        assert result.returncode != 0 and not result.stdout
        assert result.stderr == 'ERROR: unknown argument.\n', result.stderr

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
print('PASS: generic inspector, table-driven templates, former options as unknown arguments, payload filtering')
PY
fi
for script in "$plugin_scripts"/*.sh "$script_dir"/*.sh; do sh -n "$script"; done
if [ -z "${1-}" ] || [ "${1-}" = --consultation ]; then
    sh "$plugin_scripts/run-python.sh" "$script_dir/verify-consultation.py"
    sh "$plugin_scripts/run-python.sh" "$script_dir/verify-consultation-lifecycle.py"
    sh "$plugin_scripts/run-python.sh" "$script_dir/verify-consultation-limits.py"
    sh "$plugin_scripts/run-python.sh" "$script_dir/verify-consultation-native.py"
    sh "$plugin_scripts/run-python.sh" "$script_dir/verify-consultation-process.py"
fi
if [ -z "${1-}" ] || [ "${1-}" = --hooks ]; then
    sh "$plugin_scripts/run-python.sh" "$script_dir/verify-hooks.py"
    sh "$plugin_scripts/run-python.sh" "$script_dir/verify-routing.py"
fi
printf '%s\n' 'VERIFY PASSED: selected deterministic checks (no live routing claim)'
