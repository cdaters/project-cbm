"""Appliance status is actual, bounded and credential-free; OS boundary is injected."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from project_cbm import service_info as s,info,config_backend as b,configuration as c
from jsonschema import Draft202012Validator

class Source:
    def __init__(self):self.calls=[]
    def exists(self,path):return path.endswith('sharing-status.json')
    def uname(self):return {'hostname':'projectcbm'}
    def read(self,path):
        if path.endswith('configuration-policy.json'):return json.dumps({'owner_user':'pcbm'})
        if path.endswith('sharing-status.json'):return json.dumps({'schema_version':1,'username':'pcbm','password_set':True})
        if path.endswith('modem.json'):return '{"port":25232}'
        raise FileNotFoundError()
    def command(self,args):
        self.calls.append(args)
        if args[0].endswith('/ip'):return 0,'[]'
        if args[0].endswith('nmcli'):return 0,''
        if args[0].endswith('ss'):return 0,'tcp LISTEN 0 128 0.0.0.0:22 0.0.0.0:*\nudp UNCONN 0 0 [::]:5353 [::]:*\n'
        return 0,'\n\n'.join('Id='+u+'\nLoadState=loaded\nActiveState='+('active' if n in ('ssh','discovery') else 'inactive')+'\nSubState=running\nUnitFileState='+('enabled' if n in ('ssh','discovery') else 'disabled') for n,u in s.UNITS.items())

class Services(unittest.TestCase):
    def test_state_matrix_distinguishes_intent_activity_and_listener(self):
        base={'LoadState':'loaded','ActiveState':'inactive','UnitFileState':'disabled'}
        for change,listen,expected in [({},False,'off'),({'UnitFileState':'enabled'},False,'pending'),({'ActiveState':'active'},True,'on'),({'ActiveState':'active'},False,'pending'),({'ActiveState':'failed'},False,'failed'),({'LoadState':'not-found'},False,'unavailable'),({'UnitFileState':'masked'},False,'unavailable'),({'ActiveState':'activating'},False,'pending'),({'ActiveState':'active'},None,'unavailable')]:
            self.assertEqual(s.state({**base,**change},listen),expected)
    def test_structured_appliance_schema_and_one_authority(self):
        source=Source();d=info.collect_appliance(source)
        Draft202012Validator(json.loads((Path(__file__).resolve().parents[1]/'schemas/appliance-info.schema.json').read_text())).validate(d)
        self.assertEqual(d['services']['ssh']['state'],'on');self.assertEqual(d['services']['sharing']['state'],'off')
        self.assertEqual(d['owner_username'],d['sharing_username']);self.assertTrue(d['sharing_password_set'])
        self.assertEqual(len(source.calls),4)
        self.assertFalse(d['issues'])
    def test_unavailable_queries_are_not_off_or_on(self):
        source=Source();source.command=lambda args:(1,'')
        d=info.collect_appliance(source)
        self.assertTrue(all(v['state']=='unavailable' for v in d['services'].values()))
        self.assertTrue(d['issues'])
    def test_no_secret_store_or_connection_query(self):
        source=Source();paths=[];read=source.read
        source.read=lambda p:(paths.append(p),read(p))[1]
        d=info.collect_appliance(source)
        self.assertNotIn('/etc/shadow',paths)
        self.assertFalse(any('samba' in p or 'system-connections' in p for p in paths))
        self.assertNotIn('password',str(source.calls))
        self.assertNotIn('credential',json.dumps(d))
    def test_untrusted_hostname_and_owner_not_reflected(self):
        source=Source();source.uname=lambda:{'hostname':'bad\nname'}
        original=source.read;source.read=lambda p:'{"owner_user":"bad;command"}' if p.endswith('policy.json') else original(p)
        d=info.collect_appliance(source)
        self.assertIsNone(d['computer_name']);self.assertIsNone(d['owner_username'])
        self.assertNotIn('bad;',json.dumps(d))
    def test_exact_listener_parser_ipv4_ipv6_and_udp(self):
        self.assertEqual(s.listeners('tcp LISTEN 0 128 [::]:445 [::]:*\nudp UNCONN 0 0 0.0.0.0:5353 0.0.0.0:*\n'),{('tcp',445),('udp',5353)})
    def test_service_success_requires_actual_state_not_enable_exit(self):
        system=b.Linux();queries=[]
        class Result:
            returncode=0
            stdout=''
        def run(args,**kwargs):
            queries.append(args);p=Result()
            if 'show' in args:p.stdout='Id=ssh.service\nLoadState=loaded\nActiveState=active\nSubState=running\nUnitFileState=enabled'
            elif args[0].endswith('/ss'):p.stdout='tcp LISTEN 0 128 0.0.0.0:22 0.0.0.0:*'
            return p
        with patch.object(b.subprocess,'run',side_effect=run):self.assertTrue(system.service('ssh',True))
        self.assertTrue(any('show' in q for q in queries));self.assertTrue(any(q[0].endswith('/ss') for q in queries))
    def test_sharing_starts_discovery_only_on_explicit_sharing_optin(self):
        system=b.Linux();calls=[]
        original=system.service
        with patch.object(system,'run',side_effect=lambda args,stdin=None:(calls.append(args),False)[1]):
            self.assertFalse(original('sharing',True))
        self.assertEqual(calls[0][-2:],['avahi-daemon.service','avahi-daemon.socket'])
    def test_default_identity_share_and_dynamic_advertisement_config(self):
        root=Path(__file__).resolve().parents[1];stage=(root/'tools/install_poc_stage.py').read_text();share=(root/'runtime/config/file-sharing.example.conf').read_text()
        self.assertIn("owned_put('/etc/hostname','projectcbm\\n')",stage)
        self.assertIn('AllowUsers pcbm',stage);self.assertIn('mdns name = mdns',stage)
        self.assertIn('valid users = pcbm',share);self.assertNotIn('force user',share);self.assertIn('guest ok = no',share)
    def test_hostname_syntax_and_length(self):
        for value in ('projectcbm','retro-64','a'):
            c.validate({'schema_version':1,'operation':'hostname','values':{'value':value}})
        for value in ('UPPER','a.local','-bad','bad-','a'*64,'a\nname','$(id)'):
            with self.assertRaises(ValueError):c.validate({'schema_version':1,'operation':'hostname','values':{'value':value}})

if __name__=='__main__':unittest.main()
