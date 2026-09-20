"""Isolated native CCGMS/TCPser smoke test. Run as pcbm in the disposable namespace.
Requires tcpser.service already started at its initial 25232/2400 settings.
Uses a NEW output directory, synthetic loopback BBS, temporary emulator settings.
This is not physical keyboard, display or remote-BBS qualification.
"""
import subprocess,os,time,socket,pathlib,json,threading,sys
sys.path.insert(0,'/usr/share/project-cbm/runtime')
from project_cbm.applications import content_options
assert os.geteuid()==1000
assert pathlib.Path('/var/lib/project-cbm/native-staging-only').read_text()=='DISPOSABLE PCBM NAMESPACE\n'
out=pathlib.Path(sys.argv[1]);out.mkdir(exist_ok=False)
received=[]
server=socket.socket();server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);server.bind(('127.0.0.1',24680));server.listen();server.settimeout(45)
def endpoint():
 try:
  conn,_=server.accept();conn.settimeout(20);conn.sendall(b'\r\nCBM LOCAL TEST\r\n')
  while True:
   block=conn.recv(4096)
   if not block:break
   received.append(block);conn.sendall(block)
 except (socket.timeout,OSError):pass
thread=threading.Thread(target=endpoint,daemon=True);thread.start()
env=dict(os.environ,HOME=str(out),XDG_CONFIG_HOME=str(out),XDG_STATE_HOME=str(out),SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy')
media='/home/pcbm/content/programs/c64/Communications/CCGMS/CCGMS-2021.d64'
args=['x64sc','-default','-console','+sound','-warp','-remotemonitor',
      '-remotemonitoraddress','127.0.0.1:6510',*content_options(media,'x64sc'),
      '+logcolorize','-logfile','-', '-autostart',media]

with (out/'vice.log').open('w') as log:
 p=subprocess.Popen(args,env=env,stdout=log,stderr=subprocess.STDOUT)
 try:
  time.sleep(12);assert p.poll() is None
  c=socket.create_connection(('127.0.0.1',6510));c.settimeout(.3)
  def command(value):
   c.sendall(value.encode()+b'\n');data=b''
   while True:
    try:
     part=c.recv(65536)
     if not part:break
     data+=part
    except socket.timeout:break
   text=data.decode(errors='replace');print(value+'\n'+text,flush=True);return text
  def keys(data):
   command('> 0277 '+' '.join(f'{n:02x}' for n in data));command('> 00c6 '+f'{len(data):02x}');command('x');time.sleep(1);command('')
  command('');command('resourceset WarpMode 0');command('screen');keys([0x88]);command('screen');keys([0x4d]);keys([0x4d]);command('screen');keys([13]);keys([65,84,13]);screen=command('screen');assert 'OK' in screen.upper(),screen
  def typing(value):
   raw=list(value.encode())
   for at in range(0,len(raw),8):keys(raw[at:at+8])
  typing('ATDT127.0.0.1:24680\r');time.sleep(2);screen=command('screen');assert 'CBM LOCAL TEST' in screen.upper(),screen
  typing('CBM TEXT EXCHANGE\r');screen=command('screen');assert b'CBM TEXT EXCHANGE' in b''.join(received),received;assert 'CBM TEXT EXCHANGE' in screen.upper(),screen
  time.sleep(2);typing('+++');time.sleep(2);typing('ATH\r');screen=command('screen');assert 'NO CARRIER' in screen.upper(),screen
  command('quit');c.close();p.wait(timeout=10)
  print(json.dumps({'ccgms_boot':True,'modem_AT_OK':True,'local_endpoint_banner':True,'sent_text_received':True,'disconnect':True,'physical_BBS':'UNTESTED'}))
 finally:
  if p.poll() is None:p.terminate();p.wait(timeout=10)
