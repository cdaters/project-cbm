#!/usr/bin/env python3
"""Export the actual-image validator's package TSV as a portable image-bound manifest."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def manifest(raw, image_sha256):
    if not re.fullmatch('[0-9a-f]{64}',image_sha256):raise ValueError('exact image SHA-256 required')
    rows=[];seen=set()
    for line in raw.decode().splitlines():
        if not line:continue
        fields=line.split('\t')
        if len(fields)!=5:raise ValueError('expected validator package/version/architecture/size/status TSV')
        name,version,arch,size,status=fields
        if status!='installed':continue
        if not re.fullmatch('[a-z0-9][a-z0-9+.:_-]*',name) or not re.fullmatch('[a-z0-9-]+',arch) or not re.fullmatch('[A-Za-z0-9.+:~_-]+',version):raise ValueError('package metadata')
        if (name,arch) in seen:raise ValueError('duplicate installed package')
        seen.add((name,arch));size=int(size)
        if size<0:raise ValueError('negative installed size')
        rows.append({'name':name,'version':version,'architecture':arch,'installed_size_kib':size})
    if not rows:raise ValueError('empty installed manifest')
    return {'format':'project-cbm.installed-package-manifest','schema_version':1,
            'image_sha256':image_sha256,'inventory_sha256':hashlib.sha256(raw).hexdigest(),
            'package_count':len(rows),'packages':sorted(rows,key=lambda r:(r['name'],r['architecture']))}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('inventory',type=Path);p.add_argument('--image-sha256',required=True);p.add_argument('output',type=Path);a=p.parse_args()
    value=manifest(a.inventory.read_bytes(),a.image_sha256)
    with a.output.open('x') as f:json.dump(value,f,indent=2);f.write('\n')
    print('Exported',value['package_count'],'installed identities; no package acquisition or execution')


if __name__=='__main__':main()
