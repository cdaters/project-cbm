from pathlib import Path
import sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from package_manifest import manifest


class PackageManifest(unittest.TestCase):
    def test_exact_versions_architecture_and_image_binding(self):
        r=manifest(b'zlib1g\t1:1.3.dfsg+really1.3.1-1\tarm64\t170\tinstalled\nold\t1\tall\t0\tconfig-files\n','a'*64)
        self.assertEqual(r['package_count'],1);self.assertEqual(r['image_sha256'],'a'*64)
        self.assertEqual(r['packages'][0]['version'],'1:1.3.dfsg+really1.3.1-1')

    def test_rejects_ambiguous_or_unbound_manifest(self):
        row=b'pkg\t1\tall\t1\tinstalled\n'
        for raw,h in [(row,'bad'),(row+row,'a'*64),(b'pkg\t1\tall\n','a'*64),(b'','a'*64)]:
            with self.assertRaises(ValueError):manifest(raw,h)
