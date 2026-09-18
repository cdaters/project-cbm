#!/usr/bin/python3
"""Unprivileged launch/terminal owner; persistence only in private POC profiles."""
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
import struct
import subprocess
import sys
import termios
import time

STATE = Path('/home/pi/.local/state/project-cbm/diagnostics')
IDENTITY = Path('/usr/share/project-cbm/identity.json')
MARKER = Path('/etc/pcbm/engineering-poc')
LIMIT = 128 * 1024
KEEP = 4
CANCEL_GRACE = 5.0
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


def terminal_state(fd):
    """Only our controlling terminal; numeric state, never input bytes or argv."""
    result={'pid':os.getpid(),'pgrp':os.getpgrp(),'session':os.getsid(0),'captured_monotonic':time.monotonic()}
    if fd is None:return result
    for key,read in [('tty',lambda:os.ttyname(fd)),('foreground_pgrp',lambda:os.tcgetpgrp(fd)),
                     ('termios',lambda:termios.tcgetattr(fd))]:
        try:result[key]=read()
        except OSError as e:result[key+'_error']=type(e).__name__
    for key,op in [('keyboard',0x4B44),('display',0x4B3B)]:
        value=array.array('i',[0])
        try:fcntl.ioctl(fd,op,value,True);result[key]=value[0]
        except OSError as e:result[key+'_error']=type(e).__name__
    try:
        value=bytearray(8);fcntl.ioctl(fd,0x5601,value,True) # VT_GETMODE
        result['vt_mode']=list(struct.unpack('=BBhhh',value))
    except OSError as e:result['vt_mode_error']=type(e).__name__
    return result


def terminal_record(value):
    result=dict(value)
    if 'termios' in result:
        attrs=result['termios'];result['termios']=attrs[:6]+[[x[0] if isinstance(x,bytes) else x for x in attrs[6]]]
    return result


def restore_tty(fd, saved):
    """Restore the pre-presentation state, independently check every operation.

    No reset/chvt/root or guessed sane state. Never install another process's
    VT_PROCESS signal ownership or change the foreground process group.
    """
    errors=[]
    if fd is None:return {'attempted':False}
    operations=[]
    if 'keyboard' in saved:operations.append(('keyboard',lambda:fcntl.ioctl(fd,0x4B45,saved['keyboard'])))
    if 'display' in saved:operations.append(('display',lambda:fcntl.ioctl(fd,0x4B3A,saved['display'])))
    if saved.get('vt_mode',[None])[0]==0:
        operations.append(('vt_mode',lambda:fcntl.ioctl(fd,0x5602,struct.pack('=BBhhh',*saved['vt_mode']))))
    if 'termios' in saved:operations.append(('termios',lambda:termios.tcsetattr(fd,termios.TCSANOW,saved['termios'])))
    for name,operation in operations:
        try:operation()
        except OSError as e:errors.append(name+':'+type(e).__name__)
    actual=terminal_state(fd)
    compared=[k for k in ['keyboard','display','termios','vt_mode','foreground_pgrp','tty'] if k in saved]
    def equal(key):
        a=actual.get(key);b=saved[key]
        if key=='termios' and a is not None:
            # BSD's kernel-managed PENDIN bit can be set by tcsetattr itself;
            # it requests pending-input reprocessing, not a changed input mode.
            a=list(a);b=list(b)
            a[3]&=~getattr(termios,'PENDIN',0);b[3]&=~getattr(termios,'PENDIN',0)
        return a==b
    mismatch=[k for k in compared if not equal(k)]
    return {'attempted':True,'errors':errors,'mismatch':mismatch,'verified':not errors and not mismatch,
            'state':terminal_record(actual)}


