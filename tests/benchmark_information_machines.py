"""Sanitized source/fixture cost measurements; neither Linux nor Pi qualification."""
import importlib.util
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
MENU=ROOT.parent/'project-cbm-menu'
sys.path.insert(0,str(ROOT/'runtime'))
from project_cbm import info, preferences
from project_cbm.data import registry
from test_runtime_foundation import Fixture
spec=importlib.util.spec_from_file_location('view',MENU/'lib/pcbm_info_view.py')
view=importlib.util.module_from_spec(spec);spec.loader.exec_module(view)


def measure(fn,n=100):
    samples=[]
    for _ in range(n):
        start=time.perf_counter();fn();samples.append((time.perf_counter()-start)*1000)
    return {'samples':n,'median_ms':round(statistics.median(samples),3),'max_ms':round(max(samples),3)}


with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'project-cbm';profiles=registry();preferences.update({'default_machine':'xvic'},path)
    data=info.collect(Fixture(),path);raw=json.dumps(data)
    env={**os.environ,'XDG_CONFIG_HOME':tmp,'PYTHONDONTWRITEBYTECODE':'1'}
    report={'platform':platform.system(),'architecture':platform.machine(),'python':platform.python_version(),'hardware_qualification':False}
    report['fixture_info_collect']=measure(lambda:info.collect(Fixture(),path))
    report['view_parse_and_prepare_80_columns']=measure(lambda:view.render(view.parse(raw),80))
    report['registry_load_and_validate']=measure(registry)
    report['preference_read']=measure(lambda:preferences.read(path,profiles))
    report['preference_atomic_write']=measure(lambda:preferences.update({'default_machine':'xvic'},path,profiles),30)
    report['default_selection']=measure(lambda:preferences.selection(path,profiles,''))
    def cli(name,args):
        subprocess.run([sys.executable,str(ROOT/'runtime/bin'/name),*args],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,env=env,check=True)
    report['info_cli_missing_linux_interfaces']=measure(lambda:cli('pcbm-info',['--json']),20)
    report['main_default_query_cli']=measure(lambda:cli('pcbm-profiles',['default']),20)
    report['machines_model_cli']=measure(lambda:cli('pcbm-profiles',['menu']),20)
    report['bash_shared_helper_start']=measure(lambda:subprocess.run(['/bin/bash','-c','source "$1"; pcbm_ui_result 0','test',str(MENU/'lib/pcbm-ui.sh')],check=True,stdout=subprocess.DEVNULL),20)
    # Full entry scripts with fake dialog/VICE and fixture JSON; no real interaction.
    sys.path.insert(0,str(MENU/'tests'))
    from test_information_machines import Consumers
    case=Consumers();case.setUp()
    try:
        def screen(name, choices):
            result=case.run_ui(name,choices)
            if result.returncode: raise RuntimeError('fixture_screen_failed')
        report['system_information_entry_fake_dialog']=measure(lambda:screen('pcbm-system-info',['MESSAGE']),20)
        report['machines_entry_fake_dialog']=measure(lambda:screen('pcbm-machines',['RETURN']),20)
        report['main_entry_fake_dialog']=measure(lambda:screen('pcbm-menu',['QUIT']),20)
    finally:
        case.doCleanups()
    print(json.dumps(report,indent=2))
