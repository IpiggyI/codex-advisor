"""Record Windows acceptance checks for the frozen counter publication repair."""

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
REVIEW = json.loads((EVIDENCE / 'audit-review-snapshot.json').read_text(encoding='utf-8'))
SUMMARY = EVIDENCE / 'audit-limits-windows-summary.json'
ENV = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
ENV['PATH'] = (r'C:\Users\Shy\AppData\Local\Codey\codex-runtime\ef136ab93f4ff3f4'
               + os.pathsep + ENV['PATH'])
PREFIXES = ('ca-counter-check-', 'ca-consult-boundary-', 'ca-native-fixture-',
            'ca-mcp-environment-', 'codex-advisor-consult-')


def snapshot():
    return {name: hashlib.sha256((REPO / name).read_bytes()).hexdigest()
            for name in REVIEW['files']}


def temporary_outputs():
    return {path.name for path in Path(tempfile.gettempdir()).iterdir()
            if path.is_dir() and path.name.startswith(PREFIXES)}


def counts(output):
    total = re.search(r'Ran (\d+) tests? in', output)
    values = {key: int(match.group(1)) if (match := re.search(key + r'=(\d+)', output)) else 0
              for key in ('skipped', 'failures', 'errors')}
    values['ran'] = int(total.group(1)) if total else None
    values['passed'] = values['ran'] - sum(values[key] for key in ('skipped', 'failures', 'errors')) if total else None
    return values


def save():
    summary['finalSource'] = snapshot()
    summary['allCheckpointsMatchReviewSnapshot'] = all(
        source == REVIEW['files'] for item in summary['checks']
        for source in (item['beforeSource'], item['afterSource']))
    summary['finalMatchesReviewSnapshot'] = summary['finalSource'] == REVIEW['files']
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding='utf-8')


def execute(label, filename, arguments=(), timeout=240, authenticated=False):
    command = [sys.executable, '-B', str(REPO / filename), *arguments]
    before = snapshot()
    if before != REVIEW['files']:
        raise RuntimeError('Frozen delivery changed before ' + label)
    temporary_before = temporary_outputs()
    started = time.monotonic()
    print('Starting ' + label, flush=True)
    result = subprocess.run(command, env=ENV, cwd=REPO, capture_output=True, text=True,
                            encoding='utf-8', timeout=timeout)
    item = {'label': label, 'command': command, 'exitCode': result.returncode,
            'seconds': round(time.monotonic() - started, 3), 'counts': counts(result.stdout + result.stderr),
            'beforeSource': before, 'afterSource': snapshot(),
            'newTemporaryOutputs': sorted(temporary_outputs() - temporary_before)}
    summary['checks'].append(item)
    metadata = {key: value for key, value in item.items() if key not in ('beforeSource', 'afterSource')}
    if authenticated:
        (EVIDENCE / 'audit-authenticated-windows-final-astra.json').write_text(result.stdout, encoding='utf-8')
        (EVIDENCE / 'audit-authenticated-windows-final-astra.stderr.log').write_text(result.stderr, encoding='utf-8')
    (EVIDENCE / ('audit-limits-windows-' + label + '.log')).write_text(
        json.dumps(metadata, indent=2) + '\n\n' + ('' if authenticated else result.stdout + result.stderr),
        encoding='utf-8')
    save()
    print(json.dumps(metadata), flush=True)
    if result.returncode != 0 or item['afterSource'] != REVIEW['files'] or item['newTemporaryOutputs']:
        raise SystemExit(1)


native = shutil.which('codex.exe', path=ENV['PATH'])
version = subprocess.run([native, '--version'], env=ENV, capture_output=True, text=True,
                         encoding='utf-8', timeout=15)
summary = {'platform': os.name, 'pythonExecutable': sys.executable,
           'pythonVersion': sys.version.split()[0], 'nativeExecutable': native,
           'nativeVersion': version.stdout.strip(), 'nativeVersionExit': version.returncode,
           'S2A_API_KEY_Present': bool(os.environ.get('S2A_API_KEY')),
           'reviewSnapshot': REVIEW, 'checks': []}
print(json.dumps({key: value for key, value in summary.items() if key not in ('reviewSnapshot', 'checks')}), flush=True)
execute('storage', 'tests/verify-consultation-limits.py')
execute('boundary', 'tests/verify-consultation.py')
execute('env', 'tests/verify-consultation-env.py')
execute('authenticated-astra', '.scratch/consultation-native-error/authenticated-chain.py',
        (r'C:\Users\Shy\.codex\config.toml', 'gpt-6-astra'), timeout=270, authenticated=True)
