"""Synthetic FAT/ext4 ingestion in a private Linux mount namespace; no Pi/media.

Run only as root via unshare --mount, passing a NEW disposable ext4-backed directory
and the copied runtime source. Does not install packages or modify builder config.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

base, runtime = map(Path, sys.argv[1:])
assert os.geteuid() == 0 and not base.exists()
base.mkdir(mode=0o755)
base.chmod(0o755)
sys.path.insert(0, str(runtime))
from project_cbm import importer
from project_cbm.ingest_session import Session
subprocess.run(['/usr/bin/mount', '--make-rprivate', '/'], check=True)
rows = []
for filesystem, formatter in [('vfat', '/usr/sbin/mkfs.vfat'), ('ext4', '/usr/sbin/mkfs.ext4')]:
    work = base/filesystem
    work.mkdir(mode=0o755)
    source = work/'source'
    source.mkdir(mode=0o755)
    dest = work/'content'
    state = work/'state'
    for p in [dest, state]:
        p.mkdir(mode=0o700)
        os.chown(p, 1000, 1000)
    image = work/'synthetic.img'
    with image.open('xb') as stream:stream.truncate(32*1024**2)
    subprocess.run([formatter, str(image)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    loop = subprocess.check_output(['/usr/sbin/losetup', '--find', '--show', str(image)], text=True).strip()
    try:
        subprocess.run(['/usr/bin/mount', '-t', filesystem, loop, str(source)], check=True)
        try:
            collection = source/'Collection'
            collection.mkdir()
            for name in ['disk1.d64', 'disk2.D64', '._disk1.d64']:
                (collection/name).write_bytes(b'original synthetic payload')
            (source/'ignore.txt').write_text('unsupported fixture')
        finally:subprocess.run(['/usr/bin/umount', str(source)], check=True)
    finally:subprocess.run(['/usr/sbin/losetup', '-d', loop], check=True)
    before = hashlib.sha256(image.read_bytes()).hexdigest()
    loop = subprocess.check_output(['/usr/sbin/losetup', '--read-only', '--find', '--show', str(image)], text=True).strip()
    try:
        device = os.stat(loop)
        entry = {'device':loop, 'number':f'{os.major(device.st_rdev)}:{os.minor(device.st_rdev)}',
                 'filesystem':filesystem, 'diskseq':'synthetic-only', 'size_bytes':image.stat().st_size}
        importer.WORK = work
        importer.discover = lambda: [entry]  # Test-only adapter, never production admission.
        def worker(target):
            assert os.geteuid() == os.getegid() == 1000 and os.getgroups() == []
            try:(target/'write-probe').write_text('must fail')
            except OSError:pass
            else:raise AssertionError('writable source')
            session = Session(target, dest, state)
            counts = session.handle({'operation':'scan'})
            assert counts['supported'] == 2 and counts['ignored_metadata'] == 1
            assert not list(dest.iterdir())
            session.handle({'operation':'select', 'mode':'all'})
            session.handle({'operation':'plan', 'category':'games', 'family':'c64'})
            assert not list(dest.iterdir())
            return session.handle({'operation':'import'})
        first = importer.perform(entry, None, worker=worker)
        assert first['saved'] == 2 and first['source_unmounted'] is True, first
        def repeat(target):
            session=Session(target,dest,state)
            session.handle({'operation':'scan'})
            session.handle({'operation':'select','mode':'all'})
            session.handle({'operation':'plan','category':'games','family':'c64'})
            return session.handle({'operation':'import'})
        again=importer.perform(entry,None,worker=repeat)
        assert again['already_present']==2 and again['saved']==0 and again['source_unmounted'] is True,again
        assert all(p.stat().st_uid==1000 for p in dest.rglob('*'))
        assert not os.path.ismount(source)
        assert hashlib.sha256(image.read_bytes()).hexdigest()==before
        rows.append({'filesystem':filesystem,'first':first,'retry':again,'read_only':True,
                     'worker_uid_gid':1000,'source_unchanged':True,'scan_copied_nothing':True})
    finally:
        if os.path.ismount(source):subprocess.run(['/usr/bin/umount',str(source)],check=True)
        subprocess.run(['/usr/sbin/losetup','-d',loop],check=True)
print(json.dumps({'result':'PASS','rows':rows,'physical_USB':'UNTESTED','exfat':'UNTESTED: formatter absent'},indent=2))
