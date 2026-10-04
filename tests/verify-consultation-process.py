#!/usr/bin/env python3
"""Check native descendant cleanup across Linux process-group boundaries."""

import ctypes
import os
from pathlib import Path
import signal
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'plugins/codex-advisor/scripts'))
from consult_native import launch, terminate


@unittest.skipUnless(sys.platform == 'linux', 'Linux subreaper containment')
class LinuxDescendants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) != 0:
            raise RuntimeError('The test cannot contain failed-fixture descendants.')

    def check_descendant(self, parent_exits):
        program = ('import subprocess,sys,time; '
                   'child=subprocess.Popen([sys.executable,"-B","-c","import time; time.sleep(60)"],'
                   'start_new_session=True); print(child.pid,flush=True); ' +
                   ('sys.exit(0)' if parent_exits else 'time.sleep(60)'))
        with tempfile.TemporaryDirectory(prefix='ca-descendant-check-') as root:
            process = launch([sys.executable, '-B', '-c', program], dict(os.environ), Path(root))
            child = None
            try:
                child = int(process.stdout.readline())
                if parent_exits:
                    process.wait(timeout=3)
                terminate(process)
                self.assertFalse(Path('/proc', str(child)).exists(), 'A detached descendant survived cleanup.')
            finally:
                if child and Path('/proc', str(child)).exists():
                    try:
                        os.killpg(child, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    try:
                        os.waitpid(child, 0)
                    except ChildProcessError:
                        pass
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=3)
                process.stdin.close()
                process.stdout.close()

    def test_detached_descendant_is_reaped_on_cancellation(self):
        self.check_descendant(False)

    def test_detached_descendant_is_reaped_after_parent_exit(self):
        self.check_descendant(True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
