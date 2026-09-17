"""Offline payload checks detect missing/modified assets without a Pi."""
import hashlib,json,shutil,sys,tempfile,unittest,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];MENU=ROOT.parent/'project-cbm-menu'
sys.path.insert(0,str(ROOT/'tools'))
from validate_poc4_covers import inspect

class CoverPayload(unittest.TestCase):
    def test_exact_payload_then_modified_asset_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);root=base/'root';kit=base/'kit';kit.mkdir()
            def install(source,path):
                # This validator is the immutable attempt-3 contract, not a
                # next-candidate qualification of arbitrary current source.
                raw=(subprocess.check_output(['git','-C',str(MENU),'show','407ced58b711209631cdfb4db6dcd741a555f408:scripts/pcbm-run-vice'])
                     if path=='usr/bin/pcbm-run-vice' else source.read_bytes())
                dest=root/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
                descriptor={'path':hashlib.sha256(raw).hexdigest(),'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw)}
                (kit/descriptor['path']).write_bytes(raw);return descriptor
            cover={}
            for key,source,dest in [('manifest',MENU/'docs/cover-artwork.json','usr/share/doc/project-cbm-menu/cover-artwork.json'),('renderer',MENU/'lib/pcbm_cover_view.py','usr/libexec/project-cbm-menu/pcbm_cover_view.py'),('launcher',MENU/'scripts/pcbm-run-vice','usr/bin/pcbm-run-vice'),('wrapper',MENU/'scripts/pcbm-cover','usr/bin/pcbm-cover'),('registry',ROOT/'runtime/data/profiles.json','usr/share/project-cbm/runtime/data/profiles.json')]:
                cover[key]=install(source,dest)
            manifest=json.loads((MENU/'docs/cover-artwork.json').read_text())
            for f in manifest['files']:install(MENU/f['path'],'usr/share/project-cbm-menu/'+f['path'])
            for script in ('pcbm-config','pcbm-menu','pcbm-import'):install(MENU/'scripts'/script,'usr/bin/'+script)
            for tool in ('mc','alsamixer','timeout'):(root/'usr/bin'/tool).touch()
            status=root/'var/lib/dpkg/status';status.parent.mkdir(parents=True)
            names=('mc','mc-data','alsa-utils','libsdl2-image-2.0-0','libsdl2-2.0-0')
            status.write_text('\n\n'.join('Package: '+n+'\nStatus: install ok installed\nVersion: 1\nInstalled-Size: 1' for n in names))
            record={'covers':cover,'utilities':{n:{'metadata':{'Version':'1'}} for n in names[:3]}}
            result=inspect(root,record,kit);self.assertEqual(result['result'],'PASS',result)
            (root/'usr/share/project-cbm-menu/covers/pcbmcover-c64.jpg').write_bytes(b'changed')
            result=inspect(root,record,kit);self.assertEqual(result['result'],'FAIL');self.assertFalse(result['checks']['asset_c64'])

if __name__=='__main__':unittest.main()
