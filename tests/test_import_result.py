"""Broker/client/Menu result boundary; synthetic failures never mount real media."""
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runtime'))
from project_cbm import import_client, importer

REQUEST = {'schema_version': 1, 'operation': 'import', 'token': 'a' * 32,
           'category': 'games'}


class Results(unittest.TestCase):
    def client(self, answer, code):
        with patch.object(sys, 'argv', ['pcbm-import-operation']), \
                patch.object(sys, 'stdin', io.TextIOWrapper(io.BytesIO(json.dumps(REQUEST).encode()))), \
                patch.object(sys, 'stdout', new_callable=io.StringIO) as output, \
                patch.object(import_client.subprocess, 'run', return_value=subprocess.CompletedProcess([], code, json.dumps(answer), 'private diagnostic')):
            status = import_client.main()
            return status, json.loads(output.getvalue())

    def test_success_preserves_metadata_and_confirmed_release(self):
        reply = {'schema_version': 1, 'status': 'ok', 'copied': 2, 'skipped': 3,
                 'bytes': 42, 'ignored_metadata': 5, 'source_unmounted': True}
        self.assertEqual(self.client(reply, 0), (0, reply))
        del reply['ignored_metadata']
        self.assertEqual(self.client(reply, 0)[1]['ignored_metadata'], 0)

    def test_partial_copy_failure_and_cleanup_failure_reach_menu(self):
        bridge = ROOT.parent / 'project-cbm-menu/lib/pcbm_config_bridge.py'
        for error, released in [('space', True), ('access_denied', True),
                                ('copy_failed', False), ('unmount_failed', False),
                                ('unavailable', None)]:
            reply = {'schema_version': 1, 'status': 'failed', 'error': error,
                     'source_unmounted': released}
            code, answer = self.client({**reply, 'message': 'private diagnostic'}, 2)
            self.assertEqual((code, answer), (2, reply))
            p = subprocess.run([sys.executable, str(bridge), 'import-error'],
                               input=json.dumps(answer), text=True, capture_output=True)
            self.assertNotIn('private diagnostic', p.stdout)
            self.assertIn('safe to remove' if released else 'release was not confirmed', p.stdout)
            self.assertIn('New files copied before the error remain', p.stdout)

    def test_malformed_or_missing_cleanup_is_never_success(self):
        base = {'schema_version': 1, 'status': 'ok', 'copied': 1, 'skipped': 0, 'bytes': 1}
        for change in [{}, {'source_unmounted': False}, {'source_unmounted': 'true'},
                       {'source_unmounted': 1}, {'schema_version': True},
                       {'source_unmounted': True, 'ignored_metadata': -1},
                       {'source_unmounted': True, 'copied': True}]:
            code, reply = self.client({**base, **change}, 0)
            self.assertEqual(code, 2)
            self.assertIsNone(reply['source_unmounted'])
        for reply in [[], None, {'schema_version': 1, 'status': 'failed', 'error': 'private'},
                      {'schema_version': 1, 'status': 'failed', 'error': [], 'source_unmounted': True},
                      {'schema_version': 1, 'status': 'failed', 'error': 'unmount_failed', 'source_unmounted': True}]:
            self.assertIsNone(self.client(reply, 2)[1]['source_unmounted'])

    def test_exit_status_must_agree_with_reply(self):
        reply = {'schema_version': 1, 'status': 'failed', 'error': 'space', 'source_unmounted': True}
        for code in [0, 1, -15]:
            self.assertIsNone(self.client(reply, code)[1]['source_unmounted'])

    def test_timeout_remains_unconfirmed(self):
        with patch.object(sys, 'argv', ['client']), \
                patch.object(sys, 'stdin', io.TextIOWrapper(io.BytesIO(json.dumps(REQUEST).encode()))), \
                patch.object(sys, 'stdout', new_callable=io.StringIO) as output, \
                patch.object(import_client.subprocess, 'run', side_effect=subprocess.TimeoutExpired('broker', 600)):
            self.assertEqual(import_client.main(), 2)
            self.assertIsNone(json.loads(output.getvalue())['source_unmounted'])


if __name__ == '__main__':
    unittest.main()
