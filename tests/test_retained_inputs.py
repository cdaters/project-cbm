import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from retained_inputs import verify_catalog, verify_deb

def desc(path): return {'path':path.name,'size_bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

class RetainedTests(unittest.TestCase):
    def test_catalog_does_not_hide_tampered_nested_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); child=root/'input';child.write_bytes(b'pinned')
            cat=root/'catalog.json';cat.write_text(json.dumps({'format':'project-cbm.input-catalog','schema_version':1,'entries':[{'role':'package','origin':'https://deb.debian.org/debian/','artifact':desc(child)}]}))
            descriptor=desc(cat)
            self.assertEqual(verify_catalog(root,descriptor),1)
            child.write_bytes(b'edited')
            with self.assertRaises(ValueError):verify_catalog(root,descriptor)
    def test_debian_identity_mismatch(self):
        expected={'name':'project-cbm-menu','version':'1.1.0~poc1-1+pcbm1','architecture':'all'}
        with patch('retained_inputs.subprocess.check_output',return_value='Package: project-cbm-menu\nVersion: 1.1.0~poc1-1+pcbm1\nArchitecture: all\n'):
            verify_deb(Path('unread.deb'),expected)
        with patch('retained_inputs.subprocess.check_output',return_value='Package: project-cbm-menu\nVersion: wrong\nArchitecture: all\n'):
            with self.assertRaises(ValueError): verify_deb(Path('unread.deb'),expected)
