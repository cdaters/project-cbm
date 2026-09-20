import importlib.util
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from vice_performance import summarize


def records(speed=100,warp=0,count=12):
    return '\n'.join(f'VSync: CBM_PERFORMANCE sample={i+1} seconds=5.01 speed_percent={speed} emulated_fps=50.1 warp={warp}' for i in range(count))


class Performance(unittest.TestCase):
    def test_realtime_gate_and_no_private_context(self):
        out=summarize('unrelated private filename or credential\n'+records(),1,12)
        self.assertEqual(out['metric_gate'],'PASS')
        self.assertNotIn('credential',str(out));self.assertIn('NOT ESTABLISHED',out['physical_qualification'])

    def test_sustained_slowdown_and_warp_fail(self):
        for text in (records(80),records(100,1),records(103)):
            self.assertEqual(summarize(text,1,12)['metric_gate'],'FAIL')

    def test_explicit_interval_excludes_warp_and_weights_speed_and_fps(self):
        text=records(count=22)+'\nVSync: CBM_PERFORMANCE sample=23 seconds=5.01 speed_percent=195 emulated_fps=97.8 warp=1'
        out=summarize(text,10,21)
        self.assertEqual(out['metric_gate'],'PASS')
        self.assertEqual(out['sample_count'],12)
        self.assertAlmostEqual(out['weighted_emulated_fps'],50.1)
        self.assertEqual(out['samples'][0]['sample'],10)
        self.assertEqual(out['samples'][-1]['sample'],21)

    def test_missing_duplicate_short_windows_are_not_pass(self):
        for text in (records(count=10),records()+'\n'+records(count=1),records().replace('sample=5','sample=6')):
            self.assertNotEqual(summarize(text,1,12)['metric_gate'],'PASS')

    def test_bad_numeric_data_rejected(self):
        for text in (records().replace('seconds=5.01','seconds=0'),records().replace('speed_percent=100','speed_percent=nan'),records().replace('seconds=5.01','seconds=5..1')):
            with self.assertRaises(ValueError):summarize(text,1,12)
        with self.assertRaises(ValueError):summarize(records(),0,12)

    def test_seed_preserves_accuracy_features(self):
        import vice_presentation as p
        import configparser
        c=configparser.ConfigParser();c.read_string(p.defaults().decode())
        self.assertEqual(c['C64SC']['SidResidSampling'],'1')
        self.assertEqual(c['C64']['SidResidSampling'],'1')
        for section in c:
            self.assertNotIn('SidEngine',c[section]);self.assertNotIn('SidFilters',c[section])
            self.assertNotIn('Drive8TrueEmulation',c[section]);self.assertNotIn('VICIIFilter',c[section])

    def test_portable_optimization_and_bounded_telemetry(self):
        rules=(ROOT/'build/packages/vice/debian/rules').read_text()
        self.assertEqual(rules.count('-O3 -march=armv8-a -mtune=generic'),2)
        self.assertIn('hardening=+all',rules);self.assertNotIn('-march=native',rules)
        patch=(ROOT/'build/packages/vice/debian/patches/performance-diagnostics.patch').read_text()
        for required in ('cbm_records < 120','cbm_seconds >= 5.0','main_cpu_clock < cbm_clock','cbm_warp != warp_enabled','CBM_PRESENTATION_DIAGNOSTICS'):
            self.assertIn(required,patch)
        self.assertLess(patch.index('CBM_PERFORMANCE'),patch.index('if (metrics_reset)'))
