#!/usr/bin/env python3
"""Exercise a temporary installed plugin with existing provider environment auth."""

import importlib.util
import hashlib
import json
import os
from pathlib import Path
import sys
import tomllib

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('environment_check', REPO / 'tests/verify-consultation-env.py')
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
if len(sys.argv) > 2:
    assert sys.argv[2] in ('gpt-6.1-sol', 'gpt-6-astra')
    checks.EXPECTED = {'model': sys.argv[2], 'effort': 'xhigh'}
config_path = Path(sys.argv[1])
settings = tomllib.loads(config_path.read_text(encoding='utf-8'))
provider = settings['model_providers'][settings['model_provider']]
environment_auth = provider.get('env_key') == 'S2A_API_KEY'
assert environment_auth or provider.get('requires_openai_auth') is True
check = checks.NativeEnvironment()
check.setUp()
try:
    if environment_auth:
        assert os.environ.get('S2A_API_KEY')
        check.env['S2A_API_KEY'] = os.environ['S2A_API_KEY']
    else:
        auth_source = config_path.parent / 'auth.json'
        auth_before = hashlib.sha256(auth_source.read_bytes()).digest()
        (check.home / 'auth.json').symlink_to(auth_source)
    endpoint = check.start_endpoint()
    values = {'name': 'Existing configured provider', 'base_url': provider['base_url'],
              'wire_api': 'responses', 'requires_openai_auth': not environment_auth,
              'supports_websockets': False}
    if environment_auth:
        values['env_key'] = 'S2A_API_KEY'
    config = (check.home / 'config.toml').read_text().replace('model_provider = "diagnostic"',
                                                          'model_provider = "live"')
    config += '\n[model_providers.live]\n'
    config += '\n'.join(key + ' = ' + json.dumps(value) for key, value in values.items()) + '\n'
    (check.home / 'config.toml').write_text(config, encoding='utf-8')
    check.install()
    original = checks.configuration
    checks.configuration = lambda *args: dict(original(*args), model_provider='diagnostic')
    thread, completed = check.run_outer_turn(timeout=210)
    results = [item['result']['structuredContent'] for item in completed if item['type'] == 'mcpToolCall']
    assert len(results) == 1 and results[0].get('status') == 'succeeded', results
    assert results[0]['actual'] == checks.EXPECTED
    assert results[0]['failureCount'] == 0 and not results[0]['consultationDisabled']
    assert len(endpoint.requests) == 2
    assert list(check.consult_temp.iterdir()) == []
    if not environment_auth:
        assert hashlib.sha256(auth_source.read_bytes()).digest() == auth_before
    safe = {key: value for key, value in results[0].items() if key != 'advice'}
    print(json.dumps({'platform': os.name, 'outerThread': thread, 'consultation': safe,
                      'outerModelEndpoint': 'loopback', 'innerModelEndpoint': 'configured-provider',
                      'temporaryInstallation': True, 'credentialFilesCopied': False,
                      'authentication': 'environment' if environment_auth else 'existing-api-key-file-symlink'}, indent=2))
finally:
    check.doCleanups()
