"""Read-only USB discovery and selected-file access, entirely unprivileged."""
from contextlib import contextmanager
import os
from pathlib import Path
import secrets
import stat
from .ingestion import Item, IngestError, EXTENSIONS, MAX_BYTES, component, directory

MAX_ENTRIES = 10000
MAX_DEPTH = 12
HOST_METADATA = {'.DS_Store', '.Spotlight-V100', '.Trashes', '.fseventsd',
                 '.TemporaryItems', '.VolumeIcon.icns', '.AppleDouble',
                 'System Volume Information', '$RECYCLE.BIN'}


def host_metadata(name):
    return name in HOST_METADATA or name.startswith('._')


def identity(status):
    return (status.st_dev, status.st_ino, status.st_size, status.st_mtime_ns, status.st_ctime_ns)


class Discovery:
    def __init__(self, source, source_id='usb'):
        self.source = Path(source)
        self.source_id = source_id
        self.folders = {'root': ()}
        self.items = {}
        self.selected = set()
        self.generation = secrets.token_hex(16)
        self.scope = ()
        self.counts = {}

    def folders_page(self, folder='root', offset=0):
        parts = self.folders[folder]
        rows = []
        with directory(self.source, parts) as fd:
            names = self.names(fd)
            for name in names:
                if host_metadata(name):
                    continue
                try:
                    component(name)
                except IngestError:
                    continue
                st = os.stat(name, dir_fd=fd, follow_symlinks=False)
                if stat.S_ISDIR(st.st_mode) and len(parts) < MAX_DEPTH:
                    child = (*parts, name)
                    key = next((k for k, v in self.folders.items() if v == child), None)
                    if key is None:
                        if len(self.folders) >= MAX_ENTRIES:
                            raise IngestError('entries')
                        key = secrets.token_hex(8)
                        self.folders[key] = child
                    rows.append({'id': key, 'name': name[:60]})
        return {'rows': rows[offset:offset+20], 'total': len(rows), 'scope': '/'.join(parts)[-180:] or 'Whole partition'}

    @staticmethod
    def names(fd):
        # Bound allocation too: os.listdir materializes an arbitrarily large folder.
        names = []
        with os.scandir(fd) as entries:
            for entry in entries:
                names.append(entry.name)
                if len(names) > MAX_ENTRIES:
                    raise IngestError('entries')
        return sorted(names)

    def scan(self, folder='root', cancelled=lambda: False):
        scope = self.folders[folder]
        items = {}
        counts = {'supported': 0, 'unsupported': 0, 'ignored_metadata': 0,
                  'unreadable': 0, 'bytes': 0, 'visited': 0}
        self.items = {}
        self.selected.clear()
        self.generation = secrets.token_hex(16)

        def walk(fd, parts, depth):
            if depth > MAX_DEPTH:
                raise IngestError('depth')
            for name in self.names(fd):
                if cancelled():
                    raise IngestError('cancelled')
                counts['visited'] += 1
                if counts['visited'] > MAX_ENTRIES:
                    raise IngestError('entries')
                if host_metadata(name):
                    counts['ignored_metadata'] += 1
                    continue
                try:
                    component(name)
                except IngestError:
                    counts['unsupported'] += 1
                    continue
                st = os.stat(name, dir_fd=fd, follow_symlinks=False)
                if stat.S_ISDIR(st.st_mode):
                    try:
                        child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                    except PermissionError:
                        counts['unreadable'] += 1
                        continue
                    try:
                        walk(child, (*parts, name), depth+1)
                    finally:
                        os.close(child)
                elif stat.S_ISREG(st.st_mode) and Path(name).suffix.lower() in EXTENSIONS:
                    path = '/'.join((*parts, name))
                    try:
                        item = Item(secrets.token_hex(8), path, st.st_size, self.source_id, identity(st))
                    except IngestError as error:
                        if str(error) == 'limit':
                            raise
                        counts['unsupported'] += 1
                        continue
                    counts['bytes'] += st.st_size
                    if counts['bytes'] > MAX_BYTES:
                        raise IngestError('limit')
                    items[item.id] = item
                    counts['supported'] += 1
                else:
                    counts['unsupported'] += 1

        with directory(self.source, scope) as fd:
            walk(fd, (), 0)
        self.scope, self.items, self.counts = scope, items, counts
        return {**counts, 'generation': self.generation}

    def page(self, offset=0):
        return {'rows': [{**i.summary(), 'selected': i.id in self.selected}
                         for i in list(self.items.values())[offset:offset+20]],
                'total': len(self.items), 'selected': len(self.selected), **self.counts}

    def select(self, mode, ids=(), selected=True):
        if mode == 'all':
            self.selected = set(self.items)
        elif mode == 'clear':
            self.selected.clear()
        elif mode in ('files', 'folder'):
            if not ids or len(ids) > 20 or not all(i in self.items for i in ids):
                raise IngestError('selection')
            chosen = set(ids)
            if mode == 'folder':
                # Collection anchored by a discovered file, no caller path.
                parents = {tuple(self.items[i].path.split('/')[:-1]) for i in ids}
                chosen = {i.id for i in self.items.values()
                          if any(tuple(i.path.split('/')[:-1])[:len(p)] == p for p in parents)}
            self.selected = self.selected | chosen if selected else self.selected - chosen
        else:
            raise IngestError('selection')
        return {'selected': len(self.selected)}

    @contextmanager
    def open(self, item):
        parts = item.path.split('/')
        with directory(self.source, (*self.scope, *parts[:-1])) as fd:
            inp = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
            with os.fdopen(inp, 'rb') as stream:
                status = os.fstat(stream.fileno())
                if not stat.S_ISREG(status.st_mode) or identity(status) != item.identity:
                    raise IngestError('source_changed')
                yield stream
                if identity(os.fstat(stream.fileno())) != item.identity:
                    raise IngestError('source_changed')
