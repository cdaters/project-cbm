#!/usr/bin/env python3
"""Additive POC2 lock: reuse verified POC1 inputs; never mutate its kit or packages."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
from build_contracts import encode,read_json
from retained_inputs import verify_kit


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('workspace',type=Path);ap.add_argument('recipe',type=Path);ap.add_argument('integration_commit');args=ap.parse_args()
    w=args.workspace.resolve(strict=True);recipe=args.recipe.resolve(strict=True)
    if not re.fullmatch('[a-f0-9]{40}',args.integration_commit):raise ValueError('full integration commit required')
    old=w/'inputs/frozen-poc1';lock=copy.deepcopy(verify_kit((old/'release-lock.json').read_bytes(),old))
    kit=w/'inputs/frozen-poc2';kit.mkdir();shutil.copytree(old/'objects',kit/'objects',copy_function=os.link)
    def store(path):
        path=Path(path)
        with path.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
        dst=kit/'objects'/sha
        if not dst.exists():shutil.copyfile(path,dst)
        return {'path':'objects/'+sha,'sha256':sha,'size_bytes':path.stat().st_size}
    def data(obj):
        raw=encode(obj);sha=hashlib.sha256(raw).hexdigest();dst=kit/'objects'/sha
        if not dst.exists():dst.write_bytes(raw)
        return {'path':'objects/'+sha,'sha256':sha,'size_bytes':len(raw)}
    def archive(paths,base):
        temp=kit/'next.tar'
        with tarfile.open(temp,'w') as tar:
            for p in sorted(paths):
                if not p.is_file() or p.is_symlink():continue
                info=tar.gettarinfo(str(p),str(p.relative_to(base)));info.uid=info.gid=0;info.uname=info.gname='';info.mtime=1789513200
                with p.open('rb') as f:tar.addfile(info,f)
        result=store(temp);temp.unlink();return result
    lock['schema_version']=2;lock['product']={'version':'1.1.0-poc.2','candidate':'private-engineering-poc2'}
    lock['integration']['git']['commit']=args.integration_commit
    lock['integration']['source']=store(w/'inputs/project-cbm-integration-poc2.tar')
    lock['base']['configuration']=store(recipe/'build/pigen/config.json')
    for key,path in {'defaults':'build/pigen/defaults.json','assets_license_inventory':'build/pigen/assets-license-inventory.json','sealing_recipe':'tools/install_poc_stage.py','first_boot_recipe':'build/pigen/stage-cbm/files/first_boot.py'}.items():
        lock['configuration'][key]=store(recipe/path)
    package_dir=w/'packages/poc2-engineering';pins=read_json(recipe/'build/inputs-poc.json')
    for name in ['vice','menu']:
        c=lock['components'][name];pin=pins[name]
        debs=[p for p in package_dir.glob('project-cbm-'+name+'_*.deb') if 'dbgsym' not in p.name]
        if len(debs)!=1:raise ValueError('ambiguous package')
        control=dict(x.split(': ',1) for x in subprocess.check_output(['dpkg-deb','-f',str(debs[0]),'Package','Version','Architecture'],text=True).splitlines())
        upstream,revision=control['Version'].rsplit('-',1)
        c['version']=pin['version'];c['source']['artifact']=store(w/'inputs'/pin['filename'])
        if name=='menu':
            c['source']['git']={k:pin[k] for k in ['repository','ref','commit','tag_object']}
        c['package']={'name':control['Package'],'version':control['Version'],'upstream_version':upstream,'revision':revision,'architecture':control['Architecture'],'artifact':store(debs[0])}
        package_source=package_dir/'project-cbm-menu-1.1.0_poc2/debian' if name=='menu' else recipe/'build/packages/vice/debian'
        c['recipe']=archive(list(package_source.rglob('*')),package_source)
        sourcefiles=[p for p in package_dir.glob('project-cbm-'+name+'_*') if p.suffix=='.dsc' or '.tar.' in p.name]
        c['corresponding_source']=archive(sourcefiles,package_dir)
        c['build_record']=data({'component':name,'package':c['package']['artifact'],'source_sha256':pin['sha256'],'build_info':store(next(package_dir.glob('project-cbm-'+name+'_*.buildinfo'))),'source_date_epoch':1789513200,'qualification':'package construction; physical Pi UNTESTED'})
    apt=w/'inputs/apt-retained-poc2';urlmap=read_json(apt/'catalog.json')
    urlmap={url:item for url,item in urlmap.items() if not (url.endswith('.deb') and '/rpi-connect' in url)}
    binary=[]
    for url,item in urlmap.items():
        desc=store(apt/item['path'])
        if desc['sha256']!=item['sha256'] or desc['size_bytes']!=item['size_bytes']:raise ValueError('APT retained input changed')
        if url.endswith('.deb'):binary.append({'artifact':desc,'role':'binary-package','origin':url})
    lock['base']['binary_package_closure']=data({'format':'project-cbm.input-catalog','schema_version':1,'entries':binary})
    metadata=read_json(kit/lock['base']['authenticated_apt_metadata']['path'])
    metadata['entries']=[x for x in metadata['entries'] if x['role']!='frozen-url-map']
    metadata['entries'].append({'role':'frozen-url-map','origin':'https://www.debian.org/','artifact':data(urlmap)})
    lock['base']['authenticated_apt_metadata']=data(metadata)
    sources=read_json(kit/lock['base']['source_package_closure']['path'])
    extra=w/'inputs/poc2-extra-source'
    for dsc in extra.glob('*.dsc'):
        match=re.search(r'^Checksums-Sha256:\n((?:[ \t].*\n)+)',dsc.read_text(),re.M)
        if not match:raise ValueError('source descriptor lacks SHA256')
        for line in match[1].splitlines():
            sha,size,name=line.split();p=extra/name
            if Path(name).name!=name or store(p)['sha256']!=sha or p.stat().st_size!=int(size):raise ValueError('source closure mismatch')
    for p in extra.iterdir():
        if p.is_file():sources['entries'].append({'artifact':store(p),'role':'corresponding-source','origin':'https://deb.debian.org/debian/'})
    lock['base']['source_package_closure']=data(sources)
    # Debugger installation changed host dependencies after component construction.
    # Retain exact supplemental host inputs and metadata; never silently claim old host state.
    host=read_json(kit/lock['build']['host_package_closure']['path'])
    supplement=w/'inputs/poc2-host-supplement'
    results=read_json(supplement/'results.json')
    if any(r['status'] for r in results):raise ValueError('host supplement incomplete')
    for r in results:
        directory=supplement/r['directory']
        for dsc in directory.glob('*.dsc'):
            match=re.search(r'^Checksums-Sha256:\n((?:[ \t].*\n)+)',dsc.read_text(),re.M)
            if not match:raise ValueError('host source missing SHA256')
            for line in match[1].splitlines():
                sha,size,name=line.split();payload=directory/name
                if Path(name).name!=name or store(payload)['sha256']!=sha or payload.stat().st_size!=int(size):raise ValueError('host source mismatch')
        for payload in directory.iterdir():
            if payload.is_file():host['entries'].append({'artifact':store(payload),'role':'host-supplement-'+r['kind'],'origin':'https://deb.debian.org/debian/'})
    for payload in Path('/var/lib/apt/lists').iterdir():
        if payload.is_file() and payload.name!='lock':host['entries'].append({'artifact':store(payload),'role':'host-authenticated-repository-metadata','origin':'https://deb.debian.org/debian/'})
    host['entries'].append({'artifact':store(supplement/'results.json'),'role':'host-supplement-acquisition-record','origin':'https://deb.debian.org/debian/'})
    lock['build']['host_package_closure']=data(host)
    lock['build']['toolchain']=store(supplement/'inventory.tsv')
    media=w/'inputs/qualification-media-0.1.0';manifest=read_json(media/'manifest.json')
    lock['qualification_media']={'artifact':store(media/'qualification-media.tar'),'source_commit':manifest['source_commit'],'profile':'private-engineering'}
    raw=encode(lock);verify_kit(raw,kit)
    (kit/'release-lock.json').write_bytes(raw);sha=hashlib.sha256(raw).hexdigest()
    (kit/'release-lock.sha256').write_text(sha+'  release-lock.json\n')
    print('FROZEN POC2',sha)


if __name__=='__main__':main()
