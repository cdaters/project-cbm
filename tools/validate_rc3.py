#!/usr/bin/env python3
"""Actual-image RC3 additions, including the FAT boot partition; never execute target code."""
import argparse
import ast
import json
from pathlib import Path
import subprocess
import tempfile
from build_contracts import read_json
from validate_rc1 import inspect_runtime


def inspect(root, boot, record, kit):
    result = inspect_runtime(root, record, kit, single_user=True)
    checks = result['checks']
    def text(name):return (root/name).read_text()
    command = (boot/'cmdline.txt').read_text().split()
    checks['quiet_kernel_with_errors'] = all(v in command for v in ('quiet','loglevel=4','logo.nologo','systemd.show_status=auto'))
    checks['kernel_console_and_root_retained'] = 'console=tty1' in command and 'rootwait' in command and any(v.startswith('root=PARTUUID=') for v in command)
    checks['rainbow_disabled'] = '[all]\n# Project CBM boot presentation\ndisable_splash=1' in (boot/'config.txt').read_text()
    checks['kms_retained'] = 'dtoverlay=vc4-kms-v3d' in (boot/'config.txt').read_text()
    checks['primary_presentation_existing_session'] = 'boot_session.py' in text('usr/libexec/project-cbm/pcbm-console-session') and "['/usr/bin/pcbm-cover','--boot']" in text('usr/libexec/project-cbm/boot_session.py')
    checks['only_appliance_login_hushed'] = (root/'home/pcbm/.hushlogin').is_file() and not (root/'home/pi').exists()
    first = text('usr/libexec/project-cbm/first_boot.py')
    checks['completed_initialization_fast_path'] = 'if completed(STATE):' in first and 'unsafe first-boot completion marker' in first
    checks['no_baked_completion'] = not (root/'var/lib/project-cbm/first-boot/complete.json').exists()
    content = root/'home/pcbm/content'
    checks['type_machine_hierarchy'] = all((content/category/family).is_dir() for category in ('games','demos','programs','roms') for family in ('c64','c128','vic20','plus4','pet','cbm2','cbm5x0'))
    checks['no_format_directory_sprawl'] = not any((content/'games/c64'/name).exists() for name in ('disk','tape','cart','prg'))
    checks['no_loose_content_categories_in_home'] = not any((root/'home/pcbm'/name).exists() for name in ('games','demos','music','programs','roms'))
    checks['optional_disks_canonical_library'] = (content/'music/c64/Creation/SID-Wizard/SID-Wizard-1.97.d64').is_file() and (content/'programs/c64/Communications/StrikeTerm/StrikeTerm-2014-Final.d64').is_file()
    checks['content_profile_authority'] = 'library.content_profile' in text('usr/share/project-cbm/runtime/project_cbm/profiles.py')
    checks['import_family_authority'] = 'library.import_destination' in text('usr/share/project-cbm/runtime/project_cbm/importer.py') and 'pcbm-profiles content-families' in text('usr/bin/pcbm-import')
    checks['gateway_dns_authority'] = 'IP4.GATEWAY,IP4.DNS,IP6.GATEWAY,IP6.DNS' in text('usr/share/project-cbm/runtime/project_cbm/network_info.py')
    checks['detailed_network_views'] = all('gateway_ipv4' in text(name) and 'dns_ipv6' in text(name) for name in ('usr/libexec/project-cbm-menu/pcbm_info_view.py','usr/libexec/project-cbm-menu/pcbm_status_view.py'))
    checks['release_user_guides'] = all((root/'usr/share/doc/project-cbm-runtime/release'/name).is_file() for name in ('content.md','boot.md'))
    checks['network_readiness_wait_retained'] = not (root/'etc/systemd/system/NetworkManager-wait-online.service').is_symlink() or (root/'etc/systemd/system/NetworkManager-wait-online.service').readlink() != Path('/dev/null')
    import hashlib
    artwork=json.loads(text('usr/share/doc/project-cbm-menu/primary-artwork.json'))['file']
    path=root/'usr/share/project-cbm-menu'/artwork['path']
    checks['exact_primary_artwork'] = path.is_file() and path.stat().st_size==artwork['size_bytes'] and hashlib.sha256(path.read_bytes()).hexdigest()==artwork['sha256']
    checks['primary_matches_frozen_inputs'] = (
        (root/'usr/share/doc/project-cbm-menu/primary-artwork.json').read_bytes()==(kit/record['primary']['manifest']['path']).read_bytes()
        and path.read_bytes()==(kit/record['primary']['asset']['path']).read_bytes())
    checks['primary_dwell_separate'] = '(3.0 if control_fd is not None else 1.5 if primary else DURATION_SECONDS)' in text('usr/libexec/project-cbm-menu/pcbm_cover_view.py')
    checks['no_obsolete_noarg_presentation'] = '/usr/bin/pcbm-cover\n' not in text('usr/bin/pcbm-menu')
    checks['getty_no_idle_deferral'] = all('Type=simple' in text('etc/systemd/system/getty@'+tty+'.service.d/autologin.conf') for tty in ('tty1','tty2'))
    checks['boot_phase_trace'] = '/proc/uptime' in text('usr/libexec/project-cbm/boot-trace.sh') and 'dialog_dispatch' in text('usr/bin/pcbm-menu')
    importer=text('usr/share/project-cbm/runtime/project_cbm/importer.py')
    checks['fat_copy_identity_and_readonly'] = 'uid=1000,gid=1000,fmask=0177,dmask=0077' in importer and "'ro,nodev,nosuid,noexec'" in importer and "options+',noload'" in importer
    checks['import_failure_release_feedback'] = 'source_unmounted' in importer and 'import-error' in text('usr/bin/pcbm-import') and 'safe to remove' in text('usr/libexec/project-cbm-menu/pcbm_config_bridge.py')
    checks['files_usb_entry'] = 'Import from USB' in text('usr/bin/pcbm-files') and '/usr/bin/mc /home/pcbm/content /home/pcbm' in text('usr/bin/pcbm-files')
    admin=text('usr/share/project-cbm/runtime/project_cbm/admin.py')
    checks['same_user_terminal_authenticated_admin'] = "['/bin/bash','--noprofile','--norc','-i']" in admin and "['/usr/bin/sudo','-k','--'" in admin and "'/bin/su'" not in admin
    supervisor=text('usr/libexec/project-cbm/boot_session.py')
    checks['boot_readiness_pipes_and_restore'] = all(token in supervisor for token in ('os.pipe()', 'handoff=(ready_r,release_w)', "report['cleanup'].get('verified')", 'timeout=30', 'worker.wait()'))
    checks['no_late_second_splash'] = 'primary-presentation' not in text('usr/libexec/project-cbm/pcbm-console-session')
    checks['completed_setup_silent_recovery'] = 'PCBM_SETUP_QUIET=true request setup-finish' in text('usr/bin/pcbm-first-run')
    checks['ready_dialog_handoff'] = 'pcbm_boot_handoff' in text('usr/bin/pcbm-menu') and 'pcbm_boot_handoff' in text('usr/share/project-cbm-menu/pcbm-ui.sh')
    checks['getty_quiet_only_tty1'] = '--skip-login --noissue --nohostname' in text('etc/systemd/system/getty@tty1.service.d/autologin.conf') and '--skip-login' not in text('etc/systemd/system/getty@tty2.service.d/autologin.conf')
    checks['metadata_filter_before_traversal'] = 'if host_metadata(name):ignored_metadata+=1;continue' in importer and importer.index('if host_metadata(name)') < importer.index('if stat.S_ISDIR(status.st_mode)')
    tree=ast.parse(importer);metadata=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='HOST_METADATA' for t in n.targets))
    checks['narrow_metadata_names'] = metadata=={'.DS_Store','.Spotlight-V100','.Trashes','.fseventsd','.TemporaryItems','.VolumeIcon.icns','.AppleDouble','System Volume Information','$RECYCLE.BIN'} and "name.startswith('._')" in importer
    checks['separate_content_metadata_counts'] = 'content files' in text('usr/libexec/project-cbm-menu/pcbm_config_bridge.py') and 'ignored_metadata' in text('usr/libexec/project-cbm-menu/pcbm_config_bridge.py')
    hook=root/'etc/initramfs-tools/hooks/pcbm-quiet-fsck'
    checks['quiet_fsck_hook_installed'] = hook.is_file() and hook.stat().st_mode&0o777==0o755
    for name in ('initramfs8','initramfs_2712'):
        # Host decompression only. Extract onto external-backed scratch, never /tmp.
        with tempfile.TemporaryDirectory(dir=root.parent) as scratch:
            subprocess.run(['unmkinitramfs',str(boot/name),scratch],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            functions=list(Path(scratch).glob('**/scripts/functions'))
            body=functions[0].read_text() if len(functions)==1 else ''
            checks[name+'_quiet_fsck_and_verbose_recovery'] = ('Project CBM: successful quiet checks' in body and '>/run/initramfs/pcbm-fsck.console 2>&1' in body and 'if [ "$FSCKCODE" -ne 0 ]; then cat /run/initramfs/pcbm-fsck.console; fi' in body and 'fsck $spinner $force $fix -V' in body and 'filesystem failed' in body)
    result['result'] = 'PASS' if all(checks.values()) else 'FAIL'
    result['scope'] = 'Actual-image bytes/configuration; Pi boot appearance/time and complete RC3 behavior require physical qualification'
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('image','lock','kit','output'):p.add_argument(name,type=Path)
    a=p.parse_args();lock=read_json(a.lock);record=read_json(a.kit/lock['components']['menu']['build_record']['path'])
    loop=subprocess.check_output(['losetup','--read-only','--find','--show','--partscan',str(a.image)],text=True).strip()
    mounted=[]
    try:
        with tempfile.TemporaryDirectory(dir=a.output.parent) as directory:
            root=Path(directory)/'root';boot=Path(directory)/'boot';root.mkdir();boot.mkdir()
            try:
                for dev,path,flags in [(loop+'p2',root,'ro,noload'),(loop+'p1',boot,'ro')]:
                    subprocess.run(['mount','-o',flags,dev,str(path)],check=True);mounted.append(path)
                result=inspect(root,boot,record,a.kit)
            finally:
                for path in reversed(mounted):subprocess.run(['umount',str(path)],check=True)
    finally:subprocess.run(['losetup','--detach',loop],check=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'result':result['result'],'checks':len(result['checks']),'failed':[k for k,v in result['checks'].items() if not v]}))
    if result['result']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
