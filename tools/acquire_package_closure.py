#!/usr/bin/env python3
"""Resolve exact binary/source package bytes in Linux; never upgrades installed state.

Each result retains a log and exit code. Any missing version leaves closure FAILED;
no fabricated checksums or substitution with a newer version. Review results before
freezing the lock. Run after authenticated APT metadata is retained.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rootfs',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--kind',choices=['binary','source'],required=True)
    args=parser.parse_args()
    prefix=['chroot',str(args.rootfs)] if args.rootfs else []
    fmt='${binary:Package}\t${Version}\t${source:Package}\t${source:Version}\n'
    inventory=subprocess.check_output(prefix+['dpkg-query','-W','-f='+fmt],text=True)
    wanted=set()
    for line in inventory.splitlines():
        binary,version,source,sv=line.split('\t')
        if binary.startswith('project-cbm-'): continue  # Retained CBM source packages.
        wanted.add((binary,version) if args.kind=='binary' else (source,sv))
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'inventory.tsv').write_text(inventory)
    def acquire(pair):
        name,version=pair
        key=hashlib.sha256((name+'='+version).encode()).hexdigest()
        directory=args.output/key;directory.mkdir(exist_ok=True)
        guestdir=str(directory.relative_to(args.rootfs)) if args.rootfs else str(directory)
        if args.rootfs: guestdir='/'+guestdir
        command=['apt-get','download',name+'='+version] if args.kind=='binary' else ['apt-get','source','--only-source','--download-only',name+'='+version]
        # cwd must be inside the selected package namespace without shell interpolation.
        if args.rootfs:
            command=prefix+['/bin/sh','-c','cd "$1" && shift && exec "$@"','acquire',guestdir,*command]
        with (directory/'acquisition.log').open('w') as log:
            result=subprocess.run(command,cwd=directory,stdout=log,stderr=subprocess.STDOUT)
        print(name,version,'PASS' if result.returncode==0 else 'FAILED',flush=True)
        return {'package':name,'version':version,'directory':key,'status':result.returncode}
    with ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(acquire,sorted(wanted)))
    (args.output/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    if any(r['status'] for r in results): raise SystemExit('Exact package closure incomplete; review failed acquisitions')


if __name__=='__main__':main()
