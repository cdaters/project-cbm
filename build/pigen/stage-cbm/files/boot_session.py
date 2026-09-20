#!/usr/bin/env python3
"""Unprivileged boot artwork supervises preparation in the existing login session.

Anonymous inherited pipes carry one readiness byte, never user data. Only after
SDL exits/reaps and the saved tty verifies restored may the worker show its first
interactive screen. A failed/missing renderer falls through without a fixed delay.
"""
import os
from pathlib import Path
import signal
import subprocess
import engineering


def mark(phase):
    path=os.environ.get('PCBM_BOOT_TRACE','')
    if phase not in ('primary_begin','primary_done'):return
    p=Path(path)
    if p.parent!=Path('/home/pcbm/.local/state/project-cbm/boot') or not p.name.startswith('boot.') or p.is_symlink():return
    try:
        uptime=Path('/proc/uptime').read_text().split()[0]
        with p.open('a') as trace:trace.write(uptime+'\t'+phase+'\n')
    except OSError:pass


def run():
    if os.geteuid()!=1000:return 1
    fd=os.open('/dev/tty',os.O_RDWR|os.O_NOCTTY)
    saved=engineering.terminal_state(fd)
    ready_r,ready_w=os.pipe();ack_r,ack_w=os.pipe();release_r,release_w=os.pipe()
    descriptors={ready_r,ready_w,ack_r,ack_w,release_r,release_w}
    worker=None;report={'before':engineering.terminal_record(saved)};previous={}
    def close(handle):
        if handle in descriptors:os.close(handle);descriptors.remove(handle)
    def stop(signum,frame):raise InterruptedError('boot_interrupted')
    try:
        for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):previous[sig]=signal.signal(sig,stop)
        env={**os.environ,'PCBM_BOOT_READY_FD':str(ready_w),'PCBM_BOOT_ACK_FD':str(ack_r)}
        mark('primary_begin')
        worker=subprocess.Popen(['/usr/libexec/project-cbm/pcbm-console-session','--prepared'],
                                env=env,pass_fds=(ready_w,ack_r))
        close(ready_w);close(ack_r)
        cover_env={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin',
                   **{k:os.environ[k] for k in engineering.ENV_KEYS if k in os.environ},
                   'PCBM_BOOT_CONTROL_FD':str(release_r)}
        try:
            with os.fdopen(os.dup(fd),'rb',buffering=0) as terminal:
                report['presentation']=engineering.run_cover(['/usr/bin/pcbm-cover','--boot'],terminal,
                    lambda child:None,timeout=30,env=cover_env,pass_fds=(release_r,),handoff=(ready_r,release_w))
        finally:
            report['cleanup']=engineering.restore_tty(fd,saved)
        try:
            if engineering.MARKER.is_file():
                engineering.STATE.mkdir(parents=True,exist_ok=True,mode=0o700)
                engineering.atomic(engineering.STATE/'primary-presentation.json',report)
        except OSError:pass
        # Clear earlier console cells so releasing KMS cannot restore a stale dialog.
        if not report['cleanup'].get('verified'):return 1
        os.write(fd,b'\033[2J\033[H')
        try:os.write(ack_w,b'1\n')
        except BrokenPipeError:pass
        mark('primary_done')
        close(ack_w) # Subsequent UI processes see EOF: handoff is already complete.
        for sig,handler in previous.items():signal.signal(sig,handler)
        previous={}
        return worker.wait()
    finally:
        if worker is not None and worker.poll() is None:
            worker.terminate()
            try:worker.wait(timeout=1)
            except subprocess.TimeoutExpired:worker.kill();worker.wait()
        for handle in list(descriptors):close(handle)
        os.close(fd)
        for sig,handler in previous.items():signal.signal(sig,handler)


if __name__=='__main__':
    os.umask(0o077)
    try:raise SystemExit(run())
    except (OSError,KeyboardInterrupt):raise SystemExit(1)
