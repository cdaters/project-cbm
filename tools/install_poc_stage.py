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
from build_environment import environment
from vice_presentation import defaults as presentation_defaults, seed as seed_presentation
import boot_presentation

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
    target_env=environment(lock['build']['source_date_epoch'],target=True)
    def chroot(*cmd):
        return subprocess.check_output(['/usr/sbin/chroot',str(root),*cmd],text=True,env=target_env)
    if (root/'tmp').is_symlink():raise ValueError('target tmp must be a real directory')
    (root/'tmp').mkdir(exist_ok=True);(root/'tmp').chmod(0o1777)
    chroot('/bin/sh','-ec','test $(stat -c %a /tmp) = 1777; p=$(mktemp); rm -- "$p"')
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
    for dirname in ['etc/project-cbm','var/lib/project-cbm/setup','run/project-cbm','run/project-cbm/import','run/project-cbm/import/source','etc/pcbm','usr/share/project-cbm','usr/libexec/project-cbm','var/lib/project-cbm/first-boot']:
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
    for directory in ['pcbm','.config','.config/vice','.local','.local/state','.local/state/vice','.local/share','.local/share/vice']:
        target=root/'home/pi'/directory;target.mkdir(parents=True,exist_ok=True);os.chown(target,1000,1000)
    owned_put('/usr/share/project-cbm/vice-defaults.ini',presentation_defaults())
    user_config=root/'home/pi/.config/vice/sdl-vicerc'
    if seed_presentation(user_config):
        os.chown(user_config,1000,1000)
    # The user copy is user state, deliberately excluded from owned-paths.txt.
    sys.path.insert(0,str(REPO/'runtime'))
    from project_cbm.library import directories as library_directories
    for directory in library_directories():
        target=root/'home/pi/pcbm'/directory;target.mkdir(parents=True,exist_ok=True);os.chown(target,1000,1000)
        if target.parent != root/'home/pi/pcbm':os.chown(target.parent,1000,1000)
    chroot('usermod','--password','*','pi');chroot('usermod','--password','*','root')
    chroot('usermod','--shell','/bin/bash','pi')
    if 'runtime' not in lock['components']:raise ValueError('activated candidate requires declared runtime package')
    chroot('groupadd','--system','pcbm-operators')
    chroot('usermod','--append','--groups','pcbm-operators','pi')
    owned_put('/etc/hostname','projectcbm\n')
    hosts=(root/'etc/hosts').read_text()
    hosts=re.sub(r'^127\.0\.1\.1\s+.*$', '127.0.1.1\tprojectcbm', hosts, flags=re.M)
    if not re.search(r'^127\.0\.1\.1\s',hosts,re.M):hosts+='\n127.0.1.1\tprojectcbm\n'
    owned_put('/etc/hosts',hosts)
    chroot('useradd','--uid','1001','--create-home','--shell','/bin/bash','--groups','sudo','pcbm')
    chroot('usermod','--password','!','pcbm')
    # No universal credential and no normal-user blanket sudo. Debian %sudo is
    # authenticated; only the separate owner account is added for administration.
    chroot('gpasswd','--delete','pi','sudo')
    policy={'schema_version':1,'owner_user':'pcbm','appliance_user':'pi',
            'system_ready':False,'network_ready':True,
            'ready_services':['ssh','sharing','modem','discovery']}
    owned_put('/etc/project-cbm/configuration-policy.json',encode(policy))
    owned_put('/etc/project-cbm/modem.json',encode({'schema_version':1,'port':25232,'baud':2400}))
    owned_put('/etc/sudoers.d/pcbm-operations',(REPO/'runtime/config/sudoers.example').read_bytes(),0o440)
    owned_put('/usr/lib/tmpfiles.d/project-cbm.conf',
              'd /run/project-cbm 0755 root root -\nd /run/project-cbm/import 0755 root root -\nd /run/project-cbm/import/source 0755 root root -\n')
    owned_put('/etc/NetworkManager/NetworkManager.conf',
              '[main]\nplugins=keyfile\n[ifupdown]\nmanaged=false\n')
    owned_put('/var/lib/NetworkManager/NetworkManager.state',
              '[main]\nNetworkingEnabled=false\nWirelessEnabled=false\nWWANEnabled=false\n',0o600)
    owned_put('/etc/ssh/sshd_config.d/20-project-cbm.conf',
              'PermitRootLogin no\nAllowUsers pcbm\nPasswordAuthentication yes\nKbdInteractiveAuthentication no\n')
    smb=('[global]\n    server role = standalone server\n    security = user\n'
         '    map to guest = Never\n    server min protocol = SMB2\n'
         '    disable netbios = yes\n    smb ports = 445\n    load printers = no\n'
         '    mdns name = mdns\n    disable spoolss = yes\n    log level = 0\n    max log size = 1000\n')
    owned_put('/etc/samba/smb.conf',smb+(REPO/'runtime/config/file-sharing.example.conf').read_text())
    # systemd may apply presets when it sees the sealed first-boot identity marker.
    # Explicit policy prevents that normal mechanism from enabling optional services.
    optional_units=['ssh.service','ssh.socket','smbd.service','nmbd.service',
                    'samba-ad-dc.service','tcpser.service','avahi-daemon.service','avahi-daemon.socket']
    owned_put('/etc/systemd/system-preset/00-project-cbm.preset',
              ''.join('disable '+u+'\n' for u in optional_units)+
              'enable NetworkManager.service\nenable pcbm-first-boot.service\n')

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
    # Add admitted optional inputs only during construction, never to a sealed image.
    if 'optional_software' in lock:
        from optional_software import verify_optional, install as install_optional
        payload = verify_optional(args.kit, lock['optional_software']['sid_wizard'])
        paths = install_optional(root, payload)
        if 'striketerm' in lock['optional_software']:
            from private_application import check_rights, verify as verify_private, install as install_private
            check_rights(lock,'private-engineering')
            paths.extend(install_private(root,verify_private(args.kit,lock['optional_software']['striketerm'])))
        owned.extend('/'+p for p in paths)
        for name in paths:
            if name.startswith('home/pi/pcbm/'):
                path = root/name
                os.chown(path,1000,1000)
                for parent in path.parents:
                    if parent == root/'home/pi/pcbm':break
                    os.chown(parent,1000,1000)
    # One growth owner. The inspected vendor initramfs hooks both require ' resize'.
    cmdline=root/'boot/firmware/cmdline.txt'
    cmdline.write_text(boot_presentation.cmdline(cmdline.read_text()))
    config=root/'boot/firmware/config.txt'
    config.write_text(boot_presentation.firmware(config.read_text()))
    owned_put('/etc/issue',boot_presentation.ISSUE)
    # Suppress only the appliance login's routine motd/last-login prose. PAM still runs.
    put('/home/pi/.hushlogin','')
    os.chown(root/'home/pi/.hushlogin',1000,1000)
    disabled=['rpi-resize.service','systemd-growfs-root.service','userconfig.service',
              'regenerate_ssh_host_keys.service','ssh.socket','sshswitch.service',
              'sshd-keygen.service','nmbd.service','samba-ad-dc.service',
              'pcbm-console.service']
    for unit in disabled:
        subprocess.run(['systemctl','--root',str(root),'disable',unit],check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.run(['systemctl','--root',str(root),'mask',unit],check=True)
    for unit in ['NetworkManager.service','ssh.service','smbd.service','tcpser.service','avahi-daemon.service','avahi-daemon.socket']:
        subprocess.run(['systemctl','--root',str(root),'unmask',unit],check=True)
        subprocess.run(['systemctl','--root',str(root),'disable',unit],check=True)
    for unit in ['NetworkManager.service','pcbm-first-boot.service','getty@tty1.service','getty@tty2.service']:
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
    # Samba must also establish its own per-device state after flashing.
    if list((root/'var/lib/samba').rglob('*.tdb')) or list((root/'var/lib/samba').rglob('*.ldb')):
        raise ValueError('unexpected reusable Samba database state in construction root')
    # Final pi-gen exporter also seals logs and removes its APT proxy configuration.
    owned_put('/usr/share/project-cbm/owned-paths.txt','\n'.join(sorted(owned))+'\n')
    print('Private CBM stage installed and sealed; offline image validation still required')


if __name__=='__main__':main()
