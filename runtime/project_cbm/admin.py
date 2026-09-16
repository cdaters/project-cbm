"""Authenticated owner administration, separate from the passwordless appliance API."""
import argparse
import os
import subprocess
import sys
from .config_backend import policy


def command(action, owner=None):
    if action=='terminal':return ['/bin/su','--login',owner]
    if action=='owner':return ['/bin/su','--login',owner]
    if action=='raspi-config':return ['/bin/su','--login',owner,'--command','sudo -k -- /usr/bin/raspi-config']
    raise ValueError('action')


def main(argv=None):
    parser=argparse.ArgumentParser(description='Project CBM terminal and authenticated owner administration')
    parser.add_argument('action',choices=['terminal','owner','raspi-config']);args=parser.parse_args(argv)
    if os.geteuid()==0:
        print('Use this entry from the normal Project CBM user.',file=sys.stderr);return 2
    try:
        owner=None
        if args.action in ('terminal','owner','raspi-config'):
            p=policy()
            if not p['system_ready']:raise ValueError('not_initialized')
            owner=p['owner_user']
        print('Type exit to return to Project CBM. Advanced changes may affect qualification; restore settings or reflash if needed.')
        return subprocess.call(command(args.action,owner),env={**os.environ,'HISTFILE':'/dev/null'})
    except (OSError,ValueError,TypeError):
        print('Owner administration awaits first-boot account initialization. Use your existing authenticated Linux login if already configured.',file=sys.stderr)
        return 2
