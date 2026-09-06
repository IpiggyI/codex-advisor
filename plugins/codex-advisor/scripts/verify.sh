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
    filename = role_files['advisor']
    (target / filename).unlink()
    before = snapshot(root)
    install(target, '--check-role', 'advisor', ok=False)
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
assert 'model_reasoning_effort' not in reviewer, 'a fixed effort would defeat the review floor'
assert reviewer['sandbox_mode'] == 'read-only'
def select_review(*args, expected=None):
    result = subprocess.run(['sh', str(scripts / 'inspect-agent-runtime.sh'),
                             '--select-review-effort', *args], capture_output=True, text=True)
    if expected is None:
        assert result.returncode != 0 and not result.stdout and 'ERROR:' in result.stderr
    else:
        assert result.returncode == 0 and result.stdout == expected + '\n', result
review_defaults = {'low': 'high', 'medium': 'high', 'high': 'high',
                   'xhigh': 'xhigh', 'max': 'max'}
allowed_overrides = {'low': ('low', 'medium', 'high', 'xhigh', 'max'),
                     'medium': ('medium', 'high', 'xhigh', 'max'),
                     'high': ('high', 'xhigh', 'max'), 'xhigh': ('xhigh', 'max'),
                     'max': ('max',)}
for primary, default in review_defaults.items():
    select_review('--review-primary-effort', primary, expected=default)
    for override in review_defaults:
        select_review('--review-primary-effort', primary, '--reviewer-effort', override,
                      expected=override if override in allowed_overrides[primary] else None)
for unknown in ('unsupported', 'ultra', 'MAX', ''):
    select_review('--review-primary-effort', unknown)
    select_review('--review-primary-effort', 'low', '--reviewer-effort', unknown)
select_review()
select_review('--reviewer-effort', 'high')
select_review('--review-primary-effort', 'high', '--luna')
select_review('--review-primary-effort', 'high', '--advisor-effort', 'high')
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
    for effort in ('low', 'medium', 'high', 'xhigh', 'max', 'ultra'):
        turn['payload']['effort'] = effort
        write([session, turn, {'type': 'response_item', 'payload': {'text': secret}}])
        evidence = inspect('--advisor-effort', effort)
        assert evidence['model'] == 'gpt-6-astra' and evidence['effort'] == effort
        assert evidence['agent_role'] == 'codex_advisor_astra_advisor'
        assert evidence['sandbox_policy_type'] == 'read-only'
        assert set(evidence) == {'thread_id', 'parent_thread_id', 'agent_role', 'agent_path',
                                 'model_provider', 'model', 'effort', 'sandbox_policy_type',
                                 'permission_profile_type', 'cwd'}
    turn['payload']['effort'] = 'high'
    turn['payload']['sandbox_policy']['type'] = 'danger-full-access'
    turn['payload']['permission_profile']['type'] = 'disabled'
    write([session, turn])
    evidence = inspect('--advisor-effort', 'high')
    assert evidence['sandbox_policy_type'] == 'danger-full-access'
    assert evidence['permission_profile_type'] == 'disabled'
    inspect('--advisor-effort', 'medium', ok=False)
    inspect('--advisor-effort', 'unsupported', ok=False)
    for field in ('model', 'effort', 'sandbox_policy', 'permission_profile'):
        missing = json.loads(json.dumps(turn))
        del missing['payload'][field]
        write([session, missing])
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
    review_session = json.loads(json.dumps(session))
    review_session['payload']['agent_role'] = 'codex_advisor_astra_reviewer'
    review_turn = json.loads(json.dumps(turn))
    for primary, default in review_defaults.items():
        review_turn['payload']['effort'] = default
        write([review_session, review_turn])
        evidence = inspect('--review-primary-effort', primary)
        assert evidence['agent_role'] == 'codex_advisor_astra_reviewer'
        assert evidence['model'] == 'gpt-6-astra' and evidence['effort'] == default
        for override in review_defaults:
            review_turn['payload']['effort'] = override
            write([review_session, review_turn])
            inspect('--review-primary-effort', primary, '--reviewer-effort', override,
                    ok=override in allowed_overrides[primary])
    review_turn['payload']['effort'] = 'high'
    write([review_session, review_turn])
    inspect('--review-primary-effort', 'max', ok=False)
    inspect('--review-primary-effort', 'low', '--reviewer-effort', 'medium', ok=False)
    inspect('--reviewer-effort', 'high', ok=False)
    inspect('--luna', '--review-primary-effort', 'low', ok=False)
    for other_session in (session, luna_session, wrong_role):
        write([other_session, review_turn])
        inspect('--review-primary-effort', 'low', ok=False)
    for field, wrong in [('model', 'gpt-5.6-sol'), ('effort', 'medium'),
                         ('sandbox_policy', {'type': 'read-only'}),
                         ('permission_profile', {'type': 'legacy'})]:
        missing = json.loads(json.dumps(review_turn))
        del missing['payload'][field]
        write([review_session, missing])
        inspect('--review-primary-effort', 'low', ok=False)
        conflicting = json.loads(json.dumps(review_turn))
        conflicting['payload'][field] = wrong
        write([review_session, review_turn, conflicting])
        inspect('--review-primary-effort', 'low', ok=False)
    write([review_session, wrong_model])
    inspect('--review-primary-effort', 'low', ok=False)
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
print('PASS: native role evidence, Luna max, review floors and overrides, refusals, permissions and payload filtering')
PY
fi
for script in "$script_dir"/*.sh; do sh -n "$script"; done
printf '%s\n' 'VERIFY PASSED: selected deterministic checks (no live routing claim)'
