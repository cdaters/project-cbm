"""Synthetic application/media fixtures; no copyrighted reference media or Pi."""
import copy
import hashlib
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
import optional_software as apps
from project_cbm.applications import application_profile
from project_cbm.data import registry
from project_cbm import profiles, preferences
from build_contracts import validate_lock, encode


def synthetic_source(path):
    parts={'n/README':b'fixture permission', 'n/wizard':b'\x01\x08'+b'w'*32000,'n/maker':b'\x01\x08'+b'm'*17000}
    with tarfile.open(path,'w:gz') as t:
        for n,b in parts.items():
            m=tarfile.TarInfo(n);m.size=len(b);t.addfile(m,io.BytesIO(b))
    def entry(n):return {'member':n,'sha256':apps.sha(parts[n]),'size_bytes':len(parts[n])}
    return {'source':{'sha256':apps.sha(path.read_bytes()),'size_bytes':path.stat().st_size},'notice':entry('n/README'),'programs':[{**entry('n/wizard'),'disk_name':'SID-WIZARD'},{**entry('n/maker'),'disk_name':'SID-MAKER'}],'version':'1.97','license':'LicenseRef-Hermit-WTF'}


class OptionalApplications(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name).resolve();self.source=self.root/'source.tar.gz'
        self.pin=synthetic_source(self.source)

    def test_deterministic_core_only_and_exact_disk_roundtrip(self):
        a=apps.payload(self.source,self.pin);self.assertEqual(a,apps.payload(self.source,self.pin))
        with tarfile.open(fileobj=io.BytesIO(a)) as t:
            self.assertEqual(set(t.getnames()),apps.NAMES)
            d=t.extractfile('SID-Wizard-1.97.d64').read()
        self.assertEqual(len(d),174848)
        # Independent reader reconstructs both chains and checks every allocation bit.
        sector_counts=[21]*17+[19]*7+[18]*6+[17]*5
        def loc(t,s):return (sum(sector_counts[:t-1])+s)*256
        visited={(18,0),(18,1)}
        for i,n in enumerate(['n/wizard','n/maker']):
            p=loc(18,1)+32*i;t,s=d[p+3:p+5];out=b''
            while t:
                self.assertNotIn((t,s),visited);visited.add((t,s));p=loc(t,s);nt,ns=d[p:p+2]
                out+=d[p+2:p+256 if nt else p+1+ns];t,s=nt,ns
            expected=apps.reviewed_files(self.source,self.pin)[n];self.assertEqual(out,expected)
        bam=loc(18,0)
        for track in range(1,36):
            p=bam+track*4;bits=int.from_bytes(d[p+1:p+4],'little')
            free=[s for s in range(sector_counts[track-1]) if (track,s) not in visited]
            self.assertEqual(d[p],len(free));self.assertEqual(bits,sum(1<<s for s in free))

    def test_hash_member_and_prg_rejection(self):
        self.source.write_bytes(self.source.read_bytes()+b'x')
        with self.assertRaises(ValueError):apps.payload(self.source,self.pin)
        self.pin=synthetic_source(self.source);self.pin['programs'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):apps.payload(self.source,self.pin)
        with self.assertRaises(ValueError):apps.disk([('SID-WIZARD',b'bad'),('SID-MAKER',b'bad')])

    def test_source_install_and_user_state_not_overwritten(self):
        raw=apps.payload(self.source,self.pin);target=self.root/'image';target.mkdir()
        paths=apps.install(target,raw);self.assertEqual(len(paths),4)
        user=target/'home/pcbm/content'/apps.CONTENT;user.write_bytes(b'user work')
        with self.assertRaises(ValueError):apps.install(target,raw)
        self.assertEqual(user.read_bytes(),b'user work')
        self.assertEqual(len(list(target.rglob('*.d64'))),2)

    def test_archive_paths_and_destination_symlink_refused(self):
        bad=io.BytesIO()
        with tarfile.open(fileobj=bad,mode='w') as t:
            m=tarfile.TarInfo('../escape');m.size=1;t.addfile(m,io.BytesIO(b'x'))
        with self.assertRaises(ValueError):apps.install(self.root,bad.getvalue())
        (self.root/'usr').symlink_to(self.root/'outside',target_is_directory=True)
        with self.assertRaises(ValueError):apps.install(self.root,apps.payload(self.source,self.pin))
        with self.assertRaises(ValueError):apps.install(Path('/'),apps.payload(self.source,self.pin))

    def test_frozen_payload_transitive_verification_rejects_tampering(self):
        pin=copy.deepcopy(self.pin)
        pin['origin']='https://csdb.dk/getinternalfile.php/281063/SID-Wizard-1.97-sources-examples.tar.gz'
        pinfile=self.root/'pin.json';pinfile.write_text(json.dumps(pin))
        kit=self.root/'kit';kit.mkdir()
        with patch.object(apps,'PIN',pinfile):
            entry=apps.freeze(self.source,kit)['sid_wizard']
            apps.verify_optional(kit,entry)
            descriptor=entry['artifact'];target=kit/descriptor['path']
            target.write_bytes(target.read_bytes()+b'changed')
            with self.assertRaises(ValueError):apps.verify_optional(kit,entry)

    def test_frozen_kit_and_object_redirect_refused(self):
        (self.root/'release-lock.json').write_text('{}')
        with self.assertRaises(ValueError):apps.freeze(self.source,self.root)
        (self.root/'release-lock.json').unlink();(self.root/'objects').symlink_to(self.root/'outside')
        with self.assertRaises(ValueError):apps.freeze(self.source,self.root)

    def test_lock_version_and_rights_allowlist(self):
        old=json.loads((ROOT/'tests/fixtures/release-lock.synthetic.json').read_text())
        artifact=old['integration']['source']
        entry={'version':'1.97','license':'LicenseRef-Hermit-WTF','origin':'https://csdb.dk/getinternalfile.php/281063/SID-Wizard-1.97-sources-examples.tar.gz',**{k:artifact for k in ['source','artifact','recipe','rights_review']}}
        validate_lock(encode(old),True)
        for version in (1,2):
            value=copy.deepcopy(old);value['schema_version']=version;value['optional_software']={'sid_wizard':entry}
            with self.assertRaises(ValueError):validate_lock(encode(value),True)
        value=copy.deepcopy(old);value['schema_version']=3;value['optional_software']={'sid_wizard':entry}
        validate_lock(encode(value),True)
        for key,val in [('license','freeware'),('version','1.8')]:
            bad=copy.deepcopy(value);bad['optional_software']['sid_wizard'][key]=val
            with self.assertRaises(ValueError):validate_lock(encode(bad),True)
        bad=copy.deepcopy(value);bad['optional_software']['striketerm']=entry
        with self.assertRaises(ValueError):validate_lock(encode(bad),True)

    def make_app(self,folder):
        p=self.root/folder/'test disk.d64';p.parent.mkdir(parents=True);p.write_bytes(apps.disk([('SID-WIZARD',b'\x01\x08hi'),('SID-MAKER',b'\x01\x08bye')]))
        return p

    def test_known_apps_route_to_registry_c64_without_preference_write(self):
        for folder in ['music/Creation/SID-Wizard','programs/Communications/StrikeTerm','music/c64/Creation/SID-Wizard','programs/c64/Communications/StrikeTerm']:
            p=self.make_app(folder)
            self.assertEqual(application_profile(p,registry(),self.root),'x64sc')
            with self.assertRaises(ValueError):application_profile(p,[],self.root)
        self.assertFalse((self.root/'preferences.json').exists())

    def test_ordinary_content_preserves_default_policy(self):
        p=self.root/'ordinary.prg';p.write_bytes(b'program')
        self.assertIsNone(application_profile(p,registry(),self.root))

    def test_invalid_application_media_and_path_rejected(self):
        p=self.make_app('programs/Communications/StrikeTerm')
        p.write_bytes(b'not a disk')
        with self.assertRaises(ValueError):application_profile(p,registry(),self.root)
        link=self.root/'link.d64';link.symlink_to(p)
        for value in [link,str(p)+'\n',str(self.root/'..'/'escape'),'/bin/sh']:
            with self.assertRaises(ValueError):application_profile(value,registry(),self.root)

    def test_cli_returns_only_valid_profile_no_preference_write(self):
        import contextlib
        for policy,expected in [('x64sc','x64sc'),(None,'xvic')]:
            out=io.StringIO()
            with patch('project_cbm.profiles.application_profile',return_value=policy),patch('project_cbm.profiles.preferences.selection',return_value={'id':'xvic'}),patch('project_cbm.preferences.update',side_effect=AssertionError('write')),patch('project_cbm.profiles.library.content_profile',return_value='xvic'),contextlib.redirect_stdout(out):
                self.assertEqual(profiles.main(['content-profile','/unused.d64']),0)
            self.assertEqual(out.getvalue(),expected+'\n')

    def test_staging_and_launcher_contract_statically_preserved(self):
        stage=(ROOT/'tools/install_poc_stage.py').read_text()
        self.assertIn("if 'optional_software' in lock:",stage)
        self.assertIn("verify_optional(args.kit",stage)
        menu=ROOT.parent/'project-cbm-menu'
        self.assertIn('pcbm-profiles content-profile "${files[$PCBM_CHOICE]}"',(menu/'scripts/pcbm-content').read_text())
        launcher=(menu/'scripts/pcbm-run-vice').read_text()
        for literal in ['pcbm-profiles resolve', '-menukey 291', 'args+=(-autostart "$1")', 'exec /usr/libexec/project-cbm/engineering.py run', 'SDL_AUDIODRIVER=alsa']:
            self.assertIn(literal,launcher)
