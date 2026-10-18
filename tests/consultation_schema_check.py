#!/usr/bin/env python3
"""Check the local host ResponseItem union against the production policy table."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'plugins/codex-advisor/scripts'))
from consult_context import ITEM_POLICY


def missing_types(schema, policy):
    union = schema['definitions']['ResponseItem']
    variants = union.get('anyOf', union.get('oneOf'))
    if not variants:
        raise ValueError('ResponseItem union is missing.')
    kinds = {kind for variant in variants for kind in variant['properties']['type']['enum']}
    return sorted(kinds - policy.keys()), len(kinds)


def check_host():
    with tempfile.TemporaryDirectory(prefix='ca-schema-') as directory:
        result = subprocess.run(['codex', 'app-server', 'generate-json-schema',
                                 '--experimental', '--out', directory], capture_output=True)
        if result.returncode:
            raise RuntimeError('Host schema generation failed.')
        missing, counts = set(), set()
        for path in sorted(Path(directory).rglob('*.json')):
            schema = json.loads(path.read_text(encoding='utf-8'))
            if 'ResponseItem' in schema.get('definitions', {}):
                absent, count = missing_types(schema, ITEM_POLICY)
                missing.update(absent)
                counts.add(count)
        if not counts:
            raise ValueError('Generated schemas have no ResponseItem definition.')
        return {'variantCounts': sorted(counts), 'missingTypes': sorted(missing)}


def main():
    try:
        report = check_host()
    except (OSError, ValueError, KeyError, TypeError, RuntimeError):
        print(json.dumps({'code': 'schema', 'message': 'Host schema check could not be completed.'}))
        return 1
    print(json.dumps(report))
    return int(bool(report['missingTypes']))


if __name__ == '__main__':
    sys.exit(main())
