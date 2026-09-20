#!/usr/bin/env python3
"""Guarded Lima implementation of the CBM Linux host contract (macOS arm64).

Requires requirements-contracts.txt. Never registers storage implicitly, substitutes
inputs, starts a container engine, or falls back to an internal filesystem.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile

from build_contracts import check_workspace, read_json

REPO = Path(__file__).resolve().parents[1]
PINS = REPO / 'build/host/inputs.json'


def contained(root, relative):
    path = root / relative
    if not path.resolve().is_relative_to(root) or (path.exists() and path.stat().st_dev != root.stat().st_dev):
        raise ValueError('build-host path escapes configured bulk filesystem')
    return path


def digest(path, algorithm):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, algorithm).hexdigest()


def verify(path, pin):
    if not path.is_file() or path.is_symlink() or digest(path, pin['algorithm']) != pin['digest']:
        raise ValueError('missing or mismatched retained input: ' + path.name)


def layout(config):
    root = check_workspace(config)
    paths = {k: contained(root, v) for k, v in {
        'state': 'build-host/lima', 'cache': 'cache/lima',
        'temp': 'build-host/tmp', 'inputs': 'inputs/build-host',
        'tools': 'build-host/tools', 'records': 'build-host/records',
    }.items()}
    if len(os.fsencode(str(paths['state'] / 'cbm/ssh.sock'))) >= 104:
        raise ValueError('Lima socket path too long')
    return root, paths


def cache_guard(paths, create=False):
    link = Path.home() / 'Library/Caches/lima'
    if link.is_symlink():
        if link.resolve(strict=True) != paths['cache']:
            raise ValueError('Lima cache symlink points elsewhere')
    elif link.exists():
        raise ValueError('existing unrelated Lima cache must be preserved by operator')
    elif create:
        link.symlink_to(paths['cache'], target_is_directory=True)
    else:
        raise ValueError('external Lima cache link not established')


def run(args, env=None):
    return subprocess.run(args, check=True, env=env)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-config', type=Path, required=True)
    parser.add_argument('command', choices=['preflight', 'prepare', 'acquire', 'install', 'render', 'lima'])
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    config = read_json(args.workspace_config)
    root, paths = layout(config)
    pins = read_json(PINS)
    if platform.system() != 'Darwin' or platform.machine() != 'arm64':
        raise ValueError('this frontend implementation requires macOS arm64')
    if args.command == 'preflight':
        print(json.dumps({'bulk_free_bytes': shutil.disk_usage(root).free,
                          'internal_free_bytes': shutil.disk_usage(Path.home()).free,
                          'disk_capacity_bytes': 256 * 1024**3,
                          'paths': {k: str(v) for k, v in paths.items()}}, indent=2))
        return
    if args.command == 'prepare':
        for path in paths.values():
            path.mkdir(parents=True, exist_ok=True, mode=0o700)
        cache_guard(paths, create=True)
        return
    cache_guard(paths)
    env = dict(os.environ, LIMA_HOME=str(paths['state']), TMPDIR=str(paths['temp']))
    prefix = paths['tools'] / ('lima-' + pins['lima_version'])
    env['PATH'] = str(prefix / 'bin') + os.pathsep + os.environ['PATH']
    if args.command == 'acquire':
        for key in args.arguments or ['lima', 'guest']:
            pin = pins[key]
            layout(config)  # Recheck storage immediately before each download.
            dest = contained(root, 'inputs/build-host/' + pin['filename'])
            if not dest.exists():
                partial = dest.with_suffix(dest.suffix + '.partial')
                run(['curl', '--fail', '--location', '--proto', '=https', '--proto-redir', '=https',
                     '--retry', '3', '--continue-at', '-', '--output', str(partial), pin['url']], env)
                verify(partial, pin)
                partial.rename(dest)
            verify(dest, pin)
            print('verified', key, pin['digest'], flush=True)
    elif args.command == 'install':
        archive = paths['inputs'] / pins['lima']['filename']
        verify(archive, pins['lima'])
        if prefix.exists():
            raise ValueError('versioned installation already exists; inspect rather than overwrite')
        with tarfile.open(archive) as tar:
            # data filter rejects traversal, escaping links and device nodes.
            tar.extractall(prefix, filter='data')
        run([str(prefix / 'bin/limactl'), '--version'], env)
    elif args.command == 'render':
        guest = paths['inputs'] / pins['guest']['filename']
        verify(guest, pins['guest'])
        template = (REPO / 'build/host/lima.yaml').read_text()
        if template.count('__GUEST_IMAGE_JSON__') != 1 or pins['guest']['digest'] not in template:
            raise ValueError('template/input identity mismatch')
        target = paths['records'] / 'cbm.yaml'
        target.write_text(template.replace('__GUEST_IMAGE_JSON__', json.dumps(str(guest))))
        print(target)
    else:
        if not args.arguments:
            raise ValueError('explicit limactl command required; see docs/build/lima-build-host.md')
        for name in ['default.yaml', 'override.yaml', 'base.yaml']:
            if (paths['state'] / '_config' / name).exists():
                raise ValueError('unexpected global Lima configuration: ' + name)
        binary = prefix / 'bin/limactl'
        version = subprocess.check_output([str(binary), '--version'], env=env, text=True).strip()
        if version != 'limactl version ' + pins['lima_version']:
            raise ValueError('unexpected Lima binary version')
        run([str(binary), *args.arguments], env)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print('build host stopped: ' + str(exc), file=sys.stderr)
        sys.exit(1)
