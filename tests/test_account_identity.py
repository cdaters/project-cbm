import sys
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime'))
from project_cbm import config_backend as backend


class AccountIdentity(unittest.TestCase):
    def test_fixed_username_uid_home_and_sudo_contract(self):
        system=backend.Linux()
        account=SimpleNamespace(pw_uid=1000,pw_dir='/home/pcbm',pw_shell='/bin/bash')
        with patch.object(backend.pwd,'getpwnam',return_value=account),patch.object(backend.grp,'getgrnam',return_value=SimpleNamespace(gr_mem=['pcbm'])):
            self.assertTrue(system.owner_expected('pcbm'))
            self.assertFalse(system.owner_expected('owner'));self.assertFalse(system.owner_expected('pi'))
            account.pw_dir='/home/owner';self.assertFalse(system.owner_expected('pcbm'))
            account.pw_dir='/home/pcbm';account.pw_uid=0;self.assertFalse(system.owner_expected('pcbm'))

    def test_setup_role_is_not_renamed(self):
        from project_cbm import setup
        self.assertEqual(setup.STEPS,('region','owner','network'))
        from project_cbm.admin import command
        self.assertEqual(command('owner','pcbm'),['/usr/bin/sudo','-k','--','/bin/bash','--noprofile','--norc','-i'])

    def test_fresh_image_identity_surfaces_agree(self):
        stage=(ROOT/'tools/install_poc_stage.py').read_text()
        self.assertIn("'--groups','pcbm-operators,sudo','pcbm'",stage)
        self.assertIn("'owner_user':'pcbm'",stage)
        self.assertIn('AllowUsers pcbm',stage)
        sharing=(ROOT/'runtime/config/file-sharing.example.conf').read_text()
        self.assertIn('valid users = pcbm',sharing)
        self.assertNotIn('force user',sharing)
        self.assertIn('path = /home/pcbm/content',sharing)
        self.assertNotIn('AllowUsers owner',stage)
        self.assertNotIn("chroot('useradd'",stage)
        self.assertNotIn("'home/pi",stage)
        self.assertIn("chroot('id','-u','pcbm')",stage)
