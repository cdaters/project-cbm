#!/usr/bin/python3
"""Private POC diagnostics: unprivileged, bounded, no network or root operations."""
import array
from collections import deque
import fcntl
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import signal
import subprocess
import sys
import termios
import time

STATE = Path('/home/pi/.local/state/project-cbm/diagnostics')
IDENTITY = Path('/usr/share/project-cbm/identity.json')
MARKER = Path('/etc/pcbm/engineering-poc')
LIMIT = 128 * 1024
KEEP = 4
ENV_KEYS = ('HOME', 'XDG_CONFIG_HOME', 'XDG_STATE_HOME', 'XDG_DATA_HOME',
            'XDG_RUNTIME_DIR', 'XDG_SESSION_ID', 'TERM', 'LANG', 'LC_ALL', 'SDL_AUDIODRIVER')
MACHINES = {'x64', 'x64sc', 'xscpu64', 'x64dtv', 'x128', 'xcbm2', 'xcbm5x0', 'xvic', 'xplus4', 'xpet'}


def clean(text):
    text = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '?', text)
    if re.search(r'(?i)password|passphrase|private.key|authorized_keys|\bpsk\b|\btoken\b|secret', text):
        return '[redacted sensitive line]'
    text = re.sub(r'(?i)(?:https?://)?[^\s/:]+:[^\s/@]+@[^\s]+', '[redacted credential URL]', text)
    text = re.sub(r'\b(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]+', '[redacted token]', text)
    return text[:4096]


def atomic(path, value):
    temp = path.with_suffix(path.suffix + '.next')
    with temp.open('w') as f:
        json.dump(value, f, indent=2, sort_keys=True); f.write('\n'); f.flush(); os.fsync(f.fileno())
    temp.replace(path)


def command(argv):
    # No shell, no caller-selected commands, bounded capture and timeout.
    try:
        with subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              env={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin','LC_ALL':'C'}) as p:
            sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ)
            data=bytearray();end=time.monotonic()+2
            while len(data)<16384 and time.monotonic()<end:
                ready=sel.select(.1)
                if ready:
                    part=os.read(p.stdout.fileno(),min(4096,16384-len(data)))
                    if not part:break
                    data.extend(part)
                elif p.poll() is not None:break
            if p.poll() is None:p.kill()
            p.wait();sel.close()
        return '\n'.join(clean(x) for x in data.decode(errors='replace').splitlines())
    except OSError as e:return 'unavailable: '+type(e).__name__


def snapshot(pid=None):
    result={'captured_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
            'platform':command(['uname','-srm']),
            'tty':command(['tty']),
            'sessions':command(['loginctl','list-sessions','--no-legend','--no-pager']),
            'audio':command(['aplay','-l']),
            'services':command(['systemctl','is-active','getty@tty1','getty@tty2','pcbm-first-boot','ssh','NetworkManager']),
            'drm':{},'processes':[],
            'active_drm':command(['/usr/libexec/project-cbm-vice/drm-state']) or 'unavailable; no result (permissions/profile/device)'}
    try:result['identity']=json.loads(IDENTITY.read_text())
    except (OSError,ValueError):result['identity']='unavailable'
    # No full argv/environment, network addresses, device serials, machine-id or EDID.
    for p in sorted(Path('/sys/class/drm').glob('card*-*/status'))[:16]:
        try:result['drm'][p.parent.name]={'status':p.read_text()[:256], 'modes':(p.parent/'modes').read_text()[:1024]}
        except OSError:pass
    for p in Path('/proc').glob('[0-9]*'):
        try:
            name=(p/'comm').read_text().strip()
            if name not in MACHINES|{'pcbm-menu','pcbm-run-vice','agetty','login'} and p.name!=str(pid):continue
            info={k:v.strip() for k,sep,v in (x.partition(':') for x in (p/'status').read_text().splitlines()) if k in ['Name','State','Pid','PPid','Uid','Gid','Threads']}
            info['wchan']=(p/'wchan').read_text()[:128];result['processes'].append(info)
            if len(result['processes'])>=32:break
        except OSError:pass
    # Access-denied is evidence; do not add root/journal-group privileges to obtain it.
    result['kernel_graphics']=command(['journalctl','-k','-b','-n','60','--no-pager','--output=cat','--grep=drm|vc4|gpu|snd|alsa'])
    return result


def restore_tty(fd, attributes, keyboard):
    if fd is None:return
    try:
        if keyboard is not None:fcntl.ioctl(fd,0x4B45,keyboard) # KDSKBMODE saved before VICE
        fcntl.ioctl(fd,0x4B3A,0) # KDSETMODE KD_TEXT on owned VT
        if attributes is not None:termios.tcsetattr(fd,termios.TCSANOW,attributes)
        os.write(fd,b'\x1b[0m\x1b[?25h\x1b[2J\x1b[H')
    except OSError:pass
    finally:os.close(fd)


