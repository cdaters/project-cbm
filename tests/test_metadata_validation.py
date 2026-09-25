"""Static inspection follows the shared metadata policy without executing target code."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from validate_rc3 import narrow_metadata_policy


class MetadataValidation(unittest.TestCase):
    def test_shared_and_stable_policy(self):
        current = (ROOT/'runtime/project_cbm/usb_discovery.py').read_text()
        stable = subprocess.check_output(['git','-C',str(ROOT),'show',
                                         'v1.1.0:runtime/project_cbm/importer.py'], text=True)
        for source in (current, stable):
            self.assertTrue(narrow_metadata_policy(source + "\nraise RuntimeError('never execute')\n"))

    def test_missing_or_broadened_metadata_policy_fails(self):
        source = (ROOT/'runtime/project_cbm/usb_discovery.py').read_text()
        self.assertFalse(narrow_metadata_policy('from .usb_discovery import HOST_METADATA\n'))
        self.assertFalse(narrow_metadata_policy(source.replace("'.DS_Store'", "'.any-private-file'")))
        self.assertFalse(narrow_metadata_policy(source.replace("name.startswith('._')", "name.startswith('.')")))
