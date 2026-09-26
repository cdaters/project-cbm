import hashlib
import io
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from freeze_private_candidate import verify_reused_capture

class Reuse(unittest.TestCase):
    def test_exact_inputs_and_artifacts_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);recipe=root/'recipe';source=recipe/'components/pcbm-kms-capture/capture.c'
            source.parent.mkdir(parents=True);source.write_bytes(b'original');source.chmod(0o644)
            archive=root/'source.tar'
            with tarfile.open(archive,'w') as t:
                m=tarfile.TarInfo('project-cbm/components/pcbm-kms-capture/capture.c');m.size=8;m.mode=0o644;t.addfile(m,io.BytesIO(b'original'))
            package=root/'package.deb';package.write_bytes(b'exact retained package')
            def pin(p):return {'path':p.name,'size_bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            component={'source':{'artifact':pin(archive)},'package':{'artifact':pin(package)}}
            verify_reused_capture(root,recipe,component)
            source.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'changed'):verify_reused_capture(root,recipe,component)
            source.write_bytes(b'original');source.chmod(0o755)
            with self.assertRaisesRegex(ValueError,'changed'):verify_reused_capture(root,recipe,component)
            source.chmod(0o644);package.write_bytes(b'other')
            with self.assertRaises(ValueError):verify_reused_capture(root,recipe,component)
