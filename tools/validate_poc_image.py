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
from vice_presentation import defaults as presentation_defaults


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
    activated=lock['schema_version']>=4
    single_user=lock['product']['candidate']=='private-engineering-rc2'
    account='pcbm' if single_user else 'pi'
    home='home/'+account
    content=home+('/content' if single_user else '/pcbm')
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
        for unit in ['pcbm-first-boot.service']:
            path=root/'etc/systemd/system/multi-user.target.wants'/unit
            check('enabled_'+unit,path.is_symlink() and path.readlink().name==unit)
        legacy_masks=['rpi-resize.service','systemd-growfs-root.service','userconfig.service',
                     'regenerate_ssh_host_keys.service','ssh.service','ssh.socket','sshswitch.service',
                     'avahi-daemon.service','avahi-daemon.socket','smbd.service','nmbd.service',
                     'samba-ad-dc.service','tcpser.service','NetworkManager.service','pcbm-console.service']
        if activated:
            legacy_masks=[u for u in legacy_masks if u not in ['ssh.service','avahi-daemon.service','avahi-daemon.socket','smbd.service','tcpser.service','NetworkManager.service']]
        for unit in legacy_masks:
            path=root/'etc/systemd/system'/unit
            check('masked_'+unit,path.is_symlink() and str(path.readlink())=='/dev/null')
        for tty in ['tty1','tty2']:
            link=root/'etc/systemd/system/getty.target.wants'/('getty@'+tty+'.service')
            check('enabled_getty_'+tty,link.is_symlink() and link.readlink().name=='getty@.service')
            conf=(root/'etc/systemd/system'/('getty@'+tty+'.service.d/autologin.conf')).read_text()
            check('login_PAM_'+tty,'--autologin '+account in conf and '--login-program' not in conf)
        check('PAM_systemd_present','pam_systemd.so' in (root/'etc/pam.d/common-session').read_text())
        passwd=[line.split(':') for line in (root/'etc/passwd').read_text().splitlines()]
        check('runtime_valid_unprivileged_shell',any(x[0]==account and x[2]=='1000' and x[-1]=='/bin/bash' for x in passwd))
        check('engineering_only_marker',(root/'etc/pcbm/engineering-poc').read_text()==lock['product']['candidate']+'\n')
        check('diagnostic_programs_present',all((root/p).is_file() for p in ['usr/bin/pcbm-diagnostics','usr/libexec/project-cbm/engineering.py']))
        observer=(root/'usr/libexec/project-cbm/engineering.py').read_text()
        if lock['product']['candidate'] in ('private-engineering-poc3','private-engineering-poc4','private-engineering-rc1','private-engineering-rc2'):
            template=root/'usr/share/project-cbm/vice-defaults.ini'
            user=root/home/'.config/vice/sdl-vicerc'
            check('presentation_template_exact',template.read_bytes()==presentation_defaults() and template.stat().st_uid==0)
            check('presentation_user_copy_exact',user.read_bytes()==template.read_bytes() and user.stat().st_uid==1000 and user.stat().st_gid==1000)
            check('user_config_not_system_owned','/'+home+'/.config/vice/sdl-vicerc' not in (root/'usr/share/project-cbm/owned-paths.txt').read_text().splitlines())
            check('active_DRM_reporter_present',(root/'usr/libexec/project-cbm-vice/drm-state').is_file())
            check('engineering_geometry_opt_in',"env['CBM_PRESENTATION_DIAGNOSTICS']='1'" in observer and 'active_drm' in observer)
            check('VICE_telemetry_patch_present',b'CBM_PRESENTATION chip=' in (root/'usr/bin/x64sc').read_bytes())
        check('bounded_diagnostics','LIMIT = 128 * 1024' in observer and 'KEEP = 4' in observer and 'samples<3' in observer)
        launcher=(root/'usr/bin/pcbm-run-vice').read_text()
        check('VICE_unprivileged_F10','EUID != 0' in launcher and '-menukey 291' in launcher)
        check('single_shared_launch_path','pcbm-run-vice' in (root/'usr/bin/pcbm-boot').read_text() and 'pcbm-run-vice' in (root/'usr/bin/pcbm-dialog-lib.sh').read_text())
        power=(root/'etc/sudoers.d/pcbm-power').read_text()
        check('only_exact_power_sudo',power==account+' ALL=(root) NOPASSWD: /usr/sbin/poweroff "", /usr/sbin/reboot ""\n')
        grants=[p.name for p in (root/'etc/sudoers.d').iterdir() if p.is_file() and 'NOPASSWD' in p.read_text()]
        check('no_other_passwordless_grants',set(grants)==({'pcbm-power','pcbm-operations'} if activated else {'pcbm-power'}))
        if activated:
            from validate_activation import inspect
            inspect(root,lock,check,digest)
        media=json.loads((root/'usr/share/project-cbm/qualification-media.json').read_text())
        check('media_source_matches_lock',media['source_commit']==lock['qualification_media']['source_commit'])
        for entry in media['files']:
            p=root/content/entry['destination']
            check('media_'+entry['name'],p.is_file() and digest(p)==entry['sha256'] and p.stat().st_uid==1000)
        shadow={row.split(':')[0]:row.split(':')[1] for row in (root/'etc/shadow').read_text().splitlines()}
        check('locked_local_passwords',shadow.get('root')=='*' and shadow.get(account)==('!' if single_user else '*'))
        inventory=output('dpkg-query','--admindir='+str(root/'var/lib/dpkg'),'-W',
                         '-f=${binary:Package}\t${Version}\t${Architecture}\t${Installed-Size}\t${db:Status-Status}\n')
        (args.results/'packages.tsv').write_text(inventory+'\n')
        packages={}
        for line in inventory.splitlines():
            name,version,arch,size,status=line.split('\t')
            if status=='installed': packages[name.split(':')[0]]=(version,arch,int(size or 0))
        for name in ['libgl1','libglx0','libglx-mesa0','libegl1','libegl-mesa0','libgles2','libgbm1','libgl1-mesa-dri']:
            check('graphics_runtime_'+name,name in packages)
        for name in ['libGL.so.1','libGLX.so.0','libEGL.so.1','libGLESv2.so.2']:
            p=root/'usr/lib/aarch64-linux-gnu'/name
            check('graphics_loader_'+name,p.is_symlink() and (p.parent/p.readlink()).is_file())
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
        check('content_directory_owned_by_runtime',(root/content).stat().st_uid==1000)
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
