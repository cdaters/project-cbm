"""Synthetic files only: preserve canonical ownership, existing files and machine choices."""
import json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from project_cbm import library,importer,applications
from project_cbm.data import registry

class Library(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name).resolve()
 def file(self,relative):
  p=self.root/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'\x01\x08fixture');return p
 def test_family_routing_preserves_compatible_preferred_variant(self):
  for family,expected in [('c64','x64sc'),('c128','x128'),('vic20','xvic'),('plus4','xplus4'),('pet','xpet'),('cbm2','xcbm2'),('cbm5x0','xcbm5x0')]:
   p=self.file('games/'+family+'/demo.prg')
   self.assertEqual(library.content_profile(p,registry(),'x64sc',self.root),expected)
  p=self.file('demos/c128/80col/demo.prg')
  self.assertEqual(library.content_profile(p,registry(),'x64sc',self.root),'x128-80col')
  p=self.file('games/c64/example.prg')
  self.assertEqual(library.content_profile(p,registry(),'x64',self.root),'x64')
 def test_shared_and_legacy_do_not_guess_machine(self):
  for relative in ['games/shared/example.prg','demos/Imported/example.prg','demos/kong.prg']:
   self.assertEqual(library.content_profile(self.file(relative),registry(),'xvic',self.root),'xvic')
 def test_rom_resources_and_symlink_escapes_do_not_autostart(self):
  for name in ['roms/c64/kernel.rom','games/c64/expansion.reu','programs/c64/kernel.bin']:
   with self.assertRaises(ValueError):library.content_profile(self.file(name),registry(),'x64sc',self.root)
  outside=self.file('outside.prg');link=self.root/'games/c64/link.prg';link.symlink_to(outside)
  with self.assertRaises(ValueError):library.content_profile(link,registry(),'x64sc',self.root)
 def test_layout_is_type_first_and_no_format_sprawl(self):
  dirs=list(map(str,library.directories()))
  self.assertIn('demos/c64',dirs);self.assertIn('games/pet',dirs)
  self.assertNotIn('music/pet',dirs);self.assertNotIn('roms/shared',dirs)
  self.assertFalse(any(set(Path(d).parts)&{'disk','tape','cart','prg'} for d in dirs))
 def test_import_family_boundary_and_sid_destination(self):
  request={'schema_version':1,'operation':'import','token':'a'*32,'category':'games','family':'c128'}
  self.assertEqual(importer.validate_request(json.dumps(request)),request)
  for bad in ['../../pcbm','c64;id',None,[], 'other']:
   with self.assertRaises(ValueError):importer.validate_request(json.dumps({**request,'family':bad}))
  self.assertEqual(library.import_destination('games','.prg','c128'),('games','c128','Imported'))
  self.assertEqual(library.import_destination('games','.sid','shared'),('music','c64','Imported'))
 def test_import_copies_preserves_conflicts_and_uses_canonical_library(self):
  source=self.root/'usb';source.mkdir();(source/'example.prg').write_bytes(b'\x01\x08new');(source/'example.sid').write_bytes(b'fixture')
  dest=self.root/'library';dest.mkdir()
  with patch.object(importer,'CONTENT',dest),patch.object(importer.os,'geteuid',return_value=1000):
   result=importer.copy_content(source,'demos','c64');self.assertEqual(result['copied'],2)
   p=dest/'demos/c64/Imported/example.prg';p.write_bytes(b'user')
   self.assertEqual(importer.copy_content(source,'demos','c64')['copied'],0);self.assertEqual(p.read_bytes(),b'user')
  self.assertTrue((dest/'music/c64/Imported/example.sid').is_file())
  self.assertEqual(library.ROOT,Path('/home/pcbm/content'));self.assertEqual(importer.CONTENT,library.ROOT);self.assertEqual(applications.CONTENT_ROOT,library.ROOT)
if __name__=='__main__':unittest.main()
