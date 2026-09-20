"""Typed TCPser adapter. Both local modem listeners bind only to loopback."""
import os
from pathlib import Path
import sys
from .data import read_json
from .configuration import validate
from .config_backend import trusted


def arguments(settings):
    if not isinstance(settings,dict) or set(settings)!={'schema_version','port','baud'} or type(settings['schema_version']) is not int or settings['schema_version']!=1:
        raise ValueError('modem_settings')
    validate({'schema_version':1,'operation':'modem','values':{k:settings[k] for k in ('port','baud')}})
    # Pinned upstream supports address:port for both listeners. Port 0 allocates
    # an ephemeral inbound port; it does NOT disable the listener. Loopback keeps
    # it local. Public incoming BBS hosting is deliberately not this adapter's API.
    return ['/usr/bin/tcpser','-v','127.0.0.1:'+str(settings['port']),
            '-s',str(settings['baud']),'-l','0','-p','127.0.0.1:0']


def main():
    try:
        if len(sys.argv)!=1 or os.geteuid()==0:raise ValueError('invocation')
        args=arguments(read_json(trusted(Path('/etc/project-cbm/modem.json'))))
        os.execve(args[0],args,{'PATH':'/usr/bin:/bin','LANG':'C','HOME':'/home/pcbm'})
    except (OSError,ValueError,TypeError):
        print('Project CBM modem settings are unavailable or invalid.',file=sys.stderr);return 2
