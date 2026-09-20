"""Apply the initramfs hook to synthetic script bytes, preserve failure semantics."""
import os,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HOOK=ROOT/'build/pigen/stage-cbm/files/pcbm-quiet-fsck'
class QuietFsck(unittest.TestCase):
 def test_quiet_success_retains_log_and_all_nonzero_results_remain_visible(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);scripts=root/'scripts';scripts.mkdir();p=scripts/'functions'
   p.write_text('''#!/bin/sh
FSCK_LOGFILE=fixture
spinner= force= fix= TYPE=ext4 DEV=fixture
logsave() { printf 'filesystem result\\n'; return "$TEST_STATUS"; }
if [ "$TEST_QUIET" = n ]; then
 logsave verbose
 FSCKCODE=$?
else
\t\tlogsave -a -s $FSCK_LOGFILE fsck $spinner $force $fix -T -t "$TYPE" "$DEV"
\t\tFSCKCODE=$?
fi
exit "$FSCKCODE"
''')
   subprocess.run(['/bin/sh',str(HOOK)],env={**os.environ,'DESTDIR':str(root)},check=True)
   text=p.read_text();self.assertIn('logsave -a -s $FSCK_LOGFILE',text)
   # Redirect the fixture's captured output into its private temporary directory.
   p.write_text(text.replace('/run/initramfs/pcbm-fsck.console',str(root/'console')))
   for quiet,status in [('y',0),('y',1),('y',4),('y',32),('n',0)]:
    result=subprocess.run(['/bin/sh',str(p)],env={**os.environ,'TEST_STATUS':str(status),'TEST_QUIET':quiet},text=True,capture_output=True)
    self.assertEqual(result.returncode,status)
    self.assertEqual(bool(result.stdout),quiet=='n' or status!=0)
   p.write_text('unexpected vendor code')
   result=subprocess.run(['/bin/sh',str(HOOK)],env={**os.environ,'DESTDIR':str(root)},capture_output=True)
   self.assertNotEqual(result.returncode,0);self.assertEqual(p.read_text(),'unexpected vendor code')
if __name__=='__main__':unittest.main()
