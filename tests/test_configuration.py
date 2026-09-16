"""Configuration security/behavior fixtures. No real root or service operations."""
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'runtime'))
from project_cbm import configuration as c, config_backend as b, config_client as client, admin, info
from test_runtime_foundation import Fixture
from jsonschema import Draft202012Validator


def req(op,**values):return {'schema_version':1,'operation':op,'values':values}
POLICY={'schema_version':1,'owner_user':'owner_fixture','appliance_user':'pi','system_ready':True,'network_ready':True,'ready_services':list(c.SERVICES)}
CASES=[req('hostname',value='cbm-fixture'),req('locale',value='en_US.UTF-8'),req('timezone',value='America/Phoenix'),
       req('keyboard',value='us'),req('wifi-country',value='US'),req('network',enabled=False),
       req('wifi-enroll',ssid='CBM Test',password='fixture-wifi-pass'),req('sharing-password',password='fixture-samba-pass'),
       req('service',service='ssh',enabled=True),req('modem',port=25232,baud=2400),req('power',action='reboot')]


class FakeLinux:
    def __init__(self):self.calls=[];self.writes={};self.good=True;self.allowed=True;self.country=True
    def run(self,args,stdin=None):self.calls.append((args,stdin));return self.good
    def listed(self,kind,value):return self.allowed
    def ssh_keys(self):return self.good
    def modem(self,values):self.writes["/etc/project-cbm/modem.json"]=values;return self.good
    def country_ready(self):return self.country
    def credential_ready(self, user):return self.allowed
    def keyboard(self, value):self.calls.append((['keyboard-next-boot',value],None));return self.good
    def write(self,path,data):self.writes[path]=data


