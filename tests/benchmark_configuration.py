"""Source/fixture measurements. No real Linux operations, dialog or hardware tests."""
import json
import os
from pathlib import Path
import platform
import re
import statistics
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime'))
sys.path.insert(0,str(ROOT.parent/'project-cbm-menu/tests'))
from project_cbm.configuration import decode
from test_configuration import FakeLinux, POLICY, req
from project_cbm.config_backend import apply
from test_config_ui import ConfigurationUI


def measure(fn,n=30):
    samples=[]
    for _ in range(n):
        start=time.perf_counter();fn();samples.append(1000*(time.perf_counter()-start))
    return {'samples':n,'median_ms':round(statistics.median(samples),3),'max_ms':round(max(samples),3)}


request=req('hostname',value='cbm-fixture');raw=json.dumps(request)
report={'date':'2026-09-16','platform':platform.system(),'architecture':platform.machine(),
        'python':platform.python_version(),'physical_qualification':False,
        'limits':'Mac source/fake dialog/fake Linux. Not Pi latency, real UI rendering, service execution or package footprint.'}
report['request_decode_validate']=measure(lambda:decode(raw),100)
report['fixed_adapter_fake_linux']=measure(lambda:apply(request,POLICY,FakeLinux()),100)
def cli():
    subprocess.run([sys.executable,str(ROOT/'runtime/bin/pcbm-config-operation'),'--validate'],input=raw,text=True,
                   stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
report['validation_cli_startup']=measure(cli)
case=ConfigurationUI();case.setUp()
try:
    def screen(choices):
        p=case.run_ui('pcbm-config',choices)
        if p.returncode:raise RuntimeError('fixture_screen_failed')
    report['configuration_open_back_fake_dialog']=measure(lambda:screen(['BACK']),20)
    report['configuration_region_back_fake_dialog']=measure(lambda:screen(['REGION','BACK','BACK']),20)
    report['configuration_about_fake_dialog']=measure(lambda:screen(['ABOUT','MESSAGE','BACK']),20)
    report['configuration_apply_fixture_hostname']=measure(lambda:screen(['NETWORK','HOSTNAME','cbm-fixture','BACK','BACK']),20)
finally:case.doCleanups()
if platform.system()=='Darwin':
    p=subprocess.run(['/usr/bin/time','-l',sys.executable,str(ROOT/'runtime/bin/pcbm-config-operation'),'--validate'],
                     input=raw,text=True,capture_output=True,check=True)
    m=re.search(r'(\d+)\s+maximum resident set size',p.stderr)
    report['validation_cli_peak_rss_bytes']=int(m[1]) if m else None
print(json.dumps(report,indent=2))
