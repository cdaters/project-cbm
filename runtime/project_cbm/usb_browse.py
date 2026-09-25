"""Fixed unprivileged Midnight Commander session; the broker owns only its mount."""
import ctypes
import os
import signal
import subprocess
import time
from .ingestion import IngestError
from .ingest_session import emit, receive, cancellation
from . import library

MC_ENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C.UTF-8', 'HOME': '/home/pcbm'}


def child_lifetime(parent):
    """Linux parent-death kill closes the worker-crash/orphan window."""
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:  # PR_SET_PDEATHSIG
        os._exit(126)
    if os.getppid() != parent:
        os._exit(126)


def browse(source, cancelled=cancellation):
    if os.geteuid() != 1000:
        raise IngestError('identity')
    parent = os.getpid()
    terminal = os.environ.get('TERM', 'linux')
    if terminal not in ('linux', 'xterm', 'xterm-256color', 'screen', 'screen-256color'):
        terminal = 'linux'
    # No terminal bytes or MC output enter the JSON protocol. The caller's existing
    # controlling terminal remains its owner; do not change VT/mode/session setup.
    with open('/dev/tty', 'r+b', buffering=0) as tty:
        process = subprocess.Popen(['/usr/bin/mc', '-u', str(source), str(library.ROOT)],
                                   stdin=tty, stdout=tty, stderr=tty, close_fds=True,
                                   env={**MC_ENV, 'TERM': terminal},
                                   preexec_fn=lambda: child_lifetime(parent))
        try:
            while process.poll() is None:
                if cancelled():
                    raise IngestError('cancelled')
                time.sleep(0.1)
            if process.returncode:
                raise IngestError('browser_failed')
        finally:
            if process.poll() is None:
                process.terminate()
                try:process.wait(timeout=0.5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=0.5)


def run(source):
    emit({'status': 'ready'})
    try:
        while True:
            request = receive()
            if request in ({'operation': 'release'}, {'operation': 'cancel'}):
                return {'status': 'ok' if request['operation'] == 'release' else 'cancelled'}
            if request != {'operation': 'browse'}:
                raise IngestError('request')
            browse(source)
            emit({'status': 'ok'})
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        return {'status': 'cancelled' if isinstance(error, IngestError) and str(error) in ('cancelled', 'disconnected', 'expired') else 'failed',
                'error': str(error) if isinstance(error, IngestError) else 'browser_failed'}
