import configparser
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import vice_presentation as vp

class Presentation(unittest.TestCase):
    def test_chip_defaults_and_no_pixel_override(self):
        config=configparser.ConfigParser();config.optionxform=str
        config.read_string(vp.defaults().decode())
        self.assertEqual(set(config),{'DEFAULT','Version',*vp.CHIPS})
        for section,chips in vp.CHIPS.items():
            self.assertEqual(set(config[section]),{chip+suffix for chip in chips for suffix in ['AspectMode','Fullscreen','FullscreenMode']})
            for chip in chips:
                self.assertEqual(config[section][chip+'AspectMode'],'2')
                self.assertEqual(config[section][chip+'Fullscreen'],'1')
                self.assertEqual(config[section][chip+'FullscreenMode'],'0')
        for forbidden in ['MachineVideoStandard','AspectRatio=','Window0','FullscreenCustom','GLFilter','MenuKey']:
            self.assertNotIn(forbidden,vp.defaults().decode())

    def test_initial_seed_preserves_preferences_and_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'sdl-vicerc'
            self.assertTrue(vp.seed(p));self.assertEqual(p.read_bytes(),vp.defaults())
            p.write_text('[C64SC]\nVICIIAspectMode=1\nVICIIFullscreen=0\n')
            original=p.read_bytes();self.assertFalse(vp.seed(p));self.assertEqual(p.read_bytes(),original)
            p.unlink();other=Path(tmp)/'other';other.write_text('unchanged');p.symlink_to(other)
            self.assertFalse(vp.seed(p));self.assertEqual(other.read_text(),'unchanged')

    def test_no_launch_or_boot_overwrite(self):
        first=(ROOT/'build/pigen/stage-cbm/files/first_boot.py').read_text()
        observer=(ROOT/'build/pigen/stage-cbm/files/engineering.py').read_text()
        for source in [first,observer]:
            self.assertNotIn('seed_presentation',source);self.assertNotIn('-VICIIaspectmode',source)
        self.assertIn("env['CBM_PRESENTATION_DIAGNOSTICS']='1'",observer)
        self.assertIn("command(['/usr/libexec/project-cbm-vice/drm-state'])",observer)
        probe=(ROOT/'build/packages/vice/debian/drm-state.c').read_text()
        for forbidden in ['drmSetMaster','drmModeSetCrtc','O_RDWR','EDID','sudo']:
            # EDID is mentioned only in exclusion comment.
            if forbidden!='EDID':self.assertNotIn(forbidden,probe)
        self.assertIn('geteuid() == 0',probe)
        patch=(ROOT/'build/packages/vice/debian/patches/presentation-diagnostics.patch').read_text()
        self.assertIn('cbm_records < 3',patch)
        self.assertIn('getenv("CBM_PRESENTATION_DIAGNOSTICS")',patch)

if __name__=='__main__':unittest.main()
