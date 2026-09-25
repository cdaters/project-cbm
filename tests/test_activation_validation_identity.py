"""Actual activation checks select the declared account model and reject unsafe state."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from validate_activation import inspect


class ActivationValidationIdentity(unittest.TestCase):
    def account_checks(self, product, *, single=True, uid=None, ready=False, operator=True):
        class AccountChecksComplete(Exception):
            pass
        checks = {}
        def check(name, value):
            checks[name] = value
            if name == 'normal_user_helper_group':
                raise AccountChecksComplete
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'etc/project-cbm').mkdir(parents=True)
            account = 'pcbm' if single else 'pi'
            policy = dict(schema_version=1, owner_user='pcbm', appliance_user=account,
                          system_ready=ready, network_ready=True,
                          ready_services=['ssh', 'sharing', 'modem', 'discovery'])
            (root/'etc/project-cbm/configuration-policy.json').write_text(json.dumps(policy))
            owner_uid = uid if uid is not None else (1000 if single else 1001)
            passwd = f'pcbm:x:{owner_uid}:1000::/home/pcbm:/bin/bash\n'
            if not single:
                passwd += 'pi:x:1000:1000::/home/pi:/bin/bash\n'
            (root/'etc/passwd').write_text(passwd)
            (root/'etc/shadow').write_text('pcbm:!:0:0:99999:7:::\n')
            (root/'etc/group').write_text('sudo:x:27:pcbm\npcbm-operators:x:1002:' +
                                          (account if operator else '') + '\n')
            with self.assertRaises(AccountChecksComplete):
                inspect(root, {'product':product}, check, None)
        return checks

    def test_development_uses_single_owner_without_weakening_checks(self):
        product = {'version':'1.2.0-dev.1', 'candidate':'private-engineering-1.2-dev1'}
        self.assertTrue(all(self.account_checks(product).values()))
        self.assertFalse(self.account_checks(product, uid=1001)['owner_account_identity'])
        self.assertFalse(self.account_checks(product, ready=True)['activation_not_falsely_ready'])
        self.assertFalse(self.account_checks(product, operator=False)['normal_user_helper_group'])

    def test_stable_and_historical_account_models_remain_valid(self):
        for version, candidate, single in [('1.1.0','release',True),
                                          ('1.1.0-rc.4','private-engineering-rc4',True),
                                          ('1.1.0-poc.4','private-engineering-poc4',False)]:
            with self.subTest(candidate=candidate):
                self.assertTrue(all(self.account_checks(
                    {'version':version,'candidate':candidate}, single=single).values()))

    def test_mixed_development_identity_is_rejected(self):
        with self.assertRaises(ValueError):
            self.account_checks({'version':'1.2.0-dev.1','candidate':'private-engineering-1.2-dev2'})
