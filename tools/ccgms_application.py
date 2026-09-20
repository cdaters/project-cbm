#!/usr/bin/env python3
"""Verified CCGMS-only application disk; original compilation never installed."""
import io
from pathlib import Path
import tarfile
from build_contracts import encode, read_json, verify_artifact
from optional_software import application_disk, offset, sha

PIN = Path(__file__).resolve().parents[1]/'build/optional/ccgms.json'


def checked(raw, descriptor):
    if len(raw) != descriptor['size_bytes'] or sha(raw) != descriptor['sha256']:
        raise ValueError('CCGMS input identity mismatch')
    return raw


def program(disk, pin):
    checked(disk, pin['upstream_disk'])
    # Exact upstream entry 2; entry 1 is a decorative zero-block DEL separator.
    entry = disk[offset(18, 1)+32:offset(18, 1)+64]
    if entry[2] != 0x82 or entry[5:21].rstrip(b'\xa0') != b'CCGMS 2021':
        raise ValueError('CCGMS directory mismatch')
    track, sector = entry[3:5]
    seen = set(); raw = bytearray()
    while track:
        if (track, sector) in seen or track == 18:
            raise ValueError('CCGMS invalid chain')
        seen.add((track, sector))
        at = offset(track, sector); block = disk[at:at+256]
        if not block[0] and not 1 <= block[1] <= 255:
            raise ValueError('CCGMS final sector')
        raw.extend(block[2:] if block[0] else block[2:block[1]+1])
        track, sector = block[:2]
    if len(seen) != int.from_bytes(entry[30:32], 'little'):
        raise ValueError('CCGMS block count')
    return checked(bytes(raw), pin['program'])


def payload(disk, source, notice, pin):
    prg = program(disk, pin)
    checked(source, pin['source']); checked(notice, pin['notice'])
    image = application_disk([('CCGMS 2021', prg)], 'CCGMS 2021', 'CC')
    files = {'CCGMS-2021.d64': image, 'SOURCE.txt': source, 'LICENSE.txt': notice,
             'PROVENANCE.json': encode(pin)}
    files['manifest.json'] = encode({'format':'project-cbm.optional-software', 'schema_version':1,
        'id':'ccgms','version':'2021','license':'BSD-3-Clause', 'profile':'x64sc',
        'content_path':pin['content_path'], 'source_sha256':sha(source), 'program_sha256':sha(prg),
        'qualification':'PHYSICAL WORKFLOW REQUIRED',
        'files':[{'name':n,'size_bytes':len(b),'sha256':sha(b)} for n,b in sorted(files.items())]})
    result = io.BytesIO()
    with tarfile.open(fileobj=result,mode='w',format=tarfile.USTAR_FORMAT) as tar:
        for name, raw in sorted(files.items()):
            entry=tarfile.TarInfo(name);entry.size=len(raw);entry.mode=0o644
            tar.addfile(entry,io.BytesIO(raw))
    return result.getvalue()


def verify(root, entry):
    root=Path(root);pin=read_json(PIN)
    if any(entry[k] != pin[k] for k in ('version','license','origin')):
        raise ValueError('unreviewed CCGMS')
    keys=('upstream_disk','source','notice','artifact','recipe','rights_review')
    for key in keys:verify_artifact(root,entry[key])
    if (root/entry['rights_review']['path']).read_bytes()!=PIN.read_bytes():
        raise ValueError('CCGMS provenance mismatch')
    if (root/entry['recipe']['path']).read_bytes()!=Path(__file__).read_bytes():
        raise ValueError('CCGMS recipe mismatch')
    expected=payload(*[(root/entry[k]['path']).read_bytes() for k in ('upstream_disk','source','notice')],pin)
    if (root/entry['artifact']['path']).read_bytes()!=expected:
        raise ValueError('CCGMS payload mismatch')
    return expected


def install(root, raw):
    root=Path(root).resolve(strict=True)
    if root==Path('/'):raise ValueError('separate image root required')
    names={'CCGMS-2021.d64','SOURCE.txt','LICENSE.txt','PROVENANCE.json','manifest.json'}
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        members=tar.getmembers()
        if len(members)!=len(names) or {m.name for m in members}!=names or any(not m.isfile() or m.size>200000 for m in members):
            raise ValueError('unexpected CCGMS payload')
        files={m.name:tar.extractfile(m).read() for m in members}
    pin=read_json(PIN)
    destinations={'home/pcbm/content/'+pin['content_path']:files['CCGMS-2021.d64'],
        'usr/share/project-cbm/applications/ccgms/CCGMS-2021.d64':files['CCGMS-2021.d64']}
    for name in names-{'CCGMS-2021.d64'}:
        destinations['usr/share/doc/project-cbm-ccgms/'+name]=files[name]
    for name in destinations:
        p=root/name
        if p.exists() or p.is_symlink() or any(a.is_symlink() for a in p.parents if a!=root):
            raise ValueError('existing/redirected CCGMS destination')
    for name,data in destinations.items():
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f:f.write(data)
        p.chmod(0o644)
    return list(destinations)
