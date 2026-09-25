"""Small unprivileged library planner/writer. Source adapters own all access."""
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import secrets
import stat

from . import library

MAX_BYTES = 2 * 1024**3
MARGIN = 256 * 1024**2
EXTENSIONS = frozenset('.prg .p00 .t64 .tap .d64 .d71 .d81 .g64 .g71 .x64 .sid .crt .d67 .d80 .d82 .g41 .p64 .mus'.split())


class IngestError(ValueError):
    pass


def component(value):
    if (not isinstance(value, str) or not value or value in ('.', '..')
            or '/' in value or '\\' in value or not value.isprintable()
            or len(value.encode('utf-8')) > 240):
        raise IngestError('unsafe_path')
    return value


def relative(value):
    if not isinstance(value, str) or len(value.encode('utf-8')) > 2048:
        raise IngestError('unsafe_path')
    return tuple(component(p) for p in value.split('/'))


@dataclass(frozen=True)
class Item:
    id: str
    path: str
    size: int
    source: str
    identity: tuple = ()
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        relative(self.path)
        if type(self.size) is not int or not 0 <= self.size <= MAX_BYTES:
            raise IngestError('limit')
        if Path(self.path).suffix.lower() not in EXTENSIONS:
            raise IngestError('unsupported')

    @property
    def format(self):
        return Path(self.path).suffix.lower()[1:]

    def summary(self):
        # Extensions are format evidence only, never game/machine classification.
        return {'id': self.id, 'name': self.path[:60], 'bytes': self.size,
                'format': self.format, 'category': 'unknown', 'family': 'unknown'}


@contextmanager
def directory(root, parts=(), create=False):
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for name in parts:
            component(name)
            if create:
                try:
                    os.mkdir(name, 0o755, dir_fd=fd)
                except FileExistsError:
                    pass
            nxt = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
        yield fd
    finally:
        os.close(fd)


def digest(stream, size, cancelled=lambda: False):
    result = hashlib.sha256()
    count = 0
    while True:
        if cancelled():
            raise IngestError('cancelled')
        data = stream.read(min(1024 * 1024, size - count + 1))
        if not data:
            break
        count += len(data)
        if count > size:
            raise IngestError('source_changed')
        result.update(data)
    if count != size:
        raise IngestError('source_changed')
    return result.hexdigest()


def existing_hash(root, path, size):
    """Hash only a same-size destination; never crawl/hash the entire library."""
    parts = relative(path)
    try:
        with directory(root, parts[:-1]) as parent:
            status = os.stat(parts[-1], dir_fd=parent, follow_symlinks=False)
            if not stat.S_ISREG(status.st_mode) or status.st_size != size:
                return 'conflict'
            fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
            with os.fdopen(fd, 'rb') as stream:
                current = os.fstat(stream.fileno())
                if not stat.S_ISREG(current.st_mode) or (current.st_ino, current.st_dev) != (status.st_ino, status.st_dev):
                    raise IngestError('destination_changed')
                return digest(stream, size)
    except FileNotFoundError:
        return None
    except (NotADirectoryError, OSError):
        # Unsafe or inaccessible parents are never followed, including symlinks.
        raise IngestError('destination_unavailable') from None


@dataclass(frozen=True)
class Plan:
    category: str
    family: str
    collection: str
    destination: str
    rows: tuple
    bytes: int
    kept_both: bool

    def summary(self):
        return {'destination': self.destination, 'selected': len(self.rows),
                'bytes': self.bytes, 'already_present': sum(r[2] == 'already_present' for r in self.rows),
                'kept_both': self.kept_both}


