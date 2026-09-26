"""Original synthetic multi-file data through the real common ingestion writer."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from project_cbm import ingestion, online_session as s, online_backend as b

class Fixture:
    profile=b.CENTRAL
    def __init__(self):
        self.downloads=[];self.fail=False
        self.release={'id':'original-fixture','category':1,'name':'Original Test Set','group':'Test','year':2026}
        self.items=[ingestion.Item(str(i),'disk'+str(i)+'/same.prg',4,'fixture') for i in (1,2)]
    def search(self,*_):return [self.release]
    def metadata(self,*_):return self.release
    def files(self,*_):return self.items,1
    def download(self,release,item,cancelled):
        self.downloads.append(item.id)
        if self.fail:raise b.OnlineError('download_failed')
        if cancelled():raise b.OnlineError('cancelled')
        return b'\x01\x08'+item.id.encode()+b'X'

@unittest.skipUnless(sys.platform=='linux','anonymous Linux staging in native suite')
class Ingestion(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.library=self.root/'content';self.library.mkdir()
        self.state=self.root/'private';self.backend=Fixture()
        self.session=s.Session(self.backend,self.library,self.state);self.addCleanup(self.session.close)
        rows=self.session.handle({'operation':'search','fields':{'name':'Fixture'}})['rows']
        self.session.handle({'operation':'release','id':rows[0]['id']})
    def prepare(self):
        self.session.handle({'operation':'select','mode':'all'})
        return self.session.handle({'operation':'prepare','category':'demos','family':'c64'})
    def test_explicit_download_then_shared_save_preserves_set_and_provenance(self):
        self.assertEqual(self.backend.downloads,[])
        review=self.prepare()
        self.assertFalse(list(self.library.rglob('*.prg')))
        self.assertEqual(review['selected'],2)
        result=self.session.handle({'operation':'save'})
        self.assertEqual(result['saved'],2)
        self.assertEqual(sorted(p.read_bytes() for p in self.library.rglob('*.prg')),[b'\x01\x081X',b'\x01\x082X'])
        self.assertTrue((self.library/review['destination']/'disk1/same.prg').exists())
        logs=list(self.state.glob('*.jsonl'));self.assertEqual(len(logs),1)
        events=[json.loads(x) for x in logs[0].read_text().splitlines()]
        self.assertEqual(events[0]['backend'],b.CENTRAL.key)
        self.assertTrue(any(x.get('sha256')==hashlib.sha256(b'\x01\x081X').hexdigest() for x in events))
        self.assertEqual(logs[0].stat().st_mode&0o777,0o600)
        self.assertEqual(self.state.stat().st_mode&0o777,0o700)
    def test_already_present_and_keep_both(self):
        first=self.prepare();self.session.handle({'operation':'save'})
        second=self.prepare();self.assertEqual(second['already_present'],2)
        self.assertEqual(self.session.handle({'operation':'save'})['already_present'],2)
        (self.library/first['destination']/'disk1/same.prg').write_bytes(b'changed')
        third=self.prepare();self.assertTrue(third['kept_both'])
        self.assertTrue(third['destination'].endswith('(2)'))
        self.assertEqual(self.session.handle({'operation':'save'})['saved'],2)
    def test_cancel_back_and_failed_download_leave_no_staged_payload(self):
        self.prepare();self.session.handle({'operation':'select','mode':'clear'})
        self.assertFalse(self.session.staged)
        self.backend.fail=True
        with self.assertRaises(b.OnlineError):self.prepare()
        self.assertFalse(self.session.staged)
        self.assertFalse(list(self.library.rglob('*.prg')))
        self.assertEqual([p.name for p in self.state.iterdir()],['lock'])
    def test_safe_destination_and_lock(self):
        (self.library/'demos').symlink_to(self.root)
        with self.assertRaises(ingestion.IngestError):self.prepare()
        self.assertFalse(list(self.root.glob('c64/*')))
        (self.library/'demos').unlink()
        self.state.mkdir(exist_ok=True)
        with (self.state/'lock').open('w') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            with self.assertRaisesRegex(b.OnlineError,'busy'):self.prepare()
    def test_space_preflight_before_download(self):
        class Space:f_bavail=0;f_frsize=4096
        with patch.object(os,'fstatvfs',return_value=Space()):
            with self.assertRaisesRegex(b.OnlineError,'space'):self.prepare()
        self.assertEqual(self.backend.downloads,[])
    def test_exact_review_rechecked_no_overwrite(self):
        review=self.prepare();path=self.library/review['destination']/'disk1/same.prg'
        path.parent.mkdir(parents=True);path.write_bytes(b'other')
        result=self.session.handle({'operation':'save'})
        self.assertNotEqual(result['status'],'ok');self.assertEqual(path.read_bytes(),b'other')
    def test_cancelled_save_and_resource_cleanup(self):
        before=len(os.listdir('/proc/self/fd'))
        self.prepare();result=self.session.save(lambda:True)
        self.assertEqual(result['status'],'cancelled')
        self.assertFalse(list(self.library.rglob('*.prg')))
        self.assertEqual(len(os.listdir('/proc/self/fd')),before)
    def test_limits_and_unreviewed_save(self):
        with self.assertRaisesRegex(b.OnlineError,'review_required'):self.session.handle({'operation':'save'})
        with self.assertRaisesRegex(b.OnlineError,'selection_limit'):self.session.prepare('games','c64',lambda:False)
        self.session.handle({'operation':'select','mode':'all'})
        with self.assertRaisesRegex(b.OnlineError,'classification'):self.session.prepare('evil','c64',lambda:False)
