#!/usr/bin/env python3
"""Freeze the new activated candidate without changing any POC1–3 input."""
import argparse, copy, hashlib, os, re, subprocess, tarfile
from pathlib import Path
from build_contracts import encode, read_json
from retained_inputs import verify_kit
from private_application import check_rights


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('workspace',type=Path);ap.add_argument('recipe',type=Path)
    ap.add_argument('integration_commit');ap.add_argument('menu_commit');ap.add_argument('menu_tag_object')
    a=ap.parse_args();w=a.workspace.resolve(strict=True);recipe=a.recipe.resolve(strict=True)
    for pin in (a.integration_commit,a.menu_commit,a.menu_tag_object):
        if not re.fullmatch('[0-9a-f]{40}',pin):raise ValueError('exact Git identity required')
    old=w/'inputs/frozen-poc3-final';lock=copy.deepcopy(verify_kit((old/'release-lock.json').read_bytes(),old))
    kit=w/'inputs/frozen-poc4';kit.mkdir();(kit/'objects').mkdir()
    for p in (old/'objects').iterdir():os.link(p,kit/'objects'/p.name)
    def store(path):
        raw=Path(path).read_bytes();sha=hashlib.sha256(raw).hexdigest();target=kit/'objects'/sha
        if not target.exists():target.write_bytes(raw)
        return {'path':'objects/'+sha,'sha256':sha,'size_bytes':len(raw)}
    def data(value):
        p=kit/'record.tmp';p.write_bytes(encode(value));d=store(p);p.unlink();return d
    def archive(paths,base):
        p=kit/'archive.tmp'
        with tarfile.open(p,'w') as tar:
            for entry in sorted(paths):
                if not entry.is_file() or entry.is_symlink():continue
                info=tar.gettarinfo(str(entry),str(entry.relative_to(base)))
                info.uid=info.gid=0;info.uname=info.gname='';info.mtime=1789513200
                with entry.open('rb') as f:tar.addfile(info,f)
        d=store(p);p.unlink();return d
    lock['schema_version']=4
    lock['product']={'version':'1.1.0-poc.4','candidate':'private-engineering-poc4'}
    lock['integration']['git']['commit']=a.integration_commit
    lock['integration']['source']=store(w/'inputs/project-cbm-integration-poc4-final.tar')
    lock['base']['configuration']=store(recipe/'build/pigen/config.json')
    for k,p in {'defaults':'build/pigen/defaults.json','assets_license_inventory':'build/pigen/assets-license-inventory.json','sealing_recipe':'tools/install_poc_stage.py','first_boot_recipe':'build/pigen/stage-cbm/files/first_boot.py'}.items():
        lock['configuration'][k]=store(recipe/p)
    packages=w/'packages/poc4-final'
    for name,commit,origin,ref,tag,source,recipe_dir in [
        ('menu',a.menu_commit,'https://github.com/cdaters/project-cbm-menu','refs/tags/v1.1.0_poc4',a.menu_tag_object,
         w/'inputs/project-cbm-menu-1.1.0_poc4.tar',packages/'menu/debian'),
        ('runtime',a.integration_commit,'https://github.com/cdaters/project-cbm','refs/heads/feature/1.1-build-foundation',None,
         w/'inputs/project-cbm-integration-poc4-final.tar',recipe/'build/packages/runtime/debian')]:
        debs=list(packages.glob('project-cbm-'+name+'_*.deb'))
        if len(debs)!=1:raise ValueError('ambiguous package')
        fields=dict(line.split(': ',1) for line in subprocess.check_output(['dpkg-deb','-f',str(debs[0]),'Package','Version','Architecture'],text=True).splitlines())
        upstream,revision=fields['Version'].rsplit('-',1)
        package={'name':fields['Package'],'version':fields['Version'],'architecture':fields['Architecture'],
                 'upstream_version':upstream,'revision':revision,'artifact':store(debs[0])}
        c={'version':'1.1.0_poc4','source':{'origin':origin,'artifact':store(source),
             'git':{'repository':origin,'ref':ref,'commit':commit,'tag_object':tag}},
           'package':package,'recipe':archive([recipe_dir/n for n in ('control','rules','copyright','changelog','source/format','install','docs') if (recipe_dir/n).is_file()],recipe_dir),'patches':[],
           'build_options':['dpkg-buildpackage -us -uc -sa','SOURCE_DATE_EPOCH=1789513200'],
           'corresponding_source':archive([p for p in packages.glob('project-cbm-'+name+'_*') if p.suffix=='.dsc' or '.tar.' in p.name],packages)}
        c['build_record']=data({'component':name,'package':package['artifact'],'source_sha256':c['source']['artifact']['sha256'],
            'source_commit':commit,'build_info':store(next(packages.glob('project-cbm-'+name+'_*.buildinfo'))),
            'runtime_api_version':1,'configuration_request_version':1,'information_schema_version':1,
            'source_date_epoch':1789513200,'qualification':'native staging; physical candidate UNTESTED'})
        lock['components'][name]=c
    optional=w/'inputs/optional-software-2026-09-16'
    fragment=read_json(optional/'optional-software.json')
    for p in (optional/'objects').iterdir():store(p)
    lock['optional_software']=fragment['optional_software'] if 'optional_software' in fragment else fragment
    pin=read_json(recipe/'build/optional/striketerm.json')
    lock['optional_software']['striketerm']={k:pin[k] for k in ('version','origin','classification','public_release_rights')}
    lock['optional_software']['striketerm'].update(artifact=store(w/'inputs/runtime1-striketerm-review/st2014final.d64'),rights_review=store(recipe/'build/optional/striketerm.json'))
    check_rights(lock,'private-engineering')
    raw=encode(lock);verify_kit(raw,kit)
    (kit/'release-lock.json').write_bytes(raw)
    sha=hashlib.sha256(raw).hexdigest();(kit/'release-lock.sha256').write_text(sha+'  release-lock.json\n')
    print('Frozen private POC4 input lock:',sha)

if __name__=='__main__':main()
