#!/usr/bin/env python3
"""Additional read-only POC4 activation footprint and integration checks."""
import argparse,hashlib,json,os,subprocess,tempfile
from pathlib import Path


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('image',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
 def output(*args):return subprocess.check_output(args,text=True).strip()
 loop=output('losetup','--read-only','--find','--show','--partscan',str(a.image))
 checks={};record={'scope':'read-only offline; no executable from target is run','checks':checks}
 try:
  with tempfile.TemporaryDirectory(dir=a.output.parent) as tmp:
   root=Path(tmp);subprocess.run(['mount','-o','ro,noload',loop+'p2',str(root)],check=True)
   try:
    def text(p):return (root/p).read_text()
    single_user=json.loads(text('usr/share/project-cbm/identity.json'))['product']['candidate'] in ('private-engineering-rc2','private-engineering-rc3')
    content='home/pcbm/content' if single_user else 'home/pi/pcbm'
    rows={}
    for stanza in text('var/lib/dpkg/status').split('\n\n'):
     row={line.split(': ',1)[0]:line.split(': ',1)[1] for line in stanza.splitlines() if ': ' in line and not line.startswith(' ')}
     if row.get('Status')=='install ok installed':rows[row['Package']]=row
    for name in ('apparmor','network-manager','samba','openssh-server','avahi-daemon','sudo','raspi-config','locales','keyboard-configuration','console-setup','cloud-guest-utils'):
     checks['installed_'+name]=name in rows
    record['activation_packages']={name:rows[name]['Version'] for name in rows if 'installed_'+name in checks}
    checks['tmp_mode_1777']=(root/'tmp').stat().st_mode&0o7777==0o1777
    checks['runtime_dirs_recreated']=text('usr/lib/tmpfiles.d/project-cbm.conf')=='d /run/project-cbm 0755 root root -\nd /run/project-cbm/import 0755 root root -\nd /run/project-cbm/import/source 0755 root root -\n'
    checks['authenticated_owner_sudo']=any(line.strip().startswith('%sudo') and 'ALL=(ALL:ALL) ALL' in line and 'NOPASSWD' not in line for line in text('etc/sudoers').splitlines())
    checks['only_expected_local_accounts']=all(line.split(':')[0] in (('pcbm','nobody') if single_user else ('pi','pcbm','nobody')) for line in text('etc/passwd').splitlines() if int(line.split(':')[2])>=1000)
    samba=text('etc/samba/smb.conf')
    checks['samba_only_content_share']=samba.count('path =')==1 and 'path = /'+content in samba and 'guest ok = no' in samba
    checks['about_view_present']='ABOUT) show_about' in text('usr/bin/pcbm-config') and 'def about(' in text('usr/libexec/project-cbm-menu/pcbm_config_bridge.py')
    checks['firstboot_payloads_present']=all((root/name).is_file() for name in ('usr/libexec/project-cbm/first_boot.py','usr/bin/pcbm-first-run','usr/bin/pcbm-setup-state'))
    checks['admin_auth_paths']=all(token in text('usr/share/project-cbm/runtime/project_cbm/admin.py') for token in ('su','sudo','raspi-config'))
    checks['public_rights_gate_retained']=json.loads(text('usr/share/doc/project-cbm-striketerm/PRIVATE-ADMISSION.json'))['public_release_rights']=='PUBLIC-RELEASE-RIGHTS-GATE-PENDING'
    record['optional_application_bytes']={}
    for name in ('sid-wizard','striketerm'):
     paths=[root/'usr/share/project-cbm/applications'/name,root/'usr/share/doc'/('project-cbm-'+name)]
     record['optional_application_bytes'][name+'_system']=sum(f.stat().st_size for d in paths for f in d.rglob('*') if f.is_file() and not f.is_symlink())
    record['optional_application_bytes']['fresh_user_working_disks']=sum(f.stat().st_size for f in (root/content).rglob('*.d64') if f.name in ('SID-Wizard-1.97.d64','StrikeTerm-2014-Final.d64'))
    record['installed_package_size_sum_bytes']=sum(int(r.get('Installed-Size','0'))*1024 for r in rows.values())
    record['installed_package_count']=len(rows)
   finally:subprocess.run(['umount',str(root)],check=True)
 finally:subprocess.run(['losetup','--detach',loop],check=True)
 record['result']='PASS' if all(checks.values()) else 'FAIL'
 a.output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'result':record['result'],'checks':len(checks),'failed':[k for k,v in checks.items() if not v]},sort_keys=True))
 if record['result']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
