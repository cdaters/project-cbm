"""Fixture/unit tests: never an assertion of Raspberry Pi physical qualification."""
import copy
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runtime'))
from project_cbm import info, preferences
from project_cbm.data import registry, loads, LIMIT
from jsonschema import Draft202012Validator


class Fixture:
    def __init__(self, model='Raspberry Pi 3 Model B Rev 1.2'):
        self.files = {
            '/usr/share/project-cbm/identity.json': (ROOT / 'tests/fixtures/installed-identity.synthetic.json').read_text(),
            '/etc/os-release': 'ID=debian\nNAME="Debian GNU/Linux"\nPRETTY_NAME="Debian GNU/Linux 13 (trixie)"\nVERSION_ID="13"\nVERSION_CODENAME=trixie\nSECRET=do-not-export\n',
            '/etc/debian_version': '13.0\n', '/proc/device-tree/model': model + '\0',
            '/proc/device-tree/compatible': 'raspberrypi,example\0brcm,bcm2837\0',
            '/proc/cpuinfo': 'model name : ARMv8 Processor\nSerial : do-not-export\n',
            '/proc/meminfo': 'MemTotal: 948000 kB\nMemAvailable: 640000 kB\n',
            '/etc/pcbm/default-machine.conf': 'x64sc\n', '/etc/pcbm/boot-mode.conf': 'menu\n',
            '/sys/class/drm/card1-HDMI-A-1/status': 'connected\n',
            '/sys/class/drm/card1-HDMI-A-1/enabled': 'enabled\n',
            '/sys/class/net/eth0/operstate': 'up\n', '/sys/class/net/lo/operstate': 'unknown\n'}
        self.calls = []
        self.package_result = (0, 'project-cbm-menu\t1.0.0-1+pcbm1\tinstalled\nproject-cbm-vice\t3.10-1+pcbm3\tinstalled\nproject-cbm-tcpser\t1.1.6~beta-1+pcbm1\tinstalled\n')

    def read(self, path):
        if path not in self.files:
            raise FileNotFoundError(path)
        return self.files[path]

    def paths(self, pattern):
        import fnmatch
        return sorted(p for p in self.files if fnmatch.fnmatch(p, pattern))

    def exists(self, path):
        return path in self.files

    def uname(self):
        return dict(architecture='aarch64', kernel='6.12-fixture', hostname='cbm-fixture', system='Linux')

    def storage(self):
        return dict(total_bytes=16*1024**3, available_bytes=12*1024**3, free_bytes=13*1024**3)

    def command(self, args):
        self.calls.append(args)
        if args[0].endswith('/ip'):return 0, '[]'
        if args[0].endswith('/nmcli'):return 0, ''
        if args[0].endswith('dpkg-query'):
            return self.package_result
        return 0, '\n\n'.join('Id='+unit+'\nLoadState='+('not-found' if name=='tcpser' else 'masked')+'\nActiveState=inactive\nSubState=dead\nUnitFileState='+('' if name=='tcpser' else 'masked') for name,unit in info.SERVICES.items())


