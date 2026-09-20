"""Pipe-based readiness and bounded process release; no real display required."""
import importlib.util,os,subprocess,sys,tempfile,time,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('handoff_engineering',ROOT/'build/pigen/stage-cbm/files/engineering.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)

class Handoff(unittest.TestCase):
 def test_readiness_releases_renderer_and_allows_next_ui_after_eof(self):
  ready_r,ready_w=os.pipe();ack_r,ack_w=os.pipe();release_r,release_w=os.pipe()
  script='source "$1"; pcbm_boot_handoff; printf screen1; PCBM_BOOT_READY_FD=$2 PCBM_BOOT_ACK_FD=$3 pcbm_boot_handoff; printf screen2'
  env={**os.environ,'PCBM_BOOT_READY_FD':str(ready_w),'PCBM_BOOT_ACK_FD':str(ack_r)}
  worker=subprocess.Popen(['bash','-c',script,'fixture',str(ROOT/'build/pigen/stage-cbm/files/boot-trace.sh'),str(ready_w),str(ack_r)],env=env,pass_fds=(ready_w,ack_r),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  try:
   result=e.run_cover([sys.executable,'-c','import os,sys; assert os.read(int(sys.argv[1]),1)==b"1"',str(release_r)],None,lambda child:None,timeout=2,pass_fds=(release_r,),handoff=(ready_r,release_w))
   self.assertEqual(result['exit_status'],0);self.assertFalse(result['timeout']);self.assertIn('ready_monotonic',result)
   self.assertIsNone(worker.poll())
   os.write(ack_w,b'1\n');os.close(ack_w);ack_w=None
   out,err=worker.communicate(timeout=2);self.assertEqual(worker.returncode,0,err);self.assertEqual(out,b'screen1screen2')
  finally:
   if worker.poll() is None:worker.kill();worker.wait()
   for fd in [ready_r,ready_w,ack_r,ack_w,release_r,release_w]:
    if fd is not None:os.close(fd)
 def test_failed_renderer_does_not_wait_for_worker_ready(self):
  a,b=os.pipe();c,d=os.pipe()
  try:
   start=time.monotonic();result=e.run_cover([sys.executable,'-c','raise SystemExit(1)'],None,lambda child:None,timeout=2,handoff=(a,d))
   self.assertEqual(result['exit_status'],1);self.assertFalse(result['timeout']);self.assertLess(time.monotonic()-start,1)
  finally:
   for fd in [a,b,c,d]:os.close(fd)
 def test_unresponsive_renderer_is_killed_and_reaped(self):
  result=e.run_cover([sys.executable,'-c','import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(5)'],None,lambda child:None,timeout=.2,grace=.1)
  self.assertTrue(result['timeout']);self.assertTrue(result['killed'])
  with self.assertRaises(ChildProcessError):os.waitpid(result['pid'],os.WNOHANG)

if __name__=='__main__':unittest.main()
