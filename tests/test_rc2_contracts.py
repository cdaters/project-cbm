"""Focused RC2 identity/import/console contracts; no physical pass inferred."""
import importlib.util,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime'))
from project_cbm import config_backend,importer,admin

class RC2(unittest.TestCase):
 def test_factory_defaults_use_actual_strict_reader_and_correct_image_name(self):
  sys.path.insert(0,str(ROOT/'tools'))
  from build_contracts import read_json
  defaults=read_json(ROOT/'build/pigen/defaults.json')
  self.assertEqual(defaults['boot_presentation']['primary_dwell_milliseconds'],3000)
  self.assertEqual(read_json(ROOT/'build/pigen/config.json')['image_name'],'project-cbm-1.1.0-rc.3')
 def test_reused_runtime_rejects_payload_or_recipe_change(self):
  import io,tarfile
  sys.path.insert(0,str(ROOT/'tools'))
  from freeze_private_candidate import verify_reused_runtime
  with tempfile.TemporaryDirectory() as name:
   root=Path(name);p=root/'runtime/probe';p.parent.mkdir();p.write_bytes(b'original')
   with tarfile.open(root/'source.tar','w') as archive:archive.add(p,arcname='project-cbm/runtime/probe')
   component={'package':{'version':'test'},'source':{'artifact':{'path':'source.tar'}}}
   verify_reused_runtime(root,root,component,'test')
   p.write_bytes(b'changed')
   with self.assertRaises(ValueError):verify_reused_runtime(root,root,component,'test')
   with self.assertRaises(ValueError):verify_reused_runtime(root,root,component,'other')
 def test_policy_allows_only_single_appliance_identity(self):
  baseline=json.loads((ROOT/'runtime/config/configuration-policy.example.json').read_text())
  with patch.object(config_backend,'trusted',side_effect=lambda p:p),patch.object(config_backend,'read_json',return_value=baseline):
   self.assertEqual(config_backend.policy()['owner_user'],'pcbm')
  for key,value in [('owner_user','root'),('owner_user','pi'),('appliance_user','pi'),('appliance_user','other')]:
   with patch.object(config_backend,'trusted',side_effect=lambda p:p),patch.object(config_backend,'read_json',return_value={**baseline,key:value}):
    with self.assertRaises(ValueError):config_backend.policy()
 def test_terminal_same_uid_admin_reauth_no_recursive_login(self):
  self.assertEqual(admin.command('terminal','pcbm'),['/bin/bash','--noprofile','--norc','-i'])
  for action in ('owner','raspi-config'):
   self.assertEqual(admin.command(action,'pcbm')[:3],['/usr/bin/sudo','-k','--'])
  for owner in ('pi','root','pcbm;id',None):
   with self.assertRaises(ValueError):admin.command('owner',owner)
 def test_copy_errors_never_return_private_exception_text(self):
  for error,code in [(PermissionError('/private/secret'),'access_denied'),(OSError('private data'),'copy_failed'),(ValueError('space'),'space'),(ValueError('/private/name'),'copy_failed')]:
   self.assertEqual(importer.copy_failure(error),code)
 def test_getty_removes_only_output_deferral(self):
  text=(ROOT/'build/pigen/stage-cbm/files/getty-autologin.conf').read_text()
  for token in ('Type=simple','Requires=pcbm-first-boot.service','After=pcbm-first-boot.service','--autologin pcbm'):
   self.assertIn(token,text)
  for token in ('--login-program','PAMName=','TTYReset=no','NetworkManager-wait-online'):
   self.assertNotIn(token,text)
 def test_trace_has_only_fixed_phases_and_numeric_uptime(self):
  text=(ROOT/'build/pigen/stage-cbm/files/boot-trace.sh').read_text()
  for token in ('/proc/uptime','umask 077','mktemp','dialog_dispatch','first_input'):
   self.assertIn(token,text)
  for token in ('env\n','set -x','password','logger','sudo'):
   self.assertNotIn(token,text)

if __name__=='__main__':unittest.main()
