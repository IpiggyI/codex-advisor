"""Persist cumulative consultation failures for each host thread."""

from contextlib import closing
import os
import sqlite3
import tempfile

from consult_context import Failure

FAILURE_LIMIT = 4
STOP_CALLING = ('Stop calling process_consultation in this thread. '
                'Report consultation as unavailable and continue authorized work and required checks.')


def initialize_database(path):
    if path.exists():
        return
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.consultation-failures-', delete=False) as pending:
        name = pending.name
    try:
        with closing(sqlite3.connect(name, timeout=5)) as database, database:
            database.execute('CREATE TABLE failures ('
                             'thread TEXT PRIMARY KEY, count INTEGER NOT NULL CHECK(count BETWEEN 1 AND 4))')
        try:
            # Publish the complete schema without replacing another initializer's database.
            os.link(name, path)
        except FileExistsError:
            pass
    finally:
        os.unlink(name)


def failure_count(home, thread, failed=False):
    path = home / 'codex-advisor/consultation-failures.sqlite3'
    try:
        if not failed and not path.exists():
            return 0
        path.parent.mkdir(parents=True, exist_ok=True)
        if failed:
            initialize_database(path)
        with closing(sqlite3.connect(path, timeout=5)) as database, database:
            if failed:
                database.execute('INSERT INTO failures VALUES (?, 1) ON CONFLICT(thread) DO UPDATE '
                                 'SET count = MIN(count + 1, ?)', (thread, FAILURE_LIMIT))
            row = database.execute('SELECT count FROM failures WHERE thread = ?', (thread,)).fetchone()
            count = row[0] if row else 0
            if type(count) is not int or not 0 <= count <= FAILURE_LIMIT:
                raise ValueError()
            return count
    except (OSError, sqlite3.Error, ValueError):
        raise Failure('failure_state', 'Consultation failure state is unavailable. ' + STOP_CALLING) from None


def limit_result(result, home, thread):
    if home is None or thread is None:
        result.update(consultationDisabled=True, message=result['message'] + '\n' + STOP_CALLING)
        return result
    try:
        if result.get('code') == 'failure_state':
            raise Failure('failure_state', result['message'])
        count = failure_count(home, thread, result['status'] == 'failed' and result.get('code') != 'disabled')
    except Failure as error:
        return {'status': 'failed', 'code': error.code, 'message': str(error),
                'expected': result.get('expected'), 'actual': result.get('actual'), 'consultationDisabled': True}
    result.update(failureCount=count, consultationDisabled=count >= FAILURE_LIMIT)
    if count >= FAILURE_LIMIT and result.get('code') != 'disabled':
        result.update(status='failed', code=result.get('code', 'disabled'),
                      message=result.get('message', '') + '\nConsultation is disabled after four failed calls. ' + STOP_CALLING)
        result.pop('advice', None)
        result.pop('kind', None)
    return result
