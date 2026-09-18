"""The corrective validator must reject a stale, absent or redirected lifecycle owner."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
from validate_poc4_corrective import exact_payload

class CorrectivePayload(unittest.TestCase):
    def test_modified_missing_and_symlink_payload_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root/'engineering.py'
            raw = b'accepted lifecycle owner\n'
            mapping = {'engineering.py':{'size_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}}
            self.assertFalse(all(exact_payload(root,mapping).values()))
            path.write_bytes(raw)
            self.assertTrue(all(exact_payload(root,mapping).values()))
            path.write_bytes(b'stale lifecycle owner\n')
            self.assertFalse(all(exact_payload(root,mapping).values()))
            target = root/'other.py';target.write_bytes(raw)
            path.unlink();path.symlink_to(target)
            self.assertFalse(all(exact_payload(root,mapping).values()))
