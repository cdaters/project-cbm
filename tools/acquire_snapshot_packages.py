#!/usr/bin/env python3
"""Retain exact missing Debian binary versions via official snapshot API.

No package install/upgrade or APT trust-setting change. Preserve API responses,
verify published snapshot file identities, then record SHA-256. HTTPS/API identity
is acquisition evidence, not a claim of independently verified old Release signatures.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import quote
from urllib.request import urlopen

root=Path(sys.argv[1]).resolve(strict=True)
results=json.loads((root/'results.json').read_text())
recovered=[]
for item in results:
    if item['status']==0: continue
    package=item['package'].split(':')[0];version=item['version']
    directory=root/item['directory']
    url='https://snapshot.debian.org/mr/binary/'+quote(package,safe='')+'/'+quote(version,safe='')+'/binfiles?fileinfo=1'
    raw=urlopen(url,timeout=120).read();(directory/'snapshot-api.json').write_bytes(raw)
    metadata=json.loads(raw)
    choices=[r for r in metadata['result'] if r['architecture'] in ['arm64','all']]
    if len(choices)!=1: raise SystemExit('ambiguous snapshot binary '+package)
    identity=choices[0]['hash']
    info=metadata['fileinfo'][identity][0]
    target=directory/info['name']
    with urlopen('https://snapshot.debian.org/file/'+identity,timeout=120) as response, target.open('wb') as stream:
        while block:=response.read(1024*1024): stream.write(block)
    with target.open('rb') as stream:
        if hashlib.file_digest(stream,'sha1').hexdigest()!=identity: raise SystemExit('snapshot hash mismatch')
    expected_arch=choices[0]['architecture']
    actual=subprocess.check_output(['dpkg-deb','-f',str(target),'Package','Version','Architecture'],text=True)
    expected={'Package':package,'Version':version,'Architecture':expected_arch}
    if dict(line.split(': ',1) for line in actual.splitlines())!=expected: raise SystemExit('snapshot control mismatch')
    with target.open('rb') as stream: sha=hashlib.file_digest(stream,'sha256').hexdigest()
    recovered.append({'package':item['package'],'version':version,'filename':str(target.relative_to(root)),
                      'source':'https://snapshot.debian.org/file/'+identity,'sha256':sha,'size_bytes':target.stat().st_size})
    (root/'snapshot-recovered.json').write_text(json.dumps(recovered,indent=2)+'\n')
    print('Recovered exact snapshot binary',package,version,flush=True)
if len(recovered)!=sum(r['status']!=0 for r in results):raise SystemExit('incomplete snapshot recovery')
