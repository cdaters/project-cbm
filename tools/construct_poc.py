#!/usr/bin/env python3
"""Construct one private image from a frozen kit inside an isolated Linux network namespace."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tarfile
import time
from urllib.request import urlopen
from build_contracts import read_json
from retained_inputs import verify_kit
from build_host_guard import verify as verify_host


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lock',type=Path);parser.add_argument('kit',type=Path);parser.add_argument('workspace',type=Path)
    args=parser.parse_args()
    if os.geteuid()!=0:raise SystemExit('run as root inside unshare --net')
    if subprocess.check_output(['ip','route','show'],text=True).strip():raise SystemExit('external network routes forbidden for frozen construction')
    subprocess.run(['ip','link','set','lo','up'],check=True)
    kit=args.kit.resolve(strict=True);w=args.workspace.resolve(strict=True)
    raw=args.lock.read_bytes();lock=verify_kit(raw,kit)
    verify_host(lock,kit)
    subprocess.run(['arch-test','-n','arm64'],check=True)
    if subprocess.check_output(['findmnt','-T',str(w),'-no','FSTYPE'],text=True).strip()!='ext4':raise SystemExit('Linux ext4 required')
    if shutil.disk_usage(w).free<40*1024**3:raise SystemExit('insufficient guest build headroom')
    candidate=lock['product']['candidate']
    if candidate not in ['private-engineering-poc1','private-engineering-poc2','private-engineering-poc3','private-engineering-poc4']:raise ValueError('unknown candidate workspace')
    suffix='private-'+candidate.rsplit('-',1)[1]
    work=w/'builds'/suffix;work.mkdir()
    for descriptor in [lock['base']['pi_gen']['source'],lock['integration']['source']]:
        with tarfile.open(kit/descriptor['path']) as archive:archive.extractall(work,filter='data')
    recipe=work/'project-cbm';pg=work/'pi-gen'
    for patch in lock['base']['patches']:
        with (kit/patch['path']).open('rb') as stream:
            subprocess.run(['patch','--batch','-p1'],cwd=pg,stdin=stream,check=True)
    config=read_json(kit/lock['base']['configuration']['path'])
    if config!=read_json(recipe/'build/pigen/config.json'):raise ValueError('frozen config/source mismatch')
    meta=read_json(kit/lock['base']['authenticated_apt_metadata']['path'])
    urls=[e['artifact'] for e in meta['entries'] if e['role']=='frozen-url-map']
    if len(urls)!=1:raise ValueError('missing unique frozen URL map')
    urlmap=read_json(kit/urls[0]['path']);proxyroot=work/'apt-frozen';proxyroot.mkdir()
    for url,item in urlmap.items():
        source=kit/'objects'/item['sha256'];target=proxyroot/item['path']
        if target.parent!=proxyroot:raise ValueError('invalid proxy mapping')
        if not target.exists():os.link(source,target)
    (proxyroot/'catalog.json').write_text(json.dumps(urlmap,sort_keys=True,indent=2)+'\n')
    shutil.copytree(recipe/'build/pigen/stage-cbm',pg/'stage-cbm')
    for stage in ['stage0','stage1','stage2']:(pg/stage/'SKIP_IMAGES').touch()
    envconfig={
        'IMG_NAME':config['image_name'],'IMG_DATE':config['image_date'],
        'GIT_HASH':lock['base']['pi_gen']['git']['commit'],'RELEASE':config['release'],
        'WORK_DIR':str(work/'work'),'DEPLOY_DIR':str(w/'artifacts'/suffix),
        'STAGE_LIST':'stage0 stage1 stage2 stage-cbm','APT_PROXY':'http://127.0.0.1:3142',
        'ENABLE_CLOUD_INIT':'0','ENABLE_SSH':'0','PASSWORDLESS_SUDO':'0','FIRST_USER_NAME':'pi',
        'TIMEZONE_DEFAULT':config['timezone'],'LOCALE_DEFAULT':config['locale'],
        'KEYBOARD_KEYMAP':config['keyboard'],'KEYBOARD_LAYOUT':'English (US)',
        'DEPLOY_COMPRESSION':config['compression'],'COMPRESSION_LEVEL':str(config['compression_level']),
        'CBM_KIT':str(kit),'CBM_RELEASE_LOCK':str(args.lock.resolve()),'CBM_RECIPE_DIR':str(recipe),
        'SOURCE_DATE_EPOCH':str(lock['build']['source_date_epoch'])}
    (pg/'config').write_text(''.join('export '+key+'='+shlex.quote(value)+'\n' for key,value in envconfig.items()))
    log=(work/'apt-frozen.log').open('w')
    proxy=subprocess.Popen(['python3',str(recipe/'tools/apt_retention_proxy.py'),'--root',str(proxyroot),'--mode','frozen'],stdout=log,stderr=subprocess.STDOUT)
    try:
        for attempt in range(20):
            if proxy.poll() is not None:raise RuntimeError('frozen transport failed to start')
            try:
                with urlopen('http://127.0.0.1:3142/',timeout=1) as response:response.read()
                break
            except OSError:time.sleep(0.2)
        else:raise RuntimeError('frozen transport readiness timeout')
        subprocess.run(['/usr/bin/time','-v','./build.sh'],cwd=pg,check=True)
    finally:
        proxy.terminate();proxy.wait(timeout=10);log.close()
    verify_host(lock,kit)
    print('First controlled private POC build completed; offline validation required')


if __name__=='__main__':main()
