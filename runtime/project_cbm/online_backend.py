"""Original, bounded Assembly64 adapter implementing the published HTTP contract.

No reference-client code, credentials, automatic failover or background activity.
Profiles describe independently qualified server semantics, not interchangeable URLs.
"""
from dataclasses import dataclass
from email.parser import BytesParser
from email.policy import default
import http.client
import json
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request

from .ingestion import Item, IngestError, relative

MAX_JSON = 2 * 1024**2
MAX_FILE = 32 * 1024**2
MAX_SELECTION = 64 * 1024**2
PAGE = 20


class OnlineError(ValueError):
    pass


@dataclass(frozen=True)
class Profile:
    key: str
    label: str
    base: str
    client_id: str
    filters: tuple
    representations: tuple
    discovery: bool = False


CENTRAL = Profile('assembly64-central', 'Assembly64 Central',
                  'https://hackerswithstyle.se/leet/', 'cbm',
                  ('name', 'group', 'repo', 'category', 'date'),
                  ('application/octet-stream', 'multipart/mixed'), True)


def text(value, limit=240):
    if not isinstance(value, str) or not value or not value.isprintable() or len(value) > limit:
        raise OnlineError('incompatible')
    return value


def integer(value, maximum=2**31-1):
    if type(value) is not int or not 0 <= value <= maximum:
        raise OnlineError('incompatible')
    return value


def identifier(value):
    value = text(value, 128)
    if not re.fullmatch(r'[A-Za-z0-9_.-]+', value) or value in ('.', '..'):
        raise OnlineError('incompatible')
    return value


def query(fields, allowed=CENTRAL.filters):
    if not isinstance(fields, dict) or set(fields) - set(allowed):
        raise OnlineError('query')
    terms = []
    for key, value in fields.items():
        if not isinstance(value, str): raise OnlineError('query')
        value = value.strip()
        if not value: continue
        if len(value) > 100 or not value.isprintable() or re.search(r'["\\:&|()%!<>]', value):
            raise OnlineError('query')
        if key == 'date' and not re.fullmatch(r'[12][0-9]{3}', value): raise OnlineError('query')
        terms.append(key + ':"' + value + '"')
    if not terms: raise OnlineError('query')
    return ' & '.join(terms)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class Transport:
    """One request, no automatic retry. Explicit UI Retry obeys bounded cooldown."""
    def __init__(self, profile=CENTRAL, opener=None, clock=time.monotonic):
        self.profile, self.clock = profile, clock
        # Never inherit proxy credentials, .netrc, cookies or redirects.
        self.opener = opener or urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect)
        self.retry_after = 0

    def get(self, path, limit, cancelled=lambda: False):
        if self.clock() < self.retry_after: raise OnlineError('rate_limit')
        if cancelled(): raise OnlineError('cancelled')
        if path.startswith('/') or '://' in path or '..' in path.split('/'):
            raise OnlineError('request')
        request = urllib.request.Request(self.profile.base + path, headers={
            'User-Agent': 'Project-CBM/1.2-Online-Library', 'client-id': self.profile.client_id,
            'Accept': 'application/json, application/octet-stream, multipart/mixed',
            'Accept-Encoding': 'identity'})
        deadline = self.clock() + 45
        try:
            with self.opener.open(request, timeout=8) as response:
                if response.status != 200: raise OnlineError('backend_unavailable')
                if response.headers.get('Content-Encoding', 'identity').lower() != 'identity':
                    raise OnlineError('incompatible')
                size = response.headers.get('Content-Length')
                if size is not None and (not size.isdecimal() or int(size) > limit):
                    raise OnlineError('limit')
                body = bytearray()
                while True:
                    if cancelled(): raise OnlineError('cancelled')
                    if self.clock() >= deadline: raise OnlineError('timeout')
                    chunk = response.read1(min(65536, limit - len(body) + 1))
                    if not chunk: break
                    body.extend(chunk)
                    if len(body) > limit: raise OnlineError('limit')
                if size is not None and len(body) != int(size): raise OnlineError('download_failed')
                return response.headers.get('Content-Type', ''), bytes(body)
        except urllib.error.HTTPError as ex:
            with ex:
                if ex.code in (401, 403, 421, 422, 464): raise OnlineError('admission') from None
                if ex.code == 429:
                    wait = ex.headers.get('Retry-After', '')
                    self.retry_after = self.clock() + min(300, max(5, int(wait))) if wait.isdecimal() else self.clock() + 60
                    raise OnlineError('rate_limit') from None
                raise OnlineError('backend_unavailable') from None
        except (TimeoutError, socket.timeout): raise OnlineError('timeout') from None
        except urllib.error.URLError as ex:
            code = 'offline' if isinstance(ex.reason, (socket.gaierror, ConnectionRefusedError)) else 'connection'
            raise OnlineError(code) from None
        except (OSError, http.client.HTTPException): raise OnlineError('connection') from None