def run_cover(argv, stdin, active, timeout=6.0, grace=.5, env=None):
    """Same foreground group as Menu; bounded drain/TERM/KILL/reap before VICE.

    Pi 3B attempt5 exhausted the old two-second total before renderer creation.
    Six seconds bounds cold startup + presentation + release, with no fixed wait
    on success. This is a qualification budget, not measured Pi startup latency.
    Only structured renderer telemetry is retained. Untrusted SDL/backend text
    is discarded, not copied into diagnostics with potentially private strings.
    """
    result={'started_monotonic':time.monotonic(),'timeout':False,'killed':False,'events':[]}
    child=None;sel=None;tail=bytearray()
    try:
        child=subprocess.Popen(argv,stdin=stdin,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env)
        active(child);result['pid']=child.pid
        sel=selectors.DefaultSelector();sel.register(child.stdout,selectors.EVENT_READ)
        deadline=time.monotonic()+timeout
        while child.poll() is None or sel.get_map():
            now=time.monotonic()
            if now>=deadline:
                if not result['timeout']:
                    result['timeout']=True
                    if child.poll() is None:child.terminate()
                    deadline=now+grace
                else:
                    if child.poll() is None:child.kill();result['killed']=True
                    break
            for key,_ in sel.select(.02):
                data=os.read(key.fileobj.fileno(),4096)
                if data:tail.extend(data);del tail[:-LIMIT]
                else:sel.unregister(key.fileobj)
        status=child.wait()
        result.update(exit_status=status if status>=0 else 128-status,termination_signal=-status if status<0 else None)
        for line in tail.decode(errors='replace').splitlines():
            if not line.startswith('PCBM_COVER '):continue
            try:
                event=json.loads(line[len('PCBM_COVER '):])
                # Fixed fields/types; no asset paths, SDL error strings or credentials.
                if not isinstance(event,dict):continue
                safe={k:v for k,v in event.items() if k in ('stage','driver','renderer') and isinstance(v,str) and re.fullmatch(r'[A-Za-z0-9_-]{1,40}',v)
                      or k in ('width','height','elapsed_ms') and type(v) is int and 0<=v<=100000}
                if safe and len(result['events'])<24:result['events'].append(safe)
            except ValueError:pass
    except OSError as e:result.update(error=type(e).__name__,exit_status=127)
    finally:
        if child is not None:
            if child.poll() is None:child.kill()
            child.wait()
            if child.stdout:child.stdout.close()
        if sel:sel.close()
        active(None);result['ended_monotonic']=time.monotonic()
    return result


