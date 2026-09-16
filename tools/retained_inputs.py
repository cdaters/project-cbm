#!/usr/bin/env python3
"""Verify transitive retained-input catalogs and actual Debian package metadata."""
import argparse
import json
import hashlib
import re
import tarfile
from pathlib import Path
import subprocess
from build_contracts import artifacts, read_json, validate_lock, verify_artifact, public_url


def verify_catalog(root, descriptor):
    verify_artifact(root, descriptor)
    catalog=read_json(root/descriptor['path'])
    if set(catalog)!={'format','schema_version','entries'} or catalog['format']!='project-cbm.input-catalog' or catalog['schema_version']!=1:
        raise ValueError('unsupported input catalog')
    if not isinstance(catalog['entries'],list) or not catalog['entries']:
        raise ValueError('empty input closure')
    seen={}
    for entry in catalog['entries']:
        if set(entry)!={'role','artifact','origin'} or not isinstance(entry['role'],str) or not entry['role']:
            raise ValueError('invalid catalog entry')
        public_url(entry['origin'])
        descriptor=entry['artifact']
        if set(descriptor)!={'path','size_bytes','sha256'}: raise ValueError('invalid descriptor')
        if descriptor['path'] in seen and descriptor != seen[descriptor['path']]: raise ValueError('conflicting closure file')
        seen[descriptor['path']]=descriptor
        verify_artifact(root,descriptor)
    return len(seen)


def verify_deb(path, expected):
    values=subprocess.check_output(['dpkg-deb','-f',str(path),'Package','Version','Architecture'],text=True)
    metadata=dict(line.split(': ',1) for line in values.splitlines())
    if metadata!={'Package':expected['name'],'Version':expected['version'],'Architecture':expected['architecture']}:
        raise ValueError('Debian control identity mismatch')


def verify_media(path, expected):
    with tarfile.open(path) as archive:
        members=archive.getmembers()
        if any(not m.isfile() or m.size>200*1024 or '/' in m.name for m in members):
            raise ValueError('unsafe qualification archive member')
        names=[m.name for m in members]
        if len(names)!=len(set(names)) or set(names)!={'manifest.json','LICENSE','pcbm-smoke.prg','pcbm-sid-check.prg','pcbm-video-input.prg','pcbm-check.d64'}:
            raise ValueError('qualification archive inventory mismatch')
        manifest=json.loads(archive.extractfile('manifest.json').read())
        if manifest['source_commit']!=expected['source_commit'] or manifest['license']!='MIT':
            raise ValueError('qualification source/license mismatch')
        files=manifest['files']
        if len(files)!=4 or {f['name'] for f in files}!=set(names)-{'manifest.json','LICENSE'}:
            raise ValueError('qualification manifest file mismatch')
        for f in files:
            raw=archive.extractfile(f['name']).read()
            if len(raw)!=f['size_bytes'] or hashlib.sha256(raw).hexdigest()!=f['sha256']:
                raise ValueError('qualification payload hash mismatch')
            if not re.fullmatch(r'(programs|music|demos)/Qualification/[a-z0-9.-]+',f['destination']):
                raise ValueError('qualification destination invalid')
        return manifest


def verify_kit(raw, root):
    root=Path(root).resolve(strict=True)
    lock=validate_lock(raw)
    for descriptor in artifacts(lock): verify_artifact(root,descriptor)
    for key in ['authenticated_apt_metadata','binary_package_closure','source_package_closure']:
        verify_catalog(root,lock['base'][key])
    verify_catalog(root,lock['build']['host_package_closure'])
    for component in lock['components'].values():
        verify_deb(root/component['package']['artifact']['path'],component['package'])
        record=read_json(root/component['build_record']['path'])
        for descriptor in artifacts(record): verify_artifact(root,descriptor)
        if record.get('package') != component['package']['artifact']:
            raise ValueError('build record package mismatch')
        if record.get('source_sha256') != component['source']['artifact']['sha256']:
            raise ValueError('build record source mismatch')
    if 'qualification_media' in lock:
        verify_media(root/lock['qualification_media']['artifact']['path'],lock['qualification_media'])
    if 'optional_software' in lock:
        from optional_software import verify_optional
        verify_optional(root, lock['optional_software']['sid_wizard'])
        if 'striketerm' in lock['optional_software']:
            from private_application import verify
            verify(root,lock['optional_software']['striketerm'])
    return lock


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lock',type=Path);parser.add_argument('root',type=Path)
    args=parser.parse_args()
    verify_kit(args.lock.read_bytes(),args.root)
    print('Frozen direct inputs, transitive catalogs and Debian metadata verified')
