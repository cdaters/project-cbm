"""Private development admission cannot masquerade as the stable release."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from development_identity import development_number, configuration_path, export_path, valid_menu_tag
from freeze_private_candidate import verify_candidate_versions, verify_output_identity


class DevelopmentIdentity(unittest.TestCase):
    def test_explicit_private_identity(self):
        verify_candidate_versions('1.2.0-dev.1', 'private-engineering-1.2-dev1',
                                  '1.2.0~dev1-1', '1.2.0~dev1-1+pcbm1')
        self.assertEqual(development_number({'version':'1.2.0-dev.1',
                                            'candidate':'private-engineering-1.2-dev1'}), '1')

    def test_release_and_cross_identity_rejected(self):
        for version, candidate, runtime, menu in (
            ('1.2.0', 'release', '1.2.0~dev1-1', '1.2.0~dev1-1+pcbm1'),
            ('1.2.0-dev.1', 'release', '1.2.0~dev1-1', '1.2.0~dev1-1+pcbm1'),
            ('1.2.0-dev.1', 'private-engineering-1.2-dev2', '1.2.0~dev1-1', '1.2.0~dev1-1+pcbm1'),
            ('1.1.0', 'private-engineering-1.2-dev1', '1.1.0-1', '1.1.0-1+pcbm1'),
            ('1.2.0-dev.1', 'private-engineering-1.2-dev1', '1.1.0-1', '1.2.0~dev1-1+pcbm1'),
            ('1.2.0-dev.1', 'private-engineering-1.2-dev1', '1.2.0~dev1-1', '1.1.0-1+pcbm1'),
            (None, None, '1.2.0~dev1-1', '1.2.0~dev1-1+pcbm1'),
            ('1.2.0-dev.01', 'private-engineering-1.2-dev01', '1.2.0~dev1-1', '1.2.0~dev1-1+pcbm1'),
        ):
            with self.subTest(version=version,candidate=candidate), self.assertRaises(ValueError):
                verify_candidate_versions(version,candidate,runtime,menu)

    def test_legacy_release_and_private_admission_retained(self):
        verify_candidate_versions('1.1.0','release','1.1.0-1','1.1.0-1+pcbm1')
        verify_candidate_versions('1.1.0-rc.4','private-engineering-rc4','1.1.0~rc4-1','1.1.0~rc4-1+pcbm1')
        verify_candidate_versions(None,None,'1.1.0~poc4.6-1','1.1.0~poc4.6-1+pcbm1')
        for version, runtime, menu in (
            ('1.1.0-rc.4','1.1.0-1','1.1.0-1+pcbm1'),
            ('1.1.0','1.1.0~rc4-1','1.1.0-1+pcbm1'),
            ('1.1.0','1.1.0-1','1.1.0~rc4-1+pcbm1'),
            ('1.1.1','1.1.0-1','1.1.0-1+pcbm1'),
        ):
            with self.subTest(version=version,runtime=runtime,menu=menu), self.assertRaises(ValueError):
                verify_candidate_versions(version,'release',runtime,menu)

    def test_export_tag_admission(self):
        for tag in ('v1.1.0','v1.1.0_rc4','v1.1.0_poc4.6','v1.2.0_dev1'):
            self.assertTrue(valid_menu_tag(tag),tag)
        for tag in ('v1.2.0','v1.2.0_rc1','v1.2.0_dev0','v1.2.0_dev01','v1.1.1','main','v1.2.0_dev1\n'):
            self.assertFalse(valid_menu_tag(tag),tag)

    def test_config_and_export_are_separate_and_checked(self):
        stable={'version':'1.1.0','candidate':'release'}
        dev={'version':'1.2.0-dev.5','candidate':'private-engineering-1.2-dev5'}
        for product in (stable,dev):
            config=json.loads(configuration_path(ROOT,product).read_text())
            verify_output_identity(ROOT,config,product['version'],product['candidate'])
        self.assertNotEqual(configuration_path(ROOT,stable),configuration_path(ROOT,dev))
        self.assertNotEqual(export_path(ROOT,stable),export_path(ROOT,dev))
        with self.assertRaises(ValueError):
            verify_output_identity(ROOT,json.loads(configuration_path(ROOT,stable).read_text()),dev['version'],dev['candidate'])
        # Frozen stable inputs are still byte-for-byte identical to the release tag.
        for name in ('build/pigen/config.json','build/pigen/stage-cbm/EXPORT_IMAGE'):
            old=subprocess.check_output(['git','-C',str(ROOT),'show','v1.1.0:'+name])
            self.assertEqual((ROOT/name).read_bytes(),old)


if __name__ == '__main__':
    unittest.main()
