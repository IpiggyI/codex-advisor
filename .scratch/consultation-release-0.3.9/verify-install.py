"""Compare a native installation with the published source manifest."""

import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--home', type=Path, required=True)
args = parser.parse_args()
evidence = Path(__file__).with_name('evidence')
manifest = json.loads(evidence.joinpath('source-manifest.json').read_text(encoding='utf-8'))
plugin = args.home / 'plugins/cache/codex-advisor/codex-advisor' / manifest['version']
mismatches, entries = [], 0
for relative, digest in manifest['files'].items():
    path = plugin / relative
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        mismatches.append('plugin/' + relative)
    if relative.startswith('agents/') and relative.endswith('.toml'):
        entries += 1
        path = args.home / 'agents' / Path(relative).name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            mismatches.append('agents/' + path.name)
print(json.dumps({'version': manifest['version'], 'sourceCommit': manifest['sourceCommit'],
                  'pluginFiles': len(manifest['files']), 'entries': entries, 'mismatches': mismatches}))
raise SystemExit(bool(mismatches))