def plan(items, root, opener, category='programs', family='shared', collection='USB Import', cancelled=lambda: False, origin='Imported'):
    """One selected collection is never mixed with a conflicting release set."""
    if category not in ('games', 'demos', 'programs', 'music') or family not in library.FAMILIES:
        raise IngestError('classification')
    component(collection)
    if origin not in ('Imported', 'Downloaded'):raise IngestError('origin')
    if not items or len(items) > 10000 or len({i.path for i in items}) != len(items):
        raise IngestError('selection')
    if sum(i.size for i in items) > MAX_BYTES:
        raise IngestError('limit')
    hashes = {}
    base = f'{category}/{family}/{origin}'
    for suffix in range(1, 1001):
        name = collection if suffix == 1 else f'{collection} ({suffix})'
        component(name)
        destination = f'{base}/{name}'
        rows = []
        conflict = False
        for item in items:
            if cancelled():
                raise IngestError('cancelled')
            path = f'{destination}/{item.path}'
            found = existing_hash(root, path, item.size)
            if found is not None:
                if item.id not in hashes:
                    with opener(item) as stream:
                        hashes[item.id] = digest(stream, item.size, cancelled)
                if found != hashes[item.id]:
                    conflict = True
                    break
            rows.append((item, path, 'already_present' if found else 'save', hashes.get(item.id)))
        if not conflict:
            amount = sum(i.size for i, _, action, _ in rows if action == 'save')
            with directory(root) as fd:
                space = os.fstatvfs(fd)
                if space.f_bavail * space.f_frsize < amount + MARGIN:
                    raise IngestError('space')
            return Plan(category, family, collection, destination, tuple(rows), amount, suffix != 1)
    raise IngestError('collisions')


def save(planned, root, opener, record, cancelled=lambda: False):
    """Per-file atomic placement, with truthful partial results and private journal.

    `record` is supplied by the coordinator and must durably append provenance.
    An exclusive ingestion job lock is held by that coordinator during plan/save.
    """
    result = {'status': 'ok', 'saved': 0, 'already_present': 0, 'bytes': 0,
              'failed': 0, 'unattempted': len(planned.rows), 'kept_both': planned.kept_both,
              'destination': planned.destination}
    try:
        for item, path, action, expected in planned.rows:
            if cancelled():
                raise IngestError('cancelled')
            # Recheck the reviewed destination; do not silently choose a new path.
            found = existing_hash(root, path, item.size)
            if action == 'already_present':
                with opener(item) as stream:
                    current = digest(stream, item.size, cancelled)
                if found != expected or current != expected:
                    raise IngestError('plan_changed')
                result['already_present'] += 1
                result['unattempted'] -= 1
                continue
            if found is not None:
                raise IngestError('plan_changed')
            parts = relative(path)
            with directory(root, parts[:-1], create=True) as parent:
                space = os.fstatvfs(parent)
                if space.f_bavail * space.f_frsize < item.size + MARGIN:
                    raise IngestError('space')
                temp = '.pcbm-ingest-' + secrets.token_hex(16)
                record({'event': 'pending', 'path': path, 'temporary': '/'.join((*parts[:-1], temp))})
                fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644, dir_fd=parent)
                try:
                    with os.fdopen(fd, 'wb') as dst, opener(item) as src:
                        count = 0
                        hash_value = hashlib.sha256()
                        while True:
                            if cancelled():
                                raise IngestError('cancelled')
                            data = src.read(min(1024 * 1024, item.size - count + 1))
                            if not data:
                                break
                            count += len(data)
                            if count > item.size:
                                raise IngestError('source_changed')
                            dst.write(data)
                            hash_value.update(data)
                        if count != item.size:
                            raise IngestError('source_changed')
                        dst.flush()
                        os.fsync(dst.fileno())
                    # This link publishes a NEW inode, then removes its temp name.
                    # No link to source/existing content or mutable-image dedup.
                    os.link(temp, parts[-1], src_dir_fd=parent, dst_dir_fd=parent, follow_symlinks=False)
                    result['saved'] += 1
                    result['bytes'] += count
                    result['unattempted'] -= 1
                    os.fsync(parent)
                    record({'event': 'saved', 'path': path, 'source': item.source,
                            'original': item.path, 'sha256': hash_value.hexdigest(), 'bytes': count,
                            'time': datetime.now(timezone.utc).isoformat()})
                finally:
                    os.unlink(temp, dir_fd=parent)
    except (OSError, ValueError) as error:
        code = str(error) if isinstance(error, IngestError) else 'write_failed'
        result['error'] = code
        result['status'] = 'cancelled' if code == 'cancelled' else ('partial' if result['saved'] else 'failed')
        result['failed'] = 0 if code == 'cancelled' else 1
    return result
