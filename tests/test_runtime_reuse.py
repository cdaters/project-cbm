"""Development package reuse compares actual safe-extracted inputs, never just versions."""
import io
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from freeze_private_candidate import verify_reused_runtime


class RuntimeReuse(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        base=Path(self.temp.name);self.old=base/'old';self.old.mkdir();self.recipe=base/'recipe'
        (self.recipe/'runtime').mkdir(parents=True)
        self.file=self.recipe/'runtime/example.py';self.file.write_bytes(b'original\n');self.file.chmod(0o644)
        self.component={'package':{'version':'1.2.0~dev1-1'},'source':{'artifact':{'path':'source.tar'}}}
        with tarfile.open(self.old/'source.tar','w') as archive:
            member=tarfile.TarInfo('project-cbm/runtime/example.py');member.mode=0o664;member.size=9
            archive.addfile(member,io.BytesIO(b'original\n'))

    def verify(self,**kwargs):
        verify_reused_runtime(self.old,self.recipe,self.component,'1.2.0~dev1-1',**kwargs)

    def test_safe_extraction_mode_matches_only_explicit_development_path(self):
        self.verify(extracted_permissions=True)
        with self.assertRaises(ValueError):self.verify()

    def test_changed_bytes_are_rejected(self):
        self.file.write_bytes(b'changed!\n')
        with self.assertRaises(ValueError):self.verify(extracted_permissions=True)

    def test_changed_executable_permission_is_rejected(self):
        self.file.chmod(0o755)
        with self.assertRaises(ValueError):self.verify(extracted_permissions=True)


if __name__=='__main__':unittest.main()
