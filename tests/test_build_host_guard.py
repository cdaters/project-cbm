import sys
from pathlib import Path
import unittest
from unittest.mock import patch
import subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import build_host_guard as guard

class HostGuard(unittest.TestCase):
    def test_versions_not_order_or_auxiliary_columns(self):
        guard.compare('a\t1\ta\t1\nb\t2\tb\t2\n','b\t2\na\t1\n')
    def test_changed_added_removed_duplicate_and_empty_rejected(self):
        for value in ['a\t2\n','a\t1\nb\t2\n','','a\t1\na\t1\n']:
            with self.subTest(value=value),self.assertRaises(ValueError):guard.compare('a\t1\n',value)
    def test_unmasked_automatic_updates_refuse_before_build(self):
        with patch.object(subprocess,'run',return_value=subprocess.CompletedProcess([],0,'enabled\n','')):
            with self.assertRaisesRegex(ValueError,'masked'):guard.verify({},Path('/missing'))
if __name__=='__main__':unittest.main()
