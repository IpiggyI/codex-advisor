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
role_files = {'advisor': 'codex-advisor-astra-advisor.toml',
              'luna': 'codex-advisor-luna-implementer.toml',
              'explorer': 'codex-advisor-luna-explorer.toml',
              'sol-explorer': 'codex-advisor-sol-explorer.toml',
              'astra-explorer': 'codex-advisor-astra-explorer.toml',
              'astra': 'codex-advisor-astra-implementer.toml',
              'sol': 'codex-advisor-sol-implementer.toml',
              'reviewer': 'codex-advisor-astra-reviewer.toml'}
assert set(templates) == set(role_files.values())
for filename, content in templates.items():
    data = tomllib.loads(content.decode())
    assert filename.startswith('codex-advisor-')
    assert data['name'].startswith('codex_advisor_')
    assert data['description'] and data['developer_instructions']

def snapshot(root):
    return sorted((str(p.relative_to(root)), 'link', str(p.readlink())) if p.is_symlink()
                  else (str(p.relative_to(root)), 'file', p.read_bytes()) if p.is_file()
                  else (str(p.relative_to(root)), 'other', '')
                  for p in root.rglob('*'))

def install(target, *args, ok=True):
    result = subprocess.run(['sh', str(scripts / 'install-agents.sh'),
                             '--target-dir', str(target), *args], capture_output=True, text=True)
    assert (result.returncode == 0) == ok, (args, result.stdout, result.stderr)
    if not ok:
        assert 'ERROR:' in result.stderr, result.stderr
    return result

