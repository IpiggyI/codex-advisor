#!/usr/bin/env python3
"""Check atomic publication and concurrent use of consultation failure state."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import unittest
from unittest import mock

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'plugins/codex-advisor/scripts'))
import consult_limits as limits
from consult_context import Failure


class FailureStorage(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ca-counter-check-')
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.path = self.home / 'codex-advisor/consultation-failures.sqlite3'

    def test_reader_cannot_observe_partially_initialized_database(self):
        created, release = threading.Event(), threading.Event()
        original = sqlite3.connect
        results = []

        def connect(*args, **kwargs):
            database = original(*args, **kwargs)
            if threading.current_thread() is writer and not created.is_set():
                created.set()
                release.wait(3)
            return database

        def fail():
            try:
                results.append(limits.failure_count(self.home, 'writer', True))
            except Exception as error:
                results.append(error)

        writer = threading.Thread(target=fail)
        with mock.patch.object(sqlite3, 'connect', side_effect=connect):
            writer.start()
            try:
                self.assertTrue(created.wait(2))
                self.assertEqual(limits.failure_count(self.home, 'reader'), 0)
            finally:
                release.set()
                writer.join(4)
        self.assertFalse(writer.is_alive())
        self.assertEqual(results, [1])
        self.assertEqual(limits.failure_count(self.home, 'writer'), 1)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_concurrent_failures_preserve_each_thread_and_cap_counts(self):
        def fail(index):
            return limits.failure_count(self.home, 'thread-' + str(index % 4), True)
        with ThreadPoolExecutor(max_workers=12) as workers:
            counts = list(workers.map(fail, range(48)))
        self.assertTrue(all(1 <= count <= 4 for count in counts))
        self.assertEqual([limits.failure_count(self.home, 'thread-' + str(i)) for i in range(4)], [4] * 4)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def reject_existing(self, content):
        self.path.write_bytes(content)
        for failed in (False, True):
            with self.assertRaises(Failure) as raised:
                limits.failure_count(self.home, 'caller', failed)
            self.assertEqual(raised.exception.code, 'failure_state')
            self.assertEqual(self.path.read_bytes(), content)

    def test_existing_database_without_schema_is_not_reset(self):
        self.path.parent.mkdir()
        with closing(sqlite3.connect(self.path)) as database:
            database.execute('CREATE TABLE unrelated (value INTEGER)')
        self.reject_existing(self.path.read_bytes())

    def test_corrupt_database_is_not_reset(self):
        self.path.parent.mkdir()
        self.reject_existing(b'corrupt database')

    def test_failed_publication_leaves_no_database_or_private_file(self):
        with mock.patch.object(limits.os, 'link', side_effect=OSError('publication unavailable')):
            with self.assertRaises(Failure) as raised:
                limits.failure_count(self.home, 'caller', True)
        self.assertEqual(raised.exception.code, 'failure_state')
        self.assertEqual(list(self.path.parent.iterdir()), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
