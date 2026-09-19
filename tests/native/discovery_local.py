import json,os,secrets,socket,struct,subprocess,time
from pathlib import Path
assert Path('/var/lib/project-cbm/native-staging-only').read_text()=='DISPOSABLE PCBM NAMESPACE\n'
assert Path('/run/systemd/container').read_text().strip()=='pcbm-staging'
os.chdir('/')
def run(args,data=None):return subprocess.run(args,input=data,text=True,capture_output=True,timeout=65)
def request(op,**values):
 p=run(['runuser','-u','pi','--','sudo','-n','--','/usr/libexec/pcbm-config-root'],json.dumps({'schema_version':1,'operation':op,'values':values}))
 assert json.loads(p.stdout)['status']=='ok',op
secret=secrets.token_urlsafe(24)
try:
 assert run(['ip','link','add','mdnstest0','type','dummy']).returncode==0
 assert run(['ip','link','set','mdnstest0','multicast','on','up']).returncode==0
 assert run(['ip','address','add','192.0.2.77/24','dev','mdnstest0']).returncode==0
 request('sharing-password',password=secret);request('service',service='sharing',enabled=True)
 query=struct.pack('!HHHHHH',4321,0,1,0,0,0)+b'\x04_smb\x04_tcp\x05local\0'+struct.pack('!HH',12,1)
 sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);sock.bind(('192.0.2.77',0));sock.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_IF,socket.inet_aton('192.0.2.77'));sock.settimeout(1)
 found=False
 for _ in range(8):
  sock.sendto(query,('224.0.0.251',5353))
  try:
   data,addr=sock.recvfrom(4096)
   if len(data)>12 and struct.unpack('!H',data[2:4])[0]&0x8000 and b'\x04_smb\x04_tcp\x05local' in data and b'projectcbm' in data.lower():found=True;break
  except socket.timeout:pass
 assert found,'no local SMB mDNS answer'
 print(json.dumps({'local_smb_mdns_response':'PASS','interface':'synthetic isolated dummy','physical_mac_windows_discovery':'UNTESTED'}))
finally:
 for name in ('sharing','discovery'):
  try:request('service',service=name,enabled=False)
  except Exception:pass
 run(['ip','link','del','mdnstest0']);run(['smbpasswd','-x','pcbm']);Path('/var/lib/project-cbm/sharing-status.json').unlink(missing_ok=True)
 secret=None
