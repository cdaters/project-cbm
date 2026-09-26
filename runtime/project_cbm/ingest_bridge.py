"""Unprivileged protocol bridge; interactive MC never crosses sudo's PTY.

The broker owns the mount lease. Only JSON crosses its pipes; MC opens the
caller's controlling terminal directly. The Menu's existing FIFO API is unchanged.
"""
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import time

from .ingest_session import emit, receive
from .ingestion import IngestError
from . import usb_browse

SOURCE = Path('/run/project-cbm/import/browse')


class Replies:
    def __init__(self, fd):
        self.fd = fd
        self.buffer = bytearray()

    def ready(self):
        return b'\n' in self.buffer or bool(select.select([self.fd], [], [], 0)[0])

    def read(self, timeout=2):
        deadline = time.monotonic() + timeout
        while b'\n' not in self.buffer:
            if not select.select([self.fd], [], [], max(0, deadline-time.monotonic()))[0]:
                raise IngestError('disconnected')
            raw = os.read(self.fd, 8192)
            if not raw:
                raise IngestError('disconnected')
            self.buffer.extend(raw)
            if len(self.buffer) > 16384:
                raise IngestError('reply_size')
        line, _, rest = self.buffer.partition(b'\n')
        self.buffer = bytearray(rest)
        if len(line) > 8192:
            raise IngestError('reply_size')
        value = json.loads(line)
        if not isinstance(value, dict) or value.get('schema_version') != 2:
            raise IngestError('request')
        return value


def main():
    if os.geteuid() != 1000:
        return 2
    stopped = False

    def interrupt(signum, frame):
        nonlocal stopped
        stopped = True

    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, interrupt)
    broker = None
    final = False
    try:
        initial = receive(20)
        browsing = initial.get('operation') == 'browse-session'
        broker = subprocess.Popen(
            ['/usr/bin/sudo', '-n', '--', '/usr/libexec/pcbm-import-root'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            bufsize=0, close_fds=True,
            env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C',
                 'TERM': os.environ.get('TERM', 'linux')})
        replies = Replies(broker.stdout.fileno())

        def send(request):
            broker.stdin.write((json.dumps(request) + '\n').encode())

        send(initial)
        ready = False
        closing = False
        cancel_sent = False
        failure = None
        cleanup_deadline = None
        idle_deadline = time.monotonic() + 300
        while not final:
            if browsing and ready and time.monotonic() >= idle_deadline:
                stopped = True
            if stopped and not cancel_sent and not closing:
                send({'operation': 'cancel'})
                cancel_sent = True
                cleanup_deadline = time.monotonic() + 35
            if cleanup_deadline and time.monotonic() > cleanup_deadline:
                raise IngestError('disconnected')
            if replies.ready():
                answer = replies.read()
                if answer.get('status') == 'releasing':
                    closing = True
                    cleanup_deadline = time.monotonic() + 35
                    continue  # Internal lease notification, not a Menu result.
                final = 'source_unmounted' in answer
                ready = ready or answer.get('status') == 'ready'
                idle_deadline = time.monotonic() + 300
                if final and failure:
                    answer.update(status='failed', error=failure)
                emit(answer)
                continue
            inputs = [] if stopped or closing or cancel_sent else [0]
            if not select.select(inputs + [replies.fd], [], [], 0.1)[0]:
                continue
            if inputs and select.select([0], [], [], 0)[0]:
                try:
                    request = receive(2)
                except IngestError:
                    stopped = True
                    continue
                if browsing and request == {'operation': 'browse'}:
                    if not ready:
                        raise IngestError('request')

                    def cancelled():
                        nonlocal stopped, closing
                        if stopped:
                            return True
                        if replies.ready():
                            # Worker exit/expiry: stop MC before broker's bounded
                            # unmount retries. No terminal data enters this stream.
                            answer = replies.read()
                            if answer.get('status') != 'releasing':
                                raise IngestError('disconnected')
                            closing = True
                            return True
                        if select.select([0], [], [], 0)[0]:
                            value = receive(2)
                            if value != {'operation': 'cancel'}:
                                raise IngestError('request')
                            stopped = True
                            return True
                        return False

                    try:
                        usb_browse.browse(SOURCE, cancelled)
                    except (OSError, ValueError, subprocess.SubprocessError):
                        # browse() reaps MC before lease cancellation is sent.
                        failure = None if stopped or closing else 'browser_failed'
                        stopped = True
                        cleanup_deadline = time.monotonic() + 35
                    else:
                        idle_deadline = time.monotonic() + 300
                        emit({'status': 'ok'})
                else:
                    send(request)
        return 0
    except (OSError, ValueError, subprocess.SubprocessError):
        try:emit({'status': 'failed', 'error': 'unavailable', 'source_unmounted': None})
        except OSError:pass
        return 2
    finally:
        if broker:
            # EOF releases the lease even if the Menu disappeared. Do not emit a
            # safe-removal claim without the broker's verified final response.
            broker.stdin.close()
            try:broker.wait(timeout=35)
            except subprocess.TimeoutExpired:
                broker.terminate()
                try:broker.wait(timeout=30)
                except subprocess.TimeoutExpired:pass
            broker.stdout.close()
