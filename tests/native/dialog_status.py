import fcntl,json,os,pty,select,signal,struct,termios,time
from pathlib import Path
assert Path('/var/lib/project-cbm/native-staging-only').is_file()
records=[]
for cols,rows in [(80,24),(40,12),(100,36)]:
 pid,fd=pty.fork()
 if pid==0:
  fcntl.ioctl(0,termios.TIOCSWINSZ,struct.pack('HHHH',rows,cols,0,0))
  os.environ.update(TERM='xterm',LC_ALL='C.UTF-8',COLUMNS=str(cols),LINES=str(rows))
  script="source /usr/share/project-cbm-menu/pcbm-ui.sh; pcbm_ui_menu 'File Sharing' $'Status: On\\nComputer Name: projectcbm\\nEthernet: 192.0.2.12\\nUsername: owner\\nSeparate File Sharing password: Set\\nNetwork Discovery: On\\nChoose a setting.' DISABLE 'Turn Off File Sharing' PASSWORD 'Set / change File Sharing password' CONNECTION 'How to connect' REFRESH 'Refresh status' BACK Back; printf '\\nTEST_RESULT=%s\\n' \"$?\""
  os.execv('/bin/bash',['bash','-c',script])
 raw=b'';sent=False;end=time.monotonic()+4
 try:
  while time.monotonic()<end:
   if select.select([fd],[],[],.1)[0]:
    try:data=os.read(fd,65536)
    except OSError:break
    raw+=data
   if not sent and b'File Sharing' in raw:
    os.write(fd,b'\x1b\x1b');sent=True
   if b'TEST_RESULT=' in raw:break
  records.append({'size':[cols,rows],'rendered':b'File Sharing' in raw,'cancelled':b'TEST_RESULT=2' in raw,'error':b'TEST_RESULT=3' in raw})
 finally:
  os.close(fd)
  try:os.kill(pid,signal.SIGKILL)
  except ProcessLookupError:pass
  os.waitpid(pid,0)
print(json.dumps(records))
assert all(r['rendered'] and r['cancelled'] for r in records)
