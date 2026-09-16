#!/usr/bin/env python3
"""Deterministic owned BASIC V2 diagnostics and 35-track D64; Python stdlib only."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import tarfile

HERE=Path(__file__).resolve().parent
TOKENS={'END':0x80,'FOR':0x81,'NEXT':0x82,'DATA':0x83,'INPUT':0x85,'DIM':0x86,
 'READ':0x87,'LET':0x88,'GOTO':0x89,'RUN':0x8a,'IF':0x8b,'RESTORE':0x8c,
 'GOSUB':0x8d,'RETURN':0x8e,'REM':0x8f,'STOP':0x90,'POKE':0x97,'PRINT':0x99,
 'GET':0xa1,'TO':0xa4,'THEN':0xa7,'NOT':0xa8,'STEP':0xa9,'+':0xaa,'-':0xab,
 '*':0xac,'/':0xad,'^':0xae,'AND':0xaf,'OR':0xb0,'>':0xb1,'=':0xb2,'<':0xb3,
 'INT':0xb5,'PEEK':0xc2,'CHR$':0xc7,'ASC':0xc6}
PURPOSES={
 'pcbm-smoke.prg':('programs/Qualification','Visible PASS means BASIC loaded and executed; arithmetic result must be 4.'),
 'pcbm-sid-check.prg':('music/Qualification','Three separate original tones, triangle/saw/pulse; mono SID, no stereo or PSID/RSID claim.'),
 'pcbm-video-input.prg':('demos/Qualification','16 colors, moving star, key-code changes; joystick port 2 values printed; absent joystick UNTESTED.'),
 'pcbm-check.d64':('programs/Qualification','Disk autostarts the same smoke program; directory contains CBM SMOKE.')}


def tokenize(text):
    result=bytearray();quoted=False;i=0
    keys=sorted(TOKENS,key=len,reverse=True)
    while i<len(text):
        c=text[i]
        if c=='"':quoted=not quoted;result.append(ord(c));i+=1;continue
        token=next((k for k in keys if not quoted and text.startswith(k,i)),None)
        if token:result.append(TOKENS[token]);i+=len(token)
        else:
            if not 32<=ord(c)<127:raise ValueError('source must be uppercase ASCII BASIC')
            result.append(ord(c));i+=1
    if quoted:raise ValueError('unterminated string')
    return bytes(result)


def prg(source):
    result=bytearray(struct.pack('<H',0x801));address=0x801;last=-1
    for line in source.splitlines():
        number,text=line.split(' ',1);number=int(number)
        if not last<number<=63999:raise ValueError('ordered BASIC line numbers required')
        last=number;body=tokenize(text);address+=len(body)+5
        result+=struct.pack('<HH',address,number)+body+b'\0'
    return bytes(result+b'\0\0')


def sectors(track):return 21 if track<=17 else 19 if track<=24 else 18 if track<=30 else 17

def offset(track,sector):return (sum(sectors(t) for t in range(1,track))+sector)*256


def d64(program):
    disk=bytearray(174848);used={(18,0),(18,1)};chunks=[program[i:i+254] for i in range(0,len(program),254)]
    locations=[(t,s) for t in range(1,36) if t!=18 for s in range(sectors(t))][:len(chunks)]
    for i,(loc,chunk) in enumerate(zip(locations,chunks)):
        used.add(loc);p=offset(*loc)
        disk[p:p+2]=bytes(locations[i+1] if i+1<len(chunks) else (0,len(chunk)+1))
        disk[p+2:p+2+len(chunk)]=chunk
    bam=offset(18,0);disk[bam:bam+3]=bytes([18,1,65])
    for t in range(1,36):
        free=[s for s in range(sectors(t)) if (t,s) not in used];bits=sum(1<<s for s in free)
        disk[bam+t*4:bam+t*4+4]=bytes([len(free)])+bits.to_bytes(3,'little')
    disk[bam+0x90:bam+0xa0]=b'CBM QUAL 0.1.0'.ljust(16,b'\xa0')
    disk[bam+0xa0:bam+0xab]=b'\xa0\xa0CB\xa02A\xa0\xa0\xa0\xa0'
    p=offset(18,1);disk[p:p+2]=bytes([0,255]);disk[p+2:p+5]=bytes([0x82,*locations[0]])
    disk[p+5:p+21]=b'CBM SMOKE'.ljust(16,b'\xa0');disk[p+30:p+32]=len(chunks).to_bytes(2,'little')
    return bytes(disk)


def build(out,revision):
    if not re.fullmatch('[0-9a-f]{40}',revision):raise ValueError('exact source commit required')
    out.mkdir(parents=True,exist_ok=False);artifacts={}
    for source in sorted((HERE/'src').glob('*.bas')):artifacts[source.stem+'.prg']=prg(source.read_text())
    artifacts['pcbm-check.d64']=d64(artifacts['pcbm-smoke.prg'])
    manifest={'format':'project-cbm.qualification-media','version':'0.1.0','source_commit':revision,
              'author':'Project CBM contributors','license':'MIT','source_repository':'https://github.com/cdaters/project-cbm',
              'build':'python3 qualification/media/build.py OUTPUT --revision COMMIT',
              'independent_runtime_validation':'PENDING; structural/determinism checks are not known-good C64 qualification', 'files':[]}
    for name,data in artifacts.items():
        category,expectation=PURPOSES[name];(out/name).write_bytes(data)
        manifest['files'].append({'name':name,'destination':category+'/'+name,'source':'qualification/media/src/'+('pcbm-smoke.bas' if name.endswith('.d64') else name.replace('.prg','.bas')),'sha256':hashlib.sha256(data).hexdigest(),'size_bytes':len(data),'license':'MIT','expected_behavior':expectation})
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    (out/'LICENSE').write_bytes((HERE/'LICENSE').read_bytes())
    with tarfile.open(out/'qualification-media.tar','w') as archive:
        for p in sorted(out.iterdir()):
            if p.suffix=='.tar':continue
            info=tarfile.TarInfo(p.name);info.size=p.stat().st_size;info.mode=0o644;info.mtime=0
            with p.open('rb') as stream:archive.addfile(info,stream)
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output',type=Path);parser.add_argument('--revision',required=True)
    args=parser.parse_args();build(args.output,args.revision)
