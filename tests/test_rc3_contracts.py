import importlib.util,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from freeze_private_candidate import verify_output_identity
from build_contracts import read_json
class RC3(unittest.TestCase):
 def test_current_filename_and_candidate_are_coherent(self):
  verify_output_identity(ROOT,read_json(ROOT/'build/pigen/config.json'),'1.1.0','release')
 def test_stale_export_suffix_is_rejected_before_freeze(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);p=root/'build/pigen/stage-cbm/EXPORT_IMAGE';p.parent.mkdir(parents=True);p.write_text("IMG_SUFFIX='-lite-private-rc1'\n")
   with self.assertRaises(ValueError):verify_output_identity(root,{'image_name':'project-cbm-1.1.0'},'1.1.0','release')
 def test_single_user_contract_applies_to_rc3_validators(self):
  for name in ('validate_activation.py','validate_poc_image.py','validate_poc4_supplement.py'):
   self.assertIn("('private-engineering-rc2','private-engineering-rc3','private-engineering-rc4','release')",(ROOT/'tools'/name).read_text())
if __name__=='__main__':unittest.main()
