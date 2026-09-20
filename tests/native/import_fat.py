"""Read-only FAT/exFAT loop import in an isolated native mount namespace.

Usage: sudo unshare --mount python3 tests/native/import_fat.py RUNTIME_DIR
       EXFAT_FIXTURE VFAT_FIXTURE REPORT
Fixtures each contain only FS-probe.prg with the synthetic bytes below. This test
adapter bypasses discovery only for its own loop; production rejects loop devices.
No host package installation or physical media is involved.
"""
import hashlib,json,os,stat,subprocess,sys,tempfile
from pathlib import Path
assert os.geteuid()==0
runtime,exfat,vfat,report=map(Path,sys.argv[1:])
sys.path.insert(0,str(runtime));from project_cbm import importer
subprocess.run(['mount','--make-rprivate','/'],check=True)
os.umask(0o077)
rows=[]
with tempfile.TemporaryDirectory(prefix='pcbm-fat-',dir='/run') as temporary:
 work=Path(temporary);work.chmod(0o755)
 source=work/'source';source.mkdir(mode=0o755);source.chmod(0o755)
 dest=work/'content';dest.mkdir();os.chown(dest,1000,1000)
 importer.WORK=work;importer.CONTENT=dest
 for fs,image in [('exfat',exfat),('vfat',vfat)]:
  before=hashlib.sha256(image.read_bytes()).hexdigest()
  loop=subprocess.check_output(['losetup','--read-only','--find','--show',str(image)],text=True).strip()
  try:
   device=os.stat(loop);entry={'device':loop,'number':f'{os.major(device.st_rdev)}:{os.minor(device.st_rdev)}','diskseq':'test-only','filesystem':fs,'size_bytes':image.stat().st_size}
   importer.discover=lambda:[entry]
   dest.chmod(0)
   try:importer.perform(entry,'demos','c64')
   except importer.ImportFailure as error:
    assert error.code=='access_denied' and error.source_unmounted is True
   else:raise AssertionError('unreadable destination admitted')
   finally:dest.chmod(0o700)
   answer=importer.perform(entry,'demos','c64');assert answer['copied']==1,answer
   copied=dest/'demos/c64/Imported'/(fs+'-probe.prg')
   assert copied.read_bytes()==b'\x01\x08synthetic import permission test\n' and copied.stat().st_uid==1000
   again=importer.perform(entry,'demos','c64');assert again['copied']==0 and again['skipped']==1,again
   assert not os.path.ismount(source) and hashlib.sha256(image.read_bytes()).hexdigest()==before
   rows.append({'filesystem':fs,'copy':answer,'retry':again,'ownership':1000,'permission_failure_reported':True,'failure_and_success_unmounted':True,'source_unchanged':True})
  finally:
   if os.path.ismount(source):subprocess.run(['umount',str(source)],check=True)
   subprocess.run(['losetup','-d',loop],check=True)
result={'result':'PASS','tests':rows,'physical_USB':'UNTESTED'}
with report.open('x') as stream:stream.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
