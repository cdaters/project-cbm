#!/usr/bin/env python3
"""Freeze additive POC3 inputs; reuse the verified POC2 closure without modifying it."""
import argparse
import copy
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
from build_contracts import encode, read_json
from retained_inputs import verify_kit


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('workspace',type=Path);ap.add_argument('recipe',type=Path);ap.add_argument('integration_commit')
    args=ap.parse_args();w=args.workspace.resolve(strict=True);recipe=args.recipe.resolve(strict=True)
    if not re.fullmatch('[0-9a-f]{40}',args.integration_commit):raise ValueError('exact integration commit required')
    old=w/'inputs/frozen-poc2';lock=copy.deepcopy(verify_kit((old/'release-lock.json').read_bytes(),old))
    kit=w/'inputs/frozen-poc3-final';kit.mkdir();shutil.copytree(old/'objects',kit/'objects',copy_function=os.link)
    def store(path):
        path=Path(path);raw=path.read_bytes();sha=hashlib.sha256(raw).hexdigest();target=kit/'objects'/sha
        if not target.exists():target.write_bytes(raw)
        return {'path':'objects/'+sha,'sha256':sha,'size_bytes':len(raw)}
    def data(obj):
        path=kit/'new-record.json';path.write_bytes(encode(obj));result=store(path);path.unlink();return result
    def archive(paths,base):
        path=kit/'new-archive.tar'
        with tarfile.open(path,'w') as tar:
            for p in sorted(paths):
                if not p.is_file() or p.is_symlink():continue
                info=tar.gettarinfo(str(p),str(p.relative_to(base)));info.uid=info.gid=0;info.uname=info.gname='';info.mtime=1789513200
                with p.open('rb') as f:tar.addfile(info,f)
        result=store(path);path.unlink();return result
    lock['product']={'version':'1.1.0-poc.3','candidate':'private-engineering-poc3'}
    lock['integration']['git']['commit']=args.integration_commit
    lock['integration']['source']=store(w/'inputs/project-cbm-integration-poc3-final.tar')
    lock['base']['configuration']=store(recipe/'build/pigen/config.json')
    for key,path in {'defaults':'build/pigen/defaults.json','assets_license_inventory':'build/pigen/assets-license-inventory.json','sealing_recipe':'tools/install_poc_stage.py','first_boot_recipe':'build/pigen/stage-cbm/files/first_boot.py'}.items():
        lock['configuration'][key]=store(recipe/path)
    packages=w/'packages/poc3-final';c=lock['components']['vice']
    debs=[p for p in packages.glob('project-cbm-vice_*.deb') if 'dbgsym' not in p.name]
    if len(debs)!=1:raise ValueError('ambiguous VICE artifact')
    metadata=dict(l.split(': ',1) for l in subprocess.check_output(['dpkg-deb','-f',str(debs[0]),'Package','Version','Architecture'],text=True).splitlines())
    upstream,revision=metadata['Version'].rsplit('-',1)
    c['package']={'name':metadata['Package'],'version':metadata['Version'],'architecture':metadata['Architecture'],'upstream_version':upstream,'revision':revision,'artifact':store(debs[0])}
    package_recipe=recipe/'build/packages/vice/debian'
    c['recipe']=archive(list(package_recipe.rglob('*')),package_recipe)
    c['patches']=[store(package_recipe/'patches/presentation-diagnostics.patch')]
    c['corresponding_source']=archive([p for p in packages.glob('project-cbm-vice_*') if p.suffix=='.dsc' or '.tar.' in p.name],packages)
    c['build_record']=data({'component':'vice','package':c['package']['artifact'],'source_sha256':c['source']['artifact']['sha256'],'build_info':store(next(packages.glob('project-cbm-vice_*.buildinfo'))),'source_date_epoch':1789513200,'qualification':'package construction and software reference tests; physical POC3 UNTESTED'})
    supplement=w/'inputs/poc3-host-supplement'
    host=read_json(kit/lock['build']['host_package_closure']['path'])
    acquired=read_json(supplement/'results.json')
    if not acquired or any(entry['status'] for entry in acquired):raise ValueError('incomplete host supplement')
    for entry in acquired:
        directory=supplement/entry['directory']
        for dsc in directory.glob('*.dsc'):
            match=re.search(r'^Checksums-Sha256:\n((?:[ \t].*\n)+)',dsc.read_text(),re.M)
            if not match:raise ValueError('missing source SHA256 fields')
            for line in match[1].splitlines():
                sha,size,name=line.split();p=directory/name
                if Path(name).name!=name or store(p)['sha256']!=sha or p.stat().st_size!=int(size):raise ValueError('host source mismatch')
        for p in directory.iterdir():
            if p.is_file():host['entries'].append({'artifact':store(p),'role':'host-supplement-'+entry['kind'],'origin':'https://deb.debian.org/debian/'})
    for p in Path('/var/lib/apt/lists').iterdir():
        if p.is_file() and p.name!='lock':host['entries'].append({'artifact':store(p),'role':'host-authenticated-repository-metadata','origin':'https://deb.debian.org/debian/'})
    host['entries'].append({'artifact':store(supplement/'results.json'),'role':'host-supplement-acquisition-record','origin':'https://deb.debian.org/debian/'})
    lock['build']['host_package_closure']=data(host)
    lock['build']['toolchain']=store(supplement/'inventory.tsv')
    raw=encode(lock);verify_kit(raw,kit)
    (kit/'release-lock.json').write_bytes(raw);sha=hashlib.sha256(raw).hexdigest()
    (kit/'release-lock.sha256').write_text(sha+'  release-lock.json\n')
    print('FROZEN POC3',sha)

if __name__=='__main__':main()
