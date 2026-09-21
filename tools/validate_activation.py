"""Read-only schema-4 candidate checks; never executes appliance code."""
import json, stat
from pathlib import Path


def inspect(root,lock,check,digest):
    single_user=lock['product']['candidate'] in ('private-engineering-rc2','private-engineering-rc3','private-engineering-rc4','release')
    account='pcbm' if single_user else 'pi'
    content='home/pcbm/content' if single_user else 'home/pi/pcbm'
    repo=Path(__file__).resolve().parents[1]
    def text(name):return (root/name).read_text()
    def trusted(name,mode=None):
        p=root/name;s=p.lstat()
        return not p.is_symlink() and s.st_uid==0 and not s.st_mode&0o022 and (mode is None or stat.S_IMODE(s.st_mode)==mode)
    p=json.loads(text('etc/project-cbm/configuration-policy.json'))
    check('activation_not_falsely_ready',p=={'schema_version':1,'owner_user':'pcbm','appliance_user':account,'system_ready':False,'network_ready':True,'ready_services':['ssh','sharing','modem','discovery']})
    check('no_setup_completion',not (root/'var/lib/project-cbm/setup/state.json').exists() and not (root/'var/lib/project-cbm/setup/status.json').exists())
    users={r.split(':')[0]:r.split(':') for r in text('etc/passwd').splitlines()}
    check('owner_account_identity',users['pcbm'][2]==('1000' if single_user else '1001') and users['pcbm'][5:]==['/home/pcbm','/bin/bash'])
    if single_user:check('no_legacy_runtime_account','pi' not in users)
    shadow={r.split(':')[0]:r.split(':')[1] for r in text('etc/shadow').splitlines()}
    check('no_preset_owner_password',shadow.get('pcbm')=='!')
    groups={r.split(':')[0]:r.split(':')[-1].split(',') for r in text('etc/group').splitlines()}
    check('owner_authenticated_sudo_group','pcbm' in groups['sudo'] and 'pi' not in groups['sudo'])
    check('normal_user_helper_group',account in groups['pcbm-operators'])
    check('helper_policy_exact',text('etc/sudoers.d/pcbm-operations')==(repo/'runtime/config/sudoers.example').read_text())
    check('helper_policy_permissions',trusted('etc/sudoers.d/pcbm-operations',0o440))
    for name in ['pcbm-config-root','pcbm-import-root']:
        check('trusted_'+name,trusted('usr/libexec/'+name,0o755))
    check('no_generic_passwordless_grants',all('NOPASSWD: ALL' not in p.read_text() for p in (root/'etc/sudoers.d').iterdir() if p.is_file()))
    check('NM_offline_initial_state','NetworkingEnabled=false' in text('var/lib/NetworkManager/NetworkManager.state') and 'WirelessEnabled=false' in text('var/lib/NetworkManager/NetworkManager.state'))
    check('no_enrolled_wifi',not list((root/'etc/NetworkManager/system-connections').glob('*')))
    check('no_samba_databases',not list((root/'var/lib/samba').rglob('*.tdb')) and not list((root/'var/lib/samba').rglob('*.ldb')))
    check('ssh_owner_only','AllowUsers pcbm' in text('etc/ssh/sshd_config.d/20-project-cbm.conf') and 'PermitRootLogin no' in text('etc/ssh/sshd_config.d/20-project-cbm.conf'))
    optional=['ssh.service','ssh.socket','smbd.service','nmbd.service','samba-ad-dc.service','tcpser.service','avahi-daemon.service','avahi-daemon.socket']
    enabled={p.name for p in (root/'etc/systemd/system').glob('*.wants/*')}
    check('optional_services_initially_disabled',not set(optional)&enabled)
    check('network_manager_enabled','NetworkManager.service' in enabled)
    presets=text('etc/systemd/system-preset/00-project-cbm.preset')
    check('first_boot_presets_keep_services_off',all('disable '+u+'\n' in presets for u in optional))
    check('modem_typed_adapter','ExecStart=/usr/bin/pcbm-modem' in text('usr/lib/systemd/system/tcpser.service'))
    check('modem_default_loopback_settings',json.loads(text('etc/project-cbm/modem.json'))=={'schema_version':1,'port':25232,'baud':2400})
    for name in ['pcbm-info','pcbm-config-operation','pcbm-import-operation','pcbm-setup-state','pcbm-start-profile','pcbm-admin','pcbm-wifi-list']:
        p=root/'usr/bin'/name
        check('runtime_entry_'+name,p.is_symlink() and str(p.readlink())=='../share/project-cbm/runtime/bin/'+name)
    session=text('usr/libexec/project-cbm/pcbm-console-session')
    check('first_run_before_menu',session.index('/usr/bin/pcbm-first-run')<session.index('/usr/bin/pcbm-menu'))
    check('one_direct_boot_attempt',session.count('/usr/bin/pcbm-run-vice')==1 and 'pcbm-start-profile' in session)
    check('SID_autostart_refused','PSID/RSID playback awaits' in text('usr/bin/pcbm-run-vice'))
    check('system_information_structured','pcbm-info' in text('usr/bin/pcbm-system-info'))
    for name in ['pcbm-config','pcbm-first-run','pcbm-system-info']:
        check('menu_entry_'+name,(root/'usr/bin'/name).is_file())
    optional=lock['optional_software']
    pin=json.loads((repo/'build/optional/sid-wizard.json').read_text())
    template=root/'usr/share/project-cbm/applications/sid-wizard/SID-Wizard-1.97.d64'
    manifest=json.loads(text('usr/share/project-cbm/applications/sid-wizard/manifest.json'))
    expected=next(e['sha256'] for e in manifest['files'] if e['name']=='SID-Wizard-1.97.d64')
    check('sid_wizard_exact_core',digest(template)==expected and manifest['source_sha256']==optional['sid_wizard']['source']['sha256'] and manifest['license']=='LicenseRef-Hermit-WTF')
    working=list((root/content).rglob('*1.97*.d64'))
    check('sid_wizard_working_disk',len(working)==1 and digest(working[0])==digest(template) and working[0].stat().st_uid==1000 and template.stat().st_uid==0)
    if 'striketerm' in optional:
        entry=optional['striketerm'];base='usr/share/project-cbm/applications/striketerm/StrikeTerm-2014-Final.d64'
        check('striketerm_exact_private_input',digest(root/base)==entry['artifact']['sha256'])
        p=root/content/'programs/c64/Communications/StrikeTerm/StrikeTerm-2014-Final.d64'
        check('striketerm_working_copy',digest(p)==entry['artifact']['sha256'] and p.stat().st_uid==1000)
        notice=json.loads(text('usr/share/doc/project-cbm-striketerm/PRIVATE-ADMISSION.json'))
        check('striketerm_public_gate_pending',notice['public_release_rights']=='PUBLIC-RELEASE-RIGHTS-GATE-PENDING')
    check('no_reference_SID_payloads',not list((root/content).rglob('*.sid')))
