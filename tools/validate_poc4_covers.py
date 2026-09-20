#!/usr/bin/env python3
"""Read-only checks for frozen Covers, standard utilities and bounded UI changes."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
from build_contracts import read_json


def inspect(root,record,kit):
    checks={};cover=record['covers']
    def same(relative,descriptor):
        p=root/relative
        return p.is_file() and not p.is_symlink() and p.stat().st_size==descriptor['size_bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==descriptor['sha256']
    manifest=read_json(kit/cover['manifest']['path'])
    for item in manifest['files']:
        checks['asset_'+item['cover_identity']]=same('usr/share/project-cbm-menu/'+item['path'],item)
    for key,path in {'manifest':'usr/share/doc/project-cbm-menu/cover-artwork.json','renderer':'usr/libexec/project-cbm-menu/pcbm_cover_view.py','launcher':'usr/bin/pcbm-run-vice','wrapper':'usr/bin/pcbm-cover','registry':'usr/share/project-cbm/runtime/data/profiles.json'}.items():
        checks['exact_'+key]=same(path,cover[key])
    def text(p):return (root/p).read_text()
    launcher=text('usr/bin/pcbm-run-vice');wrapper=text('usr/bin/pcbm-cover');renderer=text('usr/libexec/project-cbm-menu/pcbm_cover_view.py')
    checks['bounded_shared_transition']='--kill-after=0.5s 2s /usr/bin/pcbm-cover --profile "$profile"' in launcher and '|| true' in launcher
    checks['no_root_renderer']='EUID != 0' in wrapper and 'os.geteuid() == 0' in renderer
    checks['desktop_aspect_fit']='0x1001' in renderer and 'scale = min(' in renderer and 'DURATION_SECONDS = 0.75' in renderer
    checks['no_framebuffer_or_boot_commands']=all(t not in wrapper+renderer for t in ('fbi ','fbset','convert ','chvt','sudo ','/dev/fb0','systemctl'))
    checks['shared_profile_mapping']='pcbm-profiles resolve "$2" --cover' in wrapper and 'RANDOM' not in wrapper
    files = text('usr/bin/pcbm-files') if (root/'usr/bin/pcbm-files').is_file() else ''
    menu = text('usr/bin/pcbm-menu')
    checks['mc_normal_user'] = ('\n          mc "$PCBM_CONTENT_BASE" "$PCBM_CONTENT_BASE"\n' in menu or
                                '"$SCRIPT_DIR/pcbm-files"' in menu and '/usr/bin/mc /home/pcbm/content /home/pcbm' in files) and 'sudo' not in files and 'sudo mc' not in menu
    checks['mixer_unprivileged_no_global_save']='/usr/bin/alsamixer' in text('usr/bin/pcbm-config') and 'alsactl' not in text('usr/bin/pcbm-config') and 'sudo alsamixer' not in text('usr/bin/pcbm-config')
    checks['import_destination_feedback']=any('Destination: '+base+'/$category/$family/Imported' in text('usr/bin/pcbm-import') for base in ('/home/pi/pcbm','/home/pcbm/content'))
    rows={}
    for stanza in text('var/lib/dpkg/status').split('\n\n'):
        row=dict(l.split(': ',1) for l in stanza.splitlines() if ': ' in l and not l.startswith(' '))
        if row.get('Status')=='install ok installed':rows[row['Package']]=row
    for name,entry in record['utilities'].items():
        checks['package_'+name]=rows.get(name,{}).get('Version')==entry['metadata']['Version']
    checks['SDL_image_dependency']='libsdl2-image-2.0-0' in rows
    checks['SDL_runtime_dependency']='libsdl2-2.0-0' in rows
    checks['standard_tools_present']=all((root/p).is_file() for p in ('usr/bin/mc','usr/bin/alsamixer','usr/bin/timeout'))
    return {'checks':checks,'result':'PASS' if all(checks.values()) else 'FAIL','scope':'offline byte/config checks; fixture/native lifecycle tests are separate; physical KMS/VT UNTESTED',
        'cover_bytes':sum(i['size_bytes'] for i in manifest['files']),
        'utility_packages':{n:{'version':rows.get(n,{}).get('Version'),'installed_size_bytes':int(rows.get(n,{}).get('Installed-Size',0))*1024} for n in record['utilities']}}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('image',type=Path);p.add_argument('lock',type=Path);p.add_argument('kit',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    lock=read_json(a.lock);record=read_json(a.kit/lock['components']['menu']['build_record']['path'])
    loop=subprocess.check_output(['losetup','--read-only','--find','--show','--partscan',str(a.image)],text=True).strip()
    try:
        with tempfile.TemporaryDirectory(dir=a.output.parent) as tmp:
            root=Path(tmp);subprocess.run(['mount','-o','ro,noload',loop+'p2',str(root)],check=True)
            try:result=inspect(root,record,a.kit)
            finally:subprocess.run(['umount',str(root)],check=True)
    finally:subprocess.run(['losetup','--detach',loop],check=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'result':result['result'],'checks':len(result['checks']),'failed':[k for k,v in result['checks'].items() if not v]}))
    if result['result']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