def run_launch(argv, profile, state=STATE, audio=('/usr/bin/pcbm-audio','auto','--quiet'), stdin=None, sample_after=15, cover=None):
    lock=None;directory=None
    if state is not None:
        state.mkdir(parents=True,exist_ok=True,mode=0o700)
        lock=(state/'launch.lock').open('w')
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        for p in sorted(state.glob('launch-*'))[:-(KEEP-1)]:
            if p.is_dir() and not p.is_symlink():shutil.rmtree(p)
        directory=state/('launch-'+str(time.time_ns()));directory.mkdir(mode=0o700)
    def save(name,value):
        if directory is not None:
            try:atomic(directory/name,value)
            except OSError:pass # Diagnostics must not own emulator lifecycle.
    record={'profile':profile,'executable':argv[0],'launcher_pid':os.getpid(),'uid':os.getuid(),
            'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
            'started_monotonic':time.monotonic(),'environment':{},'phase':'audio',
            'content_requested':'-autostart' in argv,'exit_status':None,'termination_signal':None}
    env={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin'}
    for key in ENV_KEYS:
        if key in os.environ:env[key]=os.environ[key];record['environment'][key]=clean(os.environ[key])
    env['SDL_AUDIODRIVER']='alsa'
    if state is not None:env['CBM_PRESENTATION_DIAGNOSTICS']='1'
    try:record['identity']=json.loads(IDENTITY.read_text())
    except (OSError,ValueError):record['identity']='unavailable'
    save('record.json',record)
    fd=None;saved={};proc=None;cover_proc=None;cancelled=None;cancelled_at=None;lines=deque();size=0;partial=b'';last_flush=0;private_block=False
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
        if directory is None:return
        try:
            with (directory/'vice.log.next').open('wb') as f:
                f.write(b''.join(lines));f.flush();os.fsync(f.fileno())
            (directory/'vice.log.next').replace(directory/'vice.log')
        except OSError:pass
    old_handlers={}
    def forward(sig,frame):
        nonlocal cancelled,cancelled_at
        cancelled=sig
        if cancelled_at is None:cancelled_at=time.monotonic()
        if cover_proc is not None and cover_proc.poll() is None:cover_proc.send_signal(sig)
        if proc is not None and proc.poll() is None:proc.send_signal(sig)
    def cover_active(child):
        nonlocal cover_proc
        cover_proc=child
    try:
        if stdin is None:
            fd=os.open('/dev/tty',os.O_RDWR);stdin=fd
        elif isinstance(stdin,int) and stdin>=0 and os.isatty(stdin):fd=os.dup(stdin)
        saved=terminal_state(fd)
        for sig in [signal.SIGTERM,signal.SIGHUP,signal.SIGINT]:
            old_handlers[sig]=signal.signal(sig,forward)
        save('pre-cover.json',terminal_record(saved))
        if cover:
            record['phase']='cover';save('record.json',record)
            save('cover.json',run_cover(cover,stdin,cover_active,env=env))
        save('post-cover.json',terminal_record(terminal_state(fd)))
        save('cover-cleanup.json',restore_tty(fd,saved))
        if cancelled:
            record.update(phase='interrupted',exit_status=128+cancelled,termination_signal=cancelled)
            save('record.json',record);return 128+cancelled
        if directory is not None:save('before.json',snapshot()) # AFTER Cover cleanup, BEFORE VICE
        # Audio helper gets a bounded timeout and bounded output, before spawn marker.
        if audio:output((command(list(audio))+'\n').encode())
        record['audio_finished_monotonic']=time.monotonic();record['phase']='spawn';save('record.json',record)
        if cancelled:
            record.update(phase='interrupted',exit_status=128+cancelled,termination_signal=cancelled)
            save('record.json',record);return 128+cancelled
        proc=subprocess.Popen(argv,stdin=stdin,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env)
        record.update(vice_pid=proc.pid,phase='running');save('record.json',record)
        sel=selectors.DefaultSelector();sel.register(proc.stdout,selectors.EVENT_READ)
        samples=0;next_sample=time.monotonic()+sample_after
        while sel.get_map():
            for key,mask in sel.select(.2):
                chunk=os.read(key.fileobj.fileno(),4096)
                if chunk:output(chunk)
                else:sel.unregister(key.fileobj)
            now=time.monotonic()
            if cancelled_at is not None and now-cancelled_at>=CANCEL_GRACE and proc.poll() is None:
                proc.kill() # Only our child, after an explicit termination request.
            if now-last_flush>=1:flush();last_flush=now
            if directory is not None and now>=next_sample and samples<3:
                save('sample-'+str(samples)+'.json',snapshot(proc.pid))
                samples+=1;next_sample=now+sample_after
                record['observation']='still running; not proof of hang';save('record.json',record)
        status=proc.wait();sel.close();proc.stdout.close()
        output(b'\n');flush()
        record.update(phase='exited',exit_status=status if status>=0 else 128-status,
                      termination_signal=-status if status<0 else None,ended_monotonic=time.monotonic())
        save('record.json',record)
        return record['exit_status']
    except OSError as e:
        record.update(phase='launcher-error',error=type(e).__name__,exit_status=127);save('record.json',record)
        return 127
    finally:
        try:
            if proc is not None and proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=5)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
        finally:
            # Cleanup must not depend on diagnostic storage being writable.
            actual=terminal_state(fd);restored=restore_tty(fd,saved)
            if fd is not None:os.close(fd)
            for sig,handler in old_handlers.items():signal.signal(sig,handler)
            if lock:lock.close()
            save('post-vice.json',terminal_record(actual));save('cleanup.json',restored)
            if restored.get('attempted') and not restored.get('verified'):
                print('Project CBM: terminal restoration could not be verified; review launch diagnostics.',file=sys.stderr)


def main():
    os.umask(0o077)
    if os.geteuid()==0:raise SystemExit('non-root only')
    if sys.argv[1:2] in (['run'],['run-with-cover']):
        profile,exe,*args=sys.argv[2:]
        if Path(exe).parent!=Path('/usr/bin') or Path(exe).name not in MACHINES:raise SystemExit('unsupported emulator')
        # Disable color before stdout-only logging: VICE 3.10 otherwise passes
        # null color-stripped strings to redirected stdout (src/log.c:746-767).
        # '-' suppresses its separate unbounded default log.
        raise SystemExit(run_launch([exe,*args,'+logcolorize','-logfile','-'],profile,
                                   state=STATE if MARKER.is_file() else None,
                                   cover=['/usr/bin/pcbm-cover','--profile',profile]))
    if not MARKER.is_file():raise SystemExit('private engineering diagnostics only')
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
