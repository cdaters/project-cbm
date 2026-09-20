#!/usr/bin/env python3
"""Freeze a private release refinement from a verified predecessor kit."""
import argparse
import copy
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tarfile
import sys
import tempfile
from build_contracts import encode, read_json, verify_artifact
from retained_inputs import verify_kit


def verify_predecessor(old, workspace):
    """Verify historical recipes with their exact retained integration, not new recipes."""
    lock = read_json(old/'release-lock.json')
    source = lock['integration']['source']
    verify_artifact(old, source)
    scratch = workspace/'scratch'
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='verify-predecessor-', dir=scratch) as name:
        target = Path(name)
        with tarfile.open(old/source['path']) as archive:
            for member in archive.getmembers():
                if (not (member.name.startswith('project-cbm/') or (member.name == 'project-cbm' and member.isdir()))
                        or '..' in Path(member.name).parts or not (member.isdir() or member.isfile())):
                    raise ValueError('unsafe predecessor integration archive')
            archive.extractall(target, filter='data')
        subprocess.run([sys.executable, str(target/'project-cbm/tools/retained_inputs.py'),
                        str(old/'release-lock.json'), str(old)], check=True,
                       env={'PATH':os.environ['PATH'],'LC_ALL':'C','PYTHONDONTWRITEBYTECODE':'1'})
    return lock


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('workspace', type=Path)
    p.add_argument('recipe', type=Path)
    p.add_argument('integration_commit')
    p.add_argument('menu_commit')
    p.add_argument('menu_tag_object')
    p.add_argument('--attempt',type=int,required=True)
    p.add_argument('--previous-attempt',type=int,required=True)
    p.add_argument('--runtime-version',required=True)
    p.add_argument('--menu-version',required=True)
    p.add_argument('--reuse-menu',action='store_true')
    p.add_argument('--vice-version')
    p.add_argument('--product-version')
    p.add_argument('--candidate')
    a = p.parse_args()
    if not 6 <= a.previous_attempt < a.attempt < 100:raise ValueError('distinct increasing attempt required')
    for version in (a.runtime_version,a.menu_version):
        if not re.fullmatch(r'1[.]1[.]0~(?:poc4[.][0-9]+|rc[0-9]+)-1(?:[+]pcbm1)?',version):raise ValueError('unsupported private package version')
    if bool(a.product_version) != bool(a.candidate):raise ValueError('complete product identity required')
    if a.candidate and not re.fullmatch(r'private-engineering-rc[0-9]+',a.candidate):raise ValueError('private RC identity required')
    if a.product_version and not re.fullmatch(r'1[.]1[.]0-rc[.][0-9]+',a.product_version):raise ValueError('RC version required')
    menu_label=a.menu_version.rsplit('-',1)[0].replace('~','_')
    runtime_label=a.runtime_version.rsplit('-',1)[0].replace('~','_')
    for pin in (a.integration_commit, a.menu_commit, a.menu_tag_object):
        if not re.fullmatch('[0-9a-f]{40}', pin):
            raise ValueError('exact Git identity required')
    w = a.workspace.resolve(strict=True)
    recipe = a.recipe.resolve(strict=True)
    export=read_json(w/'inputs'/f'candidate-export-attempt{a.attempt}.json')
    if (export['integration_commit'],export['menu_commit'],export['menu_tag_object']) != (a.integration_commit,a.menu_commit,a.menu_tag_object):raise ValueError('export identity mismatch')
    for descriptor in export['archives']:
        path=w/descriptor['path']
        if path.stat().st_size!=descriptor['size_bytes'] or hashlib.sha256(path.read_bytes()).hexdigest()!=descriptor['sha256']:raise ValueError('export bytes mismatch')
    old = w/f'inputs/frozen-poc4-attempt{a.previous_attempt}'
    oldraw = (old/'release-lock.json').read_bytes()
    lock = copy.deepcopy(verify_predecessor(old,w))
    if a.product_version:lock['product'].update(version=a.product_version,candidate=a.candidate)
    kit = w/f'inputs/frozen-poc4-attempt{a.attempt}'
    kit.mkdir()
    (kit/'objects').mkdir()
    for source in (old/'objects').iterdir():
        os.link(source, kit/'objects'/source.name)

    def store(path):
        raw = path.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        target = kit/'objects'/sha
        if not target.exists():
            target.write_bytes(raw)
        elif target.read_bytes() != raw:
            raise ValueError('content object mismatch')
        return {'path':'objects/'+sha, 'sha256':sha, 'size_bytes':len(raw)}

    def record(value):
        path = kit/'record.tmp'
        path.write_bytes(encode(value))
        descriptor = store(path)
        path.unlink()
        return descriptor

    def archive(paths, base):
        path = kit/'source.tmp'
        with tarfile.open(path, 'w') as tar:
            for entry in sorted(paths):
                if not entry.is_file() or entry.is_symlink():
                    continue
                info = tar.gettarinfo(str(entry), str(entry.relative_to(base)))
                info.uid = info.gid = 0
                info.uname = info.gname = ''
                info.mtime = lock['build']['source_date_epoch']
                with entry.open('rb') as stream:
                    tar.addfile(info, stream)
        descriptor = store(path)
        path.unlink()
        return descriptor

    integration = w/f'inputs/project-cbm-integration-poc4-attempt{a.attempt}.tar'
    lock['integration']['git']['commit'] = a.integration_commit
    lock['integration']['source'] = store(integration)
    lock['base']['configuration'] = store(recipe/'build/pigen/config.json')
    for key, source in [('defaults','build/pigen/defaults.json'),
                        ('first_boot_recipe','build/pigen/stage-cbm/files/first_boot.py'),
                        ('sealing_recipe','tools/install_poc_stage.py')]:
        lock['configuration'][key] = store(recipe/source)
    # Refresh path-bearing application manifests/recipes; payload rights remain unchanged.
    from optional_software import payload
    sid = lock['optional_software']['sid_wizard']
    sid['rights_review'] = store(recipe/'build/optional/sid-wizard.json')
    sid['recipe'] = store(recipe/'tools/optional_software.py')
    temporary = kit/'sid-payload.tmp'
    temporary.write_bytes(payload(kit/sid['source']['path'],read_json(recipe/'build/optional/sid-wizard.json')))
    sid['artifact'] = store(temporary)
    temporary.unlink()
    lock['optional_software']['striketerm']['rights_review'] = store(recipe/'build/optional/striketerm.json')
    packages = w/f'packages/poc4-attempt{a.attempt}'
    oldrecord = read_json(old/lock['components']['menu']['build_record']['path'])
    if a.reuse_menu:
        prior_menu=lock['components']['menu']
        if (prior_menu['package']['version'], prior_menu['source']['git']['commit'], prior_menu['source']['git']['tag_object']) != (a.menu_version,a.menu_commit,a.menu_tag_object):
            raise ValueError('reused Menu identity differs from predecessor')
        if hashlib.sha256((w/f'inputs/project-cbm-menu-{menu_label}.tar').read_bytes()).hexdigest()!=prior_menu['source']['artifact']['sha256']:
            raise ValueError('reused Menu source bytes differ')
    for name, version, source, commit, ref, tag in (
        ('runtime', a.runtime_version, integration, a.integration_commit,
         'refs/heads/feature/1.1-build-foundation', None),
        ('menu', a.menu_version, w/f'inputs/project-cbm-menu-{menu_label}.tar',
         a.menu_commit, 'refs/tags/v'+menu_label, a.menu_tag_object)):
        if name=='menu' and a.reuse_menu:
            continue
        debs = list(packages.glob('project-cbm-'+name+'_*.deb'))
        if len(debs) != 1:
            raise ValueError('ambiguous package')
        fields = dict(line.split(': ', 1) for line in subprocess.check_output(
            ['dpkg-deb','-f',str(debs[0]),'Package','Version','Architecture'], text=True).splitlines())
        if fields != {'Package':'project-cbm-'+name,'Version':version,'Architecture':'all'}:
            raise ValueError('wrong package identity')
        component = copy.deepcopy(lock['components'][name])
        component['version'] = runtime_label if name == 'runtime' else menu_label
        component['source']['git'].update(ref=ref, commit=commit, tag_object=tag)
        component['source']['artifact'] = store(source)
        upstream, revision = version.rsplit('-', 1)
        component['package'].update(version=version, upstream_version=upstream,
                                    revision=revision, artifact=store(debs[0]))
        d = packages/name/'debian'
        component['recipe'] = archive([f for f in d.rglob('*') if f.is_file() and
            str(f.relative_to(d)) in ('control','rules','copyright','changelog','source/format','install','docs')], d)
        component['corresponding_source'] = archive([f for f in packages.glob('project-cbm-'+name+'_*')
            if f.suffix == '.dsc' or '.tar.' in f.name], packages)
        build = {'component':name,'package':component['package']['artifact'],
            'source_sha256':component['source']['artifact']['sha256'], 'source_commit':commit,
            'build_info':store(next(packages.glob('project-cbm-'+name+'_*.buildinfo'))),
            'runtime_api_version':1,'configuration_request_version':1,'information_schema_version':1,
            'source_date_epoch':lock['build']['source_date_epoch'],'physical_qualification':'UNTESTED'}
        if name == 'menu':
            menu = packages/'menu'
            manifest = read_json(menu/'docs/cover-artwork.json')
            for item in manifest['files']:
                data = (menu/item['path']).read_bytes()
                if len(data) != item['size_bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                    raise ValueError('Cover artwork changed')
            build['covers'] = {key:store(path) for key,path in {
                'manifest':menu/'docs/cover-artwork.json','renderer':menu/'lib/pcbm_cover_view.py',
                'launcher':menu/'scripts/pcbm-run-vice','wrapper':menu/'scripts/pcbm-cover',
                'registry':recipe/'runtime/data/profiles.json'}.items()}
            build['covers']['assets'] = [store(menu/item['path']) for item in manifest['files']]
            primary_path=menu/'docs/primary-artwork.json'
            if primary_path.is_file():
                primary=read_json(primary_path)['file']
                if primary['path']!='covers/pcbmcover1.jpg':raise ValueError('primary artwork path')
                data=(menu/primary['path']).read_bytes()
                if len(data)!=primary['size_bytes'] or hashlib.sha256(data).hexdigest()!=primary['sha256']:
                    raise ValueError('primary artwork changed')
                build['primary']={'manifest':store(primary_path),'asset':store(menu/primary['path'])}
            build['utilities'] = oldrecord['utilities']
        component['build_record'] = record(build)
        lock['components'][name] = component
    if a.vice_version:
        if not re.fullmatch(r'3[.]10-1[+]pcbm[0-9]+',a.vice_version):raise ValueError('VICE package version')
        if a.vice_version==lock['components']['vice']['package']['version']:raise ValueError('changed VICE needs distinct version')
        component=copy.deepcopy(lock['components']['vice'])
        deb=packages/f'project-cbm-vice_{a.vice_version}_arm64.deb'
        fields=subprocess.check_output(['dpkg-deb','-f',str(deb),'Package','Version','Architecture'],text=True)
        if dict(line.split(': ',1) for line in fields.splitlines())!={'Package':'project-cbm-vice','Version':a.vice_version,'Architecture':'arm64'}:raise ValueError('VICE identity mismatch')
        component['package'].update(version=a.vice_version,revision=a.vice_version.split('-',1)[1],artifact=store(deb))
        d=recipe/'build/packages/vice/debian'
        component['recipe']=archive(d.rglob('*'),d)
        component['patches']=[store(d/'patches'/line.strip()) for line in (d/'patches/series').read_text().splitlines() if line.strip() and not line.startswith('#')]
        component['corresponding_source']=archive([f for f in packages.glob('project-cbm-vice_*') if f.suffix=='.dsc' or '.tar.' in f.name],packages)
        component['build_record']=record({'component':'vice','package':component['package']['artifact'],'source_sha256':component['source']['artifact']['sha256'],
            'build_info':store(next(packages.glob('project-cbm-vice_*.buildinfo'))),'source_date_epoch':lock['build']['source_date_epoch'],
            'qualification':'Bounded private performance telemetry; physical performance UNTESTED'})
        lock['components']['vice']=component
    # Integration source owns engineering.py; explicit installed-file hashes make
    # the corrected lifecycle and setup contract independently inspectable offline.
    mapping = {'usr/libexec/project-cbm/engineering.py':recipe/'build/pigen/stage-cbm/files/engineering.py'}
    for source, dest in [('lib/pcbm_status_view.py','usr/libexec/project-cbm-menu/pcbm_status_view.py'),
                         ('lib/pcbm_info_view.py','usr/libexec/project-cbm-menu/pcbm_info_view.py'),
                         ('scripts/pcbm-system-info','usr/bin/pcbm-system-info'),
                         ('scripts/pcbm-menu','usr/bin/pcbm-menu'),
                         ('scripts/pcbm-import','usr/bin/pcbm-import'),
                         ('scripts/pcbm-content','usr/bin/pcbm-content'),
                         ('scripts/pcbm-first-run','usr/bin/pcbm-first-run'),
                         ('scripts/pcbm-config','usr/bin/pcbm-config'),
                         ('lib/pcbm-setup-ui.sh','usr/share/project-cbm-menu/pcbm-setup-ui.sh'),
                         ('lib/pcbm-ui.sh','usr/share/project-cbm-menu/pcbm-ui.sh'),
                         ('lib/pcbm_config_bridge.py','usr/libexec/project-cbm-menu/pcbm_config_bridge.py')]:
        if not a.reuse_menu:
            mapping[dest] = packages/'menu'/source
    for source in (recipe/'runtime/project_cbm').glob('*.py'):
        mapping['usr/share/project-cbm/runtime/project_cbm/'+source.name] = source
    build = read_json(kit/lock['components']['menu']['build_record']['path'])
    build.setdefault('corrective_payload',{}).update({dest:store(source) for dest,source in sorted(mapping.items())})
    for source in (recipe/'docs/release').glob('*.md'):
        build['corrective_payload']['usr/share/doc/project-cbm-runtime/release/'+source.name]=store(source)
    build['appliance_schema']=store(recipe/'schemas/appliance-info.schema.json')
    build['network_summary_schema'] = store(recipe/'schemas/network-info.schema.json')
    build['information_schema'] = store(recipe/'schemas/info.schema.json')
    build['configuration_schemas'] = [store(recipe/'schemas'/name) for name in
        ('configuration-request.schema.json','configuration-result.schema.json')]
    lock['components']['menu']['build_record'] = record(build)
    raw = encode(lock)
    verify_kit(raw, kit)
    (kit/'release-lock.json').write_bytes(raw)
    sha = hashlib.sha256(raw).hexdigest()
    (kit/'release-lock.sha256').write_text(sha+'  release-lock.json\n')
    (kit/'attempt.json').write_bytes(encode({'attempt':a.attempt,'candidate':lock['product'],
        'prior_lock_sha256':hashlib.sha256(oldraw).hexdigest(),'release_lock_sha256':sha,
        'changed':['runtime package/source','integration source/commit','release documentation','corrective validation records','installed identity','optional application path manifests/recipes']
                   + ([] if a.reuse_menu else ['Menu package/tag/source']) + (['VICE package/patches'] if a.vice_version else []),
        'unchanged':(['Menu package/tag/source'] if a.reuse_menu else []) + ([] if a.vice_version else ['VICE']) + ['TCPser','all seven Covers','base and host closures','pi-gen and patches',
                     'qualification media','SID-Wizard upstream source','StrikeTerm disk bytes and rights gates'],
        'construction_argument':'--attempt '+str(a.attempt)}))
    print(sha)

if __name__ == '__main__':
    main()
