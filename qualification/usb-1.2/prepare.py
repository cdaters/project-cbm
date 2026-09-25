#!/usr/bin/env python3
"""Create original, disposable USB qualification media in a NEW host directory.

No device access, formatting, mounting, downloads or writes to existing outputs.
Only usb-root's contents belong on the test USB; retain manifest/license outside it.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('cbm_media', ROOT / 'qualification/media/build.py')
media = importlib.util.module_from_spec(spec)
spec.loader.exec_module(media)


def build(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    usb = output / 'usb-root'
    collection = 'CBM12-USB-QUAL'

    def program(label):
        return media.prg('10 PRINT "' + label + '"\n20 END\n')

    files = {
        'Single/hello.PRG': program('CBM USB HELLO'),
        'Set/disk1.d64': media.d64(program('CBM USB DISK ONE VERSION ONE')),
        'Set/disk2.d64': media.d64(program('CBM USB DISK TWO')),
        'Nested/Child/nested.prg': program('CBM USB NESTED'),
        'Skip/unwanted.prg': program('CBM USB DESELECT ME'),
        'unsupported.txt': b'Original USB qualification text; do not import.\n',
        'unsupported.bin': b'Original unsupported fixture, not a ROM.\n',
        '.DS_Store': b'Synthetic metadata marker, not a Finder database.\n',
        '._hello.PRG': b'Synthetic AppleDouble-name marker.\n',
        '.Spotlight-V100/marker.txt': b'Synthetic metadata directory marker.\n',
    }
    for n in range(1, 22):
        files[f'Pages/page{n:02}.prg'] = program(f'CBM USB PAGE {n:02}')
    payloads = {f'{collection}/{name}': data for name, data in files.items()}
    selected = ('Single/hello.PRG', 'Set/disk1.d64', 'Set/disk2.d64', 'Nested/Child/nested.prg')
    for name in selected:
        payloads[f'Variants/{collection}/{name}'] = (
            media.d64(program('CBM USB DISK ONE VERSION TWO'))
            if name == 'Set/disk1.d64' else files[name])
    rows = []
    for name, data in sorted(payloads.items()):
        target = usb / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        rows.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    result = {
        'format': 'project-cbm.usb-qualification', 'version': 1,
        'status': 'NON-RELEASE / 1.2-development; physical results UNTESTED',
        'license': 'MIT; original Project CBM diagnostics',
        'expected_scans': {
            'whole partition with only usb-root contents': {'supported': 30, 'unsupported': 2, 'ignored_metadata': 3},
            collection: {'supported': 26, 'unsupported': 2, 'ignored_metadata': 3},
            collection + '/Set': {'supported': 2, 'unsupported': 0, 'ignored_metadata': 0},
            'Variants/' + collection: {'supported': 4, 'unsupported': 0, 'ignored_metadata': 0},
        },
        'selected_four': list(selected), 'files': rows,
    }
    (output / 'manifest.json').write_text(json.dumps(result, indent=2) + '\n')
    (output / 'LICENSE').write_bytes((ROOT / 'qualification/media/LICENSE').read_bytes())
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    result = build(args.output)
    print(json.dumps({'output': str(args.output), 'files': len(result['files']),
                      'expected_scans': result['expected_scans']}, indent=2))
