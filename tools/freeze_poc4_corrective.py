#!/usr/bin/env python3
"""Freeze corrective attempt 4; retain attempt 3 and all unchanged component bytes."""
import argparse
import copy
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tarfile
from build_contracts import encode, read_json
from retained_inputs import verify_kit


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('workspace', type=Path)
    p.add_argument('recipe', type=Path)
    p.add_argument('integration_commit')
    p.add_argument('menu_commit')
    p.add_argument('menu_tag_object')
    a = p.parse_args()
    for pin in (a.integration_commit, a.menu_commit, a.menu_tag_object):
        if not re.fullmatch('[0-9a-f]{40}', pin):
            raise ValueError('exact Git identity required')
    w = a.workspace.resolve(strict=True)
    recipe = a.recipe.resolve(strict=True)
    old = w/'inputs/frozen-poc4-attempt3'
    oldraw = (old/'release-lock.json').read_bytes()
    lock = copy.deepcopy(verify_kit(oldraw, old))
    kit = w/'inputs/frozen-poc4-attempt4'
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

    integration = w/'inputs/project-cbm-integration-poc4-attempt4.tar'
    lock['integration']['git']['commit'] = a.integration_commit
    lock['integration']['source'] = store(integration)
    lock['base']['configuration'] = store(recipe/'build/pigen/config.json')
    packages = w/'packages/poc4-attempt4'
    oldrecord = read_json(old/lock['components']['menu']['build_record']['path'])
    for name, version, source, commit, ref, tag in (
        ('runtime', '1.1.0~poc4.1-1', integration, a.integration_commit,
         'refs/heads/feature/1.1-build-foundation', None),
        ('menu', '1.1.0~poc4.2-1+pcbm1', w/'inputs/project-cbm-menu-1.1.0_poc4.2.tar',
         a.menu_commit, 'refs/tags/v1.1.0_poc4.2', a.menu_tag_object)):
        debs = list(packages.glob('project-cbm-'+name+'_*.deb'))
        if len(debs) != 1:
            raise ValueError('ambiguous package')
        fields = dict(line.split(': ', 1) for line in subprocess.check_output(
            ['dpkg-deb','-f',str(debs[0]),'Package','Version','Architecture'], text=True).splitlines())
        if fields != {'Package':'project-cbm-'+name,'Version':version,'Architecture':'all'}:
            raise ValueError('wrong package identity')
        component = copy.deepcopy(lock['components'][name])
        component['version'] = '1.1.0_poc4.1' if name == 'runtime' else '1.1.0_poc4.2'
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
            build['utilities'] = oldrecord['utilities']
        component['build_record'] = record(build)
        lock['components'][name] = component
    # Integration source owns engineering.py; explicit installed-file hashes make
    # the corrected lifecycle and setup contract independently inspectable offline.
    mapping = {'usr/libexec/project-cbm/engineering.py':recipe/'build/pigen/stage-cbm/files/engineering.py'}
    for source, dest in [('scripts/pcbm-first-run','usr/bin/pcbm-first-run'),
                         ('scripts/pcbm-config','usr/bin/pcbm-config'),
                         ('lib/pcbm-setup-ui.sh','usr/share/project-cbm-menu/pcbm-setup-ui.sh'),
                         ('lib/pcbm-ui.sh','usr/share/project-cbm-menu/pcbm-ui.sh'),
                         ('lib/pcbm_config_bridge.py','usr/libexec/project-cbm-menu/pcbm_config_bridge.py')]:
        mapping[dest] = packages/'menu'/source
    for source in (recipe/'runtime/project_cbm').glob('*.py'):
        mapping['usr/share/project-cbm/runtime/project_cbm/'+source.name] = source
    build = read_json(kit/lock['components']['menu']['build_record']['path'])
    build['corrective_payload'] = {dest:store(source) for dest,source in sorted(mapping.items())}
    build['configuration_schemas'] = [store(recipe/'schemas'/name) for name in
        ('configuration-request.schema.json','configuration-result.schema.json')]
    lock['components']['menu']['build_record'] = record(build)
    raw = encode(lock)
    verify_kit(raw, kit)
    (kit/'release-lock.json').write_bytes(raw)
    sha = hashlib.sha256(raw).hexdigest()
    (kit/'release-lock.sha256').write_text(sha+'  release-lock.json\n')
    (kit/'attempt.json').write_bytes(encode({'attempt':4,'candidate':lock['product'],
        'prior_lock_sha256':hashlib.sha256(oldraw).hexdigest(),'release_lock_sha256':sha,
        'changed':['runtime package/source','Menu package/tag/source','integration source/commit',
                   'image date','corrective validation records','installed identity'],
        'unchanged':['VICE','TCPser','all seven Covers','base and host closures','pi-gen and patches',
                     'qualification media','SID-Wizard','StrikeTerm and rights gates'],
        'construction_argument':'--attempt 4'}))
    print(sha)

if __name__ == '__main__':
    main()
