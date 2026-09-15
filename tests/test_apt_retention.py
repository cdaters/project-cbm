import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from apt_retention_proxy import canonical

class LocatorTests(unittest.TestCase):
    def test_declared_upstream_uses_https(self):
        self.assertEqual(canonical('http://deb.debian.org/debian/dists/trixie/InRelease'),
                         'https://deb.debian.org/debian/dists/trixie/InRelease')
    def test_private_and_unexpected_origins_rejected(self):
        for url in ['file:///etc/passwd','http://127.0.0.1/x','http://deb.debian.org:80/x',
                    'https://user:secret@deb.debian.org/x','https://evil.invalid/x',
                    'https://deb.debian.org/x?token=secret']:
            with self.subTest(url=url),self.assertRaises(ValueError): canonical(url)
