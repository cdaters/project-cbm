#!/usr/bin/env python3
"""Export clean, exact Product/Menu Git source into a registered external workspace."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('workspace',type=Path);p.add_argument('menu',type=Path)
    p.add_argument('--attempt',type=int,required=True);p.add_argument('--menu-tag',required=True)
    p.add_argument('--reuse-menu', action='store_true', help='Export an unchanged exact annotated Menu release; current HEAD may contain later documentation')
    a=p.parse_args();root=Path(__file__).resolve().parents[1];w=a.workspace.resolve(strict=True);menu=a.menu.resolve(strict=True)
    if not 1<=a.attempt<100 or not re.fullmatch(r'v1\.1\.0_(?:poc4\.[0-9]+|rc[0-9]+)',a.menu_tag):raise ValueError('candidate identity')
    if not (w/'.project-cbm-workspace.json').is_file():raise ValueError('registered external workspace required')
    for repo in (root,menu):
        if git(repo,'status','--porcelain'):raise ValueError('dirty source: '+str(repo))
    commit=git(root,'rev-parse','HEAD');mc=git(menu,'rev-parse',a.menu_tag+'^{commit}')
    if (not a.reuse_menu and mc!=git(menu,'rev-parse','HEAD')) or git(menu,'cat-file','-t',a.menu_tag)!='tag':raise ValueError('Menu must be at exact annotated tag')
    descriptors=[]
    for repo,ref,prefix,name in [(root,commit,'project-cbm/',f'project-cbm-integration-poc4-attempt{a.attempt}.tar'),(menu,mc,'project-cbm-menu-'+a.menu_tag[1:]+'/','project-cbm-menu-'+a.menu_tag[1:]+'.tar')]:
        path=w/'inputs'/name
        command=['git','-C',str(repo),'archive','--format=tar','--prefix='+prefix,ref]
        if a.reuse_menu and repo==menu and path.exists():
            if path.read_bytes()!=subprocess.check_output(command):raise ValueError('retained Menu archive differs from exact tag')
        else:
            with path.open('xb') as stream:subprocess.run(command,stdout=stream,check=True)
        descriptors.append({'path':str(path.relative_to(w)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size_bytes':path.stat().st_size})
    result={'attempt':a.attempt,'integration_commit':commit,'menu_commit':mc,'menu_tag':a.menu_tag,'menu_tag_object':git(menu,'rev-parse',a.menu_tag),'archives':descriptors}
    path=w/'inputs'/f'candidate-export-attempt{a.attempt}.json'
    with path.open('x') as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
