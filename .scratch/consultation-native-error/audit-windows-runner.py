"""Record the final Windows checks without changing delivered files."""

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[2]
EVIDENCE = REPO / '.scratch/consultation-native-error'
RUNTIME = r'C:\Users\Shy\AppData\Local\Codey\codex-runtime\ef136ab93f4ff3f4'
ENV = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
ENV['PATH'] = RUNTIME + os.pathsep + ENV['PATH']
PREFIXES = ('ca-native-fixture-', 'ca-consult-boundary-', 'ca-native-pipe-',
            'ca-native-reader-', 'ca-native-publish-', 'ca-native-request-',
            'ca-mcp-environment-', 'ca-native-history-', 'ca-descendant-check-',
            'codex-advisor-consult-')


def snapshot():
    paths = [path for directory in ('plugins/codex-advisor', 'tests')
             for path in (REPO / directory).rglob('*')
             if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc']
    paths += [REPO / 'README.md', REPO / 'docs/agents/plugin-maintenance.md',
              EVIDENCE / 'authenticated-chain.py']
    files = {path.relative_to(REPO).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
             for path in sorted(paths)}
    digest = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    return {'sha256': digest, 'files': files}


def temporary_outputs():
    return sorted(path.name for path in Path(tempfile.gettempdir()).iterdir()
                  if path.is_dir() and path.name.startswith(PREFIXES))


def counts(output):
    ran = re.search(r'Ran (\d+) tests? in', output)
    skip = re.search(r'skipped=(\d+)', output)
    failed = re.search(r'failures=(\d+)', output)
    errors = re.search(r'errors=(\d+)', output)
    total = int(ran.group(1)) if ran else None
    skipped = int(skip.group(1)) if skip else 0
    failures = int(failed.group(1)) if failed else 0
    exceptions = int(errors.group(1)) if errors else 0
    return {'ran': total, 'passed': total - skipped - failures - exceptions if total is not None else None,
            'skipped': skipped, 'failures': failures, 'errors': exceptions,
            'skipLines': [line for line in output.splitlines() if '... skipped ' in line]}


def save_summary():
    summary['finalSource'] = snapshot()
    summary['allSourceHashesEqual'] = all(
        item['beforeSource']['sha256'] == item['afterSource']['sha256'] == summary['initialSource']['sha256']
        for item in summary['checks']) and summary['finalSource']['sha256'] == summary['initialSource']['sha256']
    baseline = {key: value for key, value in summary['initialSource']['files'].items() if key != 'README.md'}
    summary['runtimeAndTestSourceHashesEqual'] = all(
        {key: value for key, value in source['files'].items() if key != 'README.md'} == baseline
        for item in summary['checks'] for source in (item['beforeSource'], item['afterSource']))
    expected = json.loads((EVIDENCE / 'audit-review-snapshot.json').read_text(encoding='utf-8'))['files']
    summary['finalMatchesReviewSnapshot'] = all(summary['finalSource']['files'].get(key) == value
                                               for key, value in expected.items())
    (EVIDENCE / 'audit-final-windows-summary.json').write_text(
        json.dumps(summary, indent=2), encoding='utf-8')


def execute(label, command, timeout, stdout_path=None, stderr_path=None):
    before = snapshot()
    temp_before = temporary_outputs()
    started = time.monotonic()
    print('Starting ' + label, flush=True)
    try:
        result = subprocess.run(command, env=ENV, cwd=REPO, capture_output=True,
                                text=True, encoding='utf-8', timeout=timeout)
        status, stdout, stderr = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as error:
        status = None
        stdout = error.stdout.decode('utf-8', errors='replace') if isinstance(error.stdout, bytes) else error.stdout or ''
        stderr = error.stderr.decode('utf-8', errors='replace') if isinstance(error.stderr, bytes) else error.stderr or ''
        stderr += '\nThe check exceeded its timeout.\n'
    after = snapshot()
    item = {'label': label, 'command': command, 'exitCode': status,
            'seconds': round(time.monotonic() - started, 3), 'counts': counts(stdout + stderr),
            'beforeSource': before, 'afterSource': after, 'sourceUnchanged': before == after,
            'newTemporaryOutputs': sorted(set(temporary_outputs()) - set(temp_before))}
    summary['checks'].append(item)
    if stdout_path:
        stdout_path.write_text(stdout, encoding='utf-8')
        stderr_path.write_text(stderr, encoding='utf-8')
    else:
        metadata = {key: value for key, value in item.items() if key not in ('beforeSource', 'afterSource')}
        (EVIDENCE / ('audit-final-windows-' + label + '.log')).write_text(
            json.dumps(metadata, indent=2) + '\n\n' + stdout + stderr, encoding='utf-8')
    save_summary()
    print(json.dumps({key: value for key, value in item.items()
                      if key not in ('beforeSource', 'afterSource', 'command')}), flush=True)
    before_code = {key: value for key, value in before['files'].items() if key != 'README.md'}
    after_code = {key: value for key, value in after['files'].items() if key != 'README.md'}
    if status != 0 or before_code != after_code or item['newTemporaryOutputs']:
        raise SystemExit(1)


native = shutil.which('codex.exe', path=ENV['PATH'])
version = subprocess.run([native, '--version'], env=ENV, capture_output=True, text=True,
                         encoding='utf-8', timeout=15)
summary = {'platform': os.name, 'pythonExecutable': sys.executable,
           'pythonVersion': sys.version.split()[0], 'nativeExecutable': native,
           'nativeVersion': version.stdout.strip(), 'nativeVersionExit': version.returncode,
           'S2A_API_KEY_Present': bool(os.environ.get('S2A_API_KEY')),
           'initialSource': snapshot(), 'checks': []}
if '--resume' in sys.argv:
    summary = json.loads((EVIDENCE / 'audit-final-windows-summary.json').read_text(encoding='utf-8'))
    summary['documentSourceChange'] = {
        'file': 'README.md', 'before': summary['initialSource']['files']['README.md'],
        'after': snapshot()['files']['README.md'],
        'reason': 'Primary updated the consultation verified version to 0.160; runtime and test sources unchanged.',
        'runtimeRerunWaivedByPrimary': True}
print(json.dumps({key: value for key, value in summary.items() if key not in ('initialSource', 'checks')}), flush=True)
for name in ('verify-consultation', 'verify-consultation-lifecycle', 'verify-consultation-native',
             'verify-consultation-process', 'verify-consultation-host', 'verify-consultation-env'):
    label = name.removeprefix('verify-consultation').strip('-') or 'boundary'
    if any(item['label'] == label and item['exitCode'] == 0 for item in summary['checks']):
        print('Retaining completed check ' + label, flush=True)
        continue
    execute(label,
            [sys.executable, '-B', str(REPO / 'tests' / (name + '.py'))], 240)
execute('authenticated-astra', [sys.executable, '-B', str(EVIDENCE / 'authenticated-chain.py'),
        r'C:\Users\Shy\.codex\config.toml', 'gpt-6-astra'], 270,
        EVIDENCE / 'audit-authenticated-windows-astra.json',
        EVIDENCE / 'audit-authenticated-windows-astra.stderr.log')
