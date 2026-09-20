"""Host metadata never becomes content; meaningful counts and preservation."""
import sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from project_cbm import importer

class Metadata(unittest.TestCase):
 def test_copy_media_excludes_only_named_metadata_and_preserves_duplicates(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);source=root/'usb';source.mkdir();dest=root/'content';dest.mkdir()
   good=['Game/disk1.d64','Game/disk2.D64','Game/disk3.d64','.private/game.prg','Game/.hidden.d64','tape.tap','cart.crt','disk.d81','tune.sid']
   bad=['.DS_Store','._tape.tap','Game/._disk1.d64','.Spotlight-V100/hidden.prg','.Trashes/501/deleted.d64','.fseventsd/log.prg','.AppleDouble/disk.d64','System Volume Information/disk.d64','$RECYCLE.BIN/old.prg']
   for name in good+bad:
    p=source/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'fixture')
   with patch.object(importer,'CONTENT',dest),patch.object(importer.os,'geteuid',return_value=1000):
    first=importer.copy_content(source,'games','c64')
    self.assertEqual(first['copied'],len(good));self.assertEqual(first['ignored_metadata'],len(bad))
    copied=sorted(p for p in dest.rglob('*') if p.is_file())
    self.assertEqual(len(copied),len(good))
    self.assertTrue((dest/'games/c64/Imported/.private/game.prg').exists())
    self.assertTrue((dest/'music/c64/Imported/tune.sid').exists())
    copied[0].write_bytes(b'user content')
    before={str(p):p.read_bytes() for p in copied}
    second=importer.copy_content(source,'games','c64')
    self.assertEqual(second['copied'],0);self.assertEqual(second['skipped'],len(good))
    self.assertEqual(before,{str(p):p.read_bytes() for p in copied})
 def test_hidden_names_are_not_generally_metadata(self):
  for name in ['.demo.prg','.private','__MACOSX_game.prg','Spotlight.prg']:
   self.assertFalse(importer.host_metadata(name))

if __name__=='__main__':unittest.main()
