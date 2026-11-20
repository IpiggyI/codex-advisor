"""Real consultation probes: synthetic context, WebSocket versus HTTP, bounded call count."""
import json, sys, threading, time
from pathlib import Path
from unittest import mock
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'plugins/codex-advisor/scripts'))
import consult_native as native
from consult_context import Failure

HOME = Path.home() / '.codex'
EXPECTED = {'model': 'gpt-6.2-sol', 'effort': 'high'}
CALLER = {
    'base': 'You are a coding agent working in a small Python repository.',
    'items': [
        {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text':
            'A CLI tool reads a JSON config file at startup. Users report crashes when the file is missing. '
            'I plan to create a default config file automatically when it is absent. Is that the right approach?'}]},
        {'type': 'message', 'role': 'assistant', 'content': [{'type': 'output_text', 'text':
            'I will check the current loader, then decide between creating a default file and using in-memory defaults.'}]},
    ],
    'model': 'gpt-6.2-sol', 'effort': 'high', 'role': None, 'source': 'cli', 'thread': 'probe', 'hostVersion': 'probe'}
PLAN = sys.argv[1].split(',')          # e.g. ws,http,ws,http
out = Path(sys.argv[2])
original = native.configuration
for index, transport in enumerate(PLAN):
    diagnostics = native.Diagnostics()
    def configuration(root, expected, transport=transport):
        values = original(root, expected)
        values['model_providers.official.supports_websockets'] = transport == 'ws'
        return values
    started = time.time()
    with mock.patch.object(native, 'configuration', configuration), \
            mock.patch.object(native, 'Diagnostics', return_value=diagnostics):
        try:
            result = native.execute(HOME, CALLER, EXPECTED, threading.Event())
            row = {'status': 'succeeded', 'kind': result['kind'], 'actual': result['actual']}
        except Failure as error:
            row = {'status': 'failed', 'code': error.code, 'message': str(error)[:120],
                   'nativeCode': error.details.get('nativeCode'), 'httpStatusCode': error.details.get('httpStatusCode')}
    row.update(call=index + 1, transport=transport, wallMs=round((time.time() - started) * 1000),
               at=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(started)), **diagnostics.snapshot())
    with out.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(row) + '\n')
    print(json.dumps({k: row.get(k) for k in ('call', 'transport', 'status', 'code', 'wallMs', 'retryCount', 'firstOutputMs', 'lastRetry')}), flush=True)
