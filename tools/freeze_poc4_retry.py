#!/usr/bin/env python3
"""Freeze attempt #2 from immutable POC4 packages, changing only builder integration."""
import argparse, copy, hashlib, os, re
from pathlib import Path
from build_contracts import encode
from retained_inputs import verify_kit


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('workspace',type=Path);p.add_argument('recipe',type=Path)
    p.add_argument('integration_commit');a=p.parse_args()
    if not re.fullmatch('[0-9a-f]{40}',a.integration_commit):raise ValueError('exact commit required')
    w=a.workspace.resolve(strict=True);recipe=a.recipe.resolve(strict=True)
    old=w/'inputs/frozen-poc4';oldraw=(old/'release-lock.json').read_bytes()
    lock=copy.deepcopy(verify_kit(oldraw,old))
    kit=w/'inputs/frozen-poc4-attempt2';kit.mkdir();(kit/'objects').mkdir()
    for source in (old/'objects').iterdir():os.link(source,kit/'objects'/source.name)
    def store(path):
        raw=path.read_bytes();sha=hashlib.sha256(raw).hexdigest();target=kit/'objects'/sha
        if not target.exists():target.write_bytes(raw)
        return {'path':'objects/'+sha,'sha256':sha,'size_bytes':len(raw)}
    lock['integration']['git']['commit']=a.integration_commit
    lock['integration']['source']=store(w/'inputs/project-cbm-integration-poc4-attempt2.tar')
    lock['configuration']['sealing_recipe']=store(recipe/'tools/install_poc_stage.py')
    lock['base']['patches'].append(store(recipe/'build/pigen/target-environment.patch'))
    # Runtime/component packages retain their ORIGINAL source commits and hashes.
    raw=encode(lock);verify_kit(raw,kit)
    (kit/'release-lock.json').write_bytes(raw)
    digest=hashlib.sha256(raw).hexdigest()
    (kit/'release-lock.sha256').write_text(digest+'  release-lock.json\n')
    record={'candidate':lock['product']['candidate'],'attempt':2,
        'previous_attempt_lock_sha256':hashlib.sha256(oldraw).hexdigest(),
        'release_lock_sha256':digest,'integration_commit':a.integration_commit,
        'changes':['integration commit/source','target-environment pi-gen patch','sealing recipe chroot environment'],
        'unchanged':['all component package/source identities','base package/host closures','configuration defaults','first-boot payload','qualification media','optional software'],
        'installed_identity_changes':'integration commit and exact release-lock digest; not identical complete build inputs',
        'construction_argument':'--attempt 2'}
    (kit/'attempt.json').write_bytes(encode(record));print(digest)

if __name__=='__main__':main()
