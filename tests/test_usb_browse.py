"""No real terminal/mount: worker ownership, cleanup and fixed command tests."""
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'runtime'))
from project_cbm import importer, usb_browse
from project_cbm.ingestion import IngestError


class Browse(unittest.TestCase):
    def test_narrow_browse_request(self):
        request={'schema_version':2,'operation':'browse-session','token':'b'*32}
        self.assertEqual(importer.validate_request(json.dumps(request)),request)
        for key,value in [('path','/'),('command','sh'),('writable',True),('token','/dev/sda1')]:
            with self.assertRaises(ValueError):importer.validate_request(json.dumps({**request,key:value}))

    def test_mc_fixed_unprivileged_and_return(self):
        process=Mock(returncode=0)
        process.poll.return_value=0
        with patch.object(usb_browse.os,'geteuid',return_value=1000), \
                patch('builtins.open',return_value=io.BytesIO()), \
                patch.object(usb_browse.subprocess,'Popen',return_value=process) as launch:
            usb_browse.browse(Path('/run/project-cbm/import/browse'),lambda:False)
        args,kwargs=launch.call_args
        self.assertEqual(args[0],['/usr/bin/mc','-u','/run/project-cbm/import/browse','/home/pcbm/content'])
        self.assertNotIn('sudo',args[0])
        self.assertTrue(kwargs['close_fds'])
        self.assertIn('preexec_fn',kwargs)
        process.terminate.assert_not_called()
        with patch.object(usb_browse.os,'geteuid',return_value=0),self.assertRaises(IngestError):
            usb_browse.browse(Path('/run/project-cbm/import/browse'))

    def test_cancel_reaps_mc_and_escalates_when_needed(self):
        process=Mock()
        process.poll.return_value=None
        process.wait.side_effect=[subprocess.TimeoutExpired('mc',0.5),0]
        with patch.object(usb_browse.os,'geteuid',return_value=1000), \
                patch('builtins.open',return_value=io.BytesIO()), \
                patch.object(usb_browse.subprocess,'Popen',return_value=process), \
                self.assertRaisesRegex(IngestError,'cancelled'):
            usb_browse.browse(Path('/synthetic'),lambda:True)
        process.terminate.assert_called_once()
        process.kill.assert_called_once()
        self.assertEqual(process.wait.call_count,2)

    def test_exit_browse_again_and_explicit_release(self):
        with patch.object(usb_browse,'emit') as emit, \
                patch.object(usb_browse,'receive',side_effect=[{'operation':'browse'},{'operation':'browse'},{'operation':'release'}]), \
                patch.object(usb_browse,'browse') as browse:
            result=usb_browse.run(Path('/synthetic'))
        self.assertEqual(browse.call_count,2)
        self.assertEqual(result,{'status':'ok'})
        self.assertNotIn('source_unmounted',result)  # Only root parent can confirm.
        self.assertEqual(emit.call_count,3)

    def test_disconnect_or_removed_media_finishes_for_cleanup(self):
        for error in [IngestError('disconnected'),OSError('removed'),IngestError('browser_failed')]:
            with patch.object(usb_browse,'emit'),patch.object(usb_browse,'receive',side_effect=error):
                result=usb_browse.run(Path('/synthetic'))
            self.assertIn(result['status'],('failed','cancelled'))
            self.assertNotIn('source_unmounted',result)


if __name__=='__main__':unittest.main()
