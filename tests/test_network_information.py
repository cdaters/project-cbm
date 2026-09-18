"""Synthetic interface data only; no local network or credential inspection."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from project_cbm import network_info as net,info
from test_runtime_foundation import Fixture
from jsonschema import Draft202012Validator
ROW={'ifname':'wlan0','operstate':'UP','address':'02:00:00:00:00:01','addr_info':[{'family':'inet','local':'192.0.2.2','prefixlen':24},{'family':'inet6','local':'fe80::1234','prefixlen':64},{'family':'inet6','local':'2001:db8::2','prefixlen':64}]}
class Network(unittest.TestCase):
 def test_small_network_projection_uses_only_existing_authority(self):
  calls=[]
  class Source:
   def command(self,args):
    calls.append(args)
    if args==net.IP:return 0,json.dumps([ROW])
    if args==net.DEVICES:return 0,'GENERAL.DEVICE:wlan0\nGENERAL.TYPE:wifi\nGENERAL.STATE:100 (connected)\n'
    raise AssertionError('unexpected probe')
  data=info.collect_network(Source())
  self.assertEqual(calls,[net.IP,net.DEVICES]);self.assertIsNone(data['interfaces'][0]['ssid'])
  Draft202012Validator(json.loads((Path(__file__).resolve().parents[1]/'schemas/network-info.schema.json').read_text())).validate(data)
 def test_small_network_projection_failure_is_fixed_safe_result(self):
  class Source:
   def command(self,args):raise TimeoutError('private raw error')
  data=info.collect_network(Source())
  self.assertIsNone(data['interfaces']);self.assertNotIn('private raw',json.dumps(data))
 def test_live_multiple_addresses_and_current_mac(self):
  row=net.addresses(json.dumps([ROW]))[0]
  self.assertEqual(row['ipv4'],['192.0.2.2/24']);self.assertEqual(row['ipv6'],['fe80::1234/64','2001:db8::2/64']);self.assertEqual(row['mac'],'02:00:00:00:00:01')
 def test_tentative_failed_and_loopback_not_presented_as_usable(self):
  row=copy.deepcopy(ROW);row['addr_info'][0]['tentative']=True;row['addr_info'][1]['flags']=['dadfailed']
  result=net.addresses(json.dumps([row,{'ifname':'lo'}]));self.assertEqual(len(result),1);self.assertEqual(result[0]['ipv4'],[]);self.assertEqual(result[0]['ipv6'],['2001:db8::2/64'])
 def test_malformed_duplicate_and_bounds(self):
  for value in [None,[None],[ROW,ROW],[{**ROW,'operstate':None}],[{**ROW,'ifname':'bad;command'}],[{**ROW,'addr_info':[None]}],[{**ROW,'addr_info':[{'family':'inet','local':'192.0.2.2','prefixlen':True}]}],[ROW]*33]:
   with self.subTest(value=value),self.assertRaises((ValueError,KeyError)):net.addresses(json.dumps(value))
 def test_nm_numeric_state_and_no_connection_name(self):
  result=net.devices('GENERAL.DEVICE:wlan0\nGENERAL.TYPE:wifi\nGENERAL.STATE:100 (connected)\n')
  self.assertEqual(result,{'wlan0':{'type':'wifi','state':'connected'}})
  with self.assertRaises(ValueError):net.devices('GENERAL.DEVICE:wlan0\nGENERAL.CONNECTION:private-profile\n')
 def test_ssid_escaping_inactive_and_no_injection(self):
  self.assertEqual(net.active_ssids('wlan0:no:Other\nwlan0:yes:Test\\: room\\\\a\n'),{'wlan0':'Test: room\\a'})
  for raw in ['wlan0:yes:bad\x1b','wlan0:yes:'+32*'界','wlan0:yes:one\nwlan0:yes:two','wlan0:yes:bad\\q']:
   with self.assertRaises(ValueError):net.active_ssids(raw)
 def test_collector_partial_failure_and_secret_exclusion(self):
  f=Fixture();original=f.command
  def command(args):
   f.calls.append(args)
   if args==net.IP:return 0,json.dumps([ROW])
   if args==net.DEVICES:return 0,'GENERAL.DEVICE:wlan0\nGENERAL.TYPE:wifi\nGENERAL.STATE:100 (connected)\n'
   if args==net.WIFI:return 0,'wlan0:yes:Test network\n'
   return original(args)
  f.command=command
  with tempfile.TemporaryDirectory() as p:
   data=info.collect(f,Path(p)/'preferences')
   row=data['current_state']['network_interfaces'][0];self.assertEqual(row['ssid'],'Test network');self.assertEqual(row['state'],'connected')
   Draft202012Validator(json.loads((Path(__file__).resolve().parents[1]/'schemas/info.schema.json').read_text())).validate(data)
   self.assertIn('192.0.2.2/24',info.human(data))
   self.assertIn('--rescan',net.WIFI);self.assertEqual(net.WIFI[-1],'no')
   def unavailable(args):
    if args==net.IP:return 0,json.dumps([ROW])
    if args[0]=='/usr/bin/nmcli':raise TimeoutError('sensitive raw backend text')
    return original(args)
   f.command=unavailable;data=info.collect(f,Path(p)/'preferences')
   row=data['current_state']['network_interfaces'][0];self.assertEqual(row['ipv4'],['192.0.2.2/24']);self.assertIsNone(row['ssid']);self.assertEqual(row['state'],'unknown');self.assertNotIn('sensitive',json.dumps(data))
 def test_disconnected_wifi_does_not_request_ssid_or_scan(self):
  calls=[]
  class Source:
   def command(self,args):
    calls.append(args)
    return (0,json.dumps([ROW])) if args==net.IP else (0,'GENERAL.DEVICE:wlan0\nGENERAL.TYPE:wifi\nGENERAL.STATE:30 (disconnected)\n')
  rows=net.collect(Source(),lambda name,fn,fallback=None:fn());self.assertEqual(rows[0]['state'],'disconnected');self.assertNotIn(net.WIFI,calls)
if __name__=='__main__':unittest.main()
