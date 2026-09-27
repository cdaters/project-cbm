#!/usr/bin/env python3
"""Read-only development image checks; retain stable checks with named USB successors."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
from build_contracts import read_json
from development_identity import content_1_2
from validate_rc3 import inspect as inspect_previous


def inspect(root, boot, record, kit):
    lock = read_json(kit / 'release-lock.json')
    if not content_1_2(lock['product']):
        raise ValueError('explicit 1.2 image required')
    result = inspect_previous(root, boot, record, kit)
    checks = result['checks']
    def text(name): return (root / name).read_text()
    view = text('usr/libexec/project-cbm-menu/pcbm_ingest_view.py')
    menu = text('usr/bin/pcbm-import')
    session = text('usr/share/project-cbm-menu/pcbm-usb-session.sh')
    browse = text('usr/bin/pcbm-usb-browse')
    worker = text('usr/share/project-cbm/runtime/project_cbm/usb_browse.py')
    # These three old checks describe the superseded immediate-import UI.
    # All other inherited checks, including exact frozen payloads, remain required.
    result['superseded_checks'] = {
        'import_destination_feedback': 'Explicit selection/plan/review before copy',
        'import_failure_release_feedback': 'Schema 2 shared result presenter',
        'files_usb_entry': 'Separate read-only USB browsing instead of second Import path',
    }
    for name in result['superseded_checks']:
        del checks[name]
    checks['review_before_explicit_import'] = (menu.index('busy_rpc plan') < menu.index('busy_rpc import')
        and 'Import selected files' in menu and 'Library:' in view and 'Already Present:' in view)
    checks['confirmed_release_only'] = ("d.get('source_unmounted') is True" in view
        and 'Drive release was not confirmed.' in view and 'result_message' in session)
    checks['separate_readonly_browser'] = ('/usr/bin/pcbm-usb-browse' in text('usr/bin/pcbm-files')
        and 'Mount Read-Only' in browse and 'Safe Unmount' in browse
        and "rpc release" in browse and "'/usr/bin/mc'" in worker and "'-u'" in worker)
    hub = text('usr/bin/pcbm-content')
    checks['content_navigation'] = all(value in hub for value in ('Browse Library','Import from USB','pcbm-content-help'))
    checks['library_existing_launch_path'] = ('pcbm_launch_content' in text('usr/bin/pcbm-library')
        and 'pcbm-run-vice' in text('usr/bin/pcbm-dialog-lib.sh'))
    checks['private_development_marker'] = text('etc/pcbm/engineering-poc').strip() == lock['product']['candidate']
    checks['no_bundled_usb_qualification_fixtures'] = not list((root/'home/pcbm/content').rglob('CBM12-USB-QUAL*'))
    if 'kms-capture' in lock['components']:
        helper=root/'usr/libexec/pcbm-kms-capture'
        checks['capture_separate_native_helper'] = helper.is_file() and helper.read_bytes().startswith(b'\x7fELF') and helper.stat().st_mode & 0o7777 == 0o755
        checks['capture_no_file_capabilities'] = not subprocess.check_output(['getcap',str(helper)],text=True).strip()
        checks['capture_exact_package'] = lock['components']['kms-capture']['package']['version'] in ('1.0.0~dev1-1','1.0.0~dev2-1','1.0.0-1')
        checks['capture_fixed_sudo'] = ('pcbm ALL=(root) NOPASSWD: /usr/libexec/pcbm-kms-capture ""' in text('etc/sudoers.d/pcbm-operations') and '!use_pty' in text('etc/sudoers.d/pcbm-operations'))
        checks['capture_unprivileged_wrapper'] = 'from project_cbm.screenshot import main' in text('usr/bin/pcbm-screenshot')
        checks['capture_no_alias_or_menu_action'] = not (root/'usr/bin/screenshot').exists() and 'pcbm-screenshot' not in text('usr/bin/pcbm-menu')
        checks['capture_no_shipped_private_pngs'] = not (root/'home/pcbm/screenshots').exists() and not any((root/'home/pcbm/content/screenshots').iterdir())
        checks['usb_browser_hides_tags'] = 'PCBM_UI_HIDE_TAGS=true' in browse
        checks['guided_import_hides_tags'] = 'PCBM_UI_HIDE_TAGS=true' in menu
    if (root/'usr/bin/pcbm-online-session').exists():
        online = text('usr/share/project-cbm/runtime/project_cbm/online_backend.py')
        coordinator = text('usr/share/project-cbm/runtime/project_cbm/online_session.py')
        online_ui = text('usr/bin/pcbm-online')
        checks['online_explicit_content_entry'] = 'Online Library' in hub and '/usr/bin/pcbm-online' in hub
        checks['online_attribution_and_connection_notice'] = 'Powered by Assembly64' in online_ui and 'Internet connection required' in online_ui
        checks['online_registered_identity_https'] = "'https://hackerswithstyle.se/leet/', 'cbm'" in online and 'Project-CBM/1.2-Online-Library' in online
        checks['online_shared_ingestion_unprivileged'] = 'ingestion.plan(' in coordinator and 'ingestion.save(' in coordinator and 'pcbm-online' not in text('etc/sudoers.d/pcbm-operations')
        checks['online_no_bundled_payload_or_private_state'] = not list((root/'home/pcbm/content').rglob('Downloaded')) and not (root/'home/pcbm/.local/state/project-cbm/ingestion').exists()
        checks['online_explicit_review_before_save'] = online_ui.index('rpc prepare') < online_ui.index('request save') and 'Save to Library' in online_ui
        checks['import_return_to_source'] = 'stage=source; offset=0; continue' in menu and 'End Import / Release USB' in menu
        shots=root/'home/pcbm/content/screenshots'
        checks['screenshot_private_shared_directory'] = shots.stat().st_uid==1000 and shots.stat().st_mode & 0o777 == 0o700
        checks['screenshot_content_share_default'] = "'/content/screenshots/'" in text('usr/share/project-cbm/runtime/project_cbm/screenshot.py')
        checks['reusable_breadcrumbs'] = 'pcbm_ui_backtitle' in text('usr/share/project-cbm-menu/pcbm-ui.sh') and 'pcbm_ui_backtitle' in text('usr/bin/pcbm-dialog-lib.sh')
    result['result'] = 'PASS' if all(checks.values()) else 'FAIL'
    result['scope'] = '1.2 exact installed image; physical USB/exFAT/Pi behavior UNTESTED'
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('image', 'lock', 'kit', 'output'): p.add_argument(name, type=Path)
    a = p.parse_args()
    lock = read_json(a.lock)
    record = read_json(a.kit / lock['components']['menu']['build_record']['path'])
    loop = subprocess.check_output(['losetup','--read-only','--find','--show','--partscan',str(a.image)], text=True).strip()
    mounted = []
    try:
        with tempfile.TemporaryDirectory(dir=a.output.parent) as directory:
            root = Path(directory)/'root'; boot = Path(directory)/'boot'
            root.mkdir(); boot.mkdir()
            try:
                for device, path, flags in ((loop+'p2',root,'ro,noload'),(loop+'p1',boot,'ro')):
                    subprocess.run(['mount','-o',flags,device,str(path)],check=True); mounted.append(path)
                result = inspect(root,boot,record,a.kit)
            finally:
                for path in reversed(mounted): subprocess.run(['umount',str(path)],check=True)
    finally:
        subprocess.run(['losetup','--detach',loop],check=True)
    with a.output.open('x') as stream: json.dump(result,stream,indent=2); stream.write('\n')
    print(json.dumps({'result':result['result'],'checks':len(result['checks']),
                      'failed':[k for k,v in result['checks'].items() if not v]}))
    if result['result'] != 'PASS': raise SystemExit(1)


if __name__ == '__main__': main()
