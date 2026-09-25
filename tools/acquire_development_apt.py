#!/usr/bin/env python3
"""Bounded private 1.2 metadata refresh acquisition (2026-09-25).

Opt-in native-builder recipe, never a static test. Requires the verified attempt16
kit and read-only stable image. Writes a NEW dated directory and refuses reruns.
Uses current APT signature/expiry checks; only downloads the reviewed mkvtoolnix
security update/source. Nothing is installed on the host or underlying image.
"""
from pathlib import Path
import json,subprocess,sys,hashlib,os,time,shutil
from urllib.request import urlopen
assert os.geteuid()==0
w=Path('/srv/project-cbm');r=w/'recipes/poc4-attempt16/project-cbm';k=w/'inputs/frozen-poc4-attempt16';out=w/'inputs/apt-refresh-dev1-20260925';out.mkdir()
sys.path.insert(0,str(r/'tools'))
from build_host_guard import verify
from build_environment import environment
from retained_inputs import verify_kit
lock=verify_kit((k/'release-lock.json').read_bytes(),k);verify(lock,k)
cat=json.loads((k/lock['base']['authenticated_apt_metadata']['path']).read_text());urls=json.loads((k/next(e['artifact']['path'] for e in cat['entries'] if e['role']=='frozen-url-map')).read_text())
transport=out/'transport';transport.mkdir()
seed={url:entry for url,entry in urls.items() if '/debian-security/dists/trixie-security/' not in url and url!='https://deb.debian.org/debian/dists/trixie-updates/InRelease'}
for url,entry in seed.items():
 path=transport/entry['path'];assert path.parent==transport
 if not path.exists():os.link(k/'objects'/entry['sha256'],path)
(transport/'catalog.json').write_text(json.dumps(seed,indent=2)+'\n')
proxylog=(out/'transport.log').open('x')
proxy=subprocess.Popen(['python3',str(r/'tools/apt_retention_proxy.py'),'--root',str(transport),'--mode','resolve','--port','3143'],env=environment(),stdout=proxylog,stderr=subprocess.STDOUT)
child=r'''from pathlib import Path
import subprocess,os,shutil,json,hashlib
w=Path('/srv/project-cbm');out=w/'inputs/apt-refresh-dev1-20260925';stage=out/'stage';stage.mkdir()
root=stage/'root';lower=stage/'lower';upper=stage/'upper';work=stage/'work'
for p in (root,lower,upper,work):p.mkdir()
subprocess.run(['mount','--make-rprivate','/'],check=True)
raw=w/'builds/release-1.1.0-attempt-15/work/export-image/2026-09-20-project-cbm-1.1.0.img'
with raw.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()=='6c9b7599461a41f6ab30b666dd718329c34f863f11a46dfd20d61fe9830d2468'
loop=subprocess.check_output(['losetup','--read-only','--find','--show','--partscan',str(raw)],text=True).strip();mounted=[]
def mount(args,path):subprocess.run(['mount',*args,str(path)],check=True);mounted.append(path)
try:
 mount(['-o','ro,noload',loop+'p2'],lower)
 mount(['-t','overlay','overlay','-o',f'lowerdir={lower},upperdir={upper},workdir={work}'],root)
 mount(['-t','proc','proc'],root/'proc')
 mount(['-t','tmpfs','-o','mode=755,nosuid,nodev','tmpfs'],root/'run')
 (root/'etc/apt/sources.list.d/cbm-refresh-source.list').write_text('deb-src [signed-by=/usr/share/keyrings/debian-archive-keyring.pgp] http://deb.debian.org/debian-security/ trixie-security main\n')
 prefix=['chroot',str(root),'apt-get','-o','Acquire::http::Proxy=http://127.0.0.1:3143/']
 with (out/'apt-update.log').open('x') as log:subprocess.run([*prefix,'update'],stdout=log,stderr=subprocess.STDOUT,check=True)
 sim=subprocess.check_output([*prefix,'-s','install','mkvtoolnix=92.0-1+deb13u1'],text=True)
 (out/'simulation.log').write_text(sim)
 assert [line.split()[1] for line in sim.splitlines() if line.startswith('Inst ')]==['mkvtoolnix'],sim
 assert not any(line.startswith('Remv ') for line in sim.splitlines())
 p=root/'tmp/cbm-refresh-inputs';p.mkdir()
 for name,command in [('binary',['download','mkvtoolnix=92.0-1+deb13u1']),('source',['source','--only-source','--download-only','mkvtoolnix=92.0-1+deb13u1'])]:
  args=['chroot',str(root),'/bin/sh','-c','cd /tmp/cbm-refresh-inputs && exec "$@"','acquire','apt-get','-o','Acquire::http::Proxy=http://127.0.0.1:3143/',*command]
  with (out/(name+'-acquisition.log')).open('x') as log:subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,check=True)
 shutil.copytree(p,out/'packages')
 before=(lower/'var/lib/dpkg/status').read_bytes();assert (root/'var/lib/dpkg/status').read_bytes()==before
 print('APT current signature/time/index verification and one-package-only resolver delta PASS; binary/source downloaded, nothing installed',flush=True)
finally:
 for path in reversed(mounted):subprocess.run(['umount',str(path)],check=True)
 subprocess.run(['losetup','--detach',loop],check=True)
 with raw.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()=='6c9b7599461a41f6ab30b666dd718329c34f863f11a46dfd20d61fe9830d2468'
'''
try:
 for _ in range(30):
  assert proxy.poll() is None
  try:
   with urlopen('http://127.0.0.1:3143/',timeout=1) as response:assert response.read()==b'CBM retained APT transport\n'
   break
  except OSError:time.sleep(.1)
 else:raise RuntimeError('retention transport not ready')
 subprocess.run(['unshare','--mount','--pid','--fork','python3','-'],input=child,text=True,env=environment(),check=True)
finally:
 proxy.terminate();proxy.wait(timeout=10);proxylog.close();verify(lock,k)
print('Acquisition stopped; builder unchanged; refresh is not yet frozen',flush=True)
