#!/usr/bin/env python3
"""Read-only release-documentation checks; never execute appliance/build commands."""
import ast
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT.parent / 'project-cbm-menu'


def anchors(text):
    result = set()
    counts = {}
    in_code = False
    for line in text.splitlines():
        if line.startswith('```'):
            in_code = not in_code
        if in_code or not re.match(r'^#{1,6} ', line):
            continue
        title = re.sub(r'^#+\s+|\s+#+$', '', line)
        title = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', title)
        slug = ''.join(c for c in title.lower() if c in ' -_' or unicodedata.category(c)[0] in 'LN')
        slug = slug.replace(' ', '-')
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        result.add(slug if not n else slug + '-' + str(n))
    return result


def local_link_targets(text):
    """Inline Markdown links, including labels wrapped across lines."""
    # Ignore examples inside fenced blocks, which are not navigation links.
    prose = re.sub(r'^```[^\n]*\n.*?^```[^\n]*$', '', text, flags=re.M | re.S)
    return re.findall(r'\[[^\]]+\]\(([^)]+)\)', prose)


def main():
    checks = 0
    links = 0
    code_blocks = 0
    failures = []

    def check(ok, message):
        nonlocal checks
        checks += 1
        if not ok:
            failures.append(message)

    paths = [ROOT/'README.md', ROOT/'docs/README.md'] + sorted((ROOT/'docs/release').glob('*.md'))
    paths += sorted((ROOT/'docs/documentation').glob('*.md'))
    paths += [ROOT/'docs/build/official-factory-walkthrough.md']
    for p in paths:
        text = p.read_text()
        check(len(text.encode()) < 150000, f'{p}: oversized text')
        check(text.startswith('# '), f'{p}: missing title')
        check(sum(line.startswith('```') for line in text.splitlines()) % 2 == 0, f'{p}: unmatched fence')
        check(not re.search(r'-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}', text), f'{p}: secret pattern')
        if p.parent.name == 'release' or p.name == 'README.md':
            check(not re.search(r'/Volumes/|/Users/cdaters|Codex|ChatGPT|/home/pi/pcbm|Bookworm|POC4|attempt #?12', text, re.I), f'{p}: private/historical wording')
        for target in local_link_targets(text):
            if re.match(r'^[a-z]+:', target):
                continue
            name, _, fragment = target.partition('#')
            dest = p.parent / name if name else p
            check(dest.exists(), f'{p}: missing link {target}')
            if fragment and dest.exists() and dest.suffix == '.md':
                check(fragment in anchors(dest.read_text()), f'{p}: missing anchor {target}')
            links += 1
        for language, code in re.findall(r'```([^\n]*)\n(.*?)\n```', text, re.S):
            if language.strip() in ('sh', 'bash'):
                result = subprocess.run(['bash', '-n'], input=code, text=True, capture_output=True)
                check(result.returncode == 0, f'{p}: shell syntax {result.stderr.strip()}')
                code_blocks += 1
            elif language.strip() == 'python':
                try:
                    ast.parse(code)
                except SyntaxError as error:
                    check(False, f'{p}: Python example syntax {error}')
                else:
                    check(True, 'Python syntax')
        for rel in set(re.findall(r'(?<![\w/])((?:tools|build|runtime|tests)/[A-Za-z0-9_./-]+\.(?:py|sh|json|yaml|list))', text)):
            check((ROOT/rel).exists(), f'{p}: missing source path {rel}')

    manual = (ROOT/'docs/release/user-guide.md').read_text()
    all_docs = '\n'.join(p.read_text() for p in (ROOT/'docs/release').glob('*.md'))
    main_source = (MENU/'scripts/pcbm-menu').read_text()
    block = main_source.split('main_items=(', 1)[1].split('\n  )', 1)[0]
    main_items = re.findall(r'^\s+"([A-Z]+)"', block, re.M)
    check(len(main_items) == 8, 'Review main menu count change')
    for label in main_items:
        check(f'**{label}**' in manual, f'Missing Main Menu {label}')
    profiles = json.loads((ROOT/'runtime/data/profiles.json').read_text())['profiles']
    for profile in profiles:
        check(profile['name'] in manual, f'Missing user profile {profile["name"]}')
        check(f"`{profile['id']}`" in (ROOT/'docs/release/vice.md').read_text(), f'Missing technical profile {profile["id"]}')
    config = (MENU/'scripts/pcbm-config').read_text()
    # Every statically declared choose title/action, including nested CONTROL screens.
    for line in config.splitlines():
        if not re.search(r'\bchoose "', line):
            continue
        declaration = line.split('choose ', 1)[1].split(';', 1)[0]
        for label in re.findall(r'"([^"$]+)"', declaration):
            check(label.lower() in all_docs.lower(), f'Missing CONTROL title/action: {label}')
    for label in ('Starting / Pending', 'Unavailable', 'Failed', 'Turn On', 'Turn Off', 'How to connect', 'Refresh status'):
        check(label.lower() in all_docs.lower(), f'Missing state/action {label}')
    for relative, values in {
        'runtime/project_cbm/library.py': ['/home/pcbm/content'],
        'runtime/project_cbm/preferences.py': ['project-cbm', 'preferences.json'],
        'runtime/config/file-sharing.example.conf': ['[Project CBM]', 'valid users = pcbm'],
        'tools/install_poc_stage.py': ['/etc/hostname', 'projectcbm'],
    }.items():
        source = (ROOT/relative).read_text()
        for value in values:
            check(value in source, f'Path/account source changed: {relative}: {value}')
    versions = {
        'build/packages/runtime/debian/changelog': '1.1.0~rc3-1',
        'build/packages/vice/debian/changelog': '3.10-1+pcbm4',
        'build/packages/tcpser/debian/changelog': '1.1.6~beta-1+pcbm1',
    }
    for relative, version in versions.items():
        check(version in (ROOT/relative).read_text().splitlines()[0] and version in all_docs, f'Version mismatch: {relative}')
    check('1.1.0~rc3-1+pcbm1' in (MENU/'debian/changelog').read_text().splitlines()[0] and '1.1.0~rc3-1+pcbm1' in all_docs, 'Menu version mismatch')
    for rel, flags in {
        'tools/freeze_private_candidate.py': ['--attempt', '--previous-attempt', '--runtime-version', '--menu-version', '--product-version', '--candidate'],
        'tools/export_candidate.py': ['--attempt', '--menu-tag'],
        'tools/construct_poc.py': ['--attempt'],
        'tools/package_manifest.py': ['--image-sha256'],
        'tools/build_host.py': ['--workspace-config'],
    }.items():
        source = (ROOT/rel).read_text()
        for flag in flags:
            check(flag in source, f'Documented CLI flag missing: {rel} {flag}')
    inventory = json.loads((ROOT/'docs/release/installed-packages.json').read_text())
    check(inventory['package_count'] == len(inventory['packages']) == 672, 'Installed package manifest count')
    check(inventory['image_sha256'] == '5bde293b5ec6096e2a3bb2f9b31f123a8a07fdc6ac1f9077b510a4ceb5a1702e', 'Manifest image binding')
    for name in ('project-cbm-runtime', 'project-cbm-menu', 'project-cbm-vice', 'project-cbm-tcpser'):
        row = next((p for p in inventory['packages'] if p['name'] == name), None)
        check(row is not None and row['version'] in all_docs, f'Missing package version {name}')
    output = {'result': 'FAIL' if failures else 'PASS', 'checks': checks, 'documents': len(paths), 'local_links': links, 'shell_blocks_syntax_checked': code_blocks, 'main_items': main_items, 'profiles': len(profiles), 'failures': failures, 'commands_executed': 'bash -n only; no example or appliance/build command executed'}
    print(json.dumps(output, indent=2))
    return bool(failures)


if __name__ == '__main__':
    sys.exit(main())
