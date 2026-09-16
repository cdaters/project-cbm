"""User-only preference storage. Validated legacy import; no system configuration writes."""
import argparse
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import stat
import sys
import uuid

from .data import LIMIT, loads, registry

NAME = 'preferences.json'


def defaults(profiles):
    return {'schema_version': 1, 'default_machine': next(p['id'] for p in profiles if p['recommended']), 'boot_preference': 'menu'}


def validate(value, profiles):
    if not isinstance(value, dict) or set(value) != {'schema_version', 'default_machine', 'boot_preference'}:
        raise ValueError('preference_fields')
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise ValueError('preference_schema')
    if not isinstance(value['default_machine'], str) or value['default_machine'] not in {p['id'] for p in profiles}:
        raise ValueError('unknown_profile')
    if value['boot_preference'] not in ('menu', 'emulator'):
        raise ValueError('boot_preference')
    return value


def location():
    base = os.environ.get('XDG_CONFIG_HOME')
    if not base or not Path(base).is_absolute():
        base = str(Path.home() / '.config')
    return Path(base) / 'project-cbm'


def _safe_file(fd):
    s = os.fstat(fd)
    if not stat.S_ISREG(s.st_mode) or s.st_uid != os.geteuid() or s.st_nlink != 1 or s.st_mode & 0o077:
        raise ValueError('unsafe_preference_file')


def _load_at(directory):
    fd = os.open(NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
    try:
        _safe_file(fd)
        return loads(os.read(fd, LIMIT + 1))
    finally:
        os.close(fd)


@contextmanager
def _directory(path, create=False):
    if create:
        if os.geteuid() == 0:
            raise ValueError('root_write_refused')
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        s = os.fstat(fd)
        if s.st_uid != os.geteuid() or s.st_mode & 0o077:
            raise ValueError('unsafe_preference_directory')
        yield fd
    finally:
        os.close(fd)


def read(path=None, profiles=None):
    profiles = registry() if profiles is None else profiles
    path = location() if path is None else Path(path)
    try:
        with _directory(path) as fd:
            value = validate(_load_at(fd), profiles)
        return {'status': 'ok', 'source': 'user', 'values': value}
    except FileNotFoundError:
        return {'status': 'default', 'source': 'defaults', 'values': defaults(profiles)}
    except (OSError, ValueError, TypeError):
        return {'status': 'invalid', 'source': 'defaults', 'values': defaults(profiles)}


def update(changes, path=None, profiles=None, recover=False, initialize=None):
    profiles = registry() if profiles is None else profiles
    if not isinstance(changes, dict) or not set(changes) <= {'default_machine', 'boot_preference'}:
        raise ValueError('preference_fields')
    path = location() if path is None else Path(path)
    with _directory(path, create=True) as directory:
        lock = os.open('.preferences.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600, dir_fd=directory)
        try:
            _safe_file(lock)
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            malformed = False
            try:
                current = validate(_load_at(directory), profiles)
                if initialize is not None:
                    return current  # Recheck under lock: concurrent user choice wins.
            except FileNotFoundError:
                current = defaults(profiles)
                if initialize is not None:
                    current['default_machine'] = initialize
            except (ValueError, TypeError):
                if not recover:
                    raise ValueError('repair_required') from None
                # Only content/schema errors may be backed up: _safe_file is rechecked.
                old = os.open(NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
                try:
                    _safe_file(old)
                finally:
                    os.close(old)
                malformed = True
                current = defaults(profiles)
            value = validate({**current, **changes}, profiles)
            temporary = '.preferences.' + uuid.uuid4().hex
            fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
            try:
                with os.fdopen(fd, 'w') as stream:
                    json.dump(value, stream, sort_keys=True, indent=2)
                    stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
                if malformed:
                    # Copy bounded malformed bytes before replacement; interruption never
                    # changes the original's link count or destroys recovery evidence.
                    original = os.open(NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
                    try:
                        _safe_file(original)
                        raw = os.read(original, LIMIT + 1)
                        if len(raw) > LIMIT:
                            raise ValueError('oversized_manual_recovery_required')
                    finally:
                        os.close(original)
                    backup = os.open('preferences.invalid.' + uuid.uuid4().hex + '.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
                    with os.fdopen(backup, 'wb') as stream:
                        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
                os.replace(temporary, NAME, src_dir_fd=directory, dst_dir_fd=directory)
                os.fsync(directory)
            finally:
                try:
                    os.unlink(temporary, dir_fd=directory)
                except FileNotFoundError:
                    pass
            return value
        finally:
            os.close(lock)


LEGACY_MACHINE = Path('/etc/pcbm/default-machine.conf')


def legacy_machine(profiles, raw=None):
    """One bounded literal ID, never shell configuration or an executable path."""
    try:
        if raw is None:
            with LEGACY_MACHINE.open('r') as stream:
                raw = stream.read(257)
        value = raw.strip()
        return value if len(raw) <= 256 and value in {p['id'] for p in profiles} else None
    except (OSError, UnicodeError, AttributeError):
        return None


def selection(path=None, profiles=None, legacy_raw=None, *, snapshot=None):
    """Read-only effective RUN selection, including conservative compatibility fallback."""
    profiles = registry() if profiles is None else profiles
    state = read(path, profiles) if snapshot is None else snapshot
    machine = state['values']['default_machine']
    origin = state['source']
    if state['status'] != 'ok':
        legacy = legacy_machine(profiles, legacy_raw)
        if legacy:
            machine, origin = legacy, 'legacy_configuration'
    profile = next(p for p in profiles if p['id'] == machine)
    return {'id': machine, 'name': profile['name'], 'source': origin, 'preference_status': state['status']}


def initialize(path=None, profiles=None, legacy_raw=None):
    """Only missing preferences are initialized. Invalid/unsafe data stays untouched."""
    profiles = registry() if profiles is None else profiles
    state = selection(path, profiles, legacy_raw)
    if state['preference_status'] == 'default':
        update({}, path, profiles, initialize=state['id'])
    return selection(path, profiles, legacy_raw)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Project CBM user preferences')
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('show')
    setting = sub.add_parser('set'); setting.add_argument('key', choices=['default_machine', 'boot_preference']); setting.add_argument('value'); setting.add_argument('--recover', action='store_true'); setting.add_argument('--confirm', action='store_true')
    repair = sub.add_parser('recover'); repair.add_argument('--confirm', action='store_true', required=True)
    args = parser.parse_args(argv)
    try:
        if args.action == 'show':
            result = read()
        else:
            if args.action == 'set' and args.recover != args.confirm:
                raise ValueError('recovery_confirmation_required')
            result = update({args.key: args.value} if args.action == 'set' else {}, recover=args.action == 'recover' or args.recover)
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0
    except (ValueError, OSError, TypeError):
        print('Preference update could not be confirmed. Run show before retrying; check values, ownership or recovery instructions.', file=sys.stderr)
        return 2