def run_launch(argv, profile, state=STATE, audio=('/usr/bin/pcbm-audio','auto','--quiet'), stdin=None, sample_after=15):
    state.mkdir(parents=True,exist_ok=True,mode=0o700)
    lock=(state/'launch.lock').open('w')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    for p in sorted(state.glob('launch-*'))[:-(KEEP-1)]:
        if p.is_dir() and not p.is_symlink():shutil.rmtree(p)
    directory=state/('launch-'+str(time.time_ns()));directory.mkdir(mode=0o700)
    record={'profile':profile,'executable':argv[0],'launcher_pid':os.getpid(),'uid':os.getuid(),
            'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
            'started_monotonic':time.monotonic(),'environment':{},'phase':'audio',
            'content_requested':'-autostart' in argv,'exit_status':None,'termination_signal':None}
    env={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin'}
    for key in ENV_KEYS:
        if key in os.environ:env[key]=os.environ[key];record['environment'][key]=clean(os.environ[key])
    env['SDL_AUDIODRIVER']='alsa'
    env['CBM_PRESENTATION_DIAGNOSTICS']='1' # opt-in numeric/video-only package telemetry
    try:record['identity']=json.loads(IDENTITY.read_text())
    except (OSError,ValueError):record['identity']='unavailable'
    atomic(directory/'record.json',record);atomic(directory/'before.json',snapshot())
    fd=None;attributes=None;keyboard=None;proc=None;lines=deque();size=0;partial=b'';last_flush=0;private_block=False
    def output(data):
        nonlocal size,partial,private_block
        partial+=data
        while b'\n' in partial or len(partial)>4096:
            if b'\n' in partial and partial.index(b'\n')<=4096:line,partial=partial.split(b'\n',1)
            else:line,partial=partial[:4096],partial[4096:]
            text=line.decode(errors='replace')
            if 'BEGIN ' in text and 'PRIVATE KEY' in text:private_block=True
            if private_block:
                if 'END ' in text and 'PRIVATE KEY' in text:private_block=False
                text='[redacted private-key material]'
            line=(clean(text)+'\n').encode();lines.append(line);size+=len(line)
            while size>LIMIT:size-=len(lines.popleft())
    def flush():
        with (directory/'vice.log.next').open('wb') as f:
            f.write(b''.join(lines));f.flush();os.fsync(f.fileno())
        (directory/'vice.log.next').replace(directory/'vice.log')
    old_handlers={}
    def forward(sig,frame):
        if proc is not None and proc.poll() is None:proc.send_signal(sig)
    try:
        if stdin is None:
            fd=os.open('/dev/tty',os.O_RDWR);stdin=fd
            attributes=termios.tcgetattr(fd);kb=array.array('i',[0])
            try:fcntl.ioctl(fd,0x4B44,kb,True);keyboard=kb[0]
            except OSError:pass
        for sig in [signal.SIGTERM,signal.SIGHUP,signal.SIGINT]:
            old_handlers[sig]=signal.signal(sig,forward)
        # Audio helper gets a bounded timeout and bounded output, before spawn marker.
        if audio:output((command(list(audio))+'\n').encode())
        record['audio_finished_monotonic']=time.monotonic();record['phase']='spawn';atomic(directory/'record.json',record)
        proc=subprocess.Popen(argv,stdin=stdin,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env)
        record.update(vice_pid=proc.pid,phase='running');atomic(directory/'record.json',record)
        sel=selectors.DefaultSelector();sel.register(proc.stdout,selectors.EVENT_READ)
        samples=0;next_sample=time.monotonic()+sample_after
        while sel.get_map():
            for key,mask in sel.select(.2):
                chunk=os.read(key.fileobj.fileno(),4096)
                if chunk:output(chunk)
                else:sel.unregister(key.fileobj)
            now=time.monotonic()
            if now-last_flush>=1:flush();last_flush=now
            if now>=next_sample and samples<3:
                atomic(directory/('sample-'+str(samples)+'.json'),snapshot(proc.pid))
                samples+=1;next_sample=now+sample_after
                record['observation']='still running; not proof of hang';atomic(directory/'record.json',record)
        status=proc.wait();sel.close();proc.stdout.close()
        output(b'\n');flush()
        record.update(phase='exited',exit_status=status if status>=0 else 128-status,
                      termination_signal=-status if status<0 else None,ended_monotonic=time.monotonic())
        atomic(directory/'record.json',record)
        return record['exit_status']
    except OSError as e:
        record.update(phase='launcher-error',error=type(e).__name__,exit_status=127);atomic(directory/'record.json',record)
        return 127
    finally:
        if proc is not None and proc.poll() is None:proc.terminate();proc.wait(timeout=5)
        for sig,handler in old_handlers.items():signal.signal(sig,handler)
        restore_tty(fd,attributes,keyboard);lock.close()


def main():
    os.umask(0o077)
    if os.geteuid()==0 or not MARKER.is_file():raise SystemExit('private engineering profile, non-root only')
    if sys.argv[1:2]==['run']:
        profile,exe,*args=sys.argv[2:]
        if Path(exe).parent!=Path('/usr/bin') or Path(exe).name not in MACHINES:raise SystemExit('unsupported emulator')
        # Disable color before stdout-only logging: VICE 3.10 otherwise passes
        # null color-stripped strings to redirected stdout (src/log.c:746-767).
        # '-' suppresses its separate unbounded default log.
        raise SystemExit(run_launch([exe,*args,'+logcolorize','-logfile','-'],profile))
    if sys.argv[1:]!=['snapshot']:raise SystemExit('use pcbm-diagnostics')
    STATE.mkdir(parents=True,exist_ok=True,mode=0o700)
    current=snapshot();atomic(STATE/'snapshot.json',current)
    latest=sorted(STATE.glob('launch-*'))[-1:]
    report={'snapshot':current,'latest_launch':{}}
    if latest:
        for p in sorted(latest[0].glob('*')):
            if p.is_file() and p.suffix in ['.json','.log']:
                report['latest_launch'][p.name]=p.read_text(errors='replace')[:LIMIT]
    atomic(STATE/'report.json',report)
    print('Private diagnostic report: '+str(STATE/'report.json'))
    print('Logs also survive for offline SD extraction. Review before sharing; do not repair the candidate.')


if __name__=='__main__':main()
