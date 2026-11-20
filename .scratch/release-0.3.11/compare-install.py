"""Compare an installed plugin cache and entries with the release commit, byte for byte."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--commit', required=True)
parser.add_argument('--home', type=Path, required=True)
parser.add_argument('--version', required=True)
parser.add_argument('--manifest', type=Path)
args = parser.parse_args()


def show(path):
    return subprocess.run(['git', '-C', str(args.repo), 'show', f'{args.commit}:{path}'],
                          capture_output=True, check=True).stdout


names = subprocess.run(['git', '-C', str(args.repo), 'ls-tree', '-r', '--name-only', args.commit,
                        'plugins/codex-advisor'], capture_output=True, text=True, check=True).stdout.split()
source = {name.removeprefix('plugins/codex-advisor/'): show(name) for name in names}
cache = args.home / 'plugins/cache/codex-advisor/codex-advisor' / args.version
mismatches = [rel for rel, data in source.items()
              if not (cache / rel).is_file() or (cache / rel).read_bytes() != data]
entries = {rel: data for rel, data in source.items() if rel.startswith('agents/') and rel.endswith('.toml')}
mismatches += ['installed ' + rel for rel, data in entries.items()
               if not (args.home / rel).is_file() or (args.home / rel).read_bytes() != data]
models = {}
for rel in entries:
    for line in (args.home / rel).read_text(encoding='utf-8').splitlines():
        if line.startswith('model = '):
            model = line.split('"')[1]
            models[model] = models.get(model, 0) + 1
if args.manifest:
    args.manifest.write_text(json.dumps({'version': args.version, 'sourceCommit': args.commit, 'files': {
        rel: hashlib.sha256(data).hexdigest() for rel, data in sorted(source.items())}}, indent=2) + '\n')
print(json.dumps({'version': args.version, 'sourceCommit': args.commit, 'pluginFiles': len(source),
                  'entries': len(entries), 'entryModels': dict(sorted(models.items())),
                  'mismatches': mismatches}))
