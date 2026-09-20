import importlib.util
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
eng=module('engineering',ROOT/'build/pigen/stage-cbm/files/engineering.py')
media=module('media',ROOT/'qualification/media/build.py')
sys.path.insert(0,str(ROOT/'tools'))
import build_contracts as cb
import retained_inputs as retained


class POC2(unittest.TestCase):
    def test_graphics_and_session_contract(self):
        control=(ROOT/'build/packages/vice/debian/control').read_text()
        for package in ['libgl1','libglx-mesa0','libegl1','libegl-mesa0','libgles2','libgbm1','libgl1-mesa-dri']:self.assertIn(package,control)
        getty=(ROOT/'build/pigen/stage-cbm/files/getty-autologin.conf').read_text()
        self.assertIn('--autologin pcbm',getty);self.assertNotIn('--login-program',getty)
        profile=(ROOT/'build/pigen/stage-cbm/files/pcbm-profile.sh').read_text()
        self.assertIn('/dev/tty1) exec',profile);self.assertNotIn('sudo -',profile)
        install=(ROOT/'tools/install_poc_stage.py').read_text()
        self.assertNotIn('NOPASSWD: ALL',install)
        self.assertIn('poweroff ""',install);self.assertIn("'ssh.service'",install)
        self.assertNotIn('NOPASSWD: /usr/bin/raspi-config',install)

    def test_minimal_environment_and_redaction(self):
        self.assertNotIn('AWS_SECRET_ACCESS_KEY',eng.ENV_KEYS)
        self.assertNotIn('DISPLAY',eng.ENV_KEYS)
        for text in ['password=bad','PSK=bad','-----BEGIN OPENSSH PRIVATE KEY-----','https://user:bad@example.test']:
            self.assertNotIn('bad',eng.clean(text));self.assertIn('redact',eng.clean(text))

    def launch(self,code,state,sample_after=15):
        with patch.object(eng,'snapshot',return_value={'test':'bounded'}),patch.object(eng,'IDENTITY',Path('/nonexistent-identity')):
            return eng.run_launch([sys.executable,'-c',code],'x64sc',state,audio=None,stdin=subprocess.DEVNULL,sample_after=sample_after)

    def test_success_failure_signal_and_bounded_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            state=Path(tmp)
            self.assertEqual(self.launch('print("SDLVideo: software"); print("password=bad"); print("-----BEGIN PRIVATE KEY-----\\nPRIVATEBODY\\n-----END PRIVATE KEY-----")',state),0)
            log=next(state.glob('launch-*/vice.log')).read_text();self.assertNotIn('bad',log);self.assertNotIn('PRIVATEBODY',log)
            self.assertEqual(self.launch('raise SystemExit(7)',state),7)
            self.assertEqual(self.launch('import os,signal;os.kill(os.getpid(),signal.SIGTERM)',state),143)
            for _ in range(4):self.assertEqual(self.launch('print("a"*300000)',state),0)
            self.assertEqual(len(list(state.glob('launch-*'))),eng.KEEP)
            for p in state.glob('launch-*/vice.log'):self.assertLessEqual(p.stat().st_size,eng.LIMIT)

    def test_slow_process_observed_not_claimed_hung(self):
        with tempfile.TemporaryDirectory() as tmp:
            state=Path(tmp)
            self.assertEqual(self.launch('import time;time.sleep(.2)',state,sample_after=.02),0)
            self.assertTrue(list(state.glob('launch-*/sample-*.json')))
            record=json.loads(next(state.glob('launch-*/record.json')).read_text())
            self.assertEqual(record['observation'],'still running; not proof of hang')

    def test_snapshot_no_environment_or_process_argv(self):
        with patch.object(eng,'command',return_value='bounded'),patch.object(eng,'IDENTITY',Path('/nonexistent')):
            snap=eng.snapshot()
        self.assertNotIn('environ',json.dumps(snap));self.assertNotIn('cmdline',json.dumps(snap))

    def test_media_deterministic_and_disk_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=Path(tmp)/'a';b=Path(tmp)/'b';revision='1'*40
            manifest=media.build(a,revision);media.build(b,revision)
            self.assertEqual((a/'qualification-media.tar').read_bytes(),(b/'qualification-media.tar').read_bytes())
            self.assertLess(sum(f['size_bytes'] for f in manifest['files']),200*1024)
            disk=(a/'pcbm-check.d64').read_bytes();self.assertEqual(len(disk),174848)
            pos=media.offset(18,1);self.assertEqual(disk[pos+2],0x82)
            track,sector=disk[pos+3:pos+5];body=b'';seen=set()
            while track:
                self.assertNotIn((track,sector),seen);seen.add((track,sector));p=media.offset(track,sector)
                track,sector=disk[p:p+2];body+=disk[p+2:p+256 if track else p+1+sector]
            self.assertEqual(body,(a/'pcbm-smoke.prg').read_bytes())
            for p in a.glob('*.prg'):
                data=p.read_bytes();self.assertEqual(data[:2],b'\x01\x08');offset=2
                while data[offset:offset+2]!=b'\0\0':
                    next_address=int.from_bytes(data[offset:offset+2],'little');next_offset=next_address-0x801+2
                    self.assertEqual(data[next_offset-1],0);self.assertGreater(next_offset,offset);offset=next_offset
                self.assertEqual(offset+2,len(data))

    def test_media_archive_rejects_wrong_source_and_payload(self):
        import tarfile
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'media';media.build(out,'1'*40)
            expected={'source_commit':'1'*40}
            retained.verify_media(out/'qualification-media.tar',expected)
            with self.assertRaises(ValueError):retained.verify_media(out/'qualification-media.tar',{'source_commit':'2'*40})
            corrupt=Path(tmp)/'bad.tar'
            with tarfile.open(out/'qualification-media.tar') as src,tarfile.open(corrupt,'w') as dst:
                for member in src:
                    data=src.extractfile(member).read()
                    if member.name=='pcbm-smoke.prg':data=b'x'+data[1:]
                    dst.addfile(member,io.BytesIO(data))
            with self.assertRaises(ValueError):retained.verify_media(corrupt,expected)

    def test_media_lock_is_explicit_versioned_input(self):
        lock=cb.read_json(ROOT/'tests/fixtures/release-lock.synthetic.json')
        lock['schema_version']=2
        with self.assertRaises(ValueError):cb.validate_lock(cb.encode(lock),True)
        lock['qualification_media']={'artifact':lock['configuration']['defaults'],'source_commit':'1'*40,'profile':'private-engineering'}
        cb.validate_lock(cb.encode(lock),True)
        lock['schema_version']=1
        with self.assertRaises(ValueError):cb.validate_lock(cb.encode(lock),True)


if __name__=='__main__':unittest.main()
