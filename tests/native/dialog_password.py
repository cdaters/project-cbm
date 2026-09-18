"""Real dialog PTY regression; synthetic input only, never print/save its contents.

Run explicitly in disposable native Linux staging with the installed dialog.
The result pipe is separate from the terminal transcript, as in shell capture.
"""
import errno
import os
from pathlib import Path
import pty
import select
import signal
import struct
import fcntl
import termios
import time


def exercise(prompt, locale, masking=True):
    read_result, write_result = os.pipe()
    pid, fd = pty.fork()
    if pid == 0:
        os.close(read_result)
        os.dup2(write_result, 1)
        os.close(write_result)
        fcntl.ioctl(2, termios.TIOCSWINSZ, struct.pack('HHHH',24,80,0,0))
        args=['/usr/bin/dialog','--stdout','--no-mouse','--max-input','128']
        if masking: args.append('--insecure')
        args += ['--passwordbox',prompt,12,76]
        os.execve(args[0],list(map(str,args)),{'PATH':'/usr/bin:/bin','TERM':'linux','LC_ALL':locale})
    os.close(write_result)
    screen=bytearray();sent=False;submitted=False;typed_at=None;status=None;reaped=False
    value=b'Fixture-only-123!'
    deadline=time.monotonic()+5
    try:
        while time.monotonic()<deadline:
            ready,_,_=select.select([fd],[],[],.05)
            if ready:
                try: chunk=os.read(fd,65536)
                except OSError as exc:
                    if exc.errno!=errno.EIO:raise
                    chunk=b''
                screen.extend(chunk)
            if not sent and b'printable' in screen:
                assert value not in Path(f'/proc/{pid}/cmdline').read_bytes()
                os.write(fd,value);sent=True;typed_at=time.monotonic()
            if sent and not submitted and time.monotonic()-typed_at>=.15:
                assert value not in screen
                if masking: assert b'*' in screen, 'no mask feedback'
                os.write(fd,b'\n');submitted=True
            done,status=os.waitpid(pid,os.WNOHANG)
            if done:reaped=True;break
        else:raise AssertionError('dialog PTY deadline')
        assert os.waitstatus_to_exitcode(status)==0
        assert os.read(read_result,512)==value
        assert value not in screen, 'plaintext reached terminal'
        return bytes(screen)
    finally:
        if not reaped:
            try:os.kill(pid,signal.SIGKILL);os.waitpid(pid,0)
            except ProcessLookupError:pass
        os.close(fd);os.close(read_result)


for locale in ('C','C.UTF-8'):
    for guidance in ('12-128 printable characters','8-63 printable ASCII characters'):
        screen=exercise(guidance,locale)
        assert guidance.encode('ascii') in screen
        print('PASS ASCII prompt and masked entry:',locale,guidance)
# Reproduce the old byte-locale rendering mismatch without actual credentials.
old='12\u2013128 printable characters'
old_screen=exercise(old,'C',masking=False)
assert old.encode('utf-8') not in old_screen
print('PASS old UTF-8 dash fails to render intact under C locale; ASCII fixes both locales')
print('PASS result pipe, no initial value, no plaintext terminal or argv; synthetic inputs not retained')
