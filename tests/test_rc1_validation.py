"""Read-only validator accepts exact new queries and rejects widened probing."""
import ast,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import validate_rc1 as validator

class NetworkAllowlist(unittest.TestCase):
 def check(self,source):
  with tempfile.TemporaryDirectory() as name:
   root=Path(name);p=root/'usr/share/project-cbm/runtime/project_cbm/network_info.py';p.parent.mkdir(parents=True);p.write_text(source)
   with patch.object(validator,'previous_inspect',return_value={'checks':{'other_gate':True}}):
    return validator.inspect_runtime(root,{},root)['result']
 def test_current_gateway_dns_queries_pass_without_execution(self):
  source=(ROOT/'runtime/project_cbm/network_info.py').read_text()
  self.assertEqual(self.check(source+"\nraise RuntimeError('must never execute target code')\n"),'PASS')
 def test_secret_or_connection_probe_fails(self):
  source=(ROOT/'runtime/project_cbm/network_info.py').read_text()
  for replacement in (source.replace("'--terse'","'--show-secrets'"),source.replace("'device', 'show'","'connection', 'show'")):
   self.assertEqual(self.check(replacement),'FAIL')
 def test_missing_dns_field_fails(self):
  source=(ROOT/'runtime/project_cbm/network_info.py').read_text().replace(',IP6.DNS','')
  self.assertEqual(self.check(source),'FAIL')
if __name__=='__main__':unittest.main()
