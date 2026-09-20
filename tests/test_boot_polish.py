"""No host boot changes: command-line preservation and one-time completion behavior."""
import importlib.util,json,os,stat,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import boot_presentation as boot
spec=importlib.util.spec_from_file_location('first_boot_polish',ROOT/'build/pigen/stage-cbm/files/first_boot.py')
first=importlib.util.module_from_spec(spec);spec.loader.exec_module(first)

class BootPolish(unittest.TestCase):
 def test_quiet_preserves_console_and_root_parameters(self):
  before='console=serial0,115200 console=tty1 root=PARTUUID=1234-02 rootfstype=ext4 rootwait resize loglevel=7 quiet\n'
  result=boot.cmdline(before)
  for value in ['console=serial0,115200','console=tty1','root=PARTUUID=1234-02','rootfstype=ext4','rootwait']:
   self.assertIn(value,result.split())
  self.assertNotIn('resize',result.split());self.assertNotIn('loglevel=7',result.split())
  self.assertIn('systemd.show_status=auto',result);self.assertEqual(result,boot.cmdline(result))
  with self.assertRaises(ValueError):boot.cmdline('quiet console=tty1')
 def test_firmware_retains_kms_and_no_mode_switch(self):
  original='[pi4]\ndtoverlay=vc4-kms-v3d\n'
  result=boot.firmware(original);self.assertTrue(result.startswith(original))
  self.assertIn('[all]\n# Project CBM boot presentation\ndisable_splash=1',result)
  with self.assertRaises(ValueError):boot.firmware(result)
  self.assertNotIn('framebuffer',result);self.assertNotIn('hdmi_',result)
 def root_lstat(self,path,*a,**kw):
  value=self.lstat(path,*a,**kw);values=list(value);values[4]=0
  return os.stat_result(values)
 def test_completed_boot_skips_all_growth_and_global_sync(self):
  with tempfile.TemporaryDirectory() as d:
   state=Path(d);state.chmod(0o700);(state/'complete.json').write_text('{"schema_version":1,"root_growth_verified":true}');(state/'complete.json').chmod(0o600)
   self.lstat=Path.lstat
   with patch.object(Path,'lstat',lambda p,*a,**kw:self.root_lstat(p,*a,**kw)),patch.object(first,'STATE',state),patch.object(first.os,'geteuid',return_value=0),patch.object(first,'run',side_effect=AssertionError('growth rerun')),patch.object(first.subprocess,'run',side_effect=AssertionError('resize rerun')),patch.object(first.os,'sync',side_effect=AssertionError('global sync rerun')):
    first.main()
 def test_invalid_or_unprotected_completion_never_skips(self):
  with tempfile.TemporaryDirectory() as d:
   state=Path(d);state.chmod(0o700);marker=state/'complete.json'
   self.assertFalse(first.completed(state));self.lstat=Path.lstat
   with patch.object(Path,'lstat',lambda p,*a,**kw:self.root_lstat(p,*a,**kw)):
    for value in ['{}','{','{"schema_version":true,"root_growth_verified":true}','{"schema_version":1,"root_growth_verified":false}']:
     marker.write_text(value)
     with self.assertRaises((ValueError,json.JSONDecodeError)):first.completed(state)
    marker.write_text('{"schema_version":1,"root_growth_verified":true}');marker.chmod(0o666)
    with self.assertRaises(ValueError):first.completed(state)
    marker.chmod(0o644);state.chmod(0o755)
    with self.assertRaises(ValueError):first.completed(state)
 def test_presentation_uses_existing_session_without_delay(self):
  text=(ROOT/'build/pigen/stage-cbm/files/pcbm-console-session').read_text()
  prefix=text.split('# One local setup owner.')[0]
  self.assertIn('boot_session.py',prefix)
  self.assertNotIn('Starting your Commodore computer',text)
  for bad in ['sleep','chvt','sudo','/dev/fb','systemctl']:self.assertNotIn(bad,prefix)
  self.assertIn('/usr/bin/pcbm-first-run',text)
if __name__=='__main__':unittest.main()
