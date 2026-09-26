"""Disposable namespace/overlay runner for the installed USB terminal regression.

Invoke via sudo unshare --mount --pid --fork --net python3 ... WORK RECIPE BASE.
BASE must not exist. Uses read-only attempt18 only as a lower filesystem, never Pi.
Optional fourth argument is a new Runtime .deb; otherwise pre-package source trial.
"""
from pathlib import Path
import hashlib,json,os,shutil,stat,subprocess,sys,time
w,r,s=map(Path,sys.argv[1:4]);debs=[Path(value) for value in sys.argv[4:]]
assert os.geteuid()==0 and not s.exists() and str(s).startswith('/srv/project-cbm/')
s.mkdir();root=s/'root';lower=s/'lower';upper=s/'upper';work=s/'work'
for p in (root,lower,upper,work):p.mkdir()
subprocess.run(['mount','--make-rprivate','/'],check=True)
raw=w/'builds/private-1.2-dev1-attempt-18/work/export-image/2026-09-25-project-cbm-1.2.0-dev.1-lite-private-1.2-dev1.img'
expected='428da6e67c5f82aa3a09fdbdc54d12e0d6cf8fc78abd0bc25a779c728351e557'
def digest(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
assert digest(raw)==expected
loop=subprocess.check_output(['losetup','--read-only','--find','--show','--partscan',str(raw)],text=True).strip()
mounted=[];usb=None;fixture_hash=None
ENV={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin','LC_ALL':'C.UTF-8','HOME':'/root','PYTHONDONTWRITEBYTECODE':'1','TMPDIR':'/tmp','TMP':'/tmp','TEMP':'/tmp'}
def mount(args,path):subprocess.run(['mount',*args,str(path)],check=True);mounted.append(path)
def inside(*args,**kwargs):return subprocess.run(['chroot',str(root),*args],env=ENV,check=True,**kwargs)
try:
 mount(['-o','ro,noload',loop+'p2'],lower)
 mount(['-t','overlay','overlay','-o',f'lowerdir={lower},upperdir={upper},workdir={work}'],root)
 for name,options in [('run','mode=755,nosuid,nodev'),('sys','mode=755,nosuid,nodev,noexec'),('dev','mode=755,nosuid')]:mount(['-t','tmpfs','-o',options,'tmpfs'],root/name)
 for name,major,minor in [('null',1,3),('zero',1,5),('full',1,7),('random',1,8),('urandom',1,9),('tty',5,0)]:os.mknod(root/'dev'/name,stat.S_IFCHR|0o666,os.makedev(major,minor));os.chmod(root/'dev'/name,0o666)
 for name in ['pts','shm']:(root/'dev'/name).mkdir()
 (root/'dev/ptmx').symlink_to('pts/ptmx')
 mount(['-t','devpts','-o','newinstance,ptmxmode=0666,mode=0620,gid=5','devpts'],root/'dev/pts')
 mount(['-t','tmpfs','-o','mode=1777,nosuid,nodev','tmpfs'],root/'dev/shm')
 mount(['-t','proc','proc'],root/'proc')
 (root/'usr/sbin/policy-rc.d').write_text('#!/bin/sh\nexit 101\n');(root/'usr/sbin/policy-rc.d').chmod(0o755)
 if debs:
  paths=[]
  for i,deb in enumerate(debs):
   dest=f'/tmp/component-{i}.deb';shutil.copyfile(deb,root/dest.lstrip('/'));paths.append(dest)
  inside('dpkg','-i',*paths);inside('apt-get','check');inside('dpkg','--audit')
  shutil.copyfile(r/'runtime/config/sudoers.example',root/'etc/sudoers.d/pcbm-operations')
  (root/'etc/sudoers.d/pcbm-operations').chmod(0o440)
  p=inside('dpkg','--verify','project-cbm-runtime','project-cbm-menu',capture_output=True,text=True);assert not p.stdout,p.stdout
 else:
  shutil.copytree(r/'runtime/project_cbm',root/'usr/share/project-cbm/runtime/project_cbm',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
  shutil.copyfile(r/'runtime/bin/pcbm-ingest-session',root/'usr/share/project-cbm/runtime/bin/pcbm-ingest-session')
 inside('visudo','-cf','/etc/sudoers')
 policy=root/'etc/project-cbm/configuration-policy.json';d=json.loads(policy.read_text());d['system_ready']=True;policy.write_text(json.dumps(d))
 for rel in ['run/project-cbm','run/project-cbm/import','run/project-cbm/import/source']:(root/rel).mkdir(mode=0o755,exist_ok=True)
 (root/'run/cbm-disposable-usb-test').touch()
 # Synthetic ext4 fixture, populated before a read-only loop association.
 seed=s/'seed';seed.mkdir();(seed/'alpha.txt').write_text('CBM_NATIVE_ALPHA\n');(seed/'beta.txt').write_text('CBM_NATIVE_BETA\n');(seed/'0fixture.prg').write_bytes(b'\x01\x08CBM native original fixture')
 image=s/'synthetic.img'
 with image.open('xb') as f:f.truncate(16*1024**2)
 subprocess.run(['mkfs.ext4','-F','-d',str(seed),str(image)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 fixture_hash=digest(image)
 usb=subprocess.check_output(['losetup','--read-only','--find','--show',str(image)],text=True).strip();st=os.stat(usb)
 os.mknod(root/usb.lstrip('/'),stat.S_IFBLK|0o600,st.st_rdev)
 entry={'device':usb,'number':f'{os.major(st.st_rdev)}:{os.minor(st.st_rdev)}','filesystem':'ext4','diskseq':'synthetic-only','size_bytes':image.stat().st_size}
 # ONLY the discovery boundary is substituted, in this disposable wrapper.
 helper=root/'usr/libexec/pcbm-import-root';script=helper.read_text();script=script.replace('from project_cbm.importer import main','from project_cbm import importer\nimporter.discover = lambda: ['+repr(entry)+']\nmain = importer.main');helper.write_text(script)
 dest=root/'home/pcbm/content/zzzz-cbm-native.txt';dest.write_text('CBM_NATIVE_LIBRARY\n');os.chown(dest,1000,1000)
 shutil.copyfile(r/'tests/native/usb_browse_installed.py',root/'tmp/usb_browse_installed.py')
 with (s/'installed-path.log').open('x') as log:inside('python3','/tmp/usb_browse_installed.py',stdout=log,stderr=subprocess.STDOUT)
 print('Real installed USB MC path PASS',flush=True)
 if (root/'usr/libexec/pcbm-kms-capture').exists():
  # Keep fixture compilation outside the appliance. Only the disposable overlay
  # receives the test executable, never the image or frozen production package.
  component=r/'components/pcbm-kms-capture'
  source=(component/'capture.c').read_text().replace('int main(int argc,char **argv) {','#include "screenshot_fixture.h"\nint main(int argc,char **argv) {')
  (s/'capture-fixture.c').write_text(source)
  flags=subprocess.check_output(['pkg-config','--cflags','--libs','libdrm','libpng'],text=True).split()
  subprocess.run(['cc','-O2','-I'+str(component),'-I'+str(r/'tests/native'),str(s/'capture-fixture.c'),'-o',str(root/'tmp/screenshot-fixture'),*flags,'-lcap'],check=True)
  shutil.copyfile(r/'tests/native/screenshot_installed.py',root/'tmp/screenshot_installed.py')
  with (s/'screenshot-installed.log').open('x') as log:inside('python3','/tmp/screenshot_installed.py',stdout=log,stderr=subprocess.STDOUT)
  print('Installed screenshot sudo/account/drop/output path PASS',flush=True)
finally:
 # Reap adopted children in this private PID namespace before devpts teardown.
 until=time.monotonic()+30
 while time.monotonic()<until:
  try:
   while os.waitpid(-1,os.WNOHANG)[0]:pass
  except ChildProcessError:break
  time.sleep(.05)
 for trace in (root/'tmp').glob('usb-installed-*.terminal'):shutil.copyfile(trace,s/trace.name)
 # Test-created mounts may remain after an assertion; release only in this namespace.
 if os.path.ismount(root/'run/project-cbm/import/browse'):subprocess.run(['umount',str(root/'run/project-cbm/import/browse')],check=True)
 for path in reversed(mounted):subprocess.run(['umount',str(path)],check=True)
 if usb:subprocess.run(['losetup','-d',usb],check=True)
 if fixture_hash:assert digest(image)==fixture_hash
 subprocess.run(['losetup','-d',loop],check=True)
 assert digest(raw)==expected
 print('attempt18 lower image unchanged; staging mounts/loops released',flush=True)
