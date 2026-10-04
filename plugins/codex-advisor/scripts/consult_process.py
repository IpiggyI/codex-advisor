"""Contain Linux native descendants that leave their original process group."""

import ctypes
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

CLEANUP_FAILED = 125


def reap_children(children):
    deadline = time.monotonic() + 10
    while True:
        for value in children.read_text(encoding='ascii').split():
            try:
                os.kill(int(value), signal.SIGKILL)
            except ProcessLookupError:
                pass
        try:
            while os.waitpid(-1, os.WNOHANG)[0]:
                pass
        except ChildProcessError:
            return
        if time.monotonic() >= deadline:
            raise TimeoutError('Native descendants did not terminate.')
        time.sleep(.01)


def supervise_linux(command):
    children = Path('/proc/self/task', str(os.getpid()), 'children')
    try:
        children.read_text(encoding='ascii')
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER
            return CLEANUP_FAILED
    except (OSError, AttributeError):
        return CLEANUP_FAILED

    def stop(signum, _frame):
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, stop)
    try:
        process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        return process.wait()
    finally:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        try:
            reap_children(children)
        except (OSError, ValueError, TimeoutError):
            return CLEANUP_FAILED
