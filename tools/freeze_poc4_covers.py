#!/usr/bin/env python3
"""Freeze POC4 attempt 3: new Menu/Covers input, unchanged runtime/VICE/TCPser."""
import argparse, copy, hashlib, os, re, subprocess, tarfile
from pathlib import Path
from build_contracts import encode, read_json
from retained_inputs import verify_kit


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('workspace',type=Path);p.add_argument('recipe',type=Path)
    p.add_argument('integration_commit');p.add_argument('menu_commit');p.add_argument('menu_tag_object')
    a=p.parse_args()
    for value in (a.integration_commit,a.menu_commit,a.menu_tag_object):
        if not re.fullmatch('[0-9a-f]{40}',value):raise ValueError('exact Git identity required')
    w=a.workspace.resolve(strict=True);recipe=a.recipe.resolve(strict=True)
    old=w/'inputs/frozen-poc4-attempt2';oldraw=(old/'release-lock.json').read_bytes()
    lock=copy.deepcopy(verify_kit(oldraw,old))
    kit=w/'inputs/frozen-poc4-attempt3';kit.mkdir();(kit/'objects').mkdir()
    for source in (old/'objects').iterdir():os.link(source,kit/'objects'/source.name)
    def store(path):
        raw=path.read_bytes();sha=hashlib.sha256(raw).hexdigest();target=kit/'objects'/sha
        if not target.exists():target.write_bytes(raw)
        return {'path':'objects/'+sha,'sha256':sha,'size_bytes':len(raw)}
    def record(value):
        path=kit/'record.tmp';path.write_bytes(encode(value));d=store(path);path.unlink();return d
    def archive(paths,base):
        path=kit/'source.tmp'
        with tarfile.open(path,'w') as tar:
            for entry in sorted(paths):
                if not entry.is_file() or entry.is_symlink():continue
                info=tar.gettarinfo(str(entry),str(entry.relative_to(base)))
                info.uid=info.gid=0;info.uname=info.gname='';info.mtime=lock['build']['source_date_epoch']
                with entry.open('rb') as stream:tar.addfile(info,stream)
        d=store(path);path.unlink();return d
    lock['integration']['git']['commit']=a.integration_commit
    lock['integration']['source']=store(w/'inputs/project-cbm-integration-poc4-attempt3.tar')
    lock['configuration']['assets_license_inventory']=store(recipe/'build/pigen/assets-license-inventory.json')
    packages=w/'packages/poc4-attempt3';menu=packages/'project-cbm-menu'
    debs=list(packages.glob('project-cbm-menu_*.deb'))
    if len(debs)!=1:raise ValueError('ambiguous Menu package')
    fields=dict(line.split(': ',1) for line in subprocess.check_output(['dpkg-deb','-f',str(debs[0]),'Package','Version','Architecture'],text=True).splitlines())
    if fields!={'Package':'project-cbm-menu','Version':'1.1.0~poc4.1-1+pcbm1','Architecture':'all'}:raise ValueError('wrong Menu package')
    c=copy.deepcopy(lock['components']['menu']);c['version']='1.1.0_poc4.1'
    c['source']['git'].update(ref='refs/tags/v1.1.0_poc4.1',commit=a.menu_commit,tag_object=a.menu_tag_object)
    c['source']['artifact']=store(w/'inputs/project-cbm-menu-1.1.0_poc4.1.tar')
    upstream,revision=fields['Version'].rsplit('-',1)
    c['package'].update(version=fields['Version'],upstream_version=upstream,revision=revision,artifact=store(debs[0]))
    c['recipe']=archive([menu/'debian'/n for n in ('control','rules','copyright','changelog','source/format','install','docs')],menu/'debian')
    c['corresponding_source']=archive([f for f in packages.glob('project-cbm-menu_*') if f.suffix=='.dsc' or '.tar.' in f.name],packages)
    manifest=read_json(menu/'docs/cover-artwork.json')
    for item in manifest['files']:
        data=(menu/item['path']).read_bytes()
        if len(data)!=item['size_bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:raise ValueError('cover changed')
    # Existing Debian package closure is authoritative; require exact MC and mixer inputs.
    closure=read_json(kit/lock['base']['binary_package_closure']['path']);utilities={}
    for item in closure['entries']:
        path=kit/item['artifact']['path']
        values=subprocess.check_output(['dpkg-deb','-f',str(path),'Package','Version','Architecture'],text=True)
        metadata=dict(line.split(': ',1) for line in values.splitlines())
        if metadata['Package'] in ('mc','mc-data','alsa-utils'):
            utilities[metadata['Package']]={'metadata':metadata,'artifact':item['artifact'],'origin':item['origin']}
    if set(utilities)!={'mc','mc-data','alsa-utils'}:raise ValueError('missing utility closure')
    if any(utilities[n]['metadata']['Version']!='3:4.8.33-1+deb13u1' for n in ('mc','mc-data')):raise ValueError('unexpected mc version')
    c['build_record']=record({'component':'menu','package':c['package']['artifact'],'source_sha256':c['source']['artifact']['sha256'],
        'source_commit':a.menu_commit,'build_info':store(next(packages.glob('*.buildinfo'))),
        'runtime_api_version':1,'configuration_request_version':1,'information_schema_version':1,
        'source_date_epoch':lock['build']['source_date_epoch'],'covers':{'manifest':store(menu/'docs/cover-artwork.json'),
        'renderer':store(menu/'lib/pcbm_cover_view.py'),'launcher':store(menu/'scripts/pcbm-run-vice'),'wrapper':store(menu/'scripts/pcbm-cover'),'registry':store(recipe/'runtime/data/profiles.json'),
        'assets':[store(menu/item['path']) for item in manifest['files']]},'utilities':utilities,
        'bounded_changes':['Advanced Mixer without sudo/global store','explicit import destinations'],
        'physical_qualification':'UNTESTED'})
    lock['components']['menu']=c
    raw=encode(lock);verify_kit(raw,kit)
    (kit/'release-lock.json').write_bytes(raw);digest=hashlib.sha256(raw).hexdigest()
    (kit/'release-lock.sha256').write_text(digest+'  release-lock.json\n')
    (kit/'attempt.json').write_bytes(encode({'attempt':3,'candidate':lock['product'],
        'prior_lock_sha256':hashlib.sha256(oldraw).hexdigest(),'release_lock_sha256':digest,
        'changed':['Menu source/tag/package/recipe/build record','integration source/commit','asset inventory','installed identity'],
        'unchanged':['runtime/VICE/TCPser packages','base/host package closures','pi-gen/environment patches','first-boot/service/USB backend','VICE geometry','qualification media','optional software'],
        'construction_argument':'--attempt 3'}))
    print(digest)

if __name__=='__main__':main()
