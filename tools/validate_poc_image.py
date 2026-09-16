#!/usr/bin/env python3
"""Read-only private POC inspection. Never boots or executes target programs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from build_contracts import encode, make_identity, validate_lock


def output(*args):
    return subprocess.check_output(args, text=True).strip()


def digest(path, algorithm='sha256'):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, algorithm).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('lock', type=Path)
    parser.add_argument('results', type=Path)
    args = parser.parse_args()
    if os.geteuid() != 0:
        raise SystemExit('requires root for read-only loop mounts')
    image = args.image.resolve(strict=True)
    raw = args.lock.read_bytes()
    lock = validate_lock(raw)
    args.results.mkdir()
    root = args.results/'mounted-root'
    boot = args.results/'mounted-boot'
    root.mkdir(); boot.mkdir()
    record = {'scope':'offline/static only; no Raspberry Pi runtime qualification',
              'release_lock_sha256':hashlib.sha256(raw).hexdigest(),
              'image_sha256':digest(image), 'image_size_bytes':image.stat().st_size,
              'checks':{}, 'physical_qualification':'UNTESTED'}
    failures = []

    def check(name, condition):
        record['checks'][name] = 'PASS' if condition else 'FAIL'
        if not condition:
            failures.append(name)

    loop = output('losetup', '--read-only', '--find', '--show', '--partscan', str(image))
    mounted = []
    try:
        table = json.loads(output('sfdisk', '--json', loop))['partitiontable']
        record['partition_table'] = table
        check('two_partition_DOS_layout', table['label']=='dos' and len(table['partitions'])==2)
        if failures:
            raise ValueError('unexpected image geometry')
        subprocess.run(['mount','-o','ro,noload',loop+'p2',str(root)],check=True)
        mounted.append(root)
        subprocess.run(['mount','-o','ro',loop+'p1',str(boot)],check=True)
        mounted.append(boot)
        check('root_ext4',output('findmnt','-nro','FSTYPE',str(root))=='ext4')
        check('boot_vfat',output('findmnt','-nro','FSTYPE',str(boot))=='vfat')
        check('minimal_identity_matches_lock',
              (root/'usr/share/project-cbm/identity.json').read_bytes()==encode(make_identity(raw)))
        record['installed_identity_bytes']=(root/'usr/share/project-cbm/identity.json').stat().st_size
        check('fresh_machine_id_marker',(root/'etc/machine-id').read_text()=='uninitialized\n')
        check('no_dbus_machine_id',not (root/'var/lib/dbus/machine-id').exists())
        check('no_reusable_SSH_host_keys',not list((root/'etc/ssh').glob('ssh_host_*')))
        check('no_authorized_keys',not list((root/'home').rglob('authorized_keys')))
        check('no_cloud_state',not (root/'var/lib/cloud').exists())
        check('no_random_seed',not (root/'var/lib/systemd/random-seed').exists())
        check('no_builder_home',not (root/'home/builder').exists())
        check('no_build_workspace',not (root/'srv/project-cbm').exists())
        check('no_history',not list((root/'root').glob('.*history')) and
              not list((root/'home').rglob('.*history')))
        check('no_package_cache',not list((root/'var/cache/apt/archives').glob('*.deb')))
        check('no_source_tree',not any((root/'usr/src').iterdir()))
        check('no_temporary_policy_rc',not (root/'usr/sbin/policy-rc.d').exists())
        check('no_build_proxy',not (root/'etc/apt/apt.conf.d/51cache').exists())
        check('single_growth_owner','resize' not in (boot/'cmdline.txt').read_text().split())
        check('no_completed_first_boot',not (root/'var/lib/project-cbm/first-boot/complete.json').exists())
        for unit in ['pcbm-first-boot.service','pcbm-console.service']:
            path=root/'etc/systemd/system/multi-user.target.wants'/unit
            check('enabled_'+unit,path.is_symlink() and path.readlink().name==unit)
        for unit in ['rpi-resize.service','systemd-growfs-root.service','userconfig.service',
                     'regenerate_ssh_host_keys.service','ssh.service','ssh.socket','sshswitch.service',
                     'avahi-daemon.service','avahi-daemon.socket','smbd.service','nmbd.service',
                     'samba-ad-dc.service','tcpser.service','NetworkManager.service','getty@tty1.service']:
            path=root/'etc/systemd/system'/unit
            check('masked_'+unit,path.is_symlink() and str(path.readlink())=='/dev/null')
        shadow={row.split(':')[0]:row.split(':')[1] for row in (root/'etc/shadow').read_text().splitlines()}
        check('locked_local_passwords',all(shadow.get(name)=='*' for name in ['root','pi']))
        inventory=output('dpkg-query','--admindir='+str(root/'var/lib/dpkg'),'-W',
                         '-f=${binary:Package}\t${Version}\t${Architecture}\t${Installed-Size}\t${db:Status-Status}\n')
        (args.results/'packages.tsv').write_text(inventory+'\n')
        packages={}
        for line in inventory.splitlines():
            name,version,arch,size,status=line.split('\t')
            if status=='installed': packages[name.split(':')[0]]=(version,arch,int(size or 0))
        record['runtime_package_count']=len(packages)
        record['runtime_package_installed_size_bytes']=sum(p[2]*1024 for p in packages.values())
        record['component_installed_size_bytes']={}
        for component in lock['components'].values():
            expected=component['package']; name=expected['name']
            check('package_'+name,packages.get(name,())[:2]==(expected['version'],expected['architecture']))
            record['component_installed_size_bytes'][name]=packages[name][2]*1024
            checksums=root/'var/lib/dpkg/info'/(name+'.md5sums')
            valid=True
            for line in checksums.read_text().splitlines():
                checksum,path=line.split(None,1)
                valid=valid and digest(root/path,'md5')==checksum
            check('installed_payload_'+name,valid)
        forbidden=[name for name in packages if name.endswith('-dev') or name.startswith('linux-headers-')
                   or re.fullmatch(r'(gcc|g\+\+|cpp)(-[0-9]+)?(-aarch64-linux-gnu)?',name)
                   or name in ['build-essential','make','cmake','git','dpkg-dev','cloud-init','rpi-connect-lite']]
        check('no_build_or_excluded_packages',not forbidden)
        record['unexpected_packages']=forbidden
        check('VICE_x64sc_present',(root/'usr/bin/x64sc').is_file())
        check('Menu_present',(root/'usr/bin/pcbm-menu').is_file())
        check('TCPser_present',(root/'usr/bin/tcpser').is_file())
        check('content_directory_owned_by_pi',(root/'home/pi/pcbm').stat().st_uid==1000)
        record['root_filesystem_bytes']={
            'capacity':os.statvfs(root).f_blocks*os.statvfs(root).f_frsize,
            'free':os.statvfs(root).f_bfree*os.statvfs(root).f_frsize,
            'available_to_user':os.statvfs(root).f_bavail*os.statvfs(root).f_frsize}
        record['root_filesystem_bytes']['used']=record['root_filesystem_bytes']['capacity']-record['root_filesystem_bytes']['free']
        record['boot_filesystem_used_bytes']=(os.statvfs(boot).f_blocks-os.statvfs(boot).f_bfree)*os.statvfs(boot).f_frsize
        record['post_first_boot_capacity']='UNTESTED; depends on target media and successful expansion'
        record['maintenance_margin']='UNMEASURED; no minimum card size established'
        record['debian_version']=(root/'etc/debian_version').read_text().strip()
        record['initramfs_files']=[p.name for p in boot.glob('initramfs*')]
        check('both_vendor_initramfs_present',all((boot/name).is_file() for name in ['initramfs8','initramfs_2712']))
        # Search likely configuration/state text, reporting only offending path, never content.
        residues=[]
        for directory in ['etc','home','root','usr/share/project-cbm','var/lib/project-cbm']:
            for path in (root/directory).rglob('*'):
                if path.is_symlink() or not path.is_file() or path.stat().st_size>1024*1024: continue
                data=path.read_bytes()
                if any(marker in data for marker in [b'/srv/project-cbm',b'/Volumes/TheBench',b'/Users/cdaters',b'BEGIN OPENSSH PRIVATE KEY']):
                    residues.append(str(path.relative_to(root)))
        record['obvious_builder_residue_paths']=residues
        check('no_obvious_builder_path_or_key_residue',not residues)
    except Exception as exc:
        failures.append('inspection_exception_'+type(exc).__name__)
        raise
    finally:
        for path in reversed(mounted): subprocess.run(['umount',str(path)],check=True)
        subprocess.run(['losetup','--detach',loop],check=True)
        record['result']='PASS' if not failures else 'FAIL'
        (args.results/'offline-validation.json').write_bytes(encode(record))
    if failures:
        raise SystemExit('Offline failures: '+', '.join(failures))
    print('Offline/static checks passed; all physical Raspberry Pi behavior remains UNTESTED')


if __name__=='__main__': main()
