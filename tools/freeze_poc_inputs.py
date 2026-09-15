#!/usr/bin/env python3
"""Freeze a private input kit from completed exact-version acquisition and packages.

Run inside Linux after source/metadata acquisition has stopped. Creates a new kit;
never overwrites a lock. This is an engineering POC recipe, not a release publisher.
"""
import argparse
import hashlib
import io
import json
import re
from pathlib import Path
import shutil
import subprocess
import tarfile
from build_contracts import encode, validate_lock
from retained_inputs import verify_kit


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('workspace',type=Path);p.add_argument('recipe',type=Path);p.add_argument('integration_commit')
    args=p.parse_args();w=args.workspace.resolve(strict=True);recipe=args.recipe.resolve(strict=True)
    kit=w/'inputs/frozen-poc1';kit.mkdir();(kit/'objects').mkdir()
    def store(path):
        path=Path(path)
        with path.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
        dest=kit/'objects'/sha
        if not dest.exists():shutil.copyfile(path,dest)
        return {'path':'objects/'+sha,'sha256':sha,'size_bytes':path.stat().st_size}
    def data(value):
        raw=encode(value);sha=hashlib.sha256(raw).hexdigest();(kit/'objects'/sha).write_bytes(raw)
        return {'path':'objects/'+sha,'sha256':sha,'size_bytes':len(raw)}
    def archive(paths,base):
        temporary=kit/'archive-next.tar'
        with tarfile.open(temporary,'w') as tar:
            for path in sorted(paths):
                if not path.is_file() or path.is_symlink():continue
                info=tar.gettarinfo(str(path),arcname=str(path.relative_to(base)))
                info.uid=info.gid=0;info.uname=info.gname='';info.mtime=1789513200
                with path.open('rb') as stream:tar.addfile(info,stream)
        result=store(temporary);temporary.unlink();return result
    def catalog(entries):
        return data({'format':'project-cbm.input-catalog','schema_version':1,'entries':entries})
    def entry(path,role,origin):return {'artifact':store(path),'role':role,'origin':origin}
    def closure(directory,role):
        outcomes=json.loads((directory/'results.json').read_text())
        recovered=json.loads((directory/'snapshot-recovered.json').read_text()) if (directory/'snapshot-recovered.json').exists() else []
        reconciled=json.loads((directory/'source-reconciled.json').read_text()) if (directory/'source-reconciled.json').exists() else []
        recovered_pairs={(r['package'],r['version']) for r in recovered+reconciled}
        source_names={(r['package'],r['version']) for r in reconciled}
        for r in outcomes:
            if role=='corresponding-source' and r['package']=='rpi-connect-lite':continue
            if r['status'] and (r['package'],r['version']) not in recovered_pairs:
                raise ValueError('unresolved exact package input: '+r['package'])
        selected=[]
        for r in outcomes:
            if role=='corresponding-source' and r['package']=='rpi-connect-lite':continue
            files=[f for f in (directory/r['directory']).iterdir() if f.is_file() and f.suffix not in ['.log','.json']]
            if not files:raise ValueError('successful acquisition has no retained payload')
            if 'source' in role:
                descriptors=[f for f in files if f.suffix=='.dsc']
                if len(descriptors)!=1:raise ValueError('missing unique source descriptor')
                text=descriptors[0].read_text()
                fields=re.search(r'^Checksums-Sha256:\n((?:[ \t].*\n)+)',text,re.M)
                if not fields:raise ValueError('source descriptor lacks SHA-256 closure')
                for line in fields[1].splitlines():
                    sha,size,name=line.split()
                    if Path(name).name!=name:raise ValueError('unsafe source payload name')
                    payload=descriptors[0].parent/name
                    with payload.open('rb') as stream:actual=hashlib.file_digest(stream,'sha256').hexdigest()
                    if actual!=sha or payload.stat().st_size!=int(size):raise ValueError('source descriptor payload mismatch')
            log=(directory/r['directory']/'acquisition.log').read_text()
            providers=re.findall(r'Get:\d+ (https?://[^ ]+)',log)
            origin='https://snapshot.debian.org/' if r['status'] and (r['package'],r['version']) not in source_names else (providers[0].replace('http://','https://') if providers else 'https://www.debian.org/')
            selected += [entry(f,role,origin) for f in files]
            api=directory/r['directory']/'snapshot-api.json'
            if api.exists():selected.append(entry(api,'snapshot-api-record','https://snapshot.debian.org/'))
        selected += [entry(directory/'results.json','acquisition-record','https://www.debian.org/')]
        if recovered:selected += [entry(directory/'snapshot-recovered.json','snapshot-reconciliation','https://snapshot.debian.org/')]
        if reconciled:selected += [entry(directory/'source-reconciled.json','source-name-reconciliation','https://www.debian.org/')]
        return selected
    apt=w/'inputs/apt-retained';urlmap=json.loads((apt/'catalog.json').read_text())
    binary=[];metadata=[]
    urlmap={url:item for url,item in urlmap.items() if not (url.endswith('.deb') and '/rpi-connect' in url)}
    for url,item in urlmap.items():
        path=apt/item['path']
        with path.open('rb') as f: actual=hashlib.file_digest(f,'sha256').hexdigest()
        if actual!=item['sha256'] or path.stat().st_size!=item['size_bytes']:raise ValueError('APT retention changed')
        e=entry(path,'binary-package' if url.endswith('.deb') else 'authenticated-repository-input',url)
        (binary if url.endswith('.deb') else metadata).append(e)
    # URL map is retained independently so frozen transport can replay requests.
    apt_catalog=data(urlmap)
    runtime_sources=w/'builds/resolve-inputs/work/stage2/rootfs/tmp/cbm-source-closure'
    sources=closure(runtime_sources,'corresponding-source')
    host=closure(w/'inputs/host-binary-closure','host-binary-package')+closure(w/'inputs/host-source-closure','host-corresponding-source')
    for path in Path('/var/lib/apt/lists').iterdir():
        if path.is_file() and path.name!='lock':host.append(entry(path,'host-authenticated-repository-metadata','https://deb.debian.org/debian/'))
    bootstrap=store(w/'inputs/debian-13-genericcloud-arm64-20260712-2537.qcow2')
    host.append({'role':'bootstrap-image','origin':'https://cloud.debian.org/images/cloud/trixie/20260712-2537/','artifact':bootstrap})
    package_dir=w/'packages/poc2';pins=json.loads((recipe/'build/inputs-poc.json').read_text())
    components={}
    for name in ['vice','menu','tcpser']:
        pin=pins[name];debs=[f for f in package_dir.glob('project-cbm-'+name+'_*.deb') if 'dbgsym' not in f.name]
        if len(debs)!=1:raise ValueError('ambiguous component package')
        control=subprocess.check_output(['dpkg-deb','-f',str(debs[0]),'Package','Version','Architecture'],text=True)
        control=dict(line.split(': ',1) for line in control.splitlines());upstream,revision=control['Version'].rsplit('-',1)
        source={'origin':pin.get('origin',pin.get('repository')),'artifact':store(w/'inputs'/pin['filename'])}
        if name in ['menu','tcpser']:
            source['git']={'repository':pin['repository'],'commit':pin['commit'],'ref':pin.get('ref','refs/heads/master'),'tag_object':pin.get('tag_object')}
        corresponding=[f for f in package_dir.glob('project-cbm-'+name+'_*') if f.suffix=='.dsc' or '.tar.' in f.name]
        recipe_dir=package_dir/'project-cbm-menu-1.1.0_poc1/debian' if name=='menu' else recipe/'build/packages'/name/'debian'
        options=['--enable-sdl2ui','--with-alsa','--with-sdlsound','--without-pulse','--disable-arch','--enable-x64','--disable-html-docs'] if name=='vice' else []
        package_artifact=store(debs[0])
        record=data({'component':name,'package':package_artifact,'source_sha256':pin['sha256'],
                     'build_info':store(next(package_dir.glob('project-cbm-'+name+'_*.buildinfo'))),
                     'source_date_epoch':1789513200,'flags':'generic arm64; Debian flags; no march=native',
                     'qualification':'package construction only; no physical Pi execution'})
        components[name]={'version':pin['version'],'source':source,
            'package':{'name':control['Package'],'version':control['Version'],'upstream_version':upstream,'revision':revision,'architecture':control['Architecture'],'artifact':package_artifact},
            'recipe':archive(list(recipe_dir.rglob('*')),recipe_dir),'patches':[],'build_options':options,
            'build_record':record,'corresponding_source':archive(corresponding,package_dir)}
    pg=pins['pi_gen'];integration=store(w/'inputs/project-cbm-integration.tar')
    lock={'format':'project-cbm.release-lock','schema_version':1,'fixture':False,
          'product':{'version':'1.1.0-poc.1','candidate':'private-engineering-poc1'},'architecture':'arm64',
          'integration':{'git':{'repository':'https://github.com/cdaters/project-cbm.git','commit':args.integration_commit,'ref':'refs/heads/feature/1.1-build-foundation','tag_object':None},'source':integration},
          'base':{'distribution':'Raspberry Pi OS Lite','suite':'trixie','release_identity':'trixie-13.7-input-resolution-2026-09-15',
            'pi_gen':{'git':{'repository':pg['repository'],'commit':pg['commit'],'ref':pg['ref'],'tag_object':None},'source':store(w/'inputs'/pg['filename'])},
            'stages':['stage0','stage1','stage2','stage-cbm'],'configuration':store(recipe/'build/pigen/config.json'),'patches':[store(recipe/'build/pigen/exclude-connect.patch'),store(recipe/'build/pigen/frozen-export.patch')],
            'authenticated_apt_metadata':catalog(metadata+[{'role':'frozen-url-map','origin':'https://www.debian.org/','artifact':apt_catalog}]),
            'binary_package_closure':catalog(binary),'source_package_closure':catalog(sources)},
          'components':components,
          'configuration':{'schema_version':1,'defaults':store(recipe/'build/pigen/defaults.json'),
             'assets_license_inventory':store(recipe/'build/pigen/assets-license-inventory.json'),
             'sealing_recipe':store(recipe/'tools/install_poc_stage.py'),
             'first_boot_recipe':store(recipe/'build/pigen/stage-cbm/files/first_boot.py')},
          'build':{'environment_contract_version':1,'environment_recipe':archive(list((recipe/'build/host').rglob('*')),recipe/'build/host'),
             'bootstrap':bootstrap,'host_package_closure':catalog(host),
             'toolchain':store(w/'inputs/host-binary-closure/inventory.tsv'),
             'reproducibility_policy':store(recipe/'build/pigen/reproducibility-policy.json'),'source_date_epoch':1789513200}}
    raw=encode(lock);validate_lock(raw);verify_kit(raw,kit)
    (kit/'release-lock.json').write_bytes(raw)
    (kit/'release-lock.sha256').write_text(hashlib.sha256(raw).hexdigest()+'  release-lock.json\n')
    print('FROZEN',kit,hashlib.sha256(raw).hexdigest())


if __name__=='__main__':main()
