#!/usr/bin/env python3
"""Recover exact Debian source versions missing from current indexes; no upgrades."""
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import quote
from urllib.request import urlopen

root=Path(sys.argv[1]).resolve(strict=True)
results=json.loads((root/'results.json').read_text())
recovered=[]
for item in results:
    if item['status']==0: continue
    package=item['package'];version=item['version'];directory=root/item['directory']
    url='https://snapshot.debian.org/mr/package/'+quote(package,safe='')+'/'+quote(version,safe='')+'/srcfiles?fileinfo=1'
    raw=urlopen(url,timeout=120).read();(directory/'snapshot-api.json').write_bytes(raw)
    metadata=json.loads(raw);files=[]
    for entry in metadata['result']:
        identity=entry['hash'];info=metadata['fileinfo'][identity][0]
        if Path(info['name']).name!=info['name']:raise SystemExit('unsafe archive filename')
        target=directory/info['name']
        if not target.exists():
            with urlopen('https://snapshot.debian.org/file/'+identity,timeout=120) as response,target.open('wb') as stream:
                while chunk:=response.read(1024*1024):stream.write(chunk)
        with target.open('rb') as stream:
            if hashlib.file_digest(stream,'sha1').hexdigest()!=identity:raise SystemExit('snapshot source hash mismatch')
        with target.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
        files.append({'path':str(target.relative_to(root)),'sha256':digest,'size_bytes':target.stat().st_size,'origin':'https://snapshot.debian.org/file/'+identity})
    dscs=list(directory.glob('*.dsc'))
    if len(dscs)!=1:raise SystemExit('ambiguous source descriptor')
    text=dscs[0].read_text()
    if '\nSource: '+package+'\n' not in '\n'+text or '\nVersion: '+version+'\n' not in '\n'+text:
        raise SystemExit('source descriptor identity mismatch')
    recovered.append({'package':package,'version':version,'files':files})
    (root/'snapshot-recovered.json').write_text(json.dumps(recovered,indent=2)+'\n')
    print('Recovered exact snapshot source',package,version,flush=True)