with tempfile.TemporaryDirectory(prefix='codex-advisor-verify.') as tmp:
    root = Path(tmp)
    target = root / 'agents'
    install(target, '--check', ok=False)
    assert not target.exists()
    target.mkdir()
    (root / 'config.toml').write_text('model = "user-choice"\n')
    (target / 'sol-advisor-luna-implementer.toml').write_text('upstream installation\n')
    (target / 'unrelated.toml').write_text('unrelated agent\n')
    preserved = snapshot(root)
    install(target)
    assert (target / 'codex-advisor-astra-implementer.toml').is_file(), 'full installation must include Astra implementation'
    install(target, '--check-role', 'astra')
    for filename, content in templates.items():
        assert (target / filename).read_bytes() == content
    installed = snapshot(root)
    for state in preserved:
        assert state in installed
    install(target)
    install(target, '--check')
    install(target, '--check-role', 'advisor', '--check-role', 'advisor')
    assert snapshot(root) == installed
    roles = list(role_files)
    for role in roles:
        install(target, '--check-role', role)
    for args in [('--check-role',), ('--check-role', 'unknown')]:
        install(target, *args, ok=False)
        assert snapshot(root) == installed
    for role, filename in role_files.items():
        (target / filename).write_bytes(templates[filename] + b'changed\n')
        before = snapshot(root)
        install(target, '--check-role', role, ok=False)
        for other in roles:
            if other != role:
                install(target, '--check-role', other)
        install(target, '--check', ok=False)
        install(target, ok=False)
        assert snapshot(root) == before
        (target / filename).write_bytes(templates[filename])
    for role in ('advisor', 'astra'):
        filename = role_files[role]
        (target / filename).unlink()
        before = snapshot(root)
        install(target, '--check-role', role, ok=False)
        assert snapshot(root) == before
        install(target)
    default_home = root / 'default-home'
    default_home.mkdir()
    (default_home / 'config.toml').write_text('model = "user-choice"\n')
    result = subprocess.run(['sh', str(scripts / 'install-agents.sh')],
                            env=dict(os.environ, CODEX_HOME=str(default_home)),
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (default_home / 'agents' / filename).read_bytes() == templates[filename]
    assert (default_home / 'config.toml').read_text() == 'model = "user-choice"\n'
    result = subprocess.run(['sh', str(scripts / 'install-agents.sh'), '--target-dir', 'relative'],
                            cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (root / 'relative' / filename).read_bytes() == templates[filename]
    for kind in ('modified', 'symlink', 'directory', 'fifo'):
        unsafe = root / kind
        unsafe.mkdir()
        destination = unsafe / filename
        if kind == 'modified':
            destination.write_text('conflict\n')
        elif kind == 'symlink':
            destination.symlink_to(root / 'absent')
        elif kind == 'directory':
            destination.mkdir()
        else:
            os.mkfifo(destination)
        before = snapshot(root)
        install(unsafe, ok=False)
        assert snapshot(root) == before
    for role, filename in role_files.items():
        partial = root / ('partial-' + role)
        partial.mkdir()
        (partial / filename).write_text('conflict\n')
        before = snapshot(root)
        install(partial, ok=False)
        assert snapshot(root) == before, 'preflight must precede every role write'
    previous_install = root / 'previous-sol-install'
    previous_install.mkdir()
    previous_description = ('description = "Direct implementation of judgment-heavy, '
                            'context-heavy, or higher-risk work from an Astra architect\'s complete specification."')
    sol_filename = role_files['sol']
    previous_sol = '\n'.join(previous_description if line.startswith('description = ')
                             else line for line in templates[sol_filename].decode().splitlines()) + '\n'
    assert tomllib.loads(previous_sol)['model'] == 'gpt-5.6-sol'
    (previous_install / sol_filename).write_text(previous_sol)
    before = snapshot(root)
    refusal = install(previous_install, ok=False)
    assert 'modified or conflicting destination:' in refusal.stderr
    assert sol_filename in refusal.stderr
    assert snapshot(root) == before, 'old Sol must block upgrade before Astra or any other role is installed'
    link = root / 'linked-target'
    link.symlink_to(target, target_is_directory=True)
    before = snapshot(root)
    install(link, ok=False)
    install(link / 'nested', ok=False)
    install(root / 'config.toml' / 'nested', ok=False)
    install('/', ok=False)
    install('//', ok=False)
    install('///', ok=False)
    assert snapshot(root) == before
print('PASS: fork metadata, clean/repeat install, non-mutating selective checks, refusal and preservation')
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
role = scripts.parent / 'agents/codex-advisor-astra-advisor.toml'
data = tomllib.loads(role.read_text())
assert data['name'] == 'codex_advisor_astra_advisor'
assert data['model'] == 'gpt-6-astra'
assert 'model_reasoning_effort' not in data, 'role defaults would override explicit spawn effort'
assert data['sandbox_mode'] == 'read-only'
reviewer = tomllib.loads((scripts.parent / 'agents/codex-advisor-astra-reviewer.toml').read_text())
assert reviewer['name'] == 'codex_advisor_astra_reviewer'
assert reviewer['model'] == 'gpt-6-astra'
assert 'model_reasoning_effort' not in reviewer, 'a fixed effort would override caller selection'
assert reviewer['sandbox_mode'] == 'read-only'
def obsolete_review(*args):
    result = subprocess.run(['sh', str(scripts / 'inspect-agent-runtime.sh'),
                             '--select-review-effort', *args], capture_output=True, text=True)
    assert result.returncode != 0 and not result.stdout
    assert 'retired' in result.stderr and '--reviewer-effort' in result.stderr, result
obsolete_review('--review-primary-effort', 'max')
obsolete_review('--reviewer-effort', 'medium')
thread = '11111111-1111-7111-8111-111111111111'
secret = 'DO_NOT_LEAK_PROMPT_OR_CREDENTIAL'
session = {'type': 'session_meta', 'payload': {
    'id': thread, 'agent_role': 'codex_advisor_astra_advisor',
    'parent_thread_id': '00000000-0000-7000-8000-000000000000',
    'model_provider': 'openai', 'agent_path': '/root/advisor', 'secret': secret}}
turn = {'type': 'turn_context', 'payload': {
    'model': 'gpt-6-astra', 'effort': 'high', 'sandbox_policy': {'type': 'read-only'},
    'permission_profile': {'type': 'legacy'}, 'cwd': '/fixture', 'prompt': secret}}

with tempfile.TemporaryDirectory(prefix='codex-advisor-runtime-test.') as tmp:
    root = Path(tmp)
    rollout = root / f'rollout-fixture-{thread}.jsonl'
    def write(records):
        rollout.write_text('\n'.join(json.dumps(r) for r in records) + '\n')
    def inspect(*args, ok=True):
        result = subprocess.run(['sh', str(scripts / 'inspect-agent-runtime.sh'),
                                 '--sessions-dir', str(root), *args, thread],
                                capture_output=True, text=True)
        assert (result.returncode == 0) == ok, (args, result.stdout, result.stderr)
        assert secret not in result.stdout + result.stderr
        if not ok:
            assert not result.stdout and 'ERROR:' in result.stderr
        return json.loads(result.stdout) if ok else None
    def reject_efforts(session_record, turn_record, option, efforts):
        for effort in efforts:
            turn_record['payload']['effort'] = effort
            write([session_record, turn_record])
            inspect(option, effort, ok=False)
    for effort in ('medium', 'high', 'xhigh'):
        turn['payload']['effort'] = effort
        write([session, turn, {'type': 'response_item', 'payload': {'text': secret}}])
        evidence = inspect('--advisor-effort', effort)
        assert evidence['model'] == 'gpt-6-astra' and evidence['effort'] == effort
        assert evidence['agent_role'] == 'codex_advisor_astra_advisor'
        assert evidence['sandbox_policy_type'] == 'read-only'
        assert set(evidence) == {'thread_id', 'parent_thread_id', 'agent_role', 'agent_path',
                                 'model_provider', 'model', 'effort', 'sandbox_policy_type',
                                 'permission_profile_type', 'cwd'}
    reject_efforts(session, turn, '--advisor-effort', ('low', 'max', 'ultra'))
    turn['payload']['effort'] = 'high'
    turn['payload']['sandbox_policy']['type'] = 'danger-full-access'
    turn['payload']['permission_profile']['type'] = 'disabled'
    write([session, turn])
    evidence = inspect('--advisor-effort', 'high')
    assert evidence['sandbox_policy_type'] == 'danger-full-access'
    assert evidence['permission_profile_type'] == 'disabled'
    inspect('--advisor-effort', 'medium', ok=False)
    inspect('--advisor-effort', 'unsupported', ok=False)
    for field in ('model', 'effort', 'sandbox_policy', 'permission_profile', 'cwd'):
        missing = json.loads(json.dumps(turn))
        del missing['payload'][field]
        write([session, missing])
        inspect('--advisor-effort', 'high', ok=False)
    for value in (None, '', 'not-a-thread'):
        missing_parent = json.loads(json.dumps(session))
        missing_parent['payload']['parent_thread_id'] = value
        write([missing_parent, turn])
        inspect('--advisor-effort', 'high', ok=False)
    for field, wrong in [('model', 'gpt-5.6-sol'), ('effort', 'low'),
                         ('sandbox_policy', {'type': 'read-only'}),
                         ('permission_profile', {'type': 'legacy'}), ('cwd', '/other')]:
        conflicting = json.loads(json.dumps(turn))
        conflicting['payload'][field] = wrong
        write([session, turn, conflicting])
        inspect('--advisor-effort', 'high', ok=False)
    wrong_role = json.loads(json.dumps(session))
    wrong_role['payload']['agent_role'] = 'unrelated'
    write([wrong_role, turn])
    inspect('--advisor-effort', 'high', ok=False)
    wrong_model = json.loads(json.dumps(turn))
    wrong_model['payload']['model'] = 'gpt-5.6-sol'
    write([session, wrong_model])
    inspect('--advisor-effort', 'high', ok=False)
    luna_role = tomllib.loads((scripts.parent / 'agents/codex-advisor-luna-implementer.toml').read_text())
    assert luna_role['name'] == 'codex_advisor_luna_implementer'
    assert luna_role['model'] == 'gpt-5.6-luna'
    assert luna_role['model_reasoning_effort'] == 'max'
    luna_session = json.loads(json.dumps(session))
    luna_session['payload']['agent_role'] = 'codex_advisor_luna_implementer'
    luna_turn = json.loads(json.dumps(turn))
    luna_turn['payload'].update(model='gpt-5.6-luna', effort='max')
    write([luna_session, luna_turn])
    evidence = inspect('--luna')
    assert evidence['model'] == 'gpt-5.6-luna' and evidence['effort'] == 'max'
    inspect('--luna', '--advisor-effort', 'high', ok=False)
    for field, wrong in [('model', 'gpt-6-astra'), ('effort', 'high'),
                         ('sandbox_policy', None), ('permission_profile', None)]:
        invalid = json.loads(json.dumps(luna_turn))
        invalid['payload'][field] = wrong
        write([luna_session, invalid])
        inspect('--luna', ok=False)
    write([session, luna_turn])
    inspect('--luna', ok=False)
    write([luna_session, luna_turn, turn])
    inspect('--luna', ok=False)
    explorer_role = tomllib.loads((scripts.parent / 'agents/codex-advisor-luna-explorer.toml').read_text())
    assert explorer_role['name'] == 'codex_advisor_luna_explorer'
    assert explorer_role['model'] == 'gpt-5.6-luna'
    assert 'model_reasoning_effort' not in explorer_role, 'Explorer effort belongs to the caller'
    assert explorer_role['sandbox_mode'] == 'read-only'
    explorer_session = json.loads(json.dumps(session))
    explorer_session['payload']['agent_role'] = 'codex_advisor_luna_explorer'
    explorer_turn = json.loads(json.dumps(turn))
    explorer_turn['payload']['model'] = 'gpt-5.6-luna'
    for effort in ('high', 'max'):
        explorer_turn['payload']['effort'] = effort
        write([explorer_session, explorer_turn])
        evidence = inspect('--explorer-effort', effort)
        assert evidence['model'] == 'gpt-5.6-luna' and evidence['effort'] == effort
        assert evidence['agent_role'] == 'codex_advisor_luna_explorer'
        assert evidence['sandbox_policy_type'] == 'danger-full-access'
        assert evidence['permission_profile_type'] == 'disabled'
        assert set(evidence) == {'thread_id', 'parent_thread_id', 'agent_role', 'agent_path',
                                 'model_provider', 'model', 'effort', 'sandbox_policy_type',
                                 'permission_profile_type', 'cwd'}
    reject_efforts(explorer_session, explorer_turn, '--explorer-effort', ('low', 'medium', 'xhigh', 'ultra'))
    explorer_turn['payload']['effort'] = 'high'
    write([explorer_session, explorer_turn])
    for args in [('--explorer-effort', 'max'), ('--explorer-effort', 'unsupported'),
                 ('--explorer-effort', ''), ('--explorer-effort',),
                 ('--explorer-effort', 'high', '--luna'),
                 ('--explorer-effort', 'high', '--sol-effort', 'high'),
                 ('--advisor-effort', 'high', '--explorer-effort', 'high'),
                 ('--explorer-effort', 'high', '--review-primary-effort', 'low')]:
        inspect(*args, ok=False)
    for other_session in (session, luna_session, wrong_role):
        write([other_session, explorer_turn])
        inspect('--explorer-effort', 'high', ok=False)
    for field, wrong in [('model', 'gpt-6-astra'), ('effort', 'max'),
                         ('sandbox_policy', {'type': 'read-only'}),
                         ('permission_profile', {'type': 'legacy'})]:
        missing = json.loads(json.dumps(explorer_turn))
        del missing['payload'][field]
        write([explorer_session, missing])
        inspect('--explorer-effort', 'high', ok=False)
        conflicting = json.loads(json.dumps(explorer_turn))
        conflicting['payload'][field] = wrong
        write([explorer_session, explorer_turn, conflicting])
        inspect('--explorer-effort', 'high', ok=False)
    invalid_explorer = json.loads(json.dumps(explorer_turn))
    invalid_explorer['payload']['model'] = 'gpt-6-astra'
    write([explorer_session, invalid_explorer])
    inspect('--explorer-effort', 'high', ok=False)
    for model_name, model in (('sol', 'gpt-5.6-sol'), ('astra', 'gpt-6-astra')):
        native_role = f'codex_advisor_{model_name}_explorer'
        config = tomllib.loads((scripts.parent / f'agents/codex-advisor-{model_name}-explorer.toml').read_text())
        assert config['name'] == native_role and config['model'] == model
        assert config['sandbox_mode'] == 'read-only' and 'model_reasoning_effort' not in config
        allocated_session = json.loads(json.dumps(session))
        allocated_session['payload']['agent_role'] = native_role
        allocated_turn = json.loads(json.dumps(turn))
        allocated_turn['payload']['model'] = model
        option = f'--{model_name}-explorer-effort'
        for effort in ('medium', 'high', 'low', 'xhigh', 'max', 'ultra'):
            allocated_turn['payload']['effort'] = effort
            write([allocated_session, allocated_turn])
            evidence = inspect(option, effort, ok=effort in ('medium', 'high'))
            if evidence:
                assert evidence['agent_role'] == native_role and evidence['model'] == model
                assert evidence['effort'] == effort
        allocated_turn['payload']['effort'] = 'medium'
        worker_session = json.loads(json.dumps(allocated_session))
        worker_session['payload']['agent_role'] = f'codex_advisor_{model_name}_implementer'
        write([worker_session, allocated_turn])
        inspect(option, 'medium', ok=False)
        for field in ('model', 'effort', 'sandbox_policy', 'permission_profile'):
            missing = json.loads(json.dumps(allocated_turn))
            del missing['payload'][field]
            write([allocated_session, missing])
            inspect(option, 'medium', ok=False)
        write([allocated_session, allocated_turn])
        inspect(option, 'medium', '--luna', ok=False)
    sol_role = tomllib.loads((scripts.parent / 'agents/codex-advisor-sol-implementer.toml').read_text())
    assert sol_role['name'] == 'codex_advisor_sol_implementer'
    assert sol_role['model'] == 'gpt-5.6-sol'
    assert 'model_reasoning_effort' not in sol_role, 'Sol effort must remain adjustable at invocation'
    sol_session = json.loads(json.dumps(session))
    sol_session['payload']['agent_role'] = 'codex_advisor_sol_implementer'
    sol_turn = json.loads(json.dumps(turn))
    sol_turn['payload']['model'] = 'gpt-5.6-sol'
    for effort in ('high', 'xhigh'):
        sol_turn['payload']['effort'] = effort
        write([sol_session, sol_turn])
        evidence = inspect('--sol-effort', effort)
        assert evidence['model'] == 'gpt-5.6-sol' and evidence['effort'] == effort
        assert evidence['agent_role'] == 'codex_advisor_sol_implementer'
    reject_efforts(sol_session, sol_turn, '--sol-effort', ('low', 'medium', 'max', 'ultra'))
    sol_turn['payload']['effort'] = 'high'
    write([sol_session, sol_turn])
    for args in [('--sol-effort', 'medium'), ('--sol-effort', 'unsupported'),
                 ('--sol-effort', ''), ('--sol-effort',),
                 ('--sol-effort', 'high', '--luna'),
                 ('--advisor-effort', 'high', '--sol-effort', 'high'),
                 ('--sol-effort', 'high', '--review-primary-effort', 'low')]:
        inspect(*args, ok=False)
    for other_session in (session, luna_session, wrong_role):
        write([other_session, sol_turn])
        inspect('--sol-effort', 'high', ok=False)
    for field, wrong in [('model', 'gpt-5.6-luna'), ('effort', 'low'),
                         ('sandbox_policy', {'type': 'read-only'}),
                         ('permission_profile', {'type': 'legacy'})]:
        missing = json.loads(json.dumps(sol_turn))
        del missing['payload'][field]
        write([sol_session, missing])
        inspect('--sol-effort', 'high', ok=False)
        conflicting = json.loads(json.dumps(sol_turn))
        conflicting['payload'][field] = wrong
        write([sol_session, sol_turn, conflicting])
        inspect('--sol-effort', 'high', ok=False)
    invalid_sol = json.loads(json.dumps(sol_turn))
    invalid_sol['payload']['model'] = 'gpt-5.6-luna'
    write([sol_session, invalid_sol])
    inspect('--sol-effort', 'high', ok=False)
    review_session = json.loads(json.dumps(session))
    review_session['payload']['agent_role'] = 'codex_advisor_astra_reviewer'
    review_turn = json.loads(json.dumps(turn))
    for effort in ('medium', 'high', 'xhigh', 'low', 'max', 'ultra'):
        review_turn['payload']['effort'] = effort
        write([review_session, review_turn])
        evidence = inspect('--reviewer-effort', effort, ok=effort in ('medium', 'high', 'xhigh'))
        if evidence:
            assert evidence['agent_role'] == 'codex_advisor_astra_reviewer'
            assert evidence['model'] == 'gpt-6-astra' and evidence['effort'] == effort
    review_turn['payload']['effort'] = 'high'
    write([review_session, review_turn])
    inspect('--review-primary-effort', 'max', ok=False)
    inspect('--review-primary-effort', 'low', '--reviewer-effort', 'medium', ok=False)
    inspect('--reviewer-effort', 'high')
    inspect('--reviewer-effort', 'high', '--reviewer-effort', 'high', ok=False)
    inspect('--reviewer-effort', 'high', '--advisor-effort', 'high', ok=False)
    inspect('--reviewer-effort', 'high', '--luna', ok=False)
    inspect('--reviewer-effort', 'medium', ok=False)
    inspect('--luna', '--review-primary-effort', 'low', ok=False)
    for other_session in (session, luna_session, wrong_role):
        write([other_session, review_turn])
        inspect('--reviewer-effort', 'high', ok=False)
    for field, wrong in [('model', 'gpt-5.6-sol'), ('effort', 'medium'),
                         ('sandbox_policy', {'type': 'read-only'}),
                         ('permission_profile', {'type': 'legacy'})]:
        missing = json.loads(json.dumps(review_turn))
        del missing['payload'][field]
        write([review_session, missing])
        inspect('--reviewer-effort', 'high', ok=False)
        conflicting = json.loads(json.dumps(review_turn))
        conflicting['payload'][field] = wrong
        write([review_session, review_turn, conflicting])
        inspect('--reviewer-effort', 'high', ok=False)
    write([review_session, wrong_model])
    inspect('--reviewer-effort', 'high', ok=False)
    astra_role = tomllib.loads((scripts.parent / 'agents/codex-advisor-astra-implementer.toml').read_text())
    assert astra_role['name'] == 'codex_advisor_astra_implementer'
    assert astra_role['model'] == 'gpt-6-astra'
    assert 'model_reasoning_effort' not in astra_role, 'Astra implementation effort belongs to the caller'
    astra_session = json.loads(json.dumps(session))
    astra_session['payload']['agent_role'] = 'codex_advisor_astra_implementer'
    astra_turn = json.loads(json.dumps(turn))
    for effort in ('medium', 'high', 'xhigh'):
        astra_turn['payload']['effort'] = effort
        write([astra_session, astra_turn])
        evidence = inspect('--astra-effort', effort)
        assert evidence['agent_role'] == 'codex_advisor_astra_implementer'
        assert evidence['model'] == 'gpt-6-astra' and evidence['effort'] == effort
        assert set(evidence) == {'thread_id', 'parent_thread_id', 'agent_role', 'agent_path',
                                 'model_provider', 'model', 'effort', 'sandbox_policy_type',
                                 'permission_profile_type', 'cwd'}
    reject_efforts(astra_session, astra_turn, '--astra-effort', ('low', 'max', 'ultra'))
    astra_turn['payload']['effort'] = 'medium'
    write([astra_session, astra_turn])
    for args in [('--astra-effort', 'high'), ('--astra-effort', 'unsupported'),
                 ('--astra-effort', ''), ('--astra-effort',),
                 ('--astra-effort', 'medium', '--luna'),
                 ('--astra-effort', 'medium', '--sol-effort', 'high'),
                 ('--explorer-effort', 'medium', '--astra-effort', 'medium'),
                 ('--advisor-effort', 'medium', '--astra-effort', 'medium'),
                 ('--astra-effort', 'medium', '--review-primary-effort', 'low')]:
        inspect(*args, ok=False)
    for other_session in (session, review_session, luna_session, sol_session, wrong_role):
        write([other_session, astra_turn])
        inspect('--astra-effort', 'medium', ok=False)
    for model in ('gpt-5.6-luna', 'gpt-5.6-sol'):
        invalid = json.loads(json.dumps(astra_turn))
        invalid['payload']['model'] = model
        write([astra_session, invalid])
        inspect('--astra-effort', 'medium', ok=False)
    for field, wrong in [('model', 'gpt-5.6-sol'), ('effort', 'high'),
                         ('sandbox_policy', {'type': 'read-only'}),
                         ('permission_profile', {'type': 'legacy'})]:
        missing = json.loads(json.dumps(astra_turn))
        del missing['payload'][field]
        write([astra_session, missing])
        inspect('--astra-effort', 'medium', ok=False)
        conflicting = json.loads(json.dumps(astra_turn))
        conflicting['payload'][field] = wrong
        write([astra_session, astra_turn, conflicting])
        inspect('--astra-effort', 'medium', ok=False)
    for records in ([], [session], [turn], [session, session, turn]):
        write(records)
        inspect('--advisor-effort', 'high', ok=False)
    rollout.write_text('{"prompt":"' + secret + '",broken')
    inspect(ok=False)
    write([session, turn])
    duplicate = root / f'rollout-other-{thread}.jsonl'
    duplicate.write_bytes(rollout.read_bytes())
    inspect(ok=False)
    duplicate.unlink()
    rollout.unlink()
    inspect(ok=False)
    bad = subprocess.run(['sh', str(scripts / 'inspect-agent-runtime.sh'), '../invalid'],
                         capture_output=True, text=True)
    assert bad.returncode != 0 and not bad.stdout
print('PASS: native role allocations, explicit independent review, retired-floor refusal, evidence consistency, permissions and payload filtering')
PY
fi
for script in "$script_dir"/*.sh; do sh -n "$script"; done
printf '%s\n' 'VERIFY PASSED: selected deterministic checks (no live routing claim)'
