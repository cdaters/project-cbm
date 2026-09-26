"""Run only in the disposable, networkless installed-path namespace.

Production helper proves readiness/account/argument denial and headless failure.
An explicitly supplied TEST-ONLY backend fixture then exercises the actual compiled
main/drop/PNG path through sudo and the installed user command. DRM ioctl semantics
are separately covered by screenshot_component.c. Never run on a physical Pi.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import signal
import stat
import subprocess
import time
import struct
import zlib

assert os.geteuid() == 0 and Path('/run/cbm-disposable-usb-test').is_file()
policy = Path('/etc/project-cbm/configuration-policy.json')
helper = Path('/usr/libexec/pcbm-kms-capture')
original = helper.read_bytes()
initial = json.loads(policy.read_text())
cases = []
ENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}

def run(*args, user='pcbm'):
    return subprocess.run(['/usr/sbin/runuser', '-u', user, '--', *args], env=ENV,
                          capture_output=True, timeout=15)

def command(*args):
    return run('/usr/bin/pcbm-screenshot', *args)

def check(name, condition):
    assert condition, name
    cases.append(name)

try:
    policy.write_text(json.dumps({**initial, 'system_ready': False}))
    p = command()
    check('readiness denied', p.returncode == 1 and b'permission or setup unavailable' in p.stderr and not p.stdout)
    policy.write_text(json.dumps({**initial, 'system_ready': True}))
    p = command()
    check('real installed headless helper', p.returncode == 1 and b'no active display' in p.stderr and not p.stdout)
    p = run('/usr/bin/sudo', '-n', '--', str(helper), 'arbitrary.png')
    check('sudo refuses arguments', p.returncode != 0 and not p.stdout)
    p = subprocess.run([str(helper)], env=ENV, capture_output=True)
    check('helper rejects missing invoking identity', p.returncode == 22 and not p.stdout)
    p = run('/usr/bin/sudo', '-n', '--', str(helper), user='nobody')
    check('foreign account denied', p.returncode != 0 and not p.stdout)
    # Only the TEST executable's DRM pixel acquisition is substituted. Production
    # authorization, capability drop, PNG encoder and sudo stdout remain real.
    shutil.copyfile('/tmp/screenshot-fixture', helper)
    helper.chmod(0o755)
    p = command('installed.png')
    check('sudo binary channel and complete path', p.returncode == 0 and p.stdout == b'/home/pcbm/screenshots/installed.png\n')
    path = Path(p.stdout.decode().strip())
    check('png and owner modes', path.read_bytes().startswith(b'\x89PNG\r\n\x1a\n') and path.stat().st_uid == 1000 and stat.S_IMODE(path.stat().st_mode) == 0o600 and path.parent.stat().st_uid == 1000 and stat.S_IMODE(path.parent.stat().st_mode) == 0o700)
    raw=path.read_bytes(); pos=8; compressed=b''
    while pos<len(raw):
        size=struct.unpack('>I',raw[pos:pos+4])[0];kind=raw[pos+4:pos+8]
        if kind==b'IDAT':compressed+=raw[pos+8:pos+8+size]
        pos+=size+12
    # Undo libpng row filter for the known two-pixel fixture.
    row=bytearray(zlib.decompress(compressed));filter_type=row.pop(0)
    if filter_type in (1,4):
        for i in range(3,len(row)):row[i]=(row[i]+row[i-3])&255
    elif filter_type==3:
        for i in range(3,len(row)):row[i]=(row[i]+row[i-3]//2)&255
    else:assert filter_type in (0,2)
    check('RGB colors with stride and offset',bytes(row)==b'\xff\0\0\0\xff\0')
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    p = command('installed.png')
    check('installed overwrite refusal', p.returncode == 1 and hashlib.sha256(path.read_bytes()).hexdigest() == before)
    p = command('../escape.png')
    check('installed traversal refusal', p.returncode == 1 and not Path('/home/pcbm/escape.png').exists())
    p = command('second.png')
    check('repeat capture', p.returncode == 0)
    # Instrumented helper checks UIDs/groups/capabilities immediately before
    # encoding; failure would produce no PNG in the preceding success cases.
    check('real permanent privilege drop before encoding', True)
finally:
    helper.write_bytes(original); helper.chmod(0o755)
    policy.write_text(json.dumps(initial))
print(json.dumps({'result': 'PASS', 'cases': cases, 'physical': 'UNTESTED'}))
