"""Application composition/launch contracts using original synthetic PRGs."""
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'runtime')]
import ccgms_application as ccgms
from optional_software import application_disk, offset, sha
from project_cbm.applications import content_options


class CCGMS(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name).resolve()
        self.prg=b'\x01\x08'+b'original test program'*100
        self.disk=application_disk([('UNRELATED',b'\x01\x08unrelated'),('CCGMS 2021',self.prg)],'TEST','TT')
        def desc(b):return {'size_bytes':len(b),'sha256':sha(b)}
        self.pin={'upstream_disk':desc(self.disk),'program':desc(self.prg),
            'source':desc(b'source'),'notice':desc(b'license'),'content_path':'programs/c64/Communications/CCGMS/CCGMS-2021.d64'}

    def test_exact_program_only_deterministic_disk(self):
        raw=ccgms.payload(self.disk,b'source',b'license',self.pin)
        self.assertEqual(raw,ccgms.payload(self.disk,b'source',b'license',self.pin))
        with tarfile.open(fileobj=io.BytesIO(raw)) as t:
            d=t.extractfile('CCGMS-2021.d64').read()
            self.assertEqual(t.extractfile('SOURCE.txt').read(),b'source')
            self.assertEqual(t.extractfile('LICENSE.txt').read(),b'license')
        self.assertEqual(d[offset(18,1)+34],0) # no second directory entry
        track,sector=d[offset(18,1)+3:offset(18,1)+5];result=b''
        while track:
            b=d[offset(track,sector):offset(track,sector)+256]
            result+=b[2:] if b[0] else b[2:b[1]+1];track,sector=b[:2]
        self.assertEqual(result,self.prg);self.assertNotIn(b'unrelated',d)

    def test_reject_input_tampering(self):
        for args in [(self.disk[:-1],b'source',b'license'),(self.disk,b'wrong',b'license'),(self.disk,b'source',b'wrong')]:
            with self.assertRaises(ValueError):ccgms.payload(*args,self.pin)

    def test_install_preserves_existing_user_data(self):
        raw=ccgms.payload(self.disk,b'source',b'license',self.pin)
        with patch.object(ccgms,'read_json',return_value=self.pin):
            paths=ccgms.install(self.root,raw)
            self.assertEqual(len(paths),6)
            with self.assertRaises(ValueError):ccgms.install(self.root,raw)
        self.assertFalse(any('striketerm' in s.lower() for s in paths))

    def media(self,relative):
        p=self.root/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'fixture');return p

    def test_serial_options_are_application_specific_and_use_configured_port(self):
        settings=self.root/'modem.json';settings.write_text(json.dumps({'schema_version':1,'port':25233,'baud':38400}))
        p=self.media(self.pin['content_path']);opts=content_options(p,'x64sc',self.root,settings)
        self.assertIn('-myaciadev',opts);self.assertNotIn('-acia1dev',opts)
        self.assertIn('127.0.0.1:25233',opts);self.assertIn('-rsdev1ip232',opts)
        self.assertEqual(opts[opts.index('-acia1irq')+1],'1')
        self.assertEqual(content_options(self.media('games/c64/game.d64'),'x64sc',self.root),[])
        settings.write_text('{"schema_version":1,"port":22,"baud":38400}')
        with self.assertRaises(ValueError):content_options(p,'x64sc',self.root,settings)

    def test_g71_requires_supported_drive_profile(self):
        p=self.media('games/c128/.disk.G71')
        for profile in ('x64','x64sc','x128','x128-80col'):
            self.assertEqual(content_options(p,profile,self.root),['-drive8type','1571'])
        with self.assertRaises(ValueError):content_options(p,'xpet',self.root)

    def test_redirected_content_rejected(self):
        p=self.media('games/c64/file.d64');link=p.parent/'link.d64';link.symlink_to(p)
        with self.assertRaises(ValueError):content_options(link,'x64sc',self.root)

    def test_g71_routing_does_not_inherit_dtv_or_supercpu(self):
        from project_cbm.library import content_profile
        profiles=[{'id':name} for name in ('x64sc','x64','x64dtv','xscpu64','x128','x128-80col')]
        p=self.media('games/c64/disk.g71')
        for default in ('x64dtv','xscpu64'):
            self.assertEqual(content_profile(p,profiles,default,self.root),'x64sc')
        self.assertEqual(content_profile(p,profiles,'x64',self.root),'x64')
        p=self.media('programs/c128/80col/disk.g71')
        self.assertEqual(content_profile(p,profiles,'x64sc',self.root),'x128-80col')