class Information(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.prefs = Path(self.tmp.name) / 'missing'
        self.source = Fixture()

    def collect(self):
        return info.collect(self.source, self.prefs)

    def test_relocated_command_without_menu_or_pythonpath(self):
        import shutil
        stage=Path(self.tmp.name)/'runtime';shutil.copytree(ROOT/'runtime',stage,ignore=shutil.ignore_patterns('__pycache__'))
        before={str(p.relative_to(stage)):p.read_bytes() for p in stage.rglob('*') if p.is_file()}
        result=subprocess.run([sys.executable,str(stage/'bin/pcbm-info'),'--json'],capture_output=True,text=True,check=True,env={'PATH':'/usr/bin:/bin','XDG_CONFIG_HOME':str(self.prefs)})
        self.assertEqual(json.loads(result.stdout)['format'],'project-cbm.info')
        self.assertFalse(self.prefs.exists())
        after={str(p.relative_to(stage)):p.read_bytes() for p in stage.rglob('*') if p.is_file()}
        self.assertEqual(before,after)

    def test_identity_and_current_package_distinction(self):
        d = self.collect()
        self.assertEqual(d['built_as']['components']['vice']['package_version'], '3.10-1+pcbm1')
        self.assertEqual(d['current_state']['packages']['vice']['version'], '3.10-1+pcbm3')
        self.assertTrue(all(call[0] in ('/usr/bin/dpkg-query', '/usr/bin/systemctl', '/usr/sbin/ip', '/usr/bin/nmcli') for call in self.source.calls))

    def test_schema_and_unknown_field_rejection(self):
        validator=Draft202012Validator(json.loads((ROOT/'schemas/info.schema.json').read_text()))
        data=self.collect();validator.validate(data)
        data['private_key']='forbidden'
        self.assertTrue(list(validator.iter_errors(data)))

    def test_secret_exclusion(self):
        d=json.loads(self.source.files['/usr/share/project-cbm/identity.json'])
        d['builder']={'private_key':'do-not-export'};d['components']['vice']['password']='do-not-export'
        self.source.files['/usr/share/project-cbm/identity.json']=json.dumps(d)
        raw=json.dumps(self.collect());self.assertNotIn('do-not-export',raw);self.assertNotIn('Serial',raw)

    def test_invalid_identity_and_duplicate_keys(self):
        for value in ['{}','{"schema_version":1,"schema_version":2}', '{"a":NaN}', '['*2000]:
            self.source.files['/usr/share/project-cbm/identity.json']=value
            self.assertIsNone(self.collect()['built_as'])
        with self.assertRaises(ValueError):loads('x'*(LIMIT+1))

    def test_invalid_component_type_and_missing_registry(self):
        d=json.loads(self.source.files['/usr/share/project-cbm/identity.json']);d['components']=[]
        self.source.files['/usr/share/project-cbm/identity.json']=json.dumps(d)
        self.assertIsNone(self.collect()['built_as'])
        with patch('project_cbm.info.registry',side_effect=ValueError('broken')):
            data=self.collect()
        self.assertEqual(data['running_on']['model'],'Raspberry Pi 3 Model B Rev 1.2')
        self.assertIsNone(data['current_state']['preferences'])
        Draft202012Validator(json.loads((ROOT/'schemas/info.schema.json').read_text())).validate(data)
        self.assertIn('unavailable',info.human(data))

    def test_unknown_identity_version(self):
        d=json.loads(self.source.files['/usr/share/project-cbm/identity.json']);d['schema_version']=2
        self.source.files['/usr/share/project-cbm/identity.json']=json.dumps(d)
        self.assertIsNone(self.collect()['built_as'])

    def test_model_fixtures_no_model_whitelist(self):
        cases=json.loads((ROOT/'tests/fixtures/info/hardware.json').read_text())
        for case in cases:
            with self.subTest(case['name']):
                self.source.files['/proc/device-tree/model']=case['model']+'\0'
                self.source.files['/proc/meminfo']=f"MemTotal: {case['usable_kib']} kB\n"
                d=self.collect();self.assertEqual(d['running_on']['model'],case['model'])
                self.assertEqual(d['running_on']['memory']['usable_total_bytes'],case['usable_kib']*1024)

    def test_os_quoting_no_execution_and_duplicate_rejection(self):
        self.assertEqual(info.os_release('NAME="Example OS"\nID=example')['name'],'Example OS')
        self.assertEqual(info.os_release('NAME="$(echo unsafe)"')['name'],'$(echo unsafe)')
        for s in ['ID=a\nID=b','NAME="bad','NAME="bad\x1b[31m"']:
            with self.assertRaises(ValueError):info.os_release(s)

    def test_os_fallback(self):
        self.source.files['/usr/lib/os-release']=self.source.files.pop('/etc/os-release')
        self.assertEqual(self.collect()['running_on']['os']['id'],'debian')

    def test_memory_storage(self):
        d=self.collect()['running_on'];self.assertEqual(d['memory']['usable_total_bytes'],948000*1024)
        self.assertEqual(d['root_storage']['available_bytes'],12*1024**3)
        self.source.files['/proc/meminfo']='MemTotal: 1 kB\nMemAvailable: 2 kB\n'
        self.assertIsNone(self.collect()['running_on']['memory'])

    def test_missing_data_still_useful_and_valid(self):
        self.source.files={}
        with patch.object(self.source,'command',side_effect=FileNotFoundError):
            d=self.collect()
        self.assertIsNone(d['built_as']);self.assertIsNone(d['current_state']['packages'])
        self.assertIsNone(d['running_on']['displays'])
        Draft202012Validator(json.loads((ROOT/'schemas/info.schema.json').read_text())).validate(d)
        self.assertIn('unknown',info.human(d));self.assertIn('aarch64',info.human(d))

    def test_headless_and_disabled_network(self):
        self.source.files['/sys/class/drm/card1-HDMI-A-1/status']='disconnected\n'
        self.source.files['/sys/class/net/eth0/operstate']='down\n'
        d=self.collect();self.assertEqual(d['running_on']['displays'],[])
        self.assertEqual(d['current_state']['network_links'],[{'interface':'eth0','operstate':'down'}])

    def test_no_advertised_mode_guess(self):
        self.source.files['/sys/class/drm/card1-HDMI-A-1/modes']='1920x1080\n'
        d=self.collect();self.assertIsNone(d['running_on']['displays'][0]['active_mode'])

    def test_optional_existing_engineering_drm_provider(self):
        self.source.files['/usr/libexec/project-cbm-vice/drm-state']='fixture'
        self.source.files['/etc/pcbm/engineering-poc']='fixture'
        self.source.files['/sys/class/drm/card1-HDMI-A-1/connector_id']='42'
        original=self.source.command
        raw=json.dumps({'connectors':[{'card':1,'connector_id':42,'active':{'width':1920,'height':1080,'refresh_hz':60},'private':'do-not-export'}]})
        def command(args):
            if args[0].endswith('/drm-state'):return 0,raw
            return original(args)
        with patch.object(self.source,'command',side_effect=command):
            d=self.collect()
        self.assertEqual(d['running_on']['displays'][0]['active_mode'],{'width':1920,'height':1080,'refresh_hz':60})
        self.assertNotIn('do-not-export',json.dumps(d))
        self.assertIn('1920x1080 @ 60 Hz',info.human(d))
        Draft202012Validator(json.loads((ROOT/'schemas/info.schema.json').read_text())).validate(d)
        with self.assertRaises(ValueError):info.drm_modes('{"connectors":[{"card":-1,"connector_id":42,"active":null}]}')

    def test_services_masked_vs_absent(self):
        s=self.collect()['current_state']['services']
        self.assertEqual(s['ssh']['UnitFileState'],'masked')
        self.assertEqual(s['tcpser']['LoadState'],'not-found')

    def test_packages_missing_and_not_installed(self):
        self.source.package_result=(1,'project-cbm-vice\t3.10-1\tconfig-files\n')
        d=self.collect()['current_state']['packages'];self.assertFalse(d['vice']['installed']);self.assertFalse(d['menu']['installed'])
        self.source.package_result=(2,'error')
        self.assertIsNone(self.collect()['current_state']['packages'])

    def test_timeout_and_environment(self):
        with patch('project_cbm.info.subprocess.run',side_effect=subprocess.TimeoutExpired('query',1)):
            with self.assertRaises(subprocess.TimeoutExpired):info.Local().command(['/usr/bin/dpkg-query'])
        with patch('project_cbm.info.subprocess.run') as runner:
            runner.return_value=subprocess.CompletedProcess([],0,'','')
            info.Local().command(['/usr/bin/dpkg-query'])
            kwargs=runner.call_args.kwargs
            self.assertEqual(kwargs['env']['LC_ALL'],'C');self.assertNotIn('HOME',kwargs['env'])
            self.assertFalse(kwargs.get('shell',False));self.assertEqual(kwargs['timeout'],1)

    def test_preferences_are_default_launcher_state_but_not_boot(self):
        preferences.update({'default_machine':'xvic'},self.prefs)
        d=self.collect()['current_state']
        self.assertEqual(d['preferences']['values']['default_machine'],'xvic')
        self.assertEqual(d['default_machine']['id'],'xvic')
        self.assertEqual(d['default_machine']['source'],'user')
        self.assertIsNone(d['boot_mode']['effective'])

    def test_human_output_and_read_only_collection(self):
        before=set(Path(self.tmp.name).iterdir());raw=info.human(self.collect())
        self.assertIn('SYNTHETIC FIXTURE',raw);self.assertIn('Commodore 64',raw)
        self.assertNotIn('/proc/',raw);self.assertNotIn('\x1b',raw)
        self.assertEqual(before,set(Path(self.tmp.name).iterdir()))


class Preferences(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'project-cbm';self.profiles=registry()

    def test_cli_show_set_and_validation_error(self):
        env={**os.environ,'XDG_CONFIG_HOME':self.tmp.name,'PYTHONDONTWRITEBYTECODE':'1'}
        command=[sys.executable,str(ROOT/'runtime/bin/pcbm-preferences')]
        shown=subprocess.run(command+['show'],env=env,text=True,capture_output=True,check=True)
        self.assertEqual(json.loads(shown.stdout)['status'],'default')
        self.assertFalse(self.path.exists())
        saved=subprocess.run(command+['set','default_machine','xvic'],env=env,text=True,capture_output=True,check=True)
        self.assertEqual(json.loads(saved.stdout)['default_machine'],'xvic')
        bad=subprocess.run(command+['set','default_machine','invalid'],env=env,text=True,capture_output=True)
        self.assertEqual(bad.returncode,2)
        self.assertEqual(preferences.read(self.path)['values']['default_machine'],'xvic')

    def test_defaults_no_write(self):
        self.assertEqual(preferences.read(self.path)['source'],'defaults');self.assertFalse(self.path.exists())

    def test_atomic_private_write_preserves_other_preference(self):
        preferences.update({'default_machine':'xvic'},self.path)
        preferences.update({'boot_preference':'emulator'},self.path)
        d=preferences.read(self.path);self.assertEqual(d['values']['default_machine'],'xvic')
        self.assertEqual(stat.S_IMODE((self.path/'preferences.json').stat().st_mode),0o600)
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode),0o700)
        self.assertEqual(d['values']['boot_preference'],'emulator')

    def test_validation_rejects_no_overwrite(self):
        preferences.update({},self.path);p=self.path/'preferences.json';old=p.read_bytes()
        for change in [{'default_machine':'/bin/sh'},{'boot_preference':'$(bad)'},{'password':'secret'}]:
            with self.assertRaises(ValueError):preferences.update(change,self.path)
            self.assertEqual(p.read_bytes(),old)

    def test_malformed_read_and_explicit_recovery(self):
        preferences.update({},self.path);p=self.path/'preferences.json';p.write_text('{bad')
        self.assertEqual(preferences.read(self.path)['status'],'invalid');self.assertEqual(p.read_text(),'{bad')
        with self.assertRaises(ValueError):preferences.update({},self.path)
        preferences.update({},self.path,recover=True)
        self.assertEqual(preferences.read(self.path)['status'],'ok')
        backups=list(self.path.glob('preferences.invalid.*'));self.assertEqual(len(backups),1)
        self.assertEqual(backups[0].read_text(),'{bad')

    def test_replace_failure_keeps_old_and_cleans_temp(self):
        preferences.update({},self.path);p=self.path/'preferences.json';old=p.read_bytes()
        with patch('project_cbm.preferences.os.replace',side_effect=OSError('simulated')):
            with self.assertRaises(OSError):preferences.update({'default_machine':'xvic'},self.path)
        self.assertEqual(p.read_bytes(),old);self.assertEqual(list(self.path.glob('.preferences.*')), [self.path/'.preferences.lock'])

    def test_repair_interruption_can_retry(self):
        preferences.update({},self.path);p=self.path/'preferences.json';p.write_text('{bad')
        with patch('project_cbm.preferences.os.replace',side_effect=OSError('simulated')):
            with self.assertRaises(OSError):preferences.update({},self.path,recover=True)
        self.assertEqual(p.read_text(),'{bad');preferences.update({},self.path,recover=True)
        self.assertEqual(preferences.read(self.path)['status'],'ok')

    def test_symlink_refused_without_following(self):
        self.path.mkdir(mode=0o700);target=Path(self.tmp.name)/'target';target.write_text('unchanged')
        (self.path/'preferences.json').symlink_to(target)
        self.assertEqual(preferences.read(self.path)['status'],'invalid')
        with self.assertRaises(OSError):preferences.update({},self.path)
        self.assertEqual(target.read_text(),'unchanged')

    def test_shared_directory_refused(self):
        self.path.mkdir(mode=0o755)
        with self.assertRaises(ValueError):preferences.update({},self.path)

    def test_root_write_refused(self):
        with patch('project_cbm.preferences.os.geteuid',return_value=0):
            with self.assertRaises(ValueError):preferences.update({},self.path)
        self.assertFalse(self.path.exists())

    def test_schema_unknown_version_and_duplicate(self):
        for v in [True,2]:
            d=preferences.defaults(self.profiles);d['schema_version']=v
            with self.assertRaises(ValueError):preferences.validate(d,self.profiles)
        with self.assertRaises(ValueError):loads('{"a":1,"a":2}')
        Draft202012Validator(json.loads((ROOT/'schemas/preferences.schema.json').read_text())).validate(preferences.defaults(self.profiles))

    def test_xdg_relative_falls_back(self):
        with patch.dict(os.environ,{'XDG_CONFIG_HOME':'relative'}),patch('project_cbm.preferences.Path.home',return_value=Path('/example')):
            self.assertEqual(preferences.location(),Path('/example/.config/project-cbm'))

    def test_lock_contention(self):
        preferences.update({},self.path)
        import fcntl
        with (self.path/'.preferences.lock').open('r+') as stream:
            fcntl.flock(stream,fcntl.LOCK_EX|fcntl.LOCK_NB)
            with self.assertRaises(BlockingIOError):preferences.update({},self.path)


