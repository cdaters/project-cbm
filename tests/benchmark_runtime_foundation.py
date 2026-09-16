#!/usr/bin/env python3
"""Developer-only microbenchmark. Fixtures are not Pi performance qualification."""
import json
import os
from pathlib import Path
import platform
import re
import statistics
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from test_runtime_foundation import Fixture
from project_cbm import info


def benchmark():
    result={'platform':platform.system(),'architecture':platform.machine(),'python':platform.python_version(),'units':'milliseconds unless noted','physical_pi':False}
    with tempfile.TemporaryDirectory() as tmp:
        fixture=Fixture();samples=[]
        for _ in range(100):
            start=time.perf_counter();info.collect(fixture,Path(tmp)/'missing');samples.append((time.perf_counter()-start)*1000)
        result['fixture_collection']={'samples':len(samples),'median_ms':statistics.median(samples),'max_ms':max(samples),'command_calls_per_collection':len(fixture.calls)//len(samples)}
        times=[];peak=[]
        for _ in range(20):
            cmd=[sys.executable,str(ROOT/'runtime/bin/pcbm-info'),'--json']
            if platform.system()=='Darwin':cmd=['/usr/bin/time','-l',*cmd]
            start=time.perf_counter()
            run=subprocess.run(cmd,capture_output=True,text=True,check=True,env={**os.environ,'XDG_CONFIG_HOME':tmp,'PYTHONDONTWRITEBYTECODE':'1'})
            times.append((time.perf_counter()-start)*1000)
            # Validate structure; never retain the development host's raw identity.
            assert json.loads(run.stdout)['format']=='project-cbm.info'
            m=re.search(r'(\d+)\s+maximum resident set size',run.stderr)
            if m:peak.append(int(m[1]))
        result['local_cli']={'samples':len(times),'median_ms':statistics.median(times),'max_ms':max(times),'maximum_rss_bytes_macos':max(peak) if peak else None,'limitation':'Mac missing Linux interfaces; includes cold Python/process startup, not Linux/Pi collector latency'}
        ui=ROOT.parent/'project-cbm-menu/lib/pcbm-ui.sh'
        times=[]
        for _ in range(20):
            start=time.perf_counter()
            subprocess.run(['/bin/bash','-c','source "$1"; if pcbm_ui_result 1; then exit 1; else [[ $PCBM_UI_STATUS == cancel ]]; fi','test',str(ui)],check=True)
            times.append((time.perf_counter()-start)*1000)
        result['ui_source_result']={'samples':len(times),'median_ms':statistics.median(times),'max_ms':max(times),'limitation':'Includes Bash startup; no real dialog rendering measured'}
    print(json.dumps(result,indent=2))


if __name__=='__main__':benchmark()