class Configuration(unittest.TestCase):
    def test_valid_requests_and_results(self):
        for request in CASES:
            with self.subTest(request['operation']):
                self.assertEqual(c.decode(json.dumps(request)),request)
                system=FakeLinux();answer=b.apply(request,POLICY,system)
                self.assertIn(answer['status'],('ok','saved_pending','saved_restart'))
                self.assertNotIn('fixture-wifi-pass',json.dumps(answer));self.assertNotIn('fixture-samba-pass',json.dumps(answer))

    def test_arbitrary_operation_units_paths_and_shell_rejected(self):
        for request in [req('command',value='id'),req('mount',path='/dev/sda'),req('usb-mount',device='/dev/root'),
                        req('hostname',value='--help'),req('hostname',value='cbm; touch marker'),req('hostname',value='$(id)'),
                        req('service',service='sshd.service',enabled=True),req('service',service='evil',enabled=True),
                        req('service',service=['ssh'],enabled=True),req('service',service='ssh',enabled='yes'),
                        req('timezone',value='../../etc/shadow'),req('timezone',value='/etc/passwd'),req('keyboard',value='../../keymap'),
                        req('locale',value='LANG=en_US.UTF-8'),req('wifi-country',value='US;id'),req('power',action='rescue'),
                        req('modem',port=22,baud=2400),req('modem',port=25232,baud=123),req('network',enabled=1)]:
            with self.subTest(request):
                system=FakeLinux()
                with self.assertRaises(ValueError):b.apply(request,POLICY,system)
                self.assertFalse(system.calls);self.assertFalse(system.writes)

    def test_duplicate_unknown_and_oversized_input(self):
        for raw in ['{}','{"schema_version":1,"schema_version":1}', '['*5000, 'x'*4097, '{"a":NaN}']:
            with self.assertRaises(ValueError):c.decode(raw)
        d=copy.deepcopy(CASES[0]);d['values']['path']='/tmp/x'
        with self.assertRaises(ValueError):c.validate(d)

    def test_no_operations_before_activation(self):
        p={**POLICY,'system_ready':False}
        for request in CASES:
            system=FakeLinux();self.assertEqual(b.apply(request,p,system)['status'],'pending')
            self.assertFalse(system.calls);self.assertFalse(system.writes)

    def test_network_and_service_readiness_separate(self):
        for request in [req('network',enabled=True),req('wifi-country',value='US'),CASES[6]]:
            system=FakeLinux();self.assertEqual(b.apply(request,{**POLICY,'network_ready':False},system)['status'],'pending');self.assertFalse(system.calls)
        for name in c.SERVICES:
            system=FakeLinux();self.assertEqual(b.apply(req('service',service=name,enabled=True),{**POLICY,'ready_services':[]},system)['status'],'pending')
            self.assertFalse(system.calls)

    def test_service_enable_disable_exact_allowlist_no_unmask(self):
        for name,unit in c.SERVICES.items():
            for enabled in [False,True]:
                system=FakeLinux();b.apply(req('service',service=name,enabled=enabled),POLICY,system)
                expected=['/usr/bin/systemctl','--no-ask-password','enable' if enabled else 'disable','--now',unit]
                if name=='discovery':expected.append('avahi-daemon.socket')
                self.assertEqual(system.calls,[(expected,None)])

    def test_failure_not_reported_as_success(self):
        for request in CASES:
            if request['operation']=='modem':continue
            system=FakeLinux();system.good=False
            self.assertEqual(b.apply(request,POLICY,system)['status'],'failed')

    def test_locale_timezone_keyboard_country_membership(self):
        for op,value in [('locale','xx_XX.UTF-8'),('timezone','Not/AZone'),('keyboard','unknown'),('wifi-country','ZZ')]:
            system=FakeLinux();system.allowed=False
            self.assertIn(b.apply(req(op,value=value),POLICY,system)['status'],('invalid','unavailable'))
            self.assertFalse(system.calls)

    def test_wifi_secrets_only_in_fixed_private_file(self):
        secret='fixture-WiFi !#=;\\pass'
        request=req('wifi-enroll',ssid='Test #=; WiFi',password=secret)
        system=FakeLinux();self.assertEqual(b.apply(request,POLICY,system)['status'],'ok')
        self.assertNotIn(secret,str(system.calls));self.assertEqual(list(system.writes),['/etc/NetworkManager/system-connections/pcbm-wifi.nmconnection'])
        data=next(iter(system.writes.values()));self.assertIn('psk=',data);self.assertIn('uuid='+c.WIFI_UUID,data)
        self.assertEqual(system.calls[-1][0][-2:],['uuid',c.WIFI_UUID])
        self.assertIn(('/usr/bin/nmcli'),system.calls[0][0])
        system=FakeLinux();system.country=False
        self.assertEqual(b.apply(request,POLICY,system)['status'],'invalid');self.assertFalse(system.writes)
        for ssid in ['x\n[ipv4]\nmethod=manual','', 'x'*33,'1;2;3;']:
            with self.assertRaises(ValueError):c.validate(req('wifi-enroll',ssid=ssid,password=secret))

    def test_samba_credential_is_separate_and_stdin_only(self):
        system=FakeLinux();b.apply(req('sharing-password',password='fixture-samba-pass'),POLICY,system)
        self.assertEqual(system.calls[0][0],['/usr/bin/smbpasswd','-s','-a','pi'])
        self.assertEqual(system.calls[0][1],'fixture-samba-pass\nfixture-samba-pass\n')
        self.assertNotIn('passwd',system.calls[0][0][0].split('/')[-1].replace('smbpasswd',''))

    def test_root_entry_is_isolated_zero_argument(self):
        entry=(ROOT/'runtime/libexec/pcbm-config-root').read_text()
        self.assertTrue(entry.startswith('#!/usr/bin/python3 -I'))
        self.assertIn("'/usr/share/project-cbm/runtime'",entry)
        sudo=(ROOT/'runtime/config/sudoers.example').read_text()
        self.assertIn('/usr/libexec/pcbm-config-root ""',sudo)
        self.assertNotIn('NOPASSWD: ALL',sudo)
        for generic in ['/bin/sh','/bin/bash','/usr/bin/systemctl','/usr/bin/tee','/bin/mount']:
            self.assertNotIn(generic,sudo)
        self.assertIn('!log_input',sudo)

    def test_client_no_credentials_in_arguments_environment_or_result(self):
        request=CASES[6];calls=[]
        def fake(args,**kwargs):calls.append((args,kwargs));return subprocess.CompletedProcess(args,0,json.dumps(c.result('ok')),'secret leak should not escape')
        answer=client.submit(request,fake)
        self.assertEqual(answer['status'],'ok');self.assertEqual(calls[0][0],['/usr/bin/sudo','-n','--','/usr/libexec/pcbm-config-root'])
        self.assertNotIn(request['values']['password'],str(calls[0][0])+str(calls[0][1]['env'])+str(answer))
        self.assertIn(request['values']['password'],calls[0][1]['input'])

    def test_client_error_and_untrusted_messages_are_redacted(self):
        for code,body in [(1,'bad secret-data'),(0,json.dumps({**c.result('ok'),'message':'secret-data'})),(2,json.dumps(c.result('ok')))]:
            def fake(args,**kwargs):return subprocess.CompletedProcess(args,code,body,'secret-data')
            answer=client.submit(CASES[0],fake)
            self.assertNotIn('secret-data',json.dumps(answer))
        def fail(*a,**k):raise subprocess.TimeoutExpired('secret-data',75)
        self.assertNotIn('secret-data',str(client.submit(CASES[0],fail)))

    def test_os_runner_has_no_shell_or_log_output(self):
        with patch('project_cbm.config_backend.subprocess.run') as run:
            run.return_value.returncode=0
            self.assertTrue(b.Linux().run(['/usr/bin/smbpasswd','-s','-a','pi'],stdin='fixture-secret'))
            k=run.call_args.kwargs
            self.assertEqual(k['stdout'],subprocess.DEVNULL);self.assertEqual(k['stderr'],subprocess.DEVNULL)
            self.assertNotIn('shell',k);self.assertEqual(k['env']['HOME'],'/run/project-cbm')

    def test_admin_paths_authenticate_without_broad_passwordless_api(self):
        self.assertEqual(admin.command('terminal','owner_fixture'),['/bin/su','--login','owner_fixture'])
        self.assertEqual(admin.command('owner','owner_fixture'),['/bin/su','--login','owner_fixture'])
        self.assertEqual(admin.command('raspi-config','owner_fixture')[-1],'sudo -k -- /usr/bin/raspi-config')
        with self.assertRaises(ValueError):admin.command('arbitrary')
        with patch('project_cbm.admin.policy',side_effect=FileNotFoundError),patch('project_cbm.admin.subprocess.call') as call,contextlib.redirect_stderr(io.StringIO()),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(admin.main(['owner']),2);call.assert_not_called()

    def test_policy_rejects_bad_ownership_and_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'policy.json';p.write_text(json.dumps(POLICY))
            with self.assertRaises(ValueError):b.trusted(p)
            for field,value in [('owner_user','root'),('owner_user','pi'),('system_ready','yes'),('ready_services',['arbitrary.service'])]:
                p.write_text(json.dumps({**POLICY,field:value}))
                with patch('project_cbm.config_backend.POLICY',p),patch('project_cbm.config_backend.trusted',lambda x:x):
                    with self.assertRaises(ValueError):b.policy()

    def test_private_config_not_collected_by_info_or_diagnostics(self):
        f=Fixture();f.files['/etc/NetworkManager/system-connections/pcbm-wifi.nmconnection']='fixture-private-secret'
        f.files['/etc/project-cbm/modem.json']='fixture-private-secret'
        with tempfile.TemporaryDirectory() as tmp:data=info.collect(f,Path(tmp)/'none')
        self.assertNotIn('fixture-private-secret',json.dumps(data))
        diagnostics=(ROOT/'build/pigen/stage-cbm/files/engineering.py').read_text()
        for path in ['/etc/NetworkManager/system-connections','smbpasswd','/etc/project-cbm/modem.json']:self.assertNotIn(path,diagnostics)

    def test_schema_contracts(self):
        for name in ['configuration-request','configuration-result','configuration-policy']:
            schema=json.loads((ROOT/'schemas'/f'{name}.schema.json').read_text());Draft202012Validator.check_schema(schema)
            validator=Draft202012Validator(schema)
            cases=CASES if name=='configuration-request' else [POLICY] if name=='configuration-policy' else [c.result(k) for k in c.RESULTS]
            for case in cases:validator.validate(case)

    def test_fixed_file_atomicity_and_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'managed';p.write_text('old')
            with patch('project_cbm.config_backend.trusted',lambda x:x):
                with patch('project_cbm.config_backend.os.replace',side_effect=OSError('fixture')):
                    with self.assertRaises(OSError):b.Linux().write(p,'new')
                self.assertEqual(p.read_text(),'old');self.assertFalse(list(Path(tmp).glob('.pcbm-*')))
                b.Linux().write(p,'new')
            self.assertEqual(p.read_text(),'new');self.assertEqual(p.stat().st_mode&0o777,0o600)

    def test_backend_arguments_and_privilege_refused_before_execution(self):
        for argv,uid in [(['helper','--shell'],0),(['helper'],1000)]:
            with patch('sys.argv',argv),patch('project_cbm.config_backend.os.geteuid',return_value=uid),patch('project_cbm.config_backend.policy') as pol,contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(b.main(),2);pol.assert_not_called()
                self.assertEqual(json.loads(output.getvalue())['status'],'invalid')

    def test_sharing_requires_its_own_credential(self):
        system=FakeLinux();system.allowed=False
        self.assertEqual(b.apply(req('service',service='sharing',enabled=True),POLICY,system)['status'],'credentials_required')
        self.assertFalse(system.calls)

    def test_debian_keyboard_preserves_other_settings_and_never_forces_tty(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'keyboard'
            path.write_text('# owner comment\nXKBMODEL="pc105"\nXKBLAYOUT="us"\nXKBOPTIONS=""\n')
            with patch('project_cbm.config_backend.trusted',lambda p:path),patch.object(b.Linux,'write') as write,patch.object(b.Linux,'run',return_value=True) as run:
                self.assertTrue(b.Linux().keyboard('gb'))
                text=write.call_args.args[1]
                self.assertIn('XKBMODEL="pc105"',text);self.assertIn('# owner comment',text)
                self.assertEqual(text.count('XKBLAYOUT='),1);self.assertIn('XKBLAYOUT="gb"',text)
                self.assertEqual(run.call_args.args[0],['/usr/bin/setupcon','--save-only','--keyboard-only'])
