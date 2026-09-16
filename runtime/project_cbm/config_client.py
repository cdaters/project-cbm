"""Unprivileged JSON client. Secrets travel through pipes, never argv or result text."""
import argparse
import json
import subprocess
import sys
from .configuration import decode, result, FIELDS


def submit(request, runner=subprocess.run):
    from .configuration import validate
    validate(request)
    try:
        p=runner(['/usr/bin/sudo','-n','--','/usr/libexec/pcbm-config-root'],input=json.dumps(request),
                 text=True,capture_output=True,timeout=75,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
        from .data import loads
        reply=loads(p.stdout)
        if not isinstance(reply,dict) or set(reply)!={'format','schema_version','status','message'} or reply['format']!='project-cbm.config-result' or type(reply['schema_version']) is not int or reply['schema_version']!=1:
            raise ValueError('result')
        # Reconstruct all messages locally. A backend/stderr cannot inject secrets into UI.
        if (p.returncode == 0) != (reply['status'] in ('ok','saved_pending','saved_restart')):raise ValueError('status_mismatch')
        return result(reply['status'])
    except (OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError):
        return result('pending' if 'p' in locals() and p.returncode else 'unavailable')


def main(argv=None):
    parser=argparse.ArgumentParser(description='Project CBM validated configuration request via stdin')
    parser.add_argument('--validate',action='store_true')
    parser.add_argument('--ready',choices=FIELDS)
    args=parser.parse_args(argv)
    if args.ready:
        try:
            from .config_backend import policy
            p=policy()
            ready=p['system_ready'] and (p['network_ready'] if args.ready in ('network','wifi-country','wifi-enroll') else True)
            return 0 if ready else 2
        except (OSError,ValueError,TypeError):return 2
    try:
        request=decode(sys.stdin.buffer.read(4097))
        answer=result('ok') if args.validate else submit(request)
    except (ValueError,TypeError):answer=result('invalid')
    print(json.dumps(answer,sort_keys=True))
    return 0 if answer['status'] in ('ok','saved_pending','saved_restart') else 2
