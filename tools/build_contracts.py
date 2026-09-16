#!/usr/bin/env python3
"""Offline CBM input/identity contracts. No build, download, mount or provisioning."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator
from referencing import Registry

SCHEMAS = Path(__file__).resolve().parents[1] / 'schemas'
MAX_JSON_BYTES = 1024 * 1024


def loads(raw):
    """Reject ambiguous JSON before schema validation; do not normalize hash inputs."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result

    def reject(_):
        raise ValueError('non-integer JSON number')

    if len(raw) > MAX_JSON_BYTES or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('JSON size/BOM policy')
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                          parse_float=reject, parse_constant=reject)
    except (UnicodeError, RecursionError) as exc:
        raise ValueError('invalid JSON encoding/depth') from exc


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True,
                       allow_nan=False) + '\n').encode('utf-8')


def read_json(path):
    with Path(path).open('rb') as stream:
        return loads(stream.read(MAX_JSON_BYTES + 1))


def validate_schema(value, name):
    def no_remote(_):
        raise ValueError('remote schema retrieval prohibited')
    schema = read_json(SCHEMAS / (name + '.schema.json'))
    validator = Draft202012Validator(schema, registry=Registry(retrieve=no_remote))
    error = next(validator.iter_errors(value), None)
    if error:
        # Report a field location/rule, not the potentially private rejected value.
        location = '/'.join(str(x) for x in error.absolute_path)
        raise ValueError(f'{name}: {location or "root"}: {error.validator}')


def relative_path(value):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/-]*', value):
        raise ValueError('invalid artifact locator')
    if any(part in ('', '.', '..') for part in value.split('/')):
        raise ValueError('noncanonical artifact locator')
    return Path(value)


def public_url(value):
    parsed = urlsplit(value)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username is not None
            or parsed.password is not None or parsed.query or parsed.fragment
            or any(c.isspace() or ord(c) < 32 for c in value) or '\\' in value):
        raise ValueError('source must be public HTTPS URL without credentials/query/fragment')


def artifacts(value):
    if isinstance(value, dict):
        if set(value) == {'path', 'size_bytes', 'sha256'}:
            yield value
        else:
            for child in value.values():
                yield from artifacts(child)
    elif isinstance(value, list):
        for child in value:
            yield from artifacts(child)


