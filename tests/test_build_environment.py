"""Factory environments ignore hostile ambient configuration; no host mutation."""
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from build_environment import environment, PATH

class BuildEnvironment(unittest.TestCase):
    def test_hostile_environment_not_inherited(self):
        hostile={k:'/builder-only/nonexistent' for k in (
            'TMPDIR','TMP','TEMP','HOME','USER','LOGNAME','PATH','XDG_CONFIG_HOME',
            'XDG_RUNTIME_DIR','LC_ALL','LANG','http_proxy','HTTPS_PROXY','ALL_PROXY',
            'PYTHONPATH','PYTHONHOME','PYTHONSTARTUP','GIT_CONFIG_GLOBAL','GIT_DIR',
            'CBM_KIT','CBM_RELEASE_LOCK','BASH_ENV','ENV','LD_PRELOAD','SUDO_USER')}
        with patch.dict(os.environ,hostile,clear=True):
            env=environment(1789513200,target=True)
        self.assertEqual(env['TMPDIR'],'/tmp')
        self.assertEqual(env['HOME'],'/root')
        self.assertEqual(env['PATH'],PATH)
        self.assertFalse(set(env.values()) & set(hostile.values()))
        self.assertEqual(set(env),{'PATH','HOME','USER','LOGNAME','LANG','LC_ALL',
            'TMPDIR','TMP','TEMP','PYTHONDONTWRITEBYTECODE','SOURCE_DATE_EPOCH','DEBIAN_FRONTEND'})
    def test_epoch_is_declared_not_inherited(self):
        with patch.dict(os.environ,{'SOURCE_DATE_EPOCH':'evil'}):
            self.assertNotIn('SOURCE_DATE_EPOCH',environment())
        for bad in ('1;id','',-1,True,'1\n',10**12):
            with self.assertRaises(ValueError):environment(bad)
    def test_mktemp_regression(self):
        bad=environment();bad['TMPDIR']='/builder-only/nonexistent-cbm-env-test'
        old=subprocess.run(['/bin/sh','-c','p=$(mktemp) || exit; rm -- "$p"'],env=bad,capture_output=True)
        self.assertNotEqual(old.returncode,0)
        new=subprocess.run(['/bin/sh','-c','p=$(mktemp) || exit; rm -- "$p"'],env=environment(target=True),capture_output=True)
        self.assertEqual(new.returncode,0,new.stderr)
    def test_pinned_shell_boundary_matches_python_contract(self):
        text=(Path(__file__).resolve().parents[1]/'build/pigen/target-environment.patch').read_text()
        for key,value in environment(target=True).items():
            self.assertIn(key+'='+value,text)
        self.assertEqual(text.count('/usr/bin/env -i'),2)
        self.assertIn('chmod 1777',text)
        stage=(Path(__file__).resolve().parents[1]/'tools/install_poc_stage.py').read_text()
        self.assertIn('env=target_env',stage)
        self.assertNotIn('os.environ.copy()',stage)
