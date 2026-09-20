"""Real native PTY/SDL dummy readiness test; no physical KMS claim.

Run as UID1000 only inside the isolated native-staging fixture. Inject only the
worker executable and renderer admission boundary; actual pipes/supervisor/SDL/TTY
restoration run from the installed corrective source.
"""
import os,pty,select,sys,time,json,signal
from pathlib import Path
from unittest.mock import patch
assert os.geteuid()==1000
assert Path('/var/lib/project-cbm/native-staging-only').read_text()=='DISPOSABLE PCBM NAMESPACE\n'
sys.path.insert(0,'/usr/libexec/project-cbm')
import boot_session,engineering
rows=[]
for delay in (0,4):
 pid,fd=pty.fork()
 if pid==0:
  try:
   os.environ['SDL_VIDEODRIVER']='dummy';os.environ['SDL_RENDER_DRIVER']='software'
   original=boot_session.subprocess.Popen;real_cover=engineering.run_cover
   worker='source /usr/libexec/project-cbm/boot-trace.sh; sleep "$1"; pcbm_boot_handoff; printf READY; exit 0'
   def popen(argv,**kw):
    if argv==['/usr/libexec/project-cbm/pcbm-console-session','--prepared']:
     argv=['/bin/bash','-c',worker,'fixture',str(delay)]
    return original(argv,**kw)
   def cover(argv,*args,**kw):
    argv=['/usr/bin/python3','/usr/libexec/project-cbm-menu/pcbm_cover_view.py','--boot','/usr/share/project-cbm-menu/covers/pcbmcover1.jpg']
    return real_cover(argv,*args,**kw)
   with patch.object(boot_session.subprocess,'Popen',side_effect=popen),patch.object(engineering,'run_cover',side_effect=cover):
    status=boot_session.run()
   os._exit(status)
  except BaseException:os._exit(9)
 start=time.monotonic();data=b'';status=None
 try:
  while time.monotonic()-start<12:
   if select.select([fd],[],[],.1)[0]:
    try:part=os.read(fd,4096)
    except OSError:part=b''
    data+=part
   got,status=os.waitpid(pid,os.WNOHANG)
   if got:break
  else:os.kill(pid,signal.SIGKILL);os.waitpid(pid,0);raise AssertionError('boot fixture timeout')
  elapsed=time.monotonic()-start
  assert os.waitstatus_to_exitcode(status)==0 and b'READY' in data,(status,data)
  assert elapsed>=max(3,delay) and elapsed<max(3,delay)+3,elapsed
  report=json.loads(Path('/home/pcbm/.local/state/project-cbm/diagnostics/primary-presentation.json').read_text())
  assert report['cleanup']['verified'] and not report['presentation']['timeout'],report
  rows.append({'readiness_seconds':delay,'elapsed_seconds':elapsed,'tty_restored':True,'reaped':True})
 finally:os.close(fd)
print(json.dumps({'result':'PASS','tests':rows,'physical_KMS_visibility':'UNTESTED'},indent=2))
