#!/usr/bin/env python3
"""Actual-image RC1 additions, including the FAT boot partition; never execute target code."""
import argparse
import ast
import json
from pathlib import Path
import subprocess
import tempfile
from build_contracts import read_json
from validate_release_refinement import inspect as previous_inspect


def inspect_runtime(root, record, kit):
    result = previous_inspect(root, record, kit)
    # RC1 extends the existing device query, not the number/scope of probes.
    # Read literal argv from source without executing installed target code.
    network = (root/'usr/share/project-cbm/runtime/project_cbm/network_info.py').read_text()
    constants = {}
    for node in ast.parse(network).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ('IP', 'DEVICES', 'WIFI'):
                constants[node.targets[0].id] = ast.literal_eval(node.value)
    expected = {
        'IP':['/usr/sbin/ip','-j','address','show'],
        'DEVICES':['/usr/bin/nmcli','--terse','--escape','yes','--fields',
                   'GENERAL.DEVICE,GENERAL.TYPE,GENERAL.STATE,IP4.GATEWAY,IP4.DNS,IP6.GATEWAY,IP6.DNS','device','show'],
        'WIFI':['/usr/bin/nmcli','--terse','--escape','yes','--fields','DEVICE,ACTIVE,SSID','device','wifi','list','--rescan','no'],
    }
    result['checks']['bounded_fixed_network_queries'] = constants == expected and '--show-secrets' not in network and "'connection'" not in network
    result['result'] = 'PASS' if all(result['checks'].values()) else 'FAIL'
    return result


def inspect(root, boot, record, kit):
    result = inspect_runtime(root, record, kit)
    checks = result['checks']
    def text(name):return (root/name).read_text()
    command = (boot/'cmdline.txt').read_text().split()
    checks['quiet_kernel_with_errors'] = all(v in command for v in ('quiet','loglevel=4','logo.nologo','systemd.show_status=auto'))
    checks['kernel_console_and_root_retained'] = 'console=tty1' in command and 'rootwait' in command and any(v.startswith('root=PARTUUID=') for v in command)
    checks['rainbow_disabled'] = '[all]\n# Project CBM boot presentation\ndisable_splash=1' in (boot/'config.txt').read_text()
    checks['kms_retained'] = 'dtoverlay=vc4-kms-v3d' in (boot/'config.txt').read_text()
    checks['text_presentation_existing_session'] = 'PROJECT CBM' in text('etc/issue') and 'PROJECT CBM' in text('usr/libexec/project-cbm/pcbm-console-session')
    checks['only_appliance_login_hushed'] = (root/'home/pi/.hushlogin').is_file() and not (root/'home/pcbm/.hushlogin').exists()
    first = text('usr/libexec/project-cbm/first_boot.py')
    checks['completed_initialization_fast_path'] = 'if completed(STATE):' in first and 'unsafe first-boot completion marker' in first
    checks['no_baked_completion'] = not (root/'var/lib/project-cbm/first-boot/complete.json').exists()
    content = root/'home/pi/pcbm'
    checks['type_machine_hierarchy'] = all((content/category/family).is_dir() for category in ('games','demos','programs','roms') for family in ('c64','c128','vic20','plus4','pet','cbm2','cbm5x0'))
    checks['no_format_directory_sprawl'] = not any((content/'games/c64'/name).exists() for name in ('disk','tape','cart','prg'))
    checks['separate_admin_home'] = not any((root/'home/pcbm'/name).exists() for name in ('games','demos','music','programs','roms'))
    checks['optional_disks_canonical_library'] = (content/'music/c64/Creation/SID-Wizard/SID-Wizard-1.97.d64').is_file() and (content/'programs/c64/Communications/StrikeTerm/StrikeTerm-2014-Final.d64').is_file()
    checks['content_profile_authority'] = 'library.content_profile' in text('usr/share/project-cbm/runtime/project_cbm/profiles.py')
    checks['import_family_authority'] = 'library.import_destination' in text('usr/share/project-cbm/runtime/project_cbm/importer.py') and 'pcbm-profiles content-families' in text('usr/bin/pcbm-import')
    checks['gateway_dns_authority'] = 'IP4.GATEWAY,IP4.DNS,IP6.GATEWAY,IP6.DNS' in text('usr/share/project-cbm/runtime/project_cbm/network_info.py')
    checks['detailed_network_views'] = all('gateway_ipv4' in text(name) and 'dns_ipv6' in text(name) for name in ('usr/libexec/project-cbm-menu/pcbm_info_view.py','usr/libexec/project-cbm-menu/pcbm_status_view.py'))
    checks['rc1_user_guides'] = all((root/'usr/share/doc/project-cbm-runtime/release'/name).is_file() for name in ('content.md','boot.md'))
    checks['network_readiness_wait_retained'] = not (root/'etc/systemd/system/NetworkManager-wait-online.service').is_symlink() or (root/'etc/systemd/system/NetworkManager-wait-online.service').readlink() != Path('/dev/null')
    result['result'] = 'PASS' if all(checks.values()) else 'FAIL'
    result['scope'] = 'Actual-image bytes/configuration; Pi boot appearance/time and complete RC1 behavior require physical qualification'
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
