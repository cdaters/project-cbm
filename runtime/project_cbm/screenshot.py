"""On-demand, private, atomic screenshots. The privileged component has no paths."""
import datetime
import os
import pwd
import re
import selectors
import signal
import stat
import struct
import subprocess
import sys
import time
import zlib

HELPER = ('/usr/bin/sudo', '-n', '--', '/usr/libexec/pcbm-kms-capture')
HOME = '/home/pcbm'
MAX_PNG = 52 * 1024 * 1024
TIMEOUT = 12
ERRORS = {20: 'no active display', 21: 'unsupported display configuration',
          22: 'permission or setup unavailable', 24: 'display changed during capture'}


class Unavailable(Exception):
    pass


def basename(value):
    if (not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,123}\.png', value)
            or '..' in value):
        raise Unavailable('use a basename ending in .png')
    return value


def output_directory(home, uid):
    # Open every path component independently, so ancestors cannot redirect us.
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        for part in home.strip('/').split('/'):
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
            os.close(fd)
            fd = child
        if os.fstat(fd).st_uid != uid:
            raise Unavailable('private output directory unavailable')
        # The authenticated content share runs as this same account. Do not
        # relax screenshot permissions or follow a replaced content directory.
        try:
            os.mkdir('content', 0o755, dir_fd=fd)
        except FileExistsError:
            pass
        child = os.open('content', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
        os.close(fd)
        fd = child
        if os.fstat(fd).st_uid != uid:
            raise Unavailable('private output directory unavailable')
        try:
            os.mkdir('screenshots', 0o700, dir_fd=fd)
        except FileExistsError:
            pass
        child = os.open('screenshots', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
        try:
            if os.fstat(child).st_uid != uid:
                raise Unavailable('private output directory unavailable')
            os.fchmod(child, 0o700)
        except BaseException:
            os.close(child)
            raise
        return child
    finally:
        os.close(fd)


def validate_png(stream):
    """Check framing/CRC/size and exact RGB contract without decoding privileged data."""
    stream.seek(0)
    if stream.read(8) != b'\x89PNG\r\n\x1a\n':
        raise Unavailable('capture failed')
    first = True
    data_seen = False
    decoded = 0
    decoder = zlib.decompressobj()
    expected = 0
    while True:
        header = stream.read(8)
        if len(header) != 8:
            raise Unavailable('capture failed')
        length, kind = struct.unpack('>I4s', header)
        if length > MAX_PNG or kind not in (b'IHDR', b'IDAT', b'IEND'):
            raise Unavailable('capture failed')
        value = stream.read(length)
        crc = stream.read(4)
        if len(value) != length or len(crc) != 4 or struct.unpack('>I', crc)[0] != zlib.crc32(kind + value):
            raise Unavailable('capture failed')
        if first:
            if kind != b'IHDR' or length != 13:
                raise Unavailable('capture failed')
            w, h, depth, color, compression, filtering, interlace = struct.unpack('>IIBBBBB', value)
            if not (0 < w <= 4096 and 0 < h <= 4096 and (depth, color, compression, filtering, interlace) == (8, 2, 0, 0, 0)):
                raise Unavailable('unsupported display configuration')
            expected = (w * 3 + 1) * h
            first = False
        elif kind == b'IHDR':
            raise Unavailable('capture failed')
        elif kind == b'IDAT':
            data_seen = True
            try:
                decoded += len(decoder.decompress(value, expected - decoded + 1))
            except zlib.error:
                raise Unavailable('capture failed') from None
            if decoded > expected or decoder.unconsumed_tail or decoder.unused_data:
                raise Unavailable('capture failed')
        elif kind == b'IEND':
            if length or not data_seen or stream.read(1) or not decoder.eof or decoded != expected:
                raise Unavailable('capture failed')
            return


def capture(stream, command=HELPER, timeout=TIMEOUT):
    # A pipe, never a PTY: binary output must not pass through terminal processing.
    p = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL, start_new_session=True, close_fds=True,
                         env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'})
    deadline = time.monotonic() + timeout
    total = 0
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(p.stdout, selectors.EVENT_READ)
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not selector.select(remaining):
                    raise Unavailable('capture timed out')
                chunk = os.read(p.stdout.fileno(), 65536)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_PNG:
                    raise Unavailable('capture failed')
                stream.write(chunk)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise Unavailable('capture timed out')
        rc = p.wait(timeout=remaining)
        if rc:
            raise Unavailable(ERRORS.get(rc, 'capture failed'))
    except subprocess.TimeoutExpired:
        raise Unavailable('capture timed out') from None
    finally:
        if p.poll() is None:
            # sudo propagates TERM; the fixed helper also has its own 10 s alarm.
            try:
                os.killpg(p.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                p.wait(timeout=1)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(p.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                p.wait()
        p.stdout.close()


def save(name=None, *, home=HOME, uid=1000, command=HELPER, timeout=TIMEOUT):
    automatic = name is None
    if automatic:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        name = 'pcbm-' + stamp + '.png'
    basename(name)
    directory = output_directory(home, uid)
    try:
        try:
            os.stat(name, dir_fd=directory, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            if not automatic:
                raise Unavailable('filename already exists')
        # Linux ext4 anonymous inode: even SIGKILL/power loss leaves no partial
        # named PNG. Publish with linkat only after successful validation+fsync.
        fd = os.open('.', os.O_RDWR | os.O_TMPFILE | os.O_CLOEXEC, 0o600, dir_fd=directory)
        with os.fdopen(fd, 'w+b') as stream:
            os.fchmod(stream.fileno(), 0o600)
            capture(stream, command, timeout)
            stream.flush()
            validate_png(stream)
            os.fsync(stream.fileno())
            # The directory must still be the one addressed by the printed path.
            current = output_directory(home, uid)
            try:
                a, b = os.fstat(directory), os.fstat(current)
                if (a.st_dev, a.st_ino) != (b.st_dev, b.st_ino):
                    raise Unavailable('private output directory unavailable')
            finally:
                os.close(current)
            stem = name[:-4]
            for sequence in range(1000):
                candidate = name if sequence == 0 else f'{stem}-{sequence:02d}.png'
                try:
                    os.link('/proc/self/fd/' + str(stream.fileno()), candidate,
                            dst_dir_fd=directory, follow_symlinks=True)
                    name = candidate
                    break
                except FileExistsError:
                    if not automatic:
                        raise Unavailable('filename already exists') from None
            else:
                raise Unavailable('too many captures in this second')
            os.fsync(directory)
        return home + '/content/screenshots/' + name
    finally:
        os.close(directory)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    def interrupted(signum, frame):
        raise Unavailable('capture interrupted')
    for sig in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
        signal.signal(sig, interrupted)
    try:
        account = pwd.getpwnam('pcbm')
        if os.getuid() != 1000 or os.geteuid() != 1000 or account.pw_uid != 1000 or account.pw_dir != HOME:
            raise Unavailable('run as the Project CBM user')
        if len(args) > 1:
            raise Unavailable('usage: pcbm-screenshot [basename.png]')
        print(save(args[0] if args else None))
        return 0
    except (Unavailable, OSError, KeyError, ValueError, subprocess.SubprocessError) as e:
        message = str(e) if isinstance(e, Unavailable) else 'capture unavailable'
        print('Screenshot unavailable: ' + message + '.', file=sys.stderr)
        return 1
