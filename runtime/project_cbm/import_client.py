"""Unprivileged, bounded broker client. Reconstruct result fields, never raw errors."""
import json
import re
import subprocess
import sys
from .importer import validate_request
from .data import loads


def main():
    try:
        if len(sys.argv)!=1:raise ValueError('arguments')
        request=validate_request(sys.stdin.buffer.read(4097))
        p=subprocess.run(['/usr/bin/sudo','-n','--','/usr/libexec/pcbm-import-root'],
                         input=json.dumps(request),text=True,capture_output=True,timeout=600,
                         env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
        if p.returncode or len(p.stdout)>8192:raise ValueError('failed')
        reply=loads(p.stdout)
        if reply.get('schema_version')!=1 or reply.get('status')!='ok':raise ValueError('result')
        if request['operation']=='list':
            rows=reply['devices']
            if not isinstance(rows,list) or len(rows)>16:raise ValueError('devices')
            devices=[]
            for row in rows:
                if not re.fullmatch('[0-9a-f]{32}',row['token']) or not isinstance(row['label'],str) or not row['label'].isprintable() or len(row['label'])>128:raise ValueError('device')
                devices.append({'token':row['token'],'label':row['label']})
            answer={'schema_version':1,'status':'ok','devices':devices}
        else:
            if any(type(reply.get(k)) is not int or reply[k]<0 for k in ('copied','skipped','bytes')):raise ValueError('counts')
            answer={'schema_version':1,'status':'ok',**{k:reply[k] for k in ('copied','skipped','bytes')}}
        print(json.dumps(answer,sort_keys=True));return 0
    except (OSError,ValueError,TypeError,KeyError,subprocess.SubprocessError):
        print(json.dumps({'schema_version':1,'status':'failed','message':'Import unavailable or incomplete. Check setup, USB media, free space and diagnostics. Existing files are preserved.'}));return 2
