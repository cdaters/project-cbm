"""Storage and template safety independent of a VM."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import build_host as host


class HostTests(unittest.TestCase):
    def test_external_containment(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            self.assertEqual(host.contained(root, 'build-host/tmp'), root/'build-host/tmp')
            with self.assertRaises(ValueError):
                host.contained(root, '../escape')
            (root/'escape').symlink_to('/private/tmp')
            with self.assertRaises(ValueError):
                host.contained(root, 'escape/data')

    def test_cache_preserves_existing(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            link = home/'Library/Caches/lima'
            link.mkdir(parents=True)
            sentinel = link/'unrelated'; sentinel.write_text('keep')
            with patch.object(Path, 'home', return_value=home):
                with self.assertRaises(ValueError):
                    host.cache_guard({'cache': home/'external'}, create=True)
            self.assertEqual(sentinel.read_text(), 'keep')

    def test_cache_missing_rejected_and_link_verified(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp).resolve()
            (home/'Library/Caches').mkdir(parents=True)
            cache = home/'external'; cache.mkdir()
            with patch.object(Path, 'home', return_value=home):
                with self.assertRaises(ValueError): host.cache_guard({'cache': cache})
                host.cache_guard({'cache': cache}, create=True)
                host.cache_guard({'cache': cache})
                with self.assertRaises(ValueError): host.cache_guard({'cache': home/'wrong'})

    def test_digest_mismatch_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'input'; path.write_bytes(b'controlled input')
            pin = {'algorithm':'sha256', 'digest':host.digest(path,'sha256')}
            host.verify(path,pin)
            path.write_bytes(b'changed')
            with self.assertRaises(ValueError): host.verify(path,pin)
            link=Path(temp)/'link'; link.symlink_to(path)
            with self.assertRaises(ValueError): host.verify(link,pin)

    def test_template_pin_consistency(self):
        pins=json.loads(host.PINS.read_text())
        template=(host.REPO/'build/host/lima.yaml').read_text()
        self.assertIn(pins['guest']['digest'],template)
        self.assertEqual(template.count('__GUEST_IMAGE_JSON__'),1)
        self.assertNotIn('template:',template)


if __name__ == '__main__': unittest.main()