def json_body(kind, body):
    if kind.split(';')[0].strip().lower() != 'application/json': raise OnlineError('incompatible')
    try:
        def pairs(values):
            result = {}
            for k, v in values:
                if k in result: raise ValueError()
                result[k] = v
            return result
        value = json.loads(body, object_pairs_hook=pairs,
                           parse_constant=lambda x: (_ for _ in ()).throw(ValueError()))
    except (ValueError, RecursionError): raise OnlineError('incompatible') from None
    if isinstance(value, dict) and 'errorCode' in value:
        raise OnlineError('admission' if value['errorCode'] in (401,403,421,422,464) else 'backend_unavailable')
    return value


def payload(kind, body, item):
    """HTTP framing is handled by urllib; MIME is a separate bounded envelope.

    One explicitly selected file per call: exactly one part is admitted. A server
    needing set-oriented multipart downloads needs a separately qualified profile.
    """
    media = kind.split(';')[0].strip().lower()
    if media == 'multipart/mixed':
        if len(kind) > 512 or '\r' in kind or '\n' in kind: raise OnlineError('incompatible')
        message = BytesParser(policy=default).parsebytes(b'Content-Type: ' + kind.encode('ascii') + b'\r\nMIME-Version: 1.0\r\n\r\n' + body)
        if message.defects or not message.is_multipart(): raise OnlineError('incompatible')
        parts = list(message.iter_parts())
        if len(parts) != 1: raise OnlineError('unexpected_parts')
        part = parts[0]
        if part.defects or part.is_multipart() or part.get_content_type() != 'application/octet-stream':
            raise OnlineError('incompatible')
        if part.get('Content-Transfer-Encoding', 'binary').lower() not in ('binary', '8bit'):
            raise OnlineError('incompatible')
        suggested = part.get_filename()
        if suggested is not None:
            try: relative(suggested)
            except IngestError: raise OnlineError('incompatible') from None
            if suggested not in (item.path, item.path.split('/')[-1]): raise OnlineError('unexpected_parts')
        body = part.get_payload(decode=True)
        if part.defects: raise OnlineError('incompatible')
    elif media != 'application/octet-stream': raise OnlineError('incompatible')
    if not isinstance(body, bytes) or len(body) != item.size or len(body) > MAX_FILE:
        raise OnlineError('download_failed')
    # This is format plausibility, never a malware/ROM compatibility claim.
    if len(body) < 3 or body.lstrip()[:32].lower().startswith((b'<!doctype', b'<html', b'{"error', b'<error')):
        raise OnlineError('invalid_payload')
    signatures = {'sid': (b'PSID', b'RSID'), 'p00': (b'C64File\x00',), 'tap': (b'C64-TAPE-RAW', b'C16-TAPE-RAW'),
                  'crt': (b'C64 CARTRIDGE   ', b'C128 CARTRIDGE  '), 'g64': (b'GCR-1541',), 'g71': (b'GCR-1571',)}
    if item.format in signatures and not body.startswith(signatures[item.format]): raise OnlineError('invalid_payload')
    return body


