#!/usr/bin/env python3
"""Actual-image admission/network checks, retaining the established corrective gates."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
from build_contracts import read_json
from validate_poc4_corrective import inspect as inspect_corrective


def inspect(root, record, kit):
    result = inspect_corrective(root, record, kit)
    checks = result['checks']
    def text(path): return (root/path).read_text()
    renderer = text('usr/libexec/project-cbm-menu/pcbm_cover_view.py')
    wrapper = text('usr/bin/pcbm-cover')
    network = text('usr/share/project-cbm/runtime/project_cbm/network_info.py')
    info = text('usr/share/project-cbm/runtime/project_cbm/info.py')
    view = text('usr/libexec/project-cbm-menu/pcbm_info_view.py')
    checks['kernel_tty_identity'] = all(v in renderer for v in ('0x80045432', '0x401', "device(control)")) and '$(tty)' not in wrapper
    checks['active_foreground_controlling_vt'] = all(v in renderer for v in ('0x5603', 'skip_inactive_vt', 'os.tcgetpgrp(control) != os.getpgrp()', 'skip_background'))
    checks['admission_failure_open'] = '--admit || exit 0' in wrapper and "telemetry(result)" in renderer
    checks['fixed_skip_diagnostics'] = all(v in renderer+wrapper for v in ('skip_root','skip_nonterminal','skip_wrong_tty','skip_tty_unavailable','skip_profile','skip_asset','asset_ready'))
    checks['no_terminal_mode_workaround'] = all(v not in renderer for v in ('tcsetattr','tcsetpgrp','VT_ACTIVATE','setsid(','setpgid('))
    checks['network_single_authority'] = 'network_info.collect' in info and 'network_interfaces' in view and all(v not in view for v in ('subprocess','nmcli','ip -j'))
    checks['bounded_fixed_network_queries'] = all(v in network for v in ("'/usr/sbin/ip'", "'GENERAL.DEVICE,GENERAL.TYPE,GENERAL.STATE'", "'DEVICE,ACTIVE,SSID'", "'--rescan', 'no'")) and '--show-secrets' not in network and "'connection'" not in network
    checks['network_address_mac_ssid_fields'] = all(v in network for v in ("'ipv4'", "'ipv6'", "'mac'", "'ssid'", 'isprintable()', 'dadfailed'))
    checks['network_existing_ui_route'] = 'Network information (IP/MAC and status)' in text('usr/bin/pcbm-config') and 'pcbm-info --json' in text('usr/bin/pcbm-system-info')
    schema = read_json(kit/record['information_schema']['path'])
    checks['information_schema_backward_compatible'] = schema['properties']['schema_version']['const'] == 1 and 'network_interfaces' in schema['properties']['current_state']['properties']
    status = text('var/lib/dpkg/status')
    checks['network_tools_installed'] = all((root/v).is_file() for v in ('usr/sbin/ip','usr/bin/nmcli')) and 'Package: iproute2\nStatus: install ok installed' in status
    result['result'] = 'PASS' if all(checks.values()) else 'FAIL'
    result['scope'] = 'Exact actual-image payload/admission/network contracts; native behavior separate; physical Pi Cover/KMS/VT/network UNTESTED'
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
