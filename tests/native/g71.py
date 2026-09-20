"""Original G71 fixture against installed VICE; disposable native namespace only."""
import os,sys,pathlib,subprocess,time,socket,json
assert os.geteuid()==1000
assert pathlib.Path('/var/lib/project-cbm/native-staging-only').read_text()=='DISPOSABLE PCBM NAMESPACE\n'
out=pathlib.Path(sys.argv[1]);out.mkdir(exist_ok=False)
sys.path.insert(0,'/usr/share/project-cbm/runtime')
from project_cbm.applications import content_options
rows=[]
for exe in ('x64sc','x128'):
 start=0x0801 if exe=='x64sc' else 0x1c01
 body=bytes([10,0,0x99,34])+b'CBM G71 OK'+bytes([34,0])
 program=start.to_bytes(2,'little')+(start+2+len(body)).to_bytes(2,'little')+body+bytes([0,0])
 prg=out/(exe+'.prg');prg.write_bytes(program)
 media=out/(exe+'.g71')
 c=subprocess.run(['c1541','-format','CBM TEST,01','g71',str(media),'-write',str(prg),'TEST','-list'],capture_output=True,text=True,errors='replace',timeout=30)
 (out/(exe+'-directory.txt')).write_text(c.stdout+c.stderr);assert c.returncode==0
 args=[exe,'-default','-console','+sound','-warp',*content_options(media,exe),'-remotemonitor','-remotemonitoraddress','127.0.0.1:6511','+logcolorize','-logfile','-','-autostart',str(media)]
 env=dict(os.environ,HOME=str(out),XDG_CONFIG_HOME=str(out),SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy')
 with (out/(exe+'.log')).open('w') as log:
  p=subprocess.Popen(args,env=env,stdout=log,stderr=subprocess.STDOUT)
  try:
   time.sleep(12);assert p.poll() is None
   conn=socket.create_connection(('127.0.0.1',6511));conn.settimeout(.5)
   conn.sendall(b'\n')
   try:conn.recv(65536)
   except socket.timeout:pass
   time.sleep(.3);conn.sendall(b'screen\n');data=b''
   while True:
    try:
     block=conn.recv(65536)
     if not block:break
     data+=block
    except socket.timeout:break
   (out/(exe+'-screen.txt')).write_bytes(data)
   assert b'CBM G71 OK' in data.upper(),data
   conn.sendall(b'quit\n');conn.close();p.wait(timeout=10)
   assert 'AUTOSTART: Done.' in (out/(exe+'.log')).read_text()
   rows.append({'engine':exe,'g71_autostart_and_basic':True,'drive':1571})
  finally:
   if p.poll() is None:p.terminate();p.wait(timeout=10)
print(json.dumps({'results':rows,'physical_media_workflow':'UNTESTED'}))