def validate_lock(raw, allow_fixture=False):
    lock = loads(raw)
    validate_schema(lock, 'release-lock')
    if lock['fixture'] and not allow_fixture:
        raise ValueError('synthetic fixture is not a candidate')
    version = lock['schema_version']
    if version == 1 and 'qualification_media' in lock or version == 2 and 'qualification_media' not in lock:
        raise ValueError('schema 2 requires declared engineering media; schema 1 forbids it')
    if (version >= 3) != ('optional_software' in lock):
        raise ValueError('schema 3/4 requires optional software; earlier schemas forbid it')
    if (version == 4) != ('runtime' in lock['components']):
        raise ValueError('schema 4 requires the runtime package; earlier schemas forbid it')
    if version < 4 and 'striketerm' in lock.get('optional_software',{}):
        raise ValueError('private StrikeTerm admission requires schema 4')
    if 'striketerm' in lock.get('optional_software',{}):
        from private_application import check_rights
        check_rights(lock,'private-engineering')
    seen = {}
    for artifact in artifacts(lock):
        relative_path(artifact['path'])
        identity = (artifact['sha256'], artifact['size_bytes'])
        if artifact['path'] in seen and seen[artifact['path']] != identity:
            raise ValueError('conflicting artifact locator')
        seen[artifact['path']] = identity

    def urls(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in ('origin', 'repository'):
                    public_url(child)
                    if not lock['fixture'] and urlsplit(child).hostname.endswith('.invalid'):
                        raise ValueError('synthetic origin in candidate')
                else:
                    urls(child)
        elif isinstance(value, list):
            for child in value:
                urls(child)
    urls(lock)
    if lock['base']['stages'] != ['stage0', 'stage1', 'stage2', 'stage-cbm']:
        raise ValueError('unsupported POC stage sequence')
    for name, component in lock['components'].items():
        package = component['package']
        expected_arch = 'all' if name in ('menu','runtime') else 'arm64'
        if (package['name'] != 'project-cbm-' + name or package['architecture'] != expected_arch
                or package['upstream_version'] != component['version'].replace('_', '~')
                or package['version'] != package['upstream_version'] + '-' + package['revision']):
            raise ValueError('component/package identity mismatch')
        if name in ('menu', 'tcpser', 'runtime') and 'git' not in component['source']:
            raise ValueError('component requires exact Git source identity')
        if name == 'menu' and component['source']['git']['ref'] != 'refs/tags/v' + component['version']:
            raise ValueError('Menu pin requires version tag and peeled commit')
        if name == 'vice' and (component['version'] != '3.10'
                or not {'--enable-sdl2ui', '--with-alsa'} <= set(component['build_options'])):
            raise ValueError('POC requires VICE 3.10 SDL2/ALSA')
    return lock


def validate_identity(identity):
    validate_schema(identity, 'installed-identity')
    if not (identity['build_id'] == identity['release_lock_sha256']
            == identity['manifest_lookup']['build_id']):
        raise ValueError('identity build-ID mismatch')


def make_identity(raw, allow_fixture=False):
    lock = validate_lock(raw, allow_fixture)
    digest = hashlib.sha256(raw).hexdigest()
    base = lock['base']
    identity = {
        'format': 'project-cbm.image-identity', 'schema_version': 1,
        'fixture': lock['fixture'], 'product': dict(lock['product']),
        'architecture': lock['architecture'],
        'integration_commit': lock['integration']['git']['commit'],
        'base': {key: base[key] for key in ('distribution', 'suite', 'release_identity')},
        'components': {name: {'version': c['version'], 'package_version': c['package']['version'],
                              'package_sha256': c['package']['artifact']['sha256']}
                       for name, c in lock['components'].items()},
        'configuration_schema_version': lock['configuration']['schema_version'],
        'build_id': digest, 'release_lock_sha256': digest,
        'manifest_lookup': {'format': 'project-cbm.release-manifest', 'build_id': digest},
    }
    identity['base']['pi_gen_commit'] = base['pi_gen']['git']['commit']
    validate_identity(identity)
    return identity


def verify_artifact(root, artifact):
    """Verify retained bytes; no URL fetching, extraction or implicit fallback."""
    root = Path(root).resolve(strict=True)
    try:
        target = (root / relative_path(artifact['path'])).resolve(strict=True)
        if not target.is_relative_to(root) or not target.is_file():
            raise ValueError('artifact escapes root or is not a file')
        digest = hashlib.sha256()
        with target.open('rb') as stream:
            if os.fstat(stream.fileno()).st_size != artifact['size_bytes']:
                raise ValueError('artifact size mismatch')
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
        if digest.hexdigest() != artifact['sha256']:
            raise ValueError('artifact checksum mismatch')
    except OSError as exc:
        raise ValueError('artifact unavailable') from exc


def check_workspace(config):
    """Read-only preflight. Marker and mount identity are operator configuration."""
    validate_schema(config, 'workspace-config')
    try:
        mount, workspace = (Path(config[key]) for key in ('mountpoint', 'workspace'))
        if mount == Path(mount.anchor):
            raise ValueError('bulk mount cannot be the host root filesystem')
        if str(mount) != config['mountpoint'] or str(workspace) != config['workspace']:
            raise ValueError('noncanonical workspace spelling')
        for path in (mount, workspace):
            if not path.is_absolute() or path.resolve(strict=True) != path or '..' in path.parts:
                raise ValueError('workspace paths must be absolute, existing and canonical')
        if not os.path.ismount(mount) or not workspace.is_dir():
            raise ValueError('configured volume/workspace unavailable')
        if workspace == mount or not workspace.is_relative_to(mount):
            raise ValueError('workspace must be below configured mount')
        if workspace.stat().st_dev != mount.stat().st_dev:
            raise ValueError('workspace is on a different filesystem')
        marker_path = workspace / '.project-cbm-workspace.json'
        if marker_path.is_symlink():
            raise ValueError('workspace marker must not be a symlink')
        marker = read_json(marker_path)
        if marker != {'workspace_id': config['workspace_id']}:
            raise ValueError('workspace identity mismatch')
        if shutil.disk_usage(workspace).free < config['minimum_free_bytes']:
            raise ValueError('insufficient bulk free space')
    except OSError as exc:
        raise ValueError('bulk workspace unavailable') from exc
    return workspace


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'identity', 'workspace'])
    parser.add_argument('input', type=Path)
    parser.add_argument('--allow-fixture', action='store_true', help='tests only; never image assembly')
    parser.add_argument('--artifact-root', type=Path, help='also verify every directly declared input file')
    args = parser.parse_args()
    try:
        if args.command == 'workspace':
            check_workspace(read_json(args.input))
        else:
            with args.input.open('rb') as stream:
                raw = stream.read(MAX_JSON_BYTES + 1)
            lock = validate_lock(raw, args.allow_fixture)
            if args.artifact_root:
                for artifact in artifacts(lock):
                    verify_artifact(args.artifact_root, artifact)
            if args.command == 'identity':
                sys.stdout.buffer.write(encode(make_identity(raw, args.allow_fixture)))
    except (ValueError, OSError) as exc:
        print(f'contract rejected: {type(exc).__name__}: {exc}' if isinstance(exc, ValueError)
              else 'contract rejected: input unavailable', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
