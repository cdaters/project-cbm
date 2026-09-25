"""A private input refresh must retain signature/time/hash boundaries."""
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from development_apt_refresh import fresh_release, digest_rows, fields, match_packages


class DevelopmentRefresh(unittest.TestCase):
    def setUp(self):
        self.now=datetime(2026,9,25,tzinfo=timezone.utc)
        self.release='Codename: trixie-security\nDate: Thu, 24 Sep 2026 00:00:00 UTC\nValid-Until: Fri, 02 Oct 2026 00:00:00 UTC\n'

    def test_current_signed_fields(self):
        self.assertEqual(fresh_release(self.release,'trixie-security',self.now)['Codename'],'trixie-security')

    def test_expired_metadata_is_rejected(self):
        with self.assertRaises(ValueError):
            fresh_release(self.release.replace('Fri, 02 Oct','Tue, 22 Sep'),'trixie-security',self.now)

    def test_future_and_wrong_repository_rejected(self):
        with self.assertRaises(ValueError):
            fresh_release(self.release.replace('Thu, 24 Sep','Sat, 26 Sep'),'trixie-security',self.now)
        with self.assertRaises(ValueError): fresh_release(self.release,'trixie-updates',self.now)

    def test_missing_or_ambiguous_expiry_rejected(self):
        with self.assertRaises(KeyError): fresh_release(self.release.split('Valid-Until:')[0],'trixie-security',self.now)
        with self.assertRaises(ValueError): fresh_release(self.release+self.release,'trixie-security',self.now)

    def test_signed_checksum_rows(self):
        value='\n'+'a'*64+' 25 main/binary-arm64/Packages.xz'
        self.assertEqual(digest_rows(value),{'main/binary-arm64/Packages.xz':('a'*64,25)})
        for bad in ('a'*64+' 25 ../escape', 'a'*64+' 25 /escape','a'*63+' 25 name','z'*64+' 25 name',value+'\n'+value):
            with self.subTest(bad=bad),self.assertRaises(ValueError):digest_rows(bad)

    def test_continuation_fields_keep_all_source_files(self):
        data=fields('Package: test\nChecksums-Sha256:\n '+'a'*64+' 1 test.dsc\n '+'b'*64+' 2 test.tar.xz\n')
        self.assertEqual(set(digest_rows(data['Checksums-Sha256'])),{'test.dsc','test.tar.xz'})

    def test_apt_encoded_plus_does_not_relax_hash_or_completeness(self):
        url='https://deb.debian.org/debian-security/pool/package_1%2bupdate.deb'
        signed={url.replace('%2b','+'):('a'*64,25)}
        rows={url:{'sha256':'a'*64,'size_bytes':25}}
        self.assertEqual(set(match_packages(rows,signed)),{url})
        with self.assertRaises(ValueError):match_packages({},signed)
        with self.assertRaises(ValueError):match_packages({url:{'sha256':'b'*64,'size_bytes':25}},signed)

    def test_refresh_cannot_change_the_release_path(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/freeze_private_candidate.py'),'/nonexistent','/nonexistent',*['a'*40]*3,
            '--attempt','17','--previous-attempt','16','--runtime-version','1.1.0-1','--menu-version','1.1.0-1+pcbm1',
            '--product-version','1.1.0','--candidate','release','--apt-refresh','/nonexistent'],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('APT refresh is private-development only',result.stderr)


if __name__=='__main__':unittest.main()