class Registry(unittest.TestCase):
    def test_profile_coverage_and_schema(self):
        p=registry();self.assertEqual(len(p),11)
        self.assertEqual(sum(v['recommended'] for v in p),1)
        self.assertEqual(set(v['id'] for v in p),{'x64','x64sc','xscpu64','x64dtv','x128','x128-80col','xcbm2','xcbm5x0','xvic','xplus4','xpet'})
        Draft202012Validator(json.loads((ROOT/'schemas/machine-profiles.schema.json').read_text())).validate(json.loads((ROOT/'runtime/data/profiles.json').read_text()))
        enum=json.loads((ROOT/'schemas/preferences.schema.json').read_text())['properties']['default_machine']['enum']
        self.assertEqual(set(enum),{v['id'] for v in p})

    def test_duplicate_and_unsafe_executable_rejected(self):
        data=json.loads((ROOT/'runtime/data/profiles.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'profiles.json'
            d=copy.deepcopy(data);d['profiles'].append(d['profiles'][0]);path.write_text(json.dumps(d))
            with self.assertRaises(ValueError):registry(path)
            d=copy.deepcopy(data);d['profiles'][0]['executable']='/bin/sh';path.write_text(json.dumps(d))
            with self.assertRaises(ValueError):registry(path)


if __name__=='__main__':unittest.main()