class Backend:
    def __init__(self, profile=CENTRAL, transport=None, clock=time.monotonic):
        self.profile, self.clock = profile, clock
        self.transport = transport or Transport(profile)
        self.cache = {}

    def get_json(self, path, cancelled=lambda: False, ttl=300):
        previous = self.cache.get(path)
        if previous and self.clock() - previous[0] < ttl: return previous[1]
        value = json_body(*self.transport.get(path, MAX_JSON, cancelled))
        if len(self.cache) >= 32: self.cache.pop(next(iter(self.cache)))
        self.cache[path] = self.clock(), value
        return value

    def presets(self, cancelled=lambda: False):
        values = self.get_json('search/aql/presets', cancelled, 600)
        if not isinstance(values, list) or len(values) > 32: raise OnlineError('incompatible')
        result = {}
        for group in values:
            if not isinstance(group, dict): raise OnlineError('incompatible')
            key = group.get('type')
            if key not in self.profile.filters or key in ('name', 'group'): continue
            rows = group.get('values')
            if not isinstance(rows, list) or len(rows) > 128: raise OnlineError('incompatible')
            result[key] = [(text(r['aqlKey'], 40), text(r.get('name', r['aqlKey']), 80)) for r in rows]
        return result

    def discovery(self, cancelled=lambda: False):
        if not self.profile.discovery: raise OnlineError('unsupported')
        values = self.get_json('homeserver/all-public-servers', cancelled, 600)
        if not isinstance(values, list) or len(values) > 100: raise OnlineError('incompatible')
        result = []
        for row in values:
            url = text(row['url'], 512); parsed = urllib.parse.urlsplit(url)
            if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username or parsed.password:
                raise OnlineError('incompatible')
            result.append({'name': text(row['descr'], 120), 'transport': parsed.scheme,
                           'available': False, 'reason': 'Not qualified for selection in this version'})
        return result

    @staticmethod
    def release(row):
        if not isinstance(row, dict): raise OnlineError('incompatible')
        result = {'id': identifier(row['id']), 'category': integer(row['category']), 'name': text(row['name'])}
        for key in ('group', 'released', 'handle'):
            if row.get(key): result[key] = text(row[key], 1000)
        if row.get('year') is not None: result['year'] = integer(row['year'], 9999)
        return result

    def search(self, fields, offset=0, cancelled=lambda: False):
        integer(offset, 1000)
        # Never silently ignore unsupported filters or locally invented presets.
        presets = self.presets(cancelled) if any(k not in ('name','group') and v for k,v in fields.items()) else {}
        for k,v in fields.items():
            if k not in ('name','group') and v and v not in [x[0] for x in presets.get(k, [])]: raise OnlineError('query')
        path = f'search/aql/{offset}/{PAGE}?' + urllib.parse.urlencode({'query': query(fields, self.profile.filters)})
        rows = self.get_json(path, cancelled)
        if not isinstance(rows, list) or len(rows) > PAGE: raise OnlineError('incompatible')
        return [self.release(row) for row in rows]

    def metadata(self, release, cancelled=lambda: False):
        row = self.release(self.get_json(f'search/meta/{identifier(release["id"])}/{integer(release["category"])}', cancelled))
        if (row['id'],row['category']) != (release['id'],release['category']): raise OnlineError('incompatible')
        return row

    def files(self, release, cancelled=lambda: False):
        rows = self.get_json(f'search/entries/{identifier(release["id"])}/{integer(release["category"])}', cancelled)
        rows = rows.get('contentEntry') if isinstance(rows, dict) else None
        if not isinstance(rows, list) or len(rows) > 1000: raise OnlineError('incompatible')
        items, unsupported, seen, paths = [], 0, set(), set()
        for row in rows:
            key = str(integer(row['id'])); path = text(row['path'], 2048); size = integer(row['size'], 2**40)
            if key in seen or path in paths: raise OnlineError('incompatible')
            seen.add(key); paths.add(path)
            try: item = Item(key, path, size, self.profile.key, metadata={'release':release['id'],'category':release['category']})
            except IngestError as ex:
                if str(ex) in ('unsupported', 'limit'): unsupported += 1; continue
                raise OnlineError('incompatible') from None
            if size > MAX_FILE: unsupported += 1; continue
            items.append(item)
        return items, unsupported

    def download(self, release, item, cancelled=lambda: False):
        path = f'search/bin/{identifier(release["id"])}/{integer(release["category"])}/{identifier(item.id)}'
        kind, body = self.transport.get(path, min(MAX_FILE, item.size) + 65536, cancelled)
        if kind.split(';')[0].strip().lower() not in self.profile.representations: raise OnlineError('incompatible')
        return payload(kind, body, item)
