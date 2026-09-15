"""Host-only contract tests; synthetic inputs never represent a built candidate."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import build_contracts as cb

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests/fixtures/release-lock.synthetic.json'


class Contracts(unittest.TestCase):
    def setUp(self):
        self.raw = FIXTURE.read_bytes()
        self.lock = cb.loads(self.raw)

    def test_schemas_are_valid_draft202012(self):
        for path in (ROOT / 'schemas').glob('*.schema.json'):
            cb.Draft202012Validator.check_schema(cb.loads(path.read_bytes()))

    def test_fixture_requires_explicit_permission(self):
        with self.assertRaises(ValueError):
            cb.validate_lock(self.raw)
        cb.validate_lock(self.raw, allow_fixture=True)

    def test_invalid_json(self):
        for data in [b'{"a":1,"a":2}', b'{"a":{"x":1,"x":2}}', b'{"a":NaN}',
                     b'{"a":Infinity}', b'{"a":1.0}', b'\xef\xbb\xbf{}', b'\xff', b'{}junk']:
            with self.subTest(data=data), self.assertRaises(ValueError):
                cb.loads(data)

    def test_mutations_rejected(self):
        changes = [
            (['schema_version'], 2), (['schema_version'], True),
            (['architecture'], 'amd64'), (['image_sha256'], 'a'*64),
            (['qualification'], {}), (['self_sha256'], 'a'*64),
            (['builder_private'], {'hostname': 'fixture-secret'}),
            (['base','pi_gen','git','commit'], 'main'),
            (['base','suite'], 'bookworm'),
            (['base','stages'], ['stage0','stage1','stage2','stage5']),
            (['components','menu','source','git','ref'], 'refs/heads/main'),
            (['components','menu','source','git','ref'], 'refs/tags/v9.9.9'),
            (['components','menu','source','git','commit'], 'bad'),
            (['components','menu','package','version'], '9.0-1'),
            (['components','menu','package','upstream_version'], '9.0'),
            (['components','menu','package','architecture'], 'arm64'),
            (['components','vice','version'], '3.9'),
            (['components','vice','package','name'], 'wrong-package'),
            (['components','vice','build_options'], ['--enable-gtk3ui']),
            (['integration','source','sha256'], 'A'*64),
            (['integration','source','sha256'], 'a'*63),
            (['integration','source','size_bytes'], 0),
            (['integration','source','size_bytes'], True),
            (['integration','source','path'], '/private/tmp/source'),
            (['integration','source','path'], '../escape'),
            (['integration','source','path'], 'inputs/../escape'),
            (['integration','source','path'], 'inputs//source'),
            (['integration','source','path'], 'inputs/source/'),
            (['integration','source','path'], 'inputs/%2e%2e/source'),
            (['integration','git','repository'], 'https://user:secret@example.invalid/a'),
            (['integration','git','repository'], 'https://example.invalid/a?token=x'),
            (['integration','git','repository'], 'file:///private/source'),
            (['configuration','schema_version'], 0),
            (['build','environment_contract_version'], 2),
        ]
        for path, value in changes:
            with self.subTest(path=path, value=value):
                lock = copy.deepcopy(self.lock)
                target = lock
                for part in path[:-1]: target = target[part]
                target[path[-1]] = value
                with self.assertRaises(ValueError):
                    cb.validate_lock(cb.encode(lock), allow_fixture=True)

    def test_missing_pins_and_package_hashes(self):
        for path in [('components','menu','source','git'), ('components','menu','source','artifact'),
                     ('components','tcpser','source','git'), ('components','vice','package','artifact')]:
            with self.subTest(path=path):
                lock=copy.deepcopy(self.lock); target=lock
                for part in path[:-1]: target=target[part]
                del target[path[-1]]
                with self.assertRaises(ValueError): cb.validate_lock(cb.encode(lock), allow_fixture=True)

    def test_legacy_worksheet_fails(self):
        raw=(ROOT/'docs/recovery-contract.example.json').read_bytes()
        with self.assertRaises(ValueError): cb.validate_lock(raw, allow_fixture=True)

    def test_identity_is_small_allowlisted_projection(self):
        identity=cb.make_identity(self.raw, allow_fixture=True)
        cb.validate_identity(identity)
        self.assertEqual(identity['build_id'], hashlib.sha256(self.raw).hexdigest())
        self.assertEqual(identity['integration_commit'], self.lock['integration']['git']['commit'])
        self.assertEqual(identity['components']['menu']['version'], '1.0.0')
        self.assertLess(len(cb.encode(identity)), 4096)
        for field in ['source','path','build_options','bootstrap','private_key','hostname','qualification']:
            self.assertNotIn('"'+field+'"', cb.encode(identity).decode())
        self.assertEqual(cb.encode(identity),cb.encode(cb.make_identity(self.raw, allow_fixture=True)))
        self.assertEqual(cb.encode(identity), (ROOT/'tests/fixtures/installed-identity.synthetic.json').read_bytes())

    def test_identity_unknown_private_or_output_fields_rejected(self):
        identity=cb.make_identity(self.raw, allow_fixture=True)
        for key in ['private_key','home','hostname','full_lock','image_sha256','release_manifest_sha256']:
            with self.subTest(key=key):
                bad=copy.deepcopy(identity);bad[key]='fixture-secret'
                with self.assertRaises(ValueError): cb.validate_identity(bad)
        bad=copy.deepcopy(identity);bad['components']['menu']['source']={}
        with self.assertRaises(ValueError): cb.validate_identity(bad)
        bad=copy.deepcopy(identity);bad['manifest_lookup']['build_id']='a'*64
        with self.assertRaises(ValueError): cb.validate_identity(bad)

    def test_hash_scope_is_exact_lock_bytes(self):
        a=cb.make_identity(self.raw,allow_fixture=True)
        b=cb.make_identity(self.raw+b'\n',allow_fixture=True)
        self.assertNotEqual(a['build_id'],b['build_id'])

    def test_artifact_resolution_is_offline_and_contained(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'inputs').mkdir();(root/'inputs/source').write_bytes(b'x')
            a={'path':'inputs/source','size_bytes':1,'sha256':hashlib.sha256(b'x').hexdigest()}
            cb.verify_artifact(root,a)
            for field,value in [('size_bytes',2),('sha256','0'*64),('path','missing')]:
                bad=dict(a);bad[field]=value
                with self.assertRaises(ValueError):cb.verify_artifact(root,bad)
            (root/'inputs/link').symlink_to('/etc/passwd')
            with self.assertRaises(ValueError): cb.verify_artifact(root,{**a,'path':'inputs/link'})

    def test_cli_has_no_write_side_effect(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/build_contracts.py'),'identity',str(FIXTURE),'--allow-fixture'],capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(cb.loads(result.stdout)['format'],'project-cbm.image-identity')
        bad=subprocess.run([sys.executable,str(ROOT/'tools/build_contracts.py'),'identity',str(FIXTURE)],capture_output=True)
        self.assertNotEqual(bad.returncode,0)
        self.assertEqual(bad.stdout,b'')


class PreservedRefs(unittest.TestCase):
    def test_product_release_tag(self):
        value = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'refs/tags/v1.0.0'], text=True).strip()
        self.assertEqual(value, '46fbf47d66596b2f3d0f6ab53d26bdd90632c73c')

    def test_menu_release_and_recovery_tags(self):
        menu = ROOT.parent / 'project-cbm-menu'
        if not (menu / '.git').exists():
            self.skipTest('companion checkout unavailable; verify against recovery catalog separately')
        for ref, expected in {
            'refs/tags/v1.0.0': '0756331cf872dfeaec17bdb75939f84e47e04f9f',
            'refs/tags/v1.0.0^{}': '399c6158caa8ed2762744d512c1841b94ad64403',
            'refs/tags/recovered/image-v1.0.0-runtime': '21ae1d2b8d595f0339295351bd34fcea44a78db4',
            'refs/tags/recovered/image-v1.0.0-runtime^{}': 'a4148db54001790eaddb4e31104917c16149b181',
        }.items():
            with self.subTest(ref=ref):
                value = subprocess.check_output(['git', '-C', str(menu), 'rev-parse', ref], text=True).strip()
                self.assertEqual(value, expected)


class Workspace(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.mount=Path(self.temp.name).resolve();self.work=self.mount/'bulk';self.work.mkdir()
        self.config={'format':'project-cbm.workspace-config','schema_version':1,'mountpoint':str(self.mount),
                     'workspace':str(self.work),'workspace_id':'test-bulk','minimum_free_bytes':1}
        (self.work/'.project-cbm-workspace.json').write_bytes(cb.encode({'workspace_id':'test-bulk'}))

    def check(self):return cb.check_workspace(self.config)

    def test_refuses_missing_mount_without_creating_anything(self):
        before=list(self.mount.rglob('*'))
        with patch.object(cb.os.path,'ismount',return_value=False),self.assertRaises(ValueError):self.check()
        self.assertEqual(before,list(self.mount.rglob('*')))

    def test_valid_and_negative_configurations(self):
        with patch.object(cb.os.path,'ismount',return_value=True):
            self.assertEqual(self.check(),self.work)
            for key,value in [('mountpoint','/'),('workspace_id','wrong'),('workspace',str(self.mount/'missing')),('workspace','relative'),
                              ('workspace',str(self.work/'..'/'bulk')),('minimum_free_bytes',10**30),('minimum_free_bytes',0)]:
                with self.subTest(key=key):
                    config={**self.config,key:value}
                    with self.assertRaises(ValueError):cb.check_workspace(config)
            (self.mount/'alias').symlink_to(self.work,target_is_directory=True)
            with self.assertRaises(ValueError):cb.check_workspace({**self.config,'workspace':str(self.mount/'alias')})
            with self.assertRaises(ValueError):cb.check_workspace({**self.config,'workspace':'/private/tmp'})
            (self.work/'.project-cbm-workspace.json').unlink()
            with self.assertRaises(ValueError):self.check()


if __name__=='__main__':unittest.main()
