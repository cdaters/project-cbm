#!/usr/bin/env python3
"""Install/seal the minimal private POC into pi-gen's separate target rootfs."""
import argparse
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import hashlib
from build_contracts import encode, make_identity, read_json
from retained_inputs import verify_kit
from vice_presentation import defaults as presentation_defaults, seed as seed_presentation

REPO=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lock',type=Path);parser.add_argument('kit',type=Path);parser.add_argument('root',type=Path)
    args=parser.parse_args()
    root=args.root.resolve(strict=True)
    if os.geteuid()!=0 or root==Path('/') or not (root/'etc/debian_version').is_file():
        raise SystemExit('requires separate prepared Debian target rootfs as root')
    raw=args.lock.read_bytes();lock=verify_kit(raw,args.kit)
    if read_json(args.kit/lock['configuration']['defaults']['path']) != read_json(REPO/'build/pigen/defaults.json'):
        raise ValueError('frozen defaults disagree with integration recipe')
    if (args.kit/lock['configuration']['first_boot_recipe']['path']).read_bytes() != (REPO/'build/pigen/stage-cbm/files/first_boot.py').read_bytes():
        raise ValueError('frozen first-boot recipe disagrees with integration source')
    def chroot(*cmd): return subprocess.check_output(['chroot',str(root),*cmd],text=True)
    def put(path,data,mode=0o644):
        dest=root/path.lstrip('/');dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(data if isinstance(data,bytes) else data.encode());dest.chmod(mode)
    owned=[]
    def owned_put(path,data,mode=0o644): put(path,data,mode);owned.append(path)
    put('/usr/sbin/policy-rc.d','#!/bin/sh\nexit 101\n',0o755)
    temp=root/'tmp/cbm-packages';temp.mkdir(parents=True,exist_ok=True)
    package_paths=[]
    for name,component in lock['components'].items():
        target=temp/(name+'.deb');shutil.copyfile(args.kit/component['package']['artifact']['path'],target)
        package_paths.append('/tmp/cbm-packages/'+target.name)
    print(chroot('apt-get','install','-y','--no-install-recommends',*package_paths,
                 'cloud-guest-utils','libgl1-mesa-dri','libegl1','libgbm1','libgles2','samba'),flush=True)
    # Purge explicit development payload. Protect runtime ABI packages such as gcc-base.
    inventory=chroot('dpkg-query','-W','-f=${binary:Package}\t${db:Status-Status}\n')
    remove=[]
    tools={'build-essential','make','dpkg-dev','autoconf','automake','quilt','patch','cmake',
           'gdb','git','cloud-init','python3-dev','python3-pip','rpi-connect-lite'}
    for line in inventory.splitlines():
        package,status=line.split('\t');name=package.split(':')[0]
        if status!='installed': continue
        if (name in tools or name.endswith('-dev') or name.startswith('linux-headers-')
                or re.fullmatch(r'(gcc|g\+\+|cpp)(-[0-9]+)?(-aarch64-linux-gnu)?',name)):
            remove.append(package)
    if remove: print(chroot('apt-get','purge','-y',*remove),flush=True)
    remaining=chroot('dpkg-query','-W','-f=${binary:Package}\t${db:Status-Status}\n')
    for name in ['gcc','g++','cc','c++','make','cmake']:
        if (root/'usr/bin'/name).exists(): raise ValueError('build tool retained: '+name)
    for component in lock['components'].values():
        actual=chroot('dpkg-query','-W','-f=${Version}',component['package']['name']).strip()
        if actual!=component['package']['version']: raise ValueError('installed package version mismatch')
    for dirname in ['etc/pcbm','usr/share/project-cbm','usr/libexec/project-cbm','var/lib/project-cbm/first-boot']:
        (root/dirname).mkdir(parents=True,exist_ok=True)
    (root/'var/lib/project-cbm/first-boot').chmod(0o700)
    owned_put('/usr/share/project-cbm/identity.json',encode(make_identity(raw)))
    version_conf='PCBM_VERSION='+shlex.quote(lock['product']['version'])+'\nPCBM_MENU_VERSION='+shlex.quote(lock['components']['menu']['version'])+'\n'
    owned_put('/etc/pcbm/version.conf',version_conf)
    owned_put('/etc/pcbm/boot-mode.conf','menu\n')
    owned_put('/etc/pcbm/default-machine.conf','x64sc\n')
    for name in ['pcbm-first-boot.service','tcpser.service']:
        owned_put('/usr/lib/systemd/system/'+name,(REPO/'build/pigen/stage-cbm/files'/name).read_bytes())
    owned_put('/usr/libexec/project-cbm/first_boot.py',(REPO/'build/pigen/stage-cbm/files/first_boot.py').read_bytes(),0o755)
    for directory in ['pcbm','.config','.config/pcbm','.config/vice','.local','.local/state','.local/state/vice','.local/share','.local/share/vice']:
        target=root/'home/pi'/directory;target.mkdir(parents=True,exist_ok=True);os.chown(target,1000,1000)
    owned_put('/usr/share/project-cbm/vice-defaults.ini',presentation_defaults())
    user_config=root/'home/pi/.config/vice/sdl-vicerc'
    if seed_presentation(user_config):
        os.chown(user_config,1000,1000)
    # The user copy is user state, deliberately excluded from owned-paths.txt.
    for directory in ['games','demos','music','programs','roms','screenshots','saves']:
        target=root/'home/pi/pcbm'/directory;target.mkdir(exist_ok=True);os.chown(target,1000,1000)
    chroot('usermod','--password','*','pi');chroot('usermod','--password','*','root')
    chroot('usermod','--shell','/bin/bash','pi')
    # Standard getty/login/PAM owns tty sessions; no direct competing tty service.
    for tty in ['tty1','tty2']:
        owned_put('/etc/systemd/system/getty@'+tty+'.service.d/autologin.conf',
                  (REPO/'build/pigen/stage-cbm/files/getty-autologin.conf').read_bytes())
    owned_put('/etc/profile.d/pcbm-console.sh',(REPO/'build/pigen/stage-cbm/files/pcbm-profile.sh').read_bytes())
    for name in ['pcbm-console-session','engineering.py']:
        owned_put('/usr/libexec/project-cbm/'+name,(REPO/'build/pigen/stage-cbm/files'/name).read_bytes(),0o755)
    owned_put('/usr/bin/pcbm-diagnostics',(REPO/'build/pigen/stage-cbm/files/pcbm-diagnostics').read_bytes(),0o755)
    owned_put('/etc/pcbm/engineering-poc',lock['product']['candidate']+'\n')
    # Only exact no-argument power actions, required for safe qualification shutdown.
    owned_put('/etc/sudoers.d/pcbm-power','pi ALL=(root) NOPASSWD: /usr/sbin/poweroff "", /usr/sbin/reboot ""\n',0o440)
    chroot('visudo','-cf','/etc/sudoers')
    media=lock.get('qualification_media')
    if not media:raise ValueError('POC2 requires declared qualification media')
    with tarfile.open(args.kit/media['artifact']['path']) as archive:
        manifest=json.load(archive.extractfile('manifest.json'))
        if manifest['source_commit']!=media['source_commit']:raise ValueError('media source revision mismatch')
        for entry in manifest['files']:
            dest=entry['destination']
            if not re.fullmatch(r'(programs|music|demos)/Qualification/[a-z0-9.-]+',dest):raise ValueError('unsafe media destination')
            data=archive.extractfile(entry['name']).read()
            if hashlib.sha256(data).hexdigest()!=entry['sha256']:raise ValueError('media digest mismatch')
            owned_put('/home/pi/pcbm/'+dest,data)
            os.chown(root/'home/pi/pcbm'/dest,1000,1000)
            os.chown((root/'home/pi/pcbm'/dest).parent,1000,1000)
        owned_put('/usr/share/project-cbm/qualification-media.json',json.dumps(manifest,indent=2)+'\n')
        owned_put('/usr/share/doc/project-cbm-qualification/LICENSE',archive.extractfile('LICENSE').read())
    # One growth owner. The inspected vendor initramfs hooks both require ' resize'.
    cmdline=root/'boot/firmware/cmdline.txt'
    cmdline.write_text(' '.join(word for word in cmdline.read_text().split() if word!='resize')+'\n')
    disabled=['rpi-resize.service','systemd-growfs-root.service','userconfig.service',
              'regenerate_ssh_host_keys.service','ssh.service','ssh.socket','sshswitch.service',
              'sshd-keygen.service','avahi-daemon.service','avahi-daemon.socket','smbd.service',
              'nmbd.service','samba-ad-dc.service','tcpser.service','NetworkManager.service',
              'pcbm-console.service']
    for unit in disabled:
        subprocess.run(['systemctl','--root',str(root),'disable',unit],check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.run(['systemctl','--root',str(root),'mask',unit],check=True)
    for unit in ['pcbm-first-boot.service','getty@tty1.service','getty@tty2.service']:
        subprocess.run(['systemctl','--root',str(root),'enable',unit],check=True)
    # VM credentials/state are never imported. Remove identities generated in chroots.
    for pattern in ['etc/ssh/ssh_host_*','home/pi/.ssh/*']:
        for path in root.glob(pattern):
            if path.is_file() or path.is_symlink(): path.unlink()
    for name in ['etc/machine-id','var/lib/dbus/machine-id','var/lib/systemd/random-seed',
                 'root/.bash_history','home/pi/.bash_history']:
        path=root/name
        if path.is_file() or path.is_symlink(): path.unlink()
    put('/etc/machine-id','uninitialized\n')
    for name in ['var/lib/cloud','var/log/journal']:
        path=root/name
        if path.exists(): shutil.rmtree(path)
    shutil.rmtree(temp)
    for directory in ['var/cache/apt/archives','usr/src']:
        path=root/directory
        if path.exists():
            for child in path.iterdir():
                if child.is_file() or child.is_symlink(): child.unlink()
                elif child.is_dir(): shutil.rmtree(child)
    # Final pi-gen exporter also seals logs and removes its APT proxy configuration.
    owned_put('/usr/share/project-cbm/owned-paths.txt','\n'.join(sorted(owned))+'\n')
    print('Private CBM stage installed and sealed; offline image validation still required')


if __name__=='__main__':main()
