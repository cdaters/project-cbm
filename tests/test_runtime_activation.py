"""First-boot interruption boundaries; no real credentials/accounts are changed."""
import copy
import json
import sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime'))
from project_cbm import setup, configuration as c, config_backend as b
from test_configuration import FakeLinux, POLICY, req


class SetupLinux(FakeLinux):
    def __init__(self):
        super().__init__();self.state=setup.initial();self.owner=False;self.active=False
        self.fail_save=False;self.prerequisites=True
    def setup_read(self):return copy.deepcopy(self.state)
    def setup_save(self,state):
        if self.fail_save:raise OSError('interrupted before atomic replacement')
        self.state=copy.deepcopy(state)
    def owner_expected(self,user):return True
    def owner_ready(self,user):return self.owner
    def setup_prerequisites(self):return self.prerequisites
    def setup_activate(self,p):self.active=True
    def run(self,args,stdin=None):
        ok=super().run(args,stdin)
        if ok and args==['/usr/sbin/chpasswd']:self.owner=True
        return ok


class Activation(unittest.TestCase):
    def requests(self):
        return [req('setup-region',locale='en_US.UTF-8',keyboard='us',timezone='UTC'),
                req('setup-owner',password='synthetic-only-setup'),req('setup-network',enabled=False),req('setup-finish')]
    def apply(self,request,system):return b.apply(request,{**POLICY,'system_ready':False},system)
    def test_offline_setup_complete_and_no_password_reset(self):
        s=SetupLinux()
        for r in self.requests():self.assertEqual(self.apply(r,s)['status'],'ok')
        self.assertTrue(s.active);self.assertTrue(s.state['complete'])
        count=len(s.calls)
        self.assertEqual(self.apply(self.requests()[1],s)['status'],'invalid')
        self.assertEqual(len(s.calls),count)
        self.assertEqual(self.apply(req('setup-finish'),s)['status'],'ok')
        self.assertNotIn('synthetic',json.dumps(s.state))
        for args,secret in s.calls:self.assertNotIn('synthetic',str(args))
    def test_every_step_interrupted_before_marker_is_repeatable(self):
        for interrupted in range(4):
            s=SetupLinux()
            for r in self.requests()[:interrupted]:self.apply(r,s)
            before=copy.deepcopy(s.state);s.fail_save=True
            with self.assertRaises(OSError):self.apply(self.requests()[interrupted],s)
            self.assertEqual(s.state,before);self.assertFalse(s.active)
            s.fail_save=False
            for r in self.requests()[interrupted:]:self.assertEqual(self.apply(r,s)['status'],'ok')
            self.assertTrue(s.active)
    def test_no_false_completion_or_false_owner_success(self):
        s=SetupLinux();self.assertEqual(self.apply(req('setup-finish'),s)['status'],'invalid')
        self.apply(self.requests()[0],s);s.good=False
        self.assertEqual(self.apply(self.requests()[1],s)['status'],'failed')
        self.assertNotIn('owner',s.state['completed'])
        s.good=True
        for r in self.requests()[:3]:self.apply(r,s)
        s.prerequisites=False
        self.assertEqual(self.apply(req('setup-finish'),s)['status'],'failed')
        self.assertFalse(s.state['complete']);self.assertFalse(s.active)
    def test_completed_owner_marker_never_resets_but_region_network_can_be_revisited(self):
        s=SetupLinux()
        for r in self.requests()[:3]:self.apply(r,s)
        count=len(s.calls)
        self.apply(self.requests()[1],s)
        self.assertEqual(len(s.calls),count)
        for r in [self.requests()[0],self.requests()[2]]:self.apply(r,s)
        self.assertGreater(len(s.calls),count)
        self.assertEqual(s.state['completed'],['region','owner','network'])
    def test_wifi_setup_narrow_gate_does_not_activate_services(self):
        s=SetupLinux()
        for op,values in [('setup-wifi-country',{'value':'US'}),('setup-wifi-rescan',{}),('setup-wifi-enroll',{'ssid':'fixture','password':'synthetic space !'})]:
            self.assertEqual(self.apply(req(op,**values),s)['status'],'pending')
        for r in self.requests()[:3]:self.apply(r,s)
        self.assertEqual(self.apply(req('setup-wifi-rescan'),s)['status'],'ok')
        self.assertFalse(s.active);self.assertFalse(s.state['complete'])
        self.assertEqual(self.apply(req('service',service='ssh',enabled=True),s)['status'],'pending')
    def test_corrupt_state_fails_closed(self):
        for state in [{}, {'schema_version':1,'completed':['owner'],'complete':True},
                      {'schema_version':1,'completed':['owner','owner'],'complete':False}]:
            s=SetupLinux();s.state=state
            with self.assertRaises(ValueError):self.apply(req('setup-finish'),s)
            self.assertFalse(s.active)
    def test_setup_input_is_closed(self):
        for r in [req('setup-owner',password='x\nroot:evil'),req('setup-owner',password='abcdefghijk:root'),
                  req('setup-owner',password='long-valid-password',user='root'),req('setup-finish',force=True),
                  req('setup-region',locale='en_US.UTF-8',keyboard='us',timezone='../../shadow')]:
            with self.assertRaises(ValueError):c.validate(r)
