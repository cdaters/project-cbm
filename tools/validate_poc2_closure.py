#!/usr/bin/env python3
"""Additional read-only POC filesystem, unit and ELF-closure verification on Linux."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile


def output(*args):return subprocess.check_output(args,text=True,stderr=subprocess.STDOUT)


def inspect(root):
    def resolve(path):
        for _ in range(20):
            if not path.is_symlink():return path
            link=path.readlink();path=root/str(link).lstrip('/') if link.is_absolute() else path.parent/link
        raise ValueError('link cycle')
    paths=[root/'usr/lib/aarch64-linux-gnu',root/'usr/lib/aarch64-linux-gnu/pulseaudio']
    todo=[root/'usr/bin/x64sc']+[paths[0]/name for name in ['libSDL2-2.0.so.0','libGL.so.1','libGLX_mesa.so.0','libEGL_mesa.so.0','dri/vc4_dri.so']]
    helper=root/'usr/libexec/project-cbm-vice/drm-state'
    if helper.is_file():todo.append(helper)
    for relative in ('usr/lib/aarch64-linux-gnu/libSDL2_image-2.0.so.0','usr/bin/mc','usr/bin/alsamixer'):
        if (root/relative).exists():todo.append(root/relative)
    seen=set();missing=set()
    while todo:
        path=resolve(todo.pop())
        if str(path) in seen:continue
        seen.add(str(path))
        if not path.is_file():missing.add(str(path.relative_to(root)));continue
        dynamic=output('readelf','-d',str(path))
        for name in re.findall(r'\(NEEDED\).*?\[(.*?)\]',dynamic):
            found=next((resolve(d/name) for d in [path.parent,*paths] if resolve(d/name).is_file()),None)
            if found is None:missing.add(name)
            else:todo.append(found)
    units=output('systemd-analyze','--root='+str(root),'verify','pcbm-first-boot.service','getty@tty1.service','getty@tty2.service')
    return {'elf_objects_checked':len(seen),'missing_dependencies':sorted(missing),'units':'PASS','unit_output':units,'result':'PASS' if not missing else 'FAIL','scope':'read-only static; no target executable or physical Pi test'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('image',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args()
    loop=output('losetup','--read-only','--find','--show','--partscan',str(args.image)).strip()
    try:
        fs={'ext4':output('e2fsck','-f','-n',loop+'p2'),'FAT':output('fsck.fat','-n',loop+'p1')}
        with tempfile.TemporaryDirectory(dir=args.output.parent) as temp:
            root=Path(temp);subprocess.run(['mount','-o','ro,noload',loop+'p2',str(root)],check=True)
            try:record=inspect(root)
            finally:subprocess.run(['umount',str(root)],check=True)
        record['filesystem_checks']=fs;args.output.write_text(json.dumps(record,indent=2)+'\n')
        if record['result']!='PASS':raise SystemExit('missing ELF dependency')
        print('Filesystem/unit/ELF closure PASS:',record['elf_objects_checked'],'objects; no Pi runtime claim')
    finally:subprocess.run(['losetup','--detach',loop],check=True)


if __name__=='__main__':main()
