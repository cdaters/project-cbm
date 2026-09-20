#!/usr/bin/env python3
"""Exact private StrikeTerm admission and fail-closed public rights check."""
import argparse
import hashlib
import json
from pathlib import Path
from build_contracts import read_json, verify_artifact, validate_lock

PIN=Path(__file__).resolve().parents[1]/'build/optional/striketerm.json'


def check_rights(lock, purpose):
    entry=lock.get('optional_software',{}).get('striketerm')
    if entry is None:return
    if purpose!='private-engineering':raise ValueError('StrikeTerm public-release rights gate is pending')
    if (entry['classification']!='PRIVATE-ENGINEERING-ADMITTED'
            or entry['public_release_rights']!='PUBLIC-RELEASE-RIGHTS-GATE-PENDING'):
        raise ValueError('unreviewed StrikeTerm classification')
    if not lock['product']['candidate'].startswith('private-engineering-'):
        raise ValueError('private admission requires private candidate identity')


def verify(root,entry):
    pin=read_json(PIN)
    for key in ('artifact','rights_review'):verify_artifact(root,entry[key])
    for key in ('version','origin','classification','public_release_rights'):
        if entry[key]!=pin[key]:raise ValueError('unreviewed private application')
    data=(Path(root)/entry['artifact']['path']).read_bytes()
    if len(data)!=pin['size_bytes'] or hashlib.sha256(data).hexdigest()!=pin['sha256']:
        raise ValueError('StrikeTerm artifact mismatch')
    if (Path(root)/entry['rights_review']['path']).read_bytes()!=PIN.read_bytes():
        raise ValueError('StrikeTerm admission record mismatch')
    return data


def install(root,data):
    root=Path(root).resolve(strict=True);pin=read_json(PIN)
    if root==Path('/') or len(data)!=pin['size_bytes'] or hashlib.sha256(data).hexdigest()!=pin['sha256']:
        raise ValueError('invalid private application target/input')
    notice=(json.dumps(pin,indent=2)+'\n').encode()
    files={'usr/share/project-cbm/applications/striketerm/StrikeTerm-2014-Final.d64':data,
           'usr/share/doc/project-cbm-striketerm/PRIVATE-ADMISSION.json':notice,
           'home/pcbm/content/'+pin['content_path']:data}
    for name in files:
        p=root/name
        if p.exists() or p.is_symlink() or any(a.is_symlink() for a in p.parents if a!=root):
            raise ValueError('existing/redirected private application path')
    for name,raw in files.items():
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f:f.write(raw)
        p.chmod(0o644)
    return list(files)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description='Check declared public/private release rights before publication')
    ap.add_argument('lock',type=Path);ap.add_argument('--purpose',choices=['public-release','private-engineering'],default='public-release')
    args=ap.parse_args();check_rights(validate_lock(args.lock.read_bytes()),args.purpose)
    print('Declared rights gate passed for '+args.purpose+'; this does not publish or grant new rights.')
