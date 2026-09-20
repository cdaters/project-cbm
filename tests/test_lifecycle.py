"""Real child/PTY lifecycle tests; no Linux VT/KMS physical qualification."""
import json
import os
from pathlib import Path
import pty
import signal
import subprocess
import sys
import tempfile
import termios
import unittest
from unittest.mock import patch
from test_poc2 import eng


class Lifecycle(unittest.TestCase):
    def test_keyboard_baseline_is_saved_before_cover_not_after(self):
        master,slave=pty.openpty();self.addCleanup(os.close,master);self.addCleanup(os.close,slave)
        mode=[3];writes=[]
        def ioctl(fd,op,value,*rest):
            if op==0x4B44:value[0]=mode[0]
            elif op==0x4B3B:value[0]=0
            elif op==0x5601:value[:]=b'\0'*8
            elif op==0x4B45:mode[0]=value;writes.append(value)
            return 0
        def cover(*args,**kwargs):mode[0]=4;return {'exit_status':137,'timeout':True}
        with tempfile.TemporaryDirectory() as tmp,patch.object(eng.fcntl,'ioctl',side_effect=ioctl),patch.object(eng,'run_cover',side_effect=cover),patch.object(eng,'snapshot',return_value={}):
            status=eng.run_launch([sys.executable,'-c','pass'],'x64sc',Path(tmp),audio=None,stdin=slave,cover=['fixture'])
        self.assertEqual(status,0);self.assertEqual(writes,[3,3]);self.assertEqual(mode[0],3)
    def test_cover_failure_timeout_and_reap(self):
        for code,timeout,expected in [('raise SystemExit(7)',1,7),
                ('import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(10)',.1,137)]:
            with self.subTest(code=code):
                active=[]
                result=eng.run_cover([sys.executable,'-c',code],subprocess.DEVNULL,active.append,timeout,.05)
                self.assertEqual(result['exit_status'],expected)
                self.assertIsNone(active[-1]);self.assertIsNotNone(active[0].poll())
                with self.assertRaises(ChildProcessError):os.waitpid(result['pid'],os.WNOHANG)
                self.assertEqual(result['timeout'],expected==137)

    def test_cover_unavailable_and_telemetry_allowlist(self):
        result=eng.run_cover(['/nonexistent-cover'],subprocess.DEVNULL,lambda _:None)
        self.assertEqual(result['exit_status'],127)
        code='print(\'password=synthetic-never-retain\');print(\'PCBM_COVER {"stage":"presented","secret":"synthetic-never-retain","width":1920}\')'
        result=eng.run_cover([sys.executable,'-c',code],subprocess.DEVNULL,lambda _:None)
        self.assertNotIn('synthetic-never-retain',json.dumps(result))
        self.assertEqual(result['events'],[{'stage':'presented','width':1920}])

    def test_cold_cover_past_old_deadline_finishes_and_is_reaped(self):
        code='import time;time.sleep(2.1);print(\'PCBM_COVER {"stage":"released","elapsed_ms":2100}\')'
        result=eng.run_cover([sys.executable,'-c',code],subprocess.DEVNULL,lambda _:None)
        self.assertEqual(result['exit_status'],0)
        self.assertFalse(result['timeout'])
        self.assertEqual(result['events'],[{'stage':'released','elapsed_ms':2100}])
        with self.assertRaises(ChildProcessError):os.waitpid(result['pid'],os.WNOHANG)

    def test_three_cycles_restore_precover_termios_before_vice_and_after(self):
        master,slave=pty.openpty();self.addCleanup(os.close,master);self.addCleanup(os.close,slave)
        original=termios.tcgetattr(slave)
        cover='import termios;t=termios.tcgetattr(0);t[3]&=~(termios.ECHO|termios.ICANON);termios.tcsetattr(0,termios.TCSANOW,t)'
        vice='import termios;t=termios.tcgetattr(0);assert t[3]&termios.ECHO;assert t[3]&termios.ICANON;t[3]&=~termios.ECHO;termios.tcsetattr(0,termios.TCSANOW,t)'
        with tempfile.TemporaryDirectory() as tmp,patch.object(eng,'snapshot',return_value={'fixture':True}):
            for _ in range(3):
                self.assertEqual(eng.run_launch([sys.executable,'-c',vice],'x64sc',Path(tmp),audio=None,stdin=slave,
                    cover=[sys.executable,'-c',cover]),0)
                restored=termios.tcgetattr(slave)
                restored[3]&=~getattr(termios,'PENDIN',0)
                baseline=list(original);baseline[3]&=~getattr(termios,'PENDIN',0)
                self.assertEqual(restored,baseline)
                d=sorted(Path(tmp).glob('launch-*'))[-1]
                self.assertNotEqual(json.loads((d/'pre-cover.json').read_text())['termios'],json.loads((d/'post-cover.json').read_text())['termios'])
                for name in ['cover-cleanup.json','cleanup.json']:
                    self.assertTrue(json.loads((d/name).read_text())['verified'])

    def test_failed_ioctl_does_not_skip_termios_restore(self):
        attrs=[0,0,0,0,0,0,[]]
        saved={'keyboard':1,'display':0,'termios':attrs,'foreground_pgrp':22}
        with patch.object(eng.fcntl,'ioctl',side_effect=OSError),patch.object(eng.termios,'tcsetattr') as restore,patch.object(eng,'terminal_state',return_value=saved):
            result=eng.restore_tty(8,saved)
        restore.assert_called_once();self.assertFalse(result['verified']);self.assertEqual(len(result['errors']),2)

    def test_foreground_and_vt_process_not_reassigned(self):
        saved={'foreground_pgrp':10,'vt_mode':[1,0,10,12,0]}
        with patch.object(eng.fcntl,'ioctl') as ioctl,patch.object(eng,'terminal_state',return_value={'foreground_pgrp':11,'vt_mode':[0,0,0,0,0]}):
            result=eng.restore_tty(8,saved)
        ioctl.assert_not_called();self.assertFalse(result['verified'])

    def test_failed_cover_still_spawns_once_and_keeps_status(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(eng,'snapshot',return_value={}):
            status=eng.run_launch([sys.executable,'-c','print("one-launch");raise SystemExit(9)'],'x64sc',Path(tmp),audio=None,stdin=subprocess.DEVNULL,
                cover=[sys.executable,'-c','raise SystemExit(3)'])
            self.assertEqual(status,9)
            d=next(Path(tmp).glob('launch-*'))
            self.assertEqual((d/'vice.log').read_text().count('one-launch'),1)
            self.assertEqual(json.loads((d/'cover.json').read_text())['exit_status'],3)

    def test_interruption_during_cover_does_not_start_vice(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(eng,'snapshot',return_value={}):
            code='import os,signal;os.kill(os.getppid(),signal.SIGTERM)'
            old=signal.getsignal(signal.SIGTERM)
            status=eng.run_launch([sys.executable,'-c','raise Exception("must not launch")'],'x64sc',Path(tmp),audio=None,stdin=subprocess.DEVNULL,
                cover=[sys.executable,'-c',code])
            self.assertEqual(status,143);self.assertEqual(signal.getsignal(signal.SIGTERM),old)
            record=json.loads(next(Path(tmp).glob('launch-*/record.json')).read_text())
            self.assertNotIn('vice_pid',record)

    def test_signal_during_vice_is_forwarded_then_bounded_and_reaped(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(eng,'snapshot',return_value={}),patch.object(eng,'CANCEL_GRACE',.05):
            code='import os,signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);os.kill(os.getppid(),signal.SIGTERM);time.sleep(10)'
            status=eng.run_launch([sys.executable,'-c',code],'x64sc',Path(tmp),audio=None,stdin=subprocess.DEVNULL)
            self.assertEqual(status,137)
            record=json.loads(next(Path(tmp).glob('launch-*/record.json')).read_text())
            with self.assertRaises(ChildProcessError):os.waitpid(record['vice_pid'],os.WNOHANG)

    def test_primary_restores_real_terminal_after_failure_and_interruption(self):
        master,slave=pty.openpty();self.addCleanup(os.close,master);self.addCleanup(os.close,slave)
        baseline=termios.tcgetattr(slave);real_open=os.open;real_cover=eng.run_cover
        for interrupt in (False,True):
            with self.subTest(interrupt=interrupt),tempfile.TemporaryDirectory() as tmp:
                child=[]
                code='import termios,os,signal,time;t=termios.tcgetattr(0);t[3]&=~termios.ECHO;termios.tcsetattr(0,termios.TCSANOW,t);'
                code+=('os.kill(os.getppid(),signal.SIGTERM);time.sleep(10)' if interrupt else 'raise SystemExit(7)')
                def opener(name,flags,*args,**kwargs):
                    return os.dup(slave) if name=='/dev/tty' else real_open(name,flags,*args,**kwargs)
                def cover(argv,stdin,active,**kwargs):
                    self.assertEqual(argv,['/usr/bin/pcbm-cover','--primary'])
                    return real_cover([sys.executable,'-c',code],stdin,lambda process:child.append(process),**kwargs)
                old=signal.getsignal(signal.SIGTERM)
                with patch.object(eng.os,'open',side_effect=opener),patch.object(eng,'run_cover',side_effect=cover):
                    self.assertEqual(eng.primary_presentation(Path(tmp)),0)
                self.assertEqual(signal.getsignal(signal.SIGTERM),old)
                self.assertIsNotNone(child[0].poll())
                with self.assertRaises(ChildProcessError):os.waitpid(child[0].pid,os.WNOHANG)
                current=termios.tcgetattr(slave);current[3]&=~getattr(termios,'PENDIN',0)
                expected=list(baseline);expected[3]&=~getattr(termios,'PENDIN',0)
                self.assertEqual(current,expected)
                self.assertTrue(json.loads((Path(tmp)/'primary-presentation.json').read_text())['cleanup']['verified'])

    def test_primary_no_terminal_or_failed_restoration_reports_failure(self):
        with patch.object(eng.os,'open',side_effect=OSError),patch.object(eng,'run_cover') as cover:
            self.assertEqual(eng.primary_presentation(None),1);cover.assert_not_called()
        master,slave=pty.openpty();self.addCleanup(os.close,master);self.addCleanup(os.close,slave)
        with patch.object(eng.os,'open',return_value=os.dup(slave)),patch.object(eng,'run_cover',return_value={'exit_status':0}),patch.object(eng,'restore_tty',return_value={'verified':False}):
            self.assertEqual(eng.primary_presentation(None),1)
