"""Private screenshot publication; native tests exercise actual Linux inodes."""
import concurrent.futures
import importlib.util
import io
import os
from pathlib import Path
import signal
import stat
import struct
import subprocess
import sys
import tempfile
import time
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runtime'))
from project_cbm import screenshot as s


def png():
    def chunk(k, v):
        return struct.pack('>I', len(v)) + k + v + struct.pack('>I', zlib.crc32(k + v))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 2, 1, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(b'\0\xff\0\0\0\xff\0')) + chunk(b'IEND', b''))


class Contract(unittest.TestCase):
    def test_names(self):
        for name in ('hello.png', 'test-1_2.png'):
            self.assertEqual(s.basename(name), name)
        for name in ('../a.png', '/tmp/a.png', 'a/b.png', 'a\\b.png', '..png', 'a..png', '.a.png',
                     'a.PNG', 'a.png\n', '-a.png', 'x' * 129 + '.png', '', 'a\0.png'):
            with self.subTest(name=repr(name)), self.assertRaises(s.Unavailable): s.basename(name)

    def test_png(self):
        s.validate_png(io.BytesIO(png()))
        for data in (b'', png()[:-1], png() + b'x', png().replace(b'IDAT', b'XXXX')):
            with self.assertRaises(s.Unavailable): s.validate_png(io.BytesIO(data))

    def test_helper_contract(self):
        self.assertEqual(s.HELPER, ('/usr/bin/sudo', '-n', '--', '/usr/libexec/pcbm-kms-capture'))
        source = (ROOT / 'components/pcbm-kms-capture/capture.c').read_text()
        for forbidden in ('drmSetMaster(', 'drmModeSetCrtc(', 'drmModeSetPlane(', 'PROT_WRITE', 'execve(', 'system('):
            self.assertNotIn(forbidden, source)
        self.assertIn('if(!drop())', source)
        self.assertLess(source.index('if(!drop())'), source.index('if(!rc)rc=encode'))


@unittest.skipUnless(sys.platform == 'linux', 'Linux O_TMPFILE/linkat publication')
class Publication(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.command = (sys.executable, '-c', 'import sys;sys.stdout.buffer.write(' + repr(png()) + ')')

    def save(self, name=None, **kwargs):
        return s.save(name, home=str(self.home), uid=os.getuid(), command=kwargs.pop('command', self.command), **kwargs)

    def test_modes_and_default_unique(self):
        first, second = Path(self.save()), Path(self.save())
        self.assertNotEqual(first, second)
        self.assertRegex(first.name, r'^pcbm-\d{8}T\d{6}Z-[0-9a-f]{32}\.png$')
        self.assertEqual(first.read_bytes(), png())
        self.assertEqual(stat.S_IMODE(first.stat().st_mode), 0o600)
        self.assertEqual(first.stat().st_uid, os.getuid())
        self.assertEqual(stat.S_IMODE(first.parent.stat().st_mode), 0o700)

    def test_overwrite_and_file_symlink(self):
        path = Path(self.save('one.png'))
        with self.assertRaises(s.Unavailable): self.save('one.png')
        (path.parent / 'two.png').symlink_to(path)
        with self.assertRaises(s.Unavailable): self.save('two.png')
        self.assertEqual(path.read_bytes(), png())

    def test_directory_and_ancestor_symlink(self):
        (self.home / 'screenshots').symlink_to(self.home, target_is_directory=True)
        with self.assertRaises(OSError): self.save()
        (self.home / 'screenshots').unlink()
        link = self.home / 'link'
        link.symlink_to(self.home, target_is_directory=True)
        with self.assertRaises(OSError): s.save(home=str(link), uid=os.getuid(), command=self.command)

    def test_existing_directory_becomes_private(self):
        d = self.home / 'screenshots'; d.mkdir(mode=0o755)
        self.save()
        self.assertEqual(stat.S_IMODE(d.stat().st_mode), 0o700)

    def test_concurrent_no_overwrite(self):
        def attempt(_):
            try: return self.save('shared.png')
            except s.Unavailable: return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(attempt, range(8)))
        self.assertEqual(sum(x is not None for x in results), 1)
        self.assertEqual(list((self.home / 'screenshots').iterdir())[0].read_bytes(), png())

    def test_errors_and_partial_cleanup(self):
        for code in (20, 21, 22, 23, 24, 1):
            command = (sys.executable, '-c', 'import sys;sys.stdout.buffer.write(b"partial");sys.exit(' + str(code) + ')')
            with self.assertRaisesRegex(s.Unavailable, s.ERRORS.get(code, 'capture failed')):
                self.save(command=command)
        self.assertEqual(list((self.home / 'screenshots').iterdir()), [])

    def test_partial_success_rejected(self):
        with self.assertRaises(s.Unavailable):
            self.save(command=(sys.executable, '-c', 'print("partial")'))
        self.assertEqual(list((self.home / 'screenshots').iterdir()), [])

    def test_timeout(self):
        start = time.monotonic()
        with self.assertRaisesRegex(s.Unavailable, 'timed out'):
            self.save(command=(sys.executable, '-c', 'import time;print("partial",flush=True);time.sleep(20)'), timeout=.1)
        self.assertLess(time.monotonic() - start, 2)
        self.assertEqual(list((self.home / 'screenshots').iterdir()), [])

    def test_killed_writer_leaves_no_partial(self):
        code = ('import sys;sys.path.insert(0,' + repr(str(ROOT / 'runtime')) + ');'
                'from project_cbm.screenshot import save;save(home=' + repr(str(self.home)) +
                ',uid=' + str(os.getuid()) + ',command=' + repr((sys.executable, '-c', 'import time;time.sleep(2)')) + ')')
        p = subprocess.Popen((sys.executable, '-c', code), start_new_session=True)
        try:
            deadline = time.monotonic() + 3
            while not (self.home / 'screenshots').exists() and time.monotonic() < deadline: time.sleep(.01)
            os.killpg(p.pid, signal.SIGKILL); p.wait()
            self.assertEqual(list((self.home / 'screenshots').iterdir()), [])
        finally:
            if p.poll() is None: p.kill(); p.wait()

    def test_no_descriptor_leak(self):
        before = len(os.listdir('/proc/self/fd'))
        for _ in range(5): self.save()
        self.assertEqual(len(os.listdir('/proc/self/fd')), before)


if __name__ == '__main__': unittest.main()
