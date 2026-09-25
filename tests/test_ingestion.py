"""Synthetic source, destination and cancellation fixtures; no mount/network access."""
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'runtime'))
from project_cbm import ingestion as core, usb_discovery as usb, ingest_session, importer


class Ingestion(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.source = self.base / 'usb'
        self.dest = self.base / 'content'
        self.source.mkdir()
        self.dest.mkdir()
        self.scanner = usb.Discovery(self.source)
        self.events = []

    def file(self, name, data=b'fixture', root=None):
        path = (root or self.source) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def plan(self, **kwargs):
        return core.plan(list(self.scanner.items.values()), self.dest, self.scanner.open, **kwargs)

    def save(self, plan, **kwargs):
        return core.save(plan, self.dest, self.scanner.open, self.events.append, **kwargs)

    def test_empty_scan_does_not_create_or_copy(self):
        self.assertEqual(self.scanner.scan()['supported'], 0)
        self.assertEqual(list(self.dest.iterdir()), [])
        with self.assertRaisesRegex(core.IngestError, 'selection'):
            self.plan()

    def test_nested_scope_case_dot_and_metadata(self):
        for name in ['Set/disk1.D64', 'Set/sub/disk2.d64', 'Set/.hidden.prg', '.other/a.prg',
                     '.Trashes/old.prg', 'Set/._disk1.D64', 'Set/readme.txt']:
            self.file(name)
        rows = self.scanner.folders_page()['rows']
        scope = next(r['id'] for r in rows if r['name'] == 'Set')
        counts = self.scanner.scan(scope)
        self.assertEqual((counts['supported'], counts['unsupported'], counts['ignored_metadata']), (3, 1, 1))
        self.assertEqual({i.path for i in self.scanner.items.values()}, {'disk1.D64', 'sub/disk2.d64', '.hidden.prg'})
        self.assertFalse(list(self.dest.iterdir()))
        for item in self.scanner.items.values():
            self.assertEqual(item.summary()['family'], 'unknown')
            self.assertEqual(item.summary()['category'], 'unknown')

    def test_symlinks_and_special_files_not_admitted(self):
        good = self.file('good.prg')
        (self.source / 'link.prg').symlink_to(good)
        (self.source / 'linked').symlink_to(self.dest, target_is_directory=True)
        os.mkfifo(self.source / 'pipe.prg')
        result = self.scanner.scan()
        self.assertEqual(result['supported'], 1)
        self.assertEqual(result['unsupported'], 3)

    def test_traversal_and_malicious_components(self):
        for value in ['../escape', '/absolute', 'a//b', 'a/../b', 'a\\b', 'line\nname', 'a/' + 'x'*241]:
            with self.assertRaises(core.IngestError):
                core.relative(value)
        for value in ['bad\tfile.prg', 'bad\nfile.prg']:
            self.file(value)
        self.assertEqual(self.scanner.scan()['unsupported'], 2)

    def test_depth_entry_and_size_limits_leave_no_partial_snapshot(self):
        self.file('a/b/c.prg')
        with patch.object(usb, 'MAX_DEPTH', 1), self.assertRaisesRegex(core.IngestError, 'depth'):
            self.scanner.scan()
        self.assertEqual(self.scanner.items, {})
        with patch.object(usb, 'MAX_ENTRIES', 1), self.assertRaisesRegex(core.IngestError, 'entries'):
            self.scanner.scan()
        with patch.object(usb, 'MAX_BYTES', 1), self.assertRaisesRegex(core.IngestError, 'limit'):
            self.scanner.scan()
        self.assertEqual(list(self.dest.iterdir()), [])

    def test_select_all_individual_folder_and_clear(self):
        for name in ['Set/d1.d64', 'Set/d2.d64', 'Other/a.prg']:
            self.file(name)
        self.scanner.scan()
        self.scanner.select('all')
        self.assertEqual(len(self.scanner.selected), 3)
        first = next(i for i in self.scanner.items.values() if i.path == 'Set/d1.d64')
        self.scanner.select('files', [first.id], False)
        self.assertEqual(len(self.scanner.selected), 2)
        self.scanner.select('clear')
        self.scanner.select('folder', [first.id])
        self.assertEqual(len(self.scanner.selected), 2)
        with self.assertRaises(core.IngestError):
            self.scanner.select('files', ['../../escape'])

    def test_paging_bounded_and_scan_resets_selection(self):
        for i in range(45):
            self.file(f'{i:02}.prg')
        self.scanner.scan()
        generation = self.scanner.generation
        self.assertEqual(len(self.scanner.page()['rows']), 20)
        self.assertEqual(len(self.scanner.page(40)['rows']), 5)
        self.scanner.select('all')
        self.scanner.scan()
        self.assertNotEqual(generation, self.scanner.generation)
        self.assertFalse(self.scanner.selected)

    def test_same_path_identical_is_already_present(self):
        self.file('disk.d64')
        self.scanner.scan()
        first = self.save(self.plan())
        self.assertEqual(first['saved'], 1)
        destination = self.dest / first['destination'] / 'disk.d64'
        inode = destination.stat().st_ino
        second = self.save(self.plan())
        self.assertEqual((second['saved'], second['already_present']), (0, 1))
        self.assertEqual(inode, destination.stat().st_ino)
        self.assertNotEqual(inode, (self.source/'disk.d64').stat().st_ino)

    def test_conflicting_disk_set_gets_predictable_sibling_and_retry(self):
        self.file('Set/disk1.d64', b'original')
        self.file('Set/disk2.d64')
        self.scanner.scan()
        self.save(self.plan())
        self.file('Set/disk1.d64', b'changed!')
        self.scanner.scan()
        plan = self.plan()
        self.assertTrue(plan.kept_both)
        self.assertTrue(plan.destination.endswith('USB Import (2)'))
        self.assertEqual(self.save(plan)['saved'], 2)
        self.assertEqual((self.dest/'programs/shared/Imported/USB Import/Set/disk1.d64').read_bytes(), b'original')
        self.assertTrue((self.dest/'programs/shared/Imported/USB Import (2)/Set/disk2.d64').exists())
        self.assertEqual(self.save(self.plan())['already_present'], 2)

    def test_other_copy_not_hardlinked_or_flattened(self):
        self.file('a/disk.d64')
        self.file('b/disk.d64')
        self.scanner.scan()
        self.save(self.plan())
        a = self.dest/'programs/shared/Imported/USB Import/a/disk.d64'
        b = a.parent.parent/'b/disk.d64'
        self.assertNotEqual(a.stat().st_ino, b.stat().st_ino)
        a.write_bytes(b'changed by emulator')
        self.assertEqual(b.read_bytes(), b'fixture')

    def test_plan_and_scan_never_create_destination(self):
        self.file('game.prg')
        self.scanner.scan()
        self.plan(category='demos', family='c128')
        self.assertFalse(list(self.dest.iterdir()))
        self.assertFalse(self.events)

    def test_low_space_at_plan_and_mid_copy(self):
        self.file('game.prg')
        self.scanner.scan()
        plan = self.plan()
        class Space:
            f_bavail = 1
            f_frsize = 1
        with patch.object(core.os, 'fstatvfs', return_value=Space()):
            with self.assertRaisesRegex(core.IngestError, 'space'):
                self.plan()
            result = self.save(plan)
        self.assertEqual(result['error'], 'space')
        self.assertFalse(list(self.dest.rglob('*.prg')))

    def test_cancel_before_or_during_copy_removes_owned_partial(self):
        self.file('game.prg', b'x'*100)
        self.scanner.scan()
        plan = self.plan()
        self.assertEqual(self.save(plan, cancelled=lambda: True)['status'], 'cancelled')
        calls = iter([False, True])
        result = self.save(plan, cancelled=lambda: next(calls, True))
        self.assertEqual(result['status'], 'cancelled')
        self.assertFalse(list(self.dest.rglob('*.prg')))
        self.assertFalse(list(self.dest.rglob('.pcbm-ingest-*')))

    def test_removed_or_changed_source_fails_before_copy(self):
        p = self.file('game.prg')
        self.scanner.scan()
        plan = self.plan()
        p.unlink()
        self.assertEqual(self.save(plan)['status'], 'failed')
        p.write_bytes(b'replacement')
        self.assertEqual(self.save(plan)['error'], 'source_changed')
        self.assertFalse(list(self.dest.rglob('.pcbm-ingest-*')))

    def test_replaced_source_symlink_never_followed(self):
        p = self.file('game.prg')
        self.scanner.scan()
        plan = self.plan()
        p.unlink()
        p.symlink_to('/etc/passwd')
        self.assertEqual(self.save(plan)['status'], 'failed')
        self.assertFalse(list(self.dest.rglob('game.prg')))

    def test_destination_symlink_and_post_review_collision(self):
        self.file('game.prg')
        self.scanner.scan()
        (self.dest/'programs').symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(core.IngestError):
            self.plan()
        (self.dest/'programs').unlink()
        plan = self.plan()
        existing = self.file(plan.rows[0][1], b'user content', self.dest)
        self.assertEqual(self.save(plan)['error'], 'plan_changed')
        self.assertEqual(existing.read_bytes(), b'user content')

    def test_copy_failure_preserves_completed_files(self):
        self.file('a.prg')
        p = self.file('b.prg')
        self.scanner.scan()
        plan = self.plan()
        p.unlink()
        result = self.save(plan)
        self.assertEqual((result['status'], result['saved'], result['unattempted']), ('partial', 1, 1))
        saved = [r for r in self.events if r['event'] == 'saved']
        self.assertEqual(len(saved), 1)
        self.assertEqual(len(saved[0]['sha256']), 64)
        self.assertEqual(saved[0]['source'], 'usb')

    def test_journal_failure_after_commit_is_partial_not_data_loss(self):
        self.file('a.prg')
        self.scanner.scan()
        def record(event):
            if event['event'] == 'saved':
                raise OSError('full')
        result = core.save(self.plan(), self.dest, self.scanner.open, record)
        self.assertEqual((result['status'], result['saved']), ('partial', 1))
        self.assertEqual(len(list(self.dest.rglob('a.prg'))), 1)

    def test_session_explicit_import_and_private_provenance(self):
        self.file('a.prg')
        state = self.base/'state'
        session = ingest_session.Session(self.source, self.dest, state)
        session.handle({'operation': 'scan'})
        session.handle({'operation': 'select', 'mode': 'all'})
        review = session.handle({'operation': 'plan', 'category': 'programs', 'family': 'shared'})
        self.assertEqual(review['selected'], 1)
        self.assertFalse(state.exists())
        self.assertFalse(list(self.dest.iterdir()))
        result = session.handle({'operation': 'import'})
        self.assertEqual(result['saved'], 1)
        records = [json.loads(l) for l in next(state.glob('*.jsonl')).read_text().splitlines()]
        self.assertEqual([r['event'] for r in records], ['started', 'pending', 'saved', 'finished'])
        self.assertFalse(list(self.dest.rglob('*.json*')))

    def test_session_cancel_and_invalid_requests(self):
        session = ingest_session.Session(self.source, self.dest, self.base/'state')
        for request in [{'operation': 'import'}, {'operation': 'scan', 'path': '/etc'},
                        {'operation': 'folders', 'folder': '../'}, {'operation': 'page', 'offset': True},
                        {'operation': 'select', 'mode': 'files', 'ids': [None]}]:
            with self.assertRaises(core.IngestError):
                session.handle(request)
        self.assertEqual(session.handle({'operation': 'cancel'})['status'], 'cancelled')
        self.assertFalse(list(self.dest.iterdir()))

    def test_session_broker_request_only_accepts_enumerated_token_shape(self):
        request = {'schema_version': 2, 'operation': 'session', 'token': 'a'*32}
        self.assertEqual(importer.validate_request(json.dumps(request)), request)
        for change in [{'token': '/dev/sda1'}, {'path': '/'}, {'schema_version': True}, {'operation': 'exec'}]:
            with self.assertRaises(ValueError):
                importer.validate_request(json.dumps({**request, **change}))


if __name__ == '__main__':
    unittest.main()
