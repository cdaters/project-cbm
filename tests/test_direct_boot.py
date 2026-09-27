"""Actual prepared console branch and readiness pipes on a controlling PTY.

Only admission (test UID/PTY instead of appliance UID/tty1), absolute filesystem
locations and leaf commands are substituted. The branch and handoff are real.
Linux keyboard/VT ioctls and visible KMS still require physical qualification.
"""
import fcntl
import os
from pathlib import Path
import pty
import select
import shlex
import sys
import signal
import subprocess
import tempfile
import termios
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]

class DirectBoot(unittest.TestCase):
    def exercise(self, status=0, acknowledge=True, profile='x64sc'):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            def leaf(name, body):
                p=root/name;p.write_text('#!/bin/bash\n'+body+'\n');p.chmod(0o755);return str(p)
            ready_r,ready_w=os.pipe();ack_r,ack_w=os.pipe();master,slave=pty.openpty()
            source=(ROOT/'build/pigen/stage-cbm/files/pcbm-console-session').read_text()
            source=source.replace('(( EUID == 1000 ))','(( EUID == '+str(os.geteuid())+' ))')
            source=source.replace('[[ $(tty) == /dev/tty1 ]]','[[ $(tty) == '+os.ttyname(slave)+' ]]')
            source=source.replace('/usr/libexec/project-cbm/boot-trace.sh',str(ROOT/'build/pigen/stage-cbm/files/boot-trace.sh'))
            source=source.replace('/home/pcbm/content',tmp)
            for cmd,body in {
                'pcbm-first-run':'exit 0', 'pcbm-profiles':'exit 0',
                'pcbm-start-profile':'printf "%s" "'+profile+'"',
                'pcbm-run-vice':'printf LAUNCH; exit '+str(status),
                'pcbm-menu':shlex.quote(sys.executable)+" -c 'import os; assert os.tcgetpgrp(0)==os.getpgrp(); assert all(os.isatty(i) for i in range(3))' || exit 8; "+'printf MENU; read -r key; [[ $key == probe ]] || exit 7; printf RESPONSIVE; kill -TERM "$PPID"',
            }.items():source=source.replace('/usr/bin/'+cmd,leaf(cmd,body))
            script=root/'console';script.write_text(source)
            env={**os.environ,'TERM':'linux','PCBM_BOOT_READY_FD':str(ready_w),'PCBM_BOOT_ACK_FD':str(ack_r)}
            child=subprocess.Popen(['bash',str(script),'--prepared'],env=env,stdin=slave,stdout=slave,stderr=slave,
                start_new_session=True,preexec_fn=lambda:fcntl.ioctl(slave,termios.TIOCSCTTY,0),pass_fds=(ready_w,ack_r))
            data=bytearray()
            def collect(until):
                end=time.monotonic()+3
                while until not in data and time.monotonic()<end:
                    if select.select([master],[],[],.05)[0]:data.extend(os.read(master,4096))
                self.assertIn(until,data)
            try:
                if profile:
                    self.assertTrue(select.select([ready_r],[],[],3)[0],'direct branch skipped readiness')
                    self.assertEqual(os.read(ready_r,1),b'1')
                    self.assertFalse(select.select([master],[],[],.1)[0],'launch happened before release acknowledgement')
                    os.write(ack_w,b'1\n' if acknowledge else b'failed\n')
                    if not acknowledge:
                        self.assertEqual(child.wait(timeout=3),2)
                        return
                collect(b'MENU')
                self.assertEqual(data.count(b'LAUNCH'),int(bool(profile)))
                os.write(master,b'probe\n');collect(b'RESPONSIVE')
                self.assertEqual(child.wait(timeout=3),-signal.SIGTERM)
            finally:
                if child.poll() is None:os.killpg(child.pid,signal.SIGKILL);child.wait()
                for fd in (ready_r,ready_w,ack_r,ack_w,master,slave):os.close(fd)

    def test_direct_waits_for_release_then_returns_to_responsive_menu(self):self.exercise()
    def test_launch_failure_returns_once_to_responsive_menu(self):self.exercise(status=9)
    def test_terminated_launch_returns_once_to_responsive_menu(self):self.exercise(status=143)
    def test_failed_handoff_never_launches_cover_or_vice(self):self.exercise(acknowledge=False)
    def test_menu_preference_does_not_direct_launch(self):self.exercise(profile='')

if __name__=='__main__':unittest.main()
