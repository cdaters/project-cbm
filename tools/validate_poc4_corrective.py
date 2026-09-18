#!/usr/bin/env python3
"""Inspect the actual corrective image read-only; physical tty/KMS/Wi-Fi remain untested."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from build_contracts import read_json
from validate_poc4_covers import inspect as inspect_covers


def exact_payload(root, mapping):
    checks = {}
    for relative, descriptor in mapping.items():
        path = root/relative
        checks['exact_'+relative] = (path.is_file() and not path.is_symlink()
            and path.stat().st_size == descriptor['size_bytes']
            and hashlib.sha256(path.read_bytes()).hexdigest() == descriptor['sha256'])
    return checks


def inspect(root, record, kit):
    result = inspect_covers(root, record, kit)
    checks = result['checks']
    # The historical GNU-timeout launch contract is superseded only for this
    # validator. Its original validator and candidate records remain unchanged.
    del checks['bounded_shared_transition']
    checks.update(exact_payload(root, record['corrective_payload']))
    def text(relative):
        return (root/relative).read_text()
    lifecycle = text('usr/libexec/project-cbm/engineering.py')
    launcher = text('usr/bin/pcbm-run-vice')
    setup = text('usr/bin/pcbm-first-run')
    ui = text('usr/share/project-cbm-menu/pcbm-setup-ui.sh')
    backend = text('usr/share/project-cbm/runtime/project_cbm/config_backend.py')
    renderer = text('usr/libexec/project-cbm-menu/pcbm_cover_view.py')
    checks['shared_guarded_handoff'] = 'exec /usr/libexec/project-cbm/engineering.py run-with-cover' in launcher
    checks['precover_capture_order'] = lifecycle.index('saved=terminal_state(fd)') < lifecycle.index("save('cover.json',run_cover(")
    checks['same_group_supervision'] = 'start_new_session' not in lifecycle and 'process_group=' not in lifecycle and 'timeout=2.0, grace=.5' in lifecycle
    checks['terminate_kill_reap'] = all(token in lifecycle for token in ('child.terminate()','child.kill()','child.wait()','active(None)'))
    checks['previce_restore'] = lifecycle.index("save('cover-cleanup.json',restore_tty(fd,saved))") < lifecycle.index('proc=subprocess.Popen(argv')
    checks['postvice_restore_verification'] = "actual=terminal_state(fd);restored=restore_tty(fd,saved)" in lifecycle and "'verified':not errors and not mismatch" in lifecycle
    checks['terminal_phase_records'] = all("'"+name+"'" in lifecycle for name in ('pre-cover.json','post-cover.json','cover-cleanup.json','post-vice.json','cleanup.json'))
    checks['structured_cover_records'] = 'PCBM_COVER ' in lifecycle and 'PCBM_COVER ' in renderer and "'ended_monotonic'" in lifecycle
    checks['human_selectors_advanced'] = all(token in ui for token in ('PCBM_UI_HIDE_TAGS=true','United Kingdom — English','Coordinated Universal Time','ADVANCED','Advanced: enter an identifier'))
    checks['back_retry_resume'] = all(token in setup for token in ('back $? region','back $? keyboard','stage=network','step_done owner')) and all(token in ui for token in ('RETRY','SCAN','COUNTRY','OFFLINE'))
    checks['working_before_backend'] = setup.index('pcbm_ui_working "$label"') < setup.index('reply=$(printf')
    checks['wifi_before_finish'] = 'if pcbm_setup_wifi setup-;then stage=finish' in setup and 'setup-wifi-enroll' in setup
    checks['offline_path'] = 'OFFLINE) if request setup-network false;then stage=finish' in setup
    shared = text('usr/share/project-cbm-menu/pcbm-ui.sh')
    checks['hidden_password_explanation'] = 'hidden' in shared.lower() and '--passwordbox' in shared
    checks['fixed_setup_wifi_operations'] = all(token in text('usr/share/project-cbm/runtime/project_cbm/setup.py') for token in ('setup-wifi-country','setup-wifi-rescan','setup-wifi-enroll'))
    checks['unprivileged_F10_ALSA'] = all(token in launcher for token in ('EUID != 0','-menukey 291','SDL_AUDIODRIVER=alsa'))
    manifest = read_json(kit/record['covers']['manifest']['path'])
    checks['covers_readable_unprivileged'] = all((root/'usr/share/project-cbm-menu'/item['path']).stat().st_mode & 0o004 for item in manifest['files'])
    checks['diagnostics_private_marker'] = (root/'etc/pcbm/engineering-poc').is_file() and 'os.umask(0o077)' in lifecycle
    result['result'] = 'PASS' if all(checks.values()) else 'FAIL'
    result['scope'] = 'Exact installed corrective payload and offline contracts; native behavioral tests separate; physical KMS/VT and Wi-Fi UNTESTED'
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
