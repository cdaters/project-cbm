#!/usr/bin/env python3
"""Actual-image RC2 additions, including the FAT boot partition; never execute target code."""
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
    checks['primary_presentation_existing_session'] = 'primary-presentation' in text('usr/libexec/project-cbm/pcbm-console-session') and "['/usr/bin/pcbm-cover','--primary']" in text('usr/libexec/project-cbm/engineering.py')
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
    checks['primary_dwell_separate'] = '(1.5 if primary else DURATION_SECONDS)' in text('usr/libexec/project-cbm-menu/pcbm_cover_view.py')
    checks['no_obsolete_noarg_presentation'] = '/usr/bin/pcbm-cover\n' not in text('usr/bin/pcbm-menu')
    checks['getty_no_idle_deferral'] = all('Type=simple' in text('etc/systemd/system/getty@'+tty+'.service.d/autologin.conf') for tty in ('tty1','tty2'))
    checks['boot_phase_trace'] = '/proc/uptime' in text('usr/libexec/project-cbm/boot-trace.sh') and 'dialog_dispatch' in text('usr/bin/pcbm-menu')
    importer=text('usr/share/project-cbm/runtime/project_cbm/importer.py')
    checks['fat_copy_identity_and_readonly'] = 'uid=1000,gid=1000,fmask=0177,dmask=0077' in importer and "'ro,nodev,nosuid,noexec'" in importer and "options+',noload'" in importer
    checks['import_failure_release_feedback'] = 'source_unmounted' in importer and 'import-error' in text('usr/bin/pcbm-import') and 'safe to remove' in text('usr/libexec/project-cbm-menu/pcbm_config_bridge.py')
    checks['files_usb_entry'] = 'Import from USB' in text('usr/bin/pcbm-files') and '/usr/bin/mc /home/pcbm/content /home/pcbm' in text('usr/bin/pcbm-files')
    admin=text('usr/share/project-cbm/runtime/project_cbm/admin.py')
    checks['same_user_terminal_authenticated_admin'] = "['/bin/bash','--noprofile','--norc','-i']" in admin and "['/usr/bin/sudo','-k','--'" in admin and "'/bin/su'" not in admin
    result['result'] = 'PASS' if all(checks.values()) else 'FAIL'
    result['scope'] = 'Actual-image bytes/configuration; Pi boot appearance/time and complete RC2 behavior require physical qualification'
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
