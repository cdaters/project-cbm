"""Framing/EOF tests for the caller-side bridge; installed PTY coverage is native."""
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from project_cbm import ingest_bridge
from project_cbm.ingest_bridge import Replies
from project_cbm.ingestion import IngestError

class BridgeFraming(unittest.TestCase):
    def test_idle_browse_cancels_lease_and_waits_for_verified_release(self):
        broker=Mock();broker.stdout.fileno.return_value=9
        replies=Mock()
        replies.fd=9
        replies.ready.side_effect=[True,False,True]
        replies.read.side_effect=[{'schema_version':2,'status':'ready'},
            {'schema_version':2,'status':'cancelled','source_unmounted':True}]
        ticks=iter([0,0])
        with patch.object(ingest_bridge.os,'geteuid',return_value=1000), \
                patch.object(ingest_bridge.signal,'signal'), \
                patch.object(ingest_bridge,'receive',return_value={'schema_version':2,'operation':'browse-session','token':'a'*32}), \
                patch.object(ingest_bridge.subprocess,'Popen',return_value=broker), \
                patch.object(ingest_bridge,'Replies',return_value=replies), \
                patch.object(ingest_bridge.time,'monotonic',side_effect=lambda:next(ticks,301)), \
                patch.object(ingest_bridge.select,'select',return_value=([],[],[])), \
                patch.object(ingest_bridge,'emit') as emit, \
                patch.object(ingest_bridge.usb_browse,'browse') as browse:
            self.assertEqual(ingest_bridge.main(),0)
        sent=[json.loads(c.args[0]) for c in broker.stdin.write.call_args_list]
        self.assertEqual(sent[-1],{'operation':'cancel'})
        self.assertEqual(len(sent),2)
        self.assertIs(emit.call_args.args[0]['source_unmounted'],True)
        browse.assert_not_called();broker.wait.assert_called_once()

    def test_batched_notice_and_final_are_not_lost(self):
        read,write=os.pipe()
        try:
            values=[{'schema_version':2,'status':'releasing'}, {'schema_version':2,'status':'failed','source_unmounted':False}]
            os.write(write,b''.join(json.dumps(v).encode()+b'\n' for v in values))
            replies=Replies(read)
            self.assertEqual(replies.read(),values[0]);self.assertTrue(replies.ready())
            self.assertEqual(replies.read(),values[1]);self.assertFalse(replies.ready())
        finally:os.close(read);os.close(write)
    def test_eof_is_failure_not_safe_release(self):
        read,write=os.pipe();os.close(write)
        try:
            with self.assertRaisesRegex(IngestError,'disconnected'):Replies(read).read()
        finally:os.close(read)
    def test_wrong_reply_shape_rejected(self):
        for data in [b'[]\n',b'{"schema_version":1}\n',b'not-json\n']:
            read,write=os.pipe()
            try:
                os.write(write,data)
                with self.assertRaises(ValueError):Replies(read).read()
            finally:os.close(read);os.close(write)

if __name__=='__main__':unittest.main()
