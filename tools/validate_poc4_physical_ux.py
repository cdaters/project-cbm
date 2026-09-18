#!/usr/bin/env python3
"""Actual-image physical-UX contracts; retain earlier checks with explicit supersession."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
from build_contracts import read_json
from validate_poc4_admission import inspect as previous_inspect


def inspect(root, record, kit):
    result = previous_inspect(root, record, kit)
    checks = result['checks']
    def text(path): return (root/path).read_text()
    lifecycle = text('usr/libexec/project-cbm/engineering.py')
    renderer = text('usr/libexec/project-cbm-menu/pcbm_cover_view.py')
    ui = text('usr/share/project-cbm-menu/pcbm-setup-ui.sh')
    shared = text('usr/share/project-cbm-menu/pcbm-ui.sh')
    setup = text('usr/bin/pcbm-first-run')
    # These three old assertions encoded the superseded 2s/Unicode/blank-input UI.
    checks['same_group_supervision'] = 'start_new_session' not in lifecycle and 'process_group=' not in lifecycle and 'timeout=6.0, grace=.5' in lifecycle
    checks['human_selectors_advanced'] = all(v in ui for v in ('PCBM_UI_HIDE_TAGS=true','United Kingdom - English','Coordinated Universal Time','ADVANCED','Advanced: enter an identifier'))
    del checks['hidden_password_explanation']
    checks['safe_password_masking'] = all(v in shared for v in ('--insecure','--passwordbox','Typed characters are masked with asterisks.'))
    checks['ascii_password_guidance'] = '12-128 printable characters' in setup and '8-63 printable ASCII characters' in ui and all(v not in setup+ui for v in ('12–128','8–63','12—128','8—63'))
    checks['cover_dwell_after_present'] = renderer.index('sdl.SDL_RenderPresent(renderer)') < renderer.index('deadline = time.monotonic() + DURATION_SECONDS')
    checks['cover_phase_timings'] = all(v in renderer for v in ("stage('window_create')","stage('renderer_create')","stage('texture_load')","stage('present_begin')","stage('releasing')"))
    scan = text('usr/share/project-cbm/runtime/project_cbm/wifi_scan.py')
    backend = text('usr/share/project-cbm/runtime/project_cbm/config_backend.py')
    checks['fresh_scan_readiness_and_completion'] = all(v in scan for v in ('GENERAL.DBUS-PATH','LastScan','current > old','start + 25','start + 10','rounds < 2'))
    checks['scan_fixed_diagnostics_and_timeout'] = 'wifi-scan.json' in backend and 'wifi_scan_unconfirmed' in backend and 'up to 25 seconds' in setup
    menu = text('usr/bin/pcbm-menu')
    info = text('usr/share/project-cbm/runtime/project_cbm/info.py')
    view = text('usr/libexec/project-cbm-menu/pcbm_info_view.py')
    checks['main_menu_authoritative_summary'] = 'pcbm-info --json --network-only' in menu and '--network-summary' in menu and 'def collect_network(' in info and 'def network_summary(' in view
    checks['summary_bounded_no_ssid_probe'] = 'source.deadline = time.monotonic()+1' in info and 'include_ssids=False' in info
    schema = read_json(kit/record['network_summary_schema']['path'])
    checks['network_projection_schema'] = schema['properties']['format']['const']=='project-cbm.network-info' and schema['properties']['schema_version']['const']==1
    result['result'] = 'PASS' if all(checks.values()) else 'FAIL'
    result['scope'] = 'Exact installed UX/Cover/scan/IP contracts; native tests separate; physical visibility/radio/Pi timings UNTESTED'
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
