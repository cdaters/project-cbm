#!/usr/bin/env python3
"""Actual-image physical-UX contracts; retain earlier checks with explicit supersession."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
from build_contracts import read_json
from validate_poc4_physical_ux import inspect as previous_inspect


def inspect(root, record, kit):
    result = previous_inspect(root, record, kit)
    checks = result['checks']
    def text(path): return (root/path).read_text()
    menu=text('usr/bin/pcbm-menu')
    backend=text('usr/share/project-cbm/runtime/project_cbm/config_backend.py')
    info=text('usr/share/project-cbm/runtime/project_cbm/info.py')
    status=text('usr/libexec/project-cbm-menu/pcbm_status_view.py')
    config=text('usr/bin/pcbm-config')
    # Appliance projection supersedes the narrow network-only Main Menu consumer.
    checks['main_menu_authoritative_summary']='pcbm-info --json --appliance' in menu and 'pcbm_status_view.py view main' in menu and 'def collect_appliance(' in info
    checks['appliance_bounded_queries']='source.deadline=time.monotonic()+2' in info
    checks['state_aware_actions']=all(v in status for v in ("if state=='off'", "if state=='on'", "'pending'", "'failed'", "'unavailable'"))
    checks['no_menu_network_probes']=all(v not in status+config for v in ('subprocess','nmcli ','systemctl ','ss -','ip -'))
    checks['owner_connection_guidance']=all(v in status for v in ('first-boot owner password','separate password','smb://','ssh '))
    checks['confirmed_actual_services']='actual=state(rows.get(name),listening)' in backend
    checks['default_computer_name']=text('etc/hostname').strip()=='projectcbm'
    checks['computer_local_alias']=any(line.split()==['127.0.1.1','projectcbm'] for line in text('etc/hosts').splitlines())
    smb=text('etc/samba/smb.conf')
    checks['sharing_owner_content_boundary']='valid users = owner' in smb and 'force user = pi' in smb and 'guest ok = no' in smb
    checks['dynamic_samba_mdns']='mdns name = mdns' in smb
    checks['no_baked_sharing_enrollment']=not (root/'var/lib/project-cbm/sharing-status.json').exists()
    checks['sharing_discovery_explicit']='Network Discovery will also turn on' in config and "self.service('discovery',True)" in backend
    checks['safe_enrollment_metadata']='sharing-status.json' in backend and "'password_set':True" in backend
    checks['appliance_schema']=read_json(kit/record['appliance_schema']['path'])['properties']['format']['const']=='project-cbm.appliance-info'
    checks['release_documentation']=all((root/'usr/share/doc/project-cbm-runtime/release'/name).is_file() for name in ('user-guide.md','networking.md','build-your-own.md','factory.md','customization.md','development.md','recovery.md'))
    result['result'] = 'PASS' if all(checks.values()) else 'FAIL'
    result['scope'] = 'Exact installed release/service/account/discovery/docs contracts plus preserved lifecycle; physical behavior UNTESTED'
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('image','lock','kit','output'):
        p.add_argument(name, type=Path)
    a = p.parse_args()
    lock = read_json(a.lock)
    record = read_json(a.kit/lock['components']['menu']['build_record']['path'])
    loop = subprocess.check_output(['losetup','--read-only','--find','--show','--partscan',str(a.image)], text=True).strip()
    try:
        with tempfile.TemporaryDirectory(dir=a.output.parent) as tmp:
            root = Path(tmp)
            subprocess.run(['mount','-o','ro,noload',loop+'p2',str(root)], check=True)
            try:
                result = inspect(root, record, a.kit)
            finally:
                subprocess.run(['umount',str(root)], check=True)
    finally:
        subprocess.run(['losetup','--detach',loop], check=True)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'result':result['result'],'checks':len(result['checks']),
                      'failed':[k for k,v in result['checks'].items() if not v]}))
    if result['result'] != 'PASS':
        raise SystemExit(1)

if __name__ == '__main__':
    main()
