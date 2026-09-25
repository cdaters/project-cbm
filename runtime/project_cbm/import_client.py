"""Unprivileged, bounded broker client. Reconstruct result fields, never raw errors."""
import json
import re
import subprocess
import sys
from .importer import validate_request
from .data import loads

ERRORS = {'access_denied', 'space', 'limit', 'depth', 'entries', 'copy_failed',
          'mount_failed', 'unmount_failed', 'unavailable'}


def result(request, raw, returncode):
    """Allowlisted broker contract, including structured nonzero-exit results."""
    if len(raw)>8192:raise ValueError('size')
    reply=loads(raw)
    if not isinstance(reply,dict) or type(reply.get('schema_version')) is not int or reply['schema_version']!=1:
        raise ValueError('schema')
    released=reply.get('source_unmounted')
    if released is not None and type(released) is not bool:raise ValueError('cleanup')
    if reply.get('status')=='failed':
        code=reply.get('error')
        if returncode!=2 or not isinstance(code,str) or code not in ERRORS:raise ValueError('failure')
        if code=='unmount_failed' and released is True:raise ValueError('cleanup')
        return {'schema_version':1,'status':'failed','error':code,'source_unmounted':released}
    if returncode!=0 or reply.get('status')!='ok':raise ValueError('status')
    if request['operation']=='list':
        rows=reply['devices']
        if not isinstance(rows,list) or len(rows)>16:raise ValueError('devices')
        devices=[]
        for row in rows:
            if (not isinstance(row,dict) or not isinstance(row.get('token'),str)
                    or not re.fullmatch('[0-9a-f]{32}',row['token'])
                    or not isinstance(row.get('label'),str) or not row['label'].isprintable()
                    or len(row['label'])>128):raise ValueError('device')
            devices.append({'token':row['token'],'label':row['label']})
        return {'schema_version':1,'status':'ok','devices':devices}
    if released is not True:raise ValueError('cleanup_unconfirmed')
    answer={'schema_version':1,'status':'ok','source_unmounted':True}
    for key in ('copied','skipped','bytes','ignored_metadata'):
        value=reply.get(key,0) if key=='ignored_metadata' else reply.get(key)
        if type(value) is not int or value<0:raise ValueError('counts')
        answer[key]=value
    return answer


def main():
    try:
        if len(sys.argv)!=1:raise ValueError('arguments')
        request=validate_request(sys.stdin.buffer.read(4097))
        p=subprocess.run(['/usr/bin/sudo','-n','--','/usr/libexec/pcbm-import-root'],
                         input=json.dumps(request),text=True,capture_output=True,timeout=600,
                         env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
        answer=result(request,p.stdout,p.returncode)
        print(json.dumps(answer,sort_keys=True));return 0 if answer['status']=='ok' else 2
    except (OSError,ValueError,TypeError,KeyError,subprocess.SubprocessError):
        print(json.dumps({'schema_version':1,'status':'failed','error':'unavailable','source_unmounted':None,'message':'Import unavailable or incomplete. Check setup, USB media, free space and diagnostics. Existing files are preserved.'}));return 2
