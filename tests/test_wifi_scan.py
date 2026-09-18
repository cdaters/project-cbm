"""Delayed readiness/cache regression with a virtual clock; no radio or secrets."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from project_cbm import wifi_scan as w

READY = ('GENERAL.DEVICE:wlxfixture\nGENERAL.TYPE:wifi\nGENERAL.STATE:30 (disconnected)\n'
         'GENERAL.DBUS-PATH:/org/freedesktop/NetworkManager/Devices/7\n')


class Scan(unittest.TestCase):
    def run_scan(self,ready_at=0,complete_at=2,accepted=True,last_scan=True):
        now=[0.0];requests=[]
        def clock():return now[0]
        def pause(t):now[0]+=t
        def query(args):
            if args[0]==w.NM:return READY if now[0]>=ready_at else READY.replace('30 (disconnected)','20 (unavailable)')
            if not last_scan:return None
            return 'x '+('2000' if now[0]>=complete_at else '-1')+'\n'
        def request(args):requests.append((now[0],args));return accepted
        return w.scan(query,request,65,clock,pause),requests

    def test_accepted_request_waits_for_completed_scan(self):
        result,calls=self.run_scan(ready_at=1,complete_at=4)
        self.assertEqual(result['result'],'complete');self.assertEqual(result['elapsed_ms'],4000)
        self.assertEqual(calls[0][0],1);self.assertEqual(len(calls),1)
        self.assertIn('wlxfixture',calls[0][1])

    def test_automatic_scan_completion_after_request_rejection(self):
        result,_=self.run_scan(accepted=False)
        self.assertEqual(result['result'],'complete')

    def test_readiness_and_scan_timeouts_are_not_empty_success(self):
        for kwargs,status,elapsed in [({'ready_at':99},'readiness_timeout',10000),
                                    ({'complete_at':99},'scan_timeout',25000),
                                    ({'last_scan':False},'scan_state_unavailable',0)]:
            result,calls=self.run_scan(**kwargs)
            self.assertEqual(result['result'],status);self.assertEqual(result['elapsed_ms'],elapsed)
            self.assertLessEqual(len(calls),2)

    def test_late_completion_uses_only_two_requests(self):
        result,calls=self.run_scan(complete_at=12)
        self.assertEqual(result['result'],'complete');self.assertEqual(len(calls),2)

    def test_diagnostics_have_only_fixed_fields(self):
        result,_=self.run_scan()
        self.assertEqual(set(result),{'schema_version','result','request_rounds','ready_interfaces','elapsed_ms'})
        self.assertNotIn('wlxfixture',str(result))

    def test_unsafe_or_unready_device_rejected(self):
        for text in [READY.replace('wlxfixture','--bad'),READY.replace('/Devices/7','/bad'),
                     READY.replace('30 (disconnected)','10 (unmanaged)'),READY.replace('wifi','ethernet')]:
            self.assertEqual(w.devices(text),[])

    def test_all_ready_adapters_must_finish(self):
        now=[0.0]
        # Use property path rather than interface-name assumptions.
        def query(args):
            if args[0]==w.NM:return READY+READY.replace('wlxfixture','radio2').replace('/Devices/7','/Devices/8')
            return 'x '+('1' if now[0] >= (1 if args[-3].endswith('/7') else 3) else '-1')
        def pause(t):now[0]+=t
        result=w.scan(query,lambda _:True,65,lambda:now[0],pause)
        self.assertEqual(result['elapsed_ms'],3000);self.assertEqual(result['ready_interfaces'],2)

if __name__=='__main__':unittest.main()
