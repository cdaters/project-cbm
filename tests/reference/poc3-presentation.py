#!/usr/bin/env python3
"""Controlled software reference; not a Raspberry Pi or KMS qualification test.
Usage: python script.py VICE_SOURCE OUTPUT_DIR GENERATED_DEFAULTS
Uses existing compiled package binaries, no install or modification of package source.
"""
import configparser
import json
import os
from pathlib import Path
import re
import subprocess
import sys
base,out,defaults=map(Path,sys.argv[1:]);out.mkdir()
profiles={'x64':'C64','x64sc':'C64SC','xscpu64':'SCPU64','x64dtv':'C64DTV','x128':'C128','x128-80col':'C128','xcbm2':'CBM-II','xcbm5x0':'CBM-II-5x0','xvic':'VIC20','xplus4':'PLUS4','xpet':'PET'}
chips={'C64':['VICII'],'C64SC':['VICII'],'SCPU64':['VICII'],'C64DTV':['VICII'],'C128':['VICII','VDC'],'CBM-II':['Crtc'],'CBM-II-5x0':['VICII'],'VIC20':['VIC'],'PLUS4':['TED'],'PET':['Crtc']}
results=[]
for profile,section in profiles.items():
    for standard in (['pal','ntsc'] if profile=='x64sc' else ['default']):
        case=out/(profile+'-'+standard);(case/'config/vice').mkdir(parents=True);(case/'state/vice').mkdir(parents=True)
        (case/'config/vice/sdl-vicerc').write_bytes(defaults.read_bytes())
        env=dict(os.environ,XDG_CONFIG_HOME=str(case/'config'),XDG_STATE_HOME=str(case/'state'),SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',CBM_PRESENTATION_DIAGNOSTICS='1')
        exe='x128' if profile=='x128-80col' else profile
        argv=[str(base/'debian/build/src'/exe),'+logcolorize','-directory',str(base/'data'),'-sdl2backend','software','-sounddev','dummy','-logfile','-', '+sound','+warp','-limitcycles','3000000']
        if profile=='x128-80col':argv+=['-80col']
        if standard!='default':argv+=['-'+standard]
        argv+=['-dumpconfig',str(case/'resources.ini')]
        result=subprocess.run(argv,env=env,cwd=base,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30)
        log=result.stdout.decode(errors='replace');(case/'run.log').write_text(log)
        config=configparser.ConfigParser(strict=False,interpolation=None);config.optionxform=str;config.read(case/'resources.ini')
        actual={}
        for chip in chips[section]:
            for suffix,value in [('AspectMode','2'),('Fullscreen','1'),('FullscreenMode','0')]:
                key=chip+suffix;actual[key]=config[section][key];assert actual[key]==value,(profile,key,actual[key])
        geometry=[l for l in log.splitlines() if 'CBM_PRESENTATION chip=' in l]
        assert geometry,(profile,result.returncode,log[-1200:])
        assert result.returncode==1,(profile,result.returncode) # documented cycle-limit exit
        assert 'Machine initialization failed' not in log
        results.append({'profile':profile,'standard':standard,'resource_check':'PASS','geometry':geometry,'cycle_limit_exit':result.returncode})
# User preference and CLI precedence: a saved mode 1 / windowed is not overwritten.
case=out/'preferences';(case/'config/vice').mkdir(parents=True);(case/'state/vice').mkdir(parents=True)
settings=defaults.read_text().replace('[C64SC]\nVICIIAspectMode=2\nVICIIFullscreen=1','[C64SC]\nVICIIAspectMode=1\nVICIIFullscreen=0')
p=case/'config/vice/sdl-vicerc';p.write_text(settings)
env=dict(os.environ,XDG_CONFIG_HOME=str(case/'config'),XDG_STATE_HOME=str(case/'state'),SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',CBM_PRESENTATION_DIAGNOSTICS='1')
for name,extra,expected in [('saved',[],('1','0')),('cli',['-VICIIaspectmode','2','-VICIIfull'],('2','1'))]:
    args=[str(base/'debian/build/src/x64sc'),'+logcolorize','-directory',str(base/'data'),'-sdl2backend','software','-logfile','-','+sound','-warp','-limitcycles','100000',*extra,'-dumpconfig',str(case/(name+'.ini'))]
    r=subprocess.run(args,env=env,cwd=base,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=20)
    (case/(name+'.log')).write_bytes(r.stdout)
    config=configparser.ConfigParser(strict=False,interpolation=None);config.optionxform=str;config.read(case/(name+'.ini'))
    assert (config['C64SC']['VICIIAspectMode'],config['C64SC']['VICIIFullscreen'])==expected
    assert p.read_text()==settings
(out/'result.json').write_text(json.dumps({'scope':'SDL dummy/software reference only; no Pi KMS, display or audio qualification','profiles':results,'user_preferences_and_cli_precedence':'PASS'},indent=2)+'\n')
print('PASS',len(results),'profile/standard cases and preference/CLI precedence')
