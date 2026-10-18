#!/usr/bin/env python3
"""比较本机宿主协议与插件显式接受的历史类型，不修改安装。"""

import ast
import json
from pathlib import Path
import subprocess
import tempfile


repo = Path(__file__).resolve().parents[2]
source = repo / 'plugins/codex-advisor/scripts/consult_context.py'
tree = ast.parse(source.read_text())
validator = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'validate_items')
accepted = set()
for node in ast.walk(validator):
    if not isinstance(node, ast.Compare) or not isinstance(node.left, ast.Name) or node.left.id != 'kind':
        continue
    for value in node.comparators:
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            accepted.add(value.value)
        elif isinstance(value, ast.Tuple):
            accepted.update(element.value for element in value.elts if isinstance(element, ast.Constant))

version = subprocess.run(['codex', '--version'], capture_output=True, text=True, check=True).stdout.strip()
with tempfile.TemporaryDirectory(prefix='ca-schema-audit-') as directory:
    subprocess.run(['codex', 'app-server', 'generate-json-schema', '--experimental', '--out', directory],
                   capture_output=True, text=True, timeout=40, check=True)
    schema = json.loads((Path(directory) / 'codex_app_server_protocol.v2.schemas.json').read_text())
    definitions = schema['definitions']
    response_item = definitions['ResponseItem']
    variants = response_item.get('anyOf', response_item.get('oneOf', []))
    assert variants, '宿主没有提供可识别的历史类型联合定义'
    host = {value for variant in variants for value in variant['properties']['type']['enum']}
    fork = definitions['ThreadForkParams']['properties']
    result = {
        'hostVersion': version,
        'hostVariantCount': len(host),
        'validatorAcceptedCount': len(accepted),
        'validatorAcceptedTypes': sorted(accepted),
        'hostTypesWithoutValidatorBranch': sorted(host - accepted),
        'injectItemsSchema': definitions['ThreadInjectItemsParams']['properties']['items'],
        'lastTurnIdSchema': fork['lastTurnId'],
        'boundary': '类型差集不是实际故障计数；other 为协议兜底变体。',
    }
print(json.dumps(result, ensure_ascii=False, indent=2))
