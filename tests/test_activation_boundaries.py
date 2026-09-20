"""Security/dispatch fixtures for activated services, import and optional inputs."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import subprocess
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'runtime'),str(ROOT/'tools')]
from project_cbm import importer, modem, wifi, configuration
from private_application import check_rights
from build_contracts import validate_lock, encode, make_identity


class Boundaries(unittest.TestCase):
    def test_fat_source_readable_by_copy_uid_without_widening_mount_policy(self):
        for filesystem in ('vfat','exfat'):
            options=set(importer.mount_options(filesystem).split(','))
            self.assertEqual(options,{'ro','nodev','nosuid','noexec','uid=1000',
                                      'gid=1000','fmask=0177','dmask=0077'})
        self.assertEqual(importer.mount_options('ext4'),'ro,nodev,nosuid,noexec,noload')
        for filesystem in ('exfat,rw','ntfs','/dev/sda1',''):
            with self.assertRaises(ValueError):importer.mount_options(filesystem)

    def test_inaccessible_source_directory_is_skipped_not_privileged(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);src=r/'source';src.mkdir();(src/'lost+found').mkdir();dest=r/'content';dest.mkdir()
            original=os.open
            def opened(path,*args,**kwargs):
                if path=='lost+found':raise PermissionError('root-only fixture')
                return original(path,*args,**kwargs)
            with patch.object(importer,'CONTENT',dest),patch.object(importer.os,'geteuid',return_value=1000),patch.object(importer.os,'open',side_effect=opened):
                self.assertEqual(importer.copy_content(src,'programs'),{'copied':0,'skipped':1,'bytes':0})

    def test_discovery_rejects_system_disk_including_nested_device_mapper(self):
        part={'name':'/dev/sda1','type':'part','fstype':'vfat','mountpoints':[None],'size':100000,'maj:min':'8:1'}
        disk={'name':'/dev/sda','type':'disk','tran':'usb','mountpoints':[None],'children':[part]}
        def probe(d):
            p=subprocess.CompletedProcess([],0,json.dumps({'blockdevices':[d]}),'')
            with patch.object(importer.subprocess,'run',return_value=p),patch.object(Path,'resolve',return_value=Path('/sys/devices/pci/usb1/test')),patch.object(Path,'read_text',return_value='42'):
                return importer.discover()
        self.assertEqual(len(probe(disk)),1)
        for d in [{**disk,'tran':'sata'},{**disk,'type':'loop'},
                  {**disk,'mountpoints':['/']},{**disk,'children':[{**part,'mountpoints':['/boot']}]}]:
            self.assertEqual(probe(d),[])
        d=copy.deepcopy(disk)
        d['children'].append({'name':'/dev/sda2','mountpoints':[None],
                              'children':[{'name':'/dev/mapper/root','mountpoints':['/']}]})
        self.assertEqual(probe(d),[])
    def test_import_rejects_paths_commands_and_arbitrary_mounts(self):
        good={'schema_version':1,'operation':'import','token':'a'*32,'category':'programs'}
        self.assertEqual(importer.validate_request(json.dumps(good)),good)
        for d in [{**good,'device':'/dev/sda'}, {**good,'category':'../../root'},
                  {**good,'token':'$(id)'}, {**good,'schema_version':True},
                  {**good,'operation':'mount'}, {**good,'options':'rw'},
                  {**good,'category':['programs']}]:
            with self.assertRaises(ValueError):importer.validate_request(json.dumps(d))
        with self.assertRaises(ValueError):importer.validate_request('{"schema_version":1,"schema_version":1}')
    def test_copy_is_unprivileged_nonoverwriting_and_classifies_sid(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);src=r/'source';src.mkdir();dest=r/'content';dest.mkdir()
            (src/'smoke.prg').write_bytes(b'original owned diagnostic fixture')
            (src/'test.sid').write_bytes(b'synthetic SID fixture, not playable')
            (src/'ignored.sh').write_text('not executed')
            (src/'redirect.prg').symlink_to('/etc/passwd')
            with patch.object(importer,'CONTENT',dest),patch.object(importer.os,'geteuid',return_value=1000):
                result=importer.copy_content(src,'programs')
                self.assertEqual(result['copied'],2);self.assertEqual(result['skipped'],2)
                self.assertTrue((dest/'music/Imported/test.sid').is_file())
                (dest/'programs/Imported/smoke.prg').write_bytes(b'owner changed')
                self.assertEqual(importer.copy_content(src,'programs')['copied'],0)
                self.assertEqual((dest/'programs/Imported/smoke.prg').read_bytes(),b'owner changed')
            self.assertFalse(list(dest.rglob('.pcbm-import-*')))
    def test_destination_symlink_and_root_copy_refused(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);src=r/'src';src.mkdir();(src/'test.prg').write_bytes(b'test')
            dest=r/'dest';dest.mkdir();(dest/'programs').symlink_to(r/'outside')
            with patch.object(importer,'CONTENT',dest),patch.object(importer.os,'geteuid',return_value=1000):
                with self.assertRaises(OSError):importer.copy_content(src,'programs')
            with patch.object(importer.os,'geteuid',return_value=0):
                with self.assertRaises(ValueError):importer.copy_content(src,'programs')
    def test_import_bounds_and_failed_copy_does_not_publish_partial_file(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);src=r/'src';src.mkdir();(src/'test.prg').write_bytes(b'test')
            dest=r/'dest';dest.mkdir()
            with patch.object(importer,'CONTENT',dest),patch.object(importer.os,'geteuid',return_value=1000):
                with patch.object(importer,'MAX_BYTES',3):
                    with self.assertRaises(ValueError):importer.copy_content(src,'programs')
                with patch.object(importer.os,'link',side_effect=OSError('fixture failure')):
                    with self.assertRaises(OSError):importer.copy_content(src,'programs')
            self.assertFalse(list(dest.rglob('*.prg')));self.assertFalse(list(dest.rglob('.pcbm-import-*')))
    def test_modem_fixed_loopback_and_no_trace_or_shell(self):
        args=modem.arguments({'schema_version':1,'port':25232,'baud':2400})
        self.assertEqual(args,['/usr/bin/tcpser','-v','127.0.0.1:25232','-s','2400','-l','0','-p','127.0.0.1:0'])
        for change in [{'port':'25232;id'},{'baud':0},{'args':'-t i'},{'schema_version':True}]:
            with self.assertRaises(ValueError):modem.arguments({'schema_version':1,'port':25232,'baud':2400,**change})
    def test_wifi_cache_escaping_deduplication_and_unsupported_networks(self):
        rows=wifi.parse('Test\\: Network:70:WPA2\nTest\\: Network:30:WPA2\nOpen:80:--\nEnterprise:90:WPA2 802.1X\n\\x01bad:NaN:WPA2\n')
        self.assertEqual(rows,[{'ssid':'Test: Network','signal_percent':70,'security':'WPA2'}])
        self.assertNotIn('BSSID',str(rows))
    def test_public_rights_gate_is_not_private_permission(self):
        lock={'product':{'candidate':'private-engineering-poc4'},'optional_software':{'striketerm':{
            'classification':'PRIVATE-ENGINEERING-ADMITTED','public_release_rights':'PUBLIC-RELEASE-RIGHTS-GATE-PENDING'}}}
        check_rights(lock,'private-engineering')
        with self.assertRaises(ValueError):check_rights(lock,'public-release')
        lock['product']['candidate']='public-release'
        with self.assertRaises(ValueError):check_rights(lock,'private-engineering')
    def test_runtime_package_schema_is_explicit_and_identity_minimal(self):
        lock=json.loads((ROOT/'tests/fixtures/release-lock.synthetic.json').read_text())
        lock['schema_version']=4
        a=lock['integration']['source']
        lock['optional_software']={'sid_wizard':{'version':'1.97','license':'LicenseRef-Hermit-WTF',
            'origin':'https://csdb.dk/getinternalfile.php/281063/SID-Wizard-1.97-sources-examples.tar.gz',
            **{k:a for k in ('source','artifact','recipe','rights_review')}}}
        c=copy.deepcopy(lock['components']['menu']);c['package']['name']='project-cbm-runtime'
        lock['components']['runtime']=c
        validate_lock(encode(lock),True)
        identity=make_identity(encode(lock),True)
        self.assertIn('runtime',identity['components']);self.assertNotIn('optional_software',identity)
        lock['schema_version']=3
        with self.assertRaises(ValueError):validate_lock(encode(lock),True)
