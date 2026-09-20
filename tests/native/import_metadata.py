"""Native FAT/exFAT metadata/counter test using copies of synthetic retained fixtures.

Run inside a private mount namespace as root: SCRIPT RUNTIME FIXTURES OUTPUT_DIR.
No physical device or original fixture is modified; production discovery rejects loops.
"""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
assert os.geteuid()==0
runtime,fixtures,out=map(Path,sys.argv[1:]);out.mkdir(exist_ok=False)
sys.path.insert(0,str(runtime));from project_cbm import importer,library
assert str(library.ROOT)=='/home/pcbm/content'
subprocess.run(['mount','--make-rprivate','/'],check=True)
os.umask(0o077)
good=['Game/LOTA0.D64','Game/LOTA1.D64','Game/LOTA2.D64','.private/example.prg','tape.tap','cart.crt','disk.d81','tune.sid']
bad=['.DS_Store','._tape.tap','Game/._LOTA0.D64','Game/._LOTA1.D64','Game/._LOTA2.D64','.Trashes/501/old.prg','.Spotlight-V100/index.prg','.fseventsd/log.prg','.AppleDouble/cart.crt']
rows=[]
with tempfile.TemporaryDirectory(prefix='pcbm-metadata-',dir='/run') as temp:
 work=Path(temp);work.chmod(0o755);source=work/'source';source.mkdir(mode=0o755);source.chmod(0o755)
 importer.WORK=work
 for fs in ['exfat','vfat']:
  image=out/(fs+'-metadata.img');shutil.copyfile(fixtures/(fs+'-fixture.img'),image)
  loop=subprocess.check_output(['losetup','--find','--show',str(image)],text=True).strip()
  try:
   subprocess.run(['mount','-t',fs,loop,str(source)],check=True)
   for name in good+bad:
    p=source/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'\x01\x08synthetic test media\n')
   subprocess.run(['umount',str(source)],check=True)
  finally:
   if os.path.ismount(source):subprocess.run(['umount',str(source)],check=True)
   subprocess.run(['losetup','-d',loop],check=True)
  before=hashlib.sha256(image.read_bytes()).hexdigest()
  loop=subprocess.check_output(['losetup','--read-only','--find','--show',str(image)],text=True).strip()
  try:
   destination=work/fs;destination.mkdir();os.chown(destination,1000,1000);importer.CONTENT=destination
   dev=os.stat(loop);entry={'device':loop,'number':f'{os.major(dev.st_rdev)}:{os.minor(dev.st_rdev)}','diskseq':'synthetic','filesystem':fs,'size_bytes':image.stat().st_size}
   importer.discover=lambda:[entry]
   result=importer.perform(entry,'games','c64')
   assert result['copied']==len(good)+1 and result['ignored_metadata']==len(bad),result
   files=[p for p in destination.rglob('*') if p.is_file()]
   assert len(files)==len(good)+1 and all(p.stat().st_uid==1000 and p.stat().st_gid==1000 for p in files)
   assert (destination/'music/c64/Imported/tune.sid').is_file()
   assert (destination/'games/c64/Imported/.private/example.prg').is_file()
   assert not any(importer.host_metadata(part) for p in files for part in p.relative_to(destination).parts)
   files[0].write_bytes(b'user changed content')
   retained={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
   again=importer.perform(entry,'games','c64')
   assert again['copied']==0 and again['skipped']==len(good)+1,again
   assert retained=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
   assert not os.path.ismount(source) and hashlib.sha256(image.read_bytes()).hexdigest()==before
   rows.append({'filesystem':fs,'copied':result,'retry':again,'source_sha256':before,'source_unchanged':True,'unmounted':True,'ownership':1000,'canonical_layout':True})
  finally:
   if os.path.ismount(source):subprocess.run(['umount',str(source)],check=True)
   subprocess.run(['losetup','-d',loop],check=True)
(out/'report.json').write_text(json.dumps({'result':'PASS','tests':rows,'physical_USB':'UNTESTED'},indent=2)+'\n')
print(json.dumps(rows,indent=2))
