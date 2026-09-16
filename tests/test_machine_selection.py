"""Product authority and migration tests; no Linux/VICE/hardware execution."""
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'runtime'))
from project_cbm import preferences, profiles
from project_cbm.data import registry


class Selection(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'config'
        self.rows = registry()

    def select(self, legacy=''):
        return preferences.selection(self.path, self.rows, legacy)

    def test_missing_read_has_no_side_effect_and_recommended_default(self):
        self.assertEqual(self.select()['id'], 'x64sc')
        self.assertEqual(self.select()['source'], 'defaults')
        self.assertFalse(self.path.exists())

    def test_legacy_import_and_precedence(self):
        self.assertEqual(self.select('x128-80col\n')['id'], 'x128-80col')
        preferences.initialize(self.path, self.rows, 'x128-80col\n')
        self.assertEqual(self.select('xvic')['id'], 'x128-80col')
        preferences.update({'default_machine':'xpet'}, self.path)
        preferences.initialize(self.path, self.rows, 'x64')
        self.assertEqual(self.select()['id'], 'xpet')
        self.assertEqual(self.select()['source'], 'user')

    def test_original_legacy_file_unchanged(self):
        old=Path(self.tmp.name)/'legacy';old.write_text('xvic\n')
        with patch('project_cbm.preferences.LEGACY_MACHINE', old):
            preferences.initialize(self.path, self.rows)
        self.assertEqual(old.read_bytes(), b'xvic\n')
        self.assertEqual(self.select()['id'], 'xvic')

    def test_invalid_legacy_not_executed(self):
        for raw in ['xunknown','/usr/bin/x64sc','x64sc; touch BAD','$(touch BAD)','x64sc\nxvic','xvic'*100]:
            self.assertEqual(self.select(raw)['id'], 'x64sc')

    def test_invalid_new_state_preserved_and_explicit_recovery(self):
        self.path.mkdir(mode=0o700); f=self.path/'preferences.json'
        f.write_text('{broken'); f.chmod(0o600)
        self.assertEqual(self.select('xvic')['id'], 'xvic')
        preferences.initialize(self.path,self.rows,'xvic')
        self.assertEqual(f.read_text(),'{broken')
        with self.assertRaises(ValueError):preferences.update({'default_machine':'xpet'},self.path)
        preferences.update({'default_machine':'xpet'},self.path,recover=True)
        self.assertEqual(self.select('xvic')['id'],'xpet')
        self.assertEqual(next(self.path.glob('preferences.invalid.*')).read_text(),'{broken')

    def test_concurrent_initialization_never_overwrites_user_choice(self):
        preferences.update({'default_machine':'xpet'},self.path)
        preferences.update({},self.path,initialize='xvic')
        self.assertEqual(self.select()['id'],'xpet')

    def test_all_launches_have_bounded_fields(self):
        for row in self.rows:
            out=io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(profiles.main(['resolve',row['id'],'--launch-fields']),0)
            self.assertEqual(out.getvalue().splitlines(),[row['executable'],*row['launch_options']])
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(profiles.main(['resolve','/bin/sh','--launch-fields']),2)

    def test_registry_rejects_executable_injection_and_flag_drift(self):
        for change in [{'id':'xevil','executable':'xevil'}, {'executable':'/bin/sh'}, {'launch_options':['-config','/tmp/evil']}, {'cover_asset':'../../evil'}, {'name':'bad\tname'}]:
            d={'schema_version':1,'profiles':json.loads(json.dumps(self.rows))};d['profiles'][0].update(change)
            p=Path(self.tmp.name)/'profiles.json';p.write_text(json.dumps(d))
            with self.assertRaises(ValueError):registry(p)

    def test_menu_contract_is_registry_driven_and_current(self):
        with patch.dict(os.environ, {'XDG_CONFIG_HOME':self.tmp.name}):
            preferences.update({'default_machine':'xvic'})
            out=io.StringIO()
            with contextlib.redirect_stdout(out):self.assertEqual(profiles.main(['menu']),0)
        lines=[x.split('\t') for x in out.getvalue().splitlines()]
        self.assertEqual(lines[0],['state','xvic','Commodore VIC-20','ok'])
        self.assertEqual([x[1] for x in lines[1:]],[p['id'] for p in self.rows])
        self.assertTrue(all(len(x)==4 for x in lines))

    def test_cli_recovery_requires_explicit_confirmation(self):
        with patch.dict(os.environ, {'XDG_CONFIG_HOME':self.tmp.name}), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(preferences.main(['set','default_machine','xvic','--recover']),2)
            self.assertFalse((Path(self.tmp.name)/'project-cbm').exists())

    def test_info_uses_one_atomic_preference_snapshot(self):
        from project_cbm import info
        from test_runtime_foundation import Fixture
        preferences.update({'default_machine':'xpet'},self.path)
        original=preferences.read
        with patch('project_cbm.preferences.read', wraps=original) as reader:
            d=info.collect(Fixture(),self.path)
        self.assertEqual(reader.call_count,1)
        self.assertEqual(d['current_state']['default_machine']['id'],d['current_state']['preferences']['values']['default_machine'])
