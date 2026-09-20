#!/usr/bin/env python3
"""Prepare/verify admitted C64 application inputs offline; no downloader or emulator."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import tarfile
from build_contracts import encode, read_json, verify_artifact, check_workspace

PIN = Path(__file__).resolve().parents[1] / 'build/optional/sid-wizard.json'
CONTENT = 'music/c64/Creation/SID-Wizard/SID-Wizard-1.97.d64'
NAMES = {'SID-Wizard-1.97.d64', 'UPSTREAM-NOTICE.txt', 'manifest.json'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def sectors(track):
    return 21 if track <= 17 else 19 if track <= 24 else 18 if track <= 30 else 17


def offset(track, sector):
    if not 1 <= track <= 35 or not 0 <= sector < sectors(track):
        raise ValueError('invalid D64 location')
    return (sum(sectors(t) for t in range(1, track)) + sector) * 256


def disk(programs):
    """Original minimal two-program working disk; never imports upstream music."""
    if len(programs) != 2 or [n for n, _ in programs] != ['SID-WIZARD', 'SID-MAKER']:
        raise ValueError('only admitted core programs')
    out = bytearray(174848)
    used = {(18, 0), (18, 1)}
    available = [(t, s) for t in range(1, 36) if t != 18 for s in range(sectors(t))]
    cursor = 0
    for index, (name, raw) in enumerate(programs):
        if not 3 <= len(raw) <= 65536 or raw[:2] != b'\x01\x08':
            raise ValueError('expected C64 BASIC-start PRG')
        chunks = [raw[i:i+254] for i in range(0, len(raw), 254)]
        chain = available[cursor:cursor+len(chunks)];cursor += len(chunks)
        if len(chain) != len(chunks):
            raise ValueError('disk full')
        for i, (loc, chunk) in enumerate(zip(chain, chunks)):
            p = offset(*loc);used.add(loc)
            out[p:p+2] = bytes(chain[i+1] if i+1 < len(chain) else (0, len(chunk)+1))
            out[p+2:p+2+len(chunk)] = chunk
        p = offset(18, 1) + index*32
        out[p+2:p+5] = bytes([0x82, *chain[0]])
        out[p+5:p+21] = name.encode('ascii').ljust(16, b'\xa0')
        out[p+30:p+32] = len(chain).to_bytes(2, 'little')
    p = offset(18, 1);out[p:p+2] = bytes([0, 255])
    bam = offset(18, 0);out[bam:bam+3] = bytes([18, 1, 65])
    for t in range(1, 36):
        free = [s for s in range(sectors(t)) if (t, s) not in used]
        out[bam+t*4:bam+t*4+4] = bytes([len(free)]) + sum(1 << s for s in free).to_bytes(3, 'little')
    out[bam+0x90:bam+0xa0] = b'SID-WIZARD 1.97'.ljust(16, b'\xa0')
    out[bam+0xa0:bam+0xab] = b'\xa0\xa0SW\xa02A\xa0\xa0\xa0\xa0'
    return bytes(out)


def reviewed_files(source, pin):
    raw = Path(source).read_bytes()
    if len(raw) != pin['source']['size_bytes'] or sha(raw) != pin['source']['sha256']:
        raise ValueError('upstream source hash mismatch')
    selected = {}
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        members = archive.getmembers()
        for entry in [pin['notice'], *pin['programs']]:
            matches = [m for m in members if m.name == entry['member']]
            if len(matches) != 1 or not matches[0].isfile() or matches[0].size != entry['size_bytes']:
                raise ValueError('ambiguous/unsafe upstream member')
            data = archive.extractfile(matches[0]).read()
            if sha(data) != entry['sha256']:
                raise ValueError('upstream member hash mismatch')
            selected[entry['member']] = data
    return selected


def payload(source, pin):
    selected = reviewed_files(source, pin)
    d64 = disk([(e['disk_name'], selected[e['member']]) for e in pin['programs']])
    files = {'SID-Wizard-1.97.d64': d64, 'UPSTREAM-NOTICE.txt': selected[pin['notice']['member']]}
    manifest = {'format': 'project-cbm.optional-software', 'schema_version': 1,
                'id': 'sid-wizard', 'version': pin['version'], 'license': pin['license'],
                'source_sha256': pin['source']['sha256'], 'profile': 'x64sc',
                'content_path': CONTENT, 'qualification': 'PENDING',
                'files': [{'name': n, 'sha256': sha(b), 'size_bytes': len(b)} for n, b in sorted(files.items())]}
    files['manifest.json'] = encode(manifest)
    result = io.BytesIO()
    with tarfile.open(fileobj=result, mode='w', format=tarfile.USTAR_FORMAT) as tar:
        for name, raw in sorted(files.items()):
            info = tarfile.TarInfo(name);info.size = len(raw);info.mode = 0o644
            tar.addfile(info, io.BytesIO(raw))
    return result.getvalue()


def verify_optional(root, entry):
    """Compare exact reconstruction to prevent archive paths/extra assets being trusted."""
    pin = read_json(PIN)
    if entry['version'] != pin['version'] or entry['license'] != pin['license'] or entry['origin'] != pin['origin']:
        raise ValueError('unreviewed optional software')
    for key in ('source', 'artifact', 'recipe', 'rights_review'):
        verify_artifact(root, entry[key])
    if (Path(root)/entry['rights_review']['path']).read_bytes() != PIN.read_bytes():
        raise ValueError('optional rights review mismatch')
    if (Path(root)/entry['recipe']['path']).read_bytes() != Path(__file__).read_bytes():
        raise ValueError('optional recipe mismatch')
    expected = payload(Path(root)/entry['source']['path'], pin)
    if (Path(root)/entry['artifact']['path']).read_bytes() != expected:
        raise ValueError('optional payload does not match reviewed source/subset')
    return expected


def install(root, raw):
    """Fresh image staging only. Existing templates/user state are never overwritten."""
    root = Path(root).resolve(strict=True)
    if root == Path('/'):
        raise ValueError('separate image root required')
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        members = tar.getmembers()
        if len(members) != 3 or {m.name for m in members} != NAMES or any(not m.isfile() or m.size > 200000 for m in members):
            raise ValueError('unexpected optional payload members')
        files = {m.name: tar.extractfile(m).read() for m in members}
    destinations = {
        'usr/share/project-cbm/applications/sid-wizard/SID-Wizard-1.97.d64': files['SID-Wizard-1.97.d64'],
        'usr/share/project-cbm/applications/sid-wizard/manifest.json': files['manifest.json'],
        'usr/share/doc/project-cbm-sid-wizard/UPSTREAM-NOTICE.txt': files['UPSTREAM-NOTICE.txt'],
        'home/pcbm/content/'+CONTENT: files['SID-Wizard-1.97.d64']}
    for name in destinations:
        p = root/name
        if p.exists() or p.is_symlink() or any(a.is_symlink() for a in p.parents if a != root):
            raise ValueError('existing or redirected application destination')
    for name, data in destinations.items():
        p = root/name;p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as stream:stream.write(data)
        p.chmod(0o644)
    return list(destinations)


def freeze(source, kit):
    """Add content-addressed objects to an unfrozen kit; return input-lock fields."""
    kit = Path(kit).resolve(strict=True)
    if (kit/'release-lock.json').exists():
        raise ValueError('refuse frozen kit')
    if (kit/'objects').is_symlink():
        raise ValueError('redirected object store')
    pin = read_json(PIN);raw = payload(source, pin)
    def store(data):
        digest = sha(data);p = kit/'objects'/digest;p.parent.mkdir(exist_ok=True)
        if p.is_symlink():raise ValueError('redirected input object')
        if p.exists():
            if p.read_bytes() != data:raise ValueError('input object collision')
        else:
            with p.open('xb') as stream:stream.write(data)
        return {'path': 'objects/'+digest, 'size_bytes': len(data), 'sha256': digest}
    entry = {'version': pin['version'], 'license': pin['license'], 'origin': pin['origin'],
             'source': store(Path(source).read_bytes()), 'artifact': store(raw),
             'recipe': store(Path(__file__).read_bytes()), 'rights_review': store(PIN.read_bytes())}
    verify_optional(kit, entry)
    return {'sid_wizard': entry}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path);parser.add_argument('unfrozen_kit', type=Path)
    parser.add_argument('--workspace-config', required=True, type=Path)
    args = parser.parse_args()
    workspace = check_workspace(read_json(args.workspace_config))
    if not args.unfrozen_kit.resolve(strict=True).is_relative_to(workspace):
        raise ValueError('optional kit must be in guarded bulk workspace')
    print(json.dumps(freeze(args.source, args.unfrozen_kit), indent=2, sort_keys=True))
