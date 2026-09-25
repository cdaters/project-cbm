"""Broker adapters fake all privileged calls; test cleanup and device admission."""
from contextlib import ExitStack
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'runtime'))
from project_cbm import importer


class Broker(unittest.TestCase):
    def perform(self, result, status=0, unmount_error=False, still_mounted=False, timeout=False):
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            base = Path(tmp)
            device = base/'device'
            device.write_bytes(b'fake device')
            entry = {'device': str(device), 'number': '0:0', 'filesystem': 'vfat'}
            def command(args, **kwargs):
                if args[0] == '/usr/bin/umount' and unmount_error:
                    raise subprocess.CalledProcessError(1, args)
                return subprocess.CompletedProcess(args, 0)
            for target, kwargs in [
                ('WORK', {'new': base}), ('trusted', {'side_effect': lambda p:p}),
                ('discover', {'return_value': [entry]}),
                ('os.fork', {'return_value': 12345}), ('stat.S_ISBLK', {'return_value': True}),
                ('os.path.ismount', {'side_effect': [False, still_mounted]}),
                ('os.read', {'return_value': json.dumps(result).encode()}),
                ('os.waitpid', {'return_value': (12345, status)}),
                ('os.kill', {}), ('subprocess.run', {'side_effect': command})]:
                stack.enter_context(patch('project_cbm.importer.'+target, **kwargs))
            stack.enter_context(patch('select.select', return_value=([] if timeout else [1], [], [])))
            return importer.perform(entry, 'games', worker=lambda _: result)

    def test_success_requires_unmount_and_postcheck(self):
        result = self.perform({'status': 'ok', 'saved': 2})
        self.assertIs(result['source_unmounted'], True)
        for kwargs in [{'unmount_error': True}, {'still_mounted': True}]:
            with self.assertRaises(importer.ImportFailure) as error:
                self.perform({'status': 'ok', 'saved': 2}, **kwargs)
            self.assertEqual(error.exception.code, 'unmount_failed')
            self.assertIs(error.exception.source_unmounted, False)
            self.assertEqual(error.exception.result['saved'], 2)

    def test_partial_failure_cleanup_and_worker_failure(self):
        result = self.perform({'status': 'partial', 'saved': 1, 'error': 'space'})
        self.assertEqual(result['saved'], 1)
        self.assertIs(result['source_unmounted'], True)
        with self.assertRaises(importer.ImportFailure) as error:
            self.perform({'error': 'access_denied'}, status=2)
        self.assertEqual(error.exception.code, 'access_denied')
        self.assertIs(error.exception.source_unmounted, True)

    def test_worker_deadline_stops_and_reaps(self):
        with self.assertRaises(importer.ImportFailure) as error:
            self.perform({}, timeout=True)
        self.assertEqual(error.exception.code, 'copy_failed')
        self.assertIs(error.exception.source_unmounted, False)  # conservative on timeout

    def test_removed_or_replaced_device_not_mounted(self):
        with patch.object(importer, 'discover', return_value=[]), patch.object(importer.subprocess, 'run') as command:
            with self.assertRaisesRegex(ValueError, 'device_changed'):
                importer.perform({'device': '/dev/sda1'}, 'games')
            command.assert_not_called()

    def test_multiple_partitions_but_no_mounted_system_or_nonusb_disks(self):
        def disk(name, transport='usb', mounts=None):
            return {'name': '/dev/'+name, 'type': 'disk', 'tran': transport,
                    'mountpoints': mounts, 'children': [
                        {'name': '/dev/'+name+str(n), 'type': 'part', 'fstype': fs,
                         'mountpoints': [], 'size': 100, 'maj:min': '8:'+str(n)}
                        for n, fs in [(1, 'vfat'), (2, 'exfat'), (3, 'ntfs')]]}
        data = {'blockdevices': [disk('sda'), disk('sdb', mounts=['/']), disk('sdc', 'sata')]}
        original = Path.resolve
        def resolve(path, *args, **kwargs):
            return Path('/sys/devices/usb1/fixture') if str(path).startswith('/sys/class/block/') else original(path, *args, **kwargs)
        with patch.object(importer.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps(data))), \
                patch.object(Path, 'resolve', resolve), patch.object(Path, 'read_text', return_value='7'):
            found = importer.discover()
        self.assertEqual([p['device'] for p in found], ['/dev/sda1', '/dev/sda2'])
        self.assertTrue(all(p['diskseq'] == '7' for p in found))

    def test_fixed_mount_flags_unchanged(self):
        self.assertEqual(importer.mount_options('ext4'), 'ro,nodev,nosuid,noexec,noload')
        for fs in ['vfat', 'exfat']:
            self.assertIn('uid=1000,gid=1000,fmask=0177,dmask=0077', importer.mount_options(fs))
        with self.assertRaises(ValueError):
            importer.mount_options('ntfs')


if __name__ == '__main__':
    unittest.main()
