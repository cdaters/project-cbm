"""Verify a bounded private-development APT refresh; never downloads or changes a host.

The separate acquisition uses the existing HTTPS retention proxy and normal APT
authentication. This freeze-time check independently verifies fresh signatures,
expiry, index hashes, and the one admitted binary/corresponding-source delta.
"""
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
import gzip
import hashlib
import lzma
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import unquote
from build_contracts import read_json, verify_artifact
from build_environment import environment

SECURITY = 'https://deb.debian.org/debian-security/dists/trixie-security/'
UPDATES = 'https://deb.debian.org/debian/dists/trixie-updates/'
POOL = 'https://deb.debian.org/debian-security/'
VERSION = '92.0-1+deb13u1'


def fields(text):
    result = {}; key = None
    for line in text.splitlines():
        if line.startswith(' ') and key:
            result[key] += '\n' + line[1:]
        elif ': ' in line or line.endswith(':'):
            key, _, value = line.partition(':')
            if key in result: raise ValueError('duplicate repository field')
            result[key] = value.strip()
    return result


def fresh_release(text, codename, now=None):
    data = fields(text)
    now = now or datetime.now(timezone.utc)
    if data.get('Codename') != codename: raise ValueError('repository codename')
    start = parsedate_to_datetime(data['Date']); end = parsedate_to_datetime(data['Valid-Until'])
    if start.tzinfo is None or end.tzinfo is None or start > now + timedelta(seconds=10) or end <= now or end <= start:
        raise ValueError('repository metadata expired or not yet valid')
    return data


def digest_rows(value):
    result = {}
    for line in value.splitlines():
        if not line.strip(): continue
        sha, size, name = line.split()
        if len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha) or not size.isdigit():
            raise ValueError('repository checksum')
        if name.startswith('/') or '..' in Path(name).parts or name in result:
            raise ValueError('repository path')
        result[name] = (sha, int(size))
    return result


def match_packages(urls, advertised):
    admitted = {url:advertised[unquote(url)] for url in urls if unquote(url) in advertised}
    if {unquote(url) for url in admitted} != set(advertised):
        raise ValueError('incomplete authenticated package/source closure')
    for url,expected in admitted.items():
        row=urls[url]
        if (row['sha256'],row['size_bytes']) != expected: raise ValueError('package/source authentication mismatch')
    return admitted


def verify_refresh(directory, previous_urls):
    directory = Path(directory); transport = directory/'transport'
    urls = read_json(transport/'catalog.json')
    for row in urls.values(): verify_artifact(transport,row)
    # Other repository snapshots and previously captured pool bytes stay identical.
    for url, row in previous_urls.items():
        if not url.startswith(SECURITY) and url != UPDATES+'InRelease':
            if urls.get(url) != row: raise ValueError('refresh changed unrelated frozen input')
    releases = {}
    for base, codename in ((UPDATES,'trixie-updates'),(SECURITY,'trixie-security')):
        path = transport/urls[base+'InRelease']['path']
        with tempfile.TemporaryDirectory(prefix='verify-development-apt-',dir=directory.parent) as temp:
            authenticated=Path(temp)/'Release'
            subprocess.run(['/usr/bin/sqv','--keyring','/usr/share/keyrings/debian-archive-keyring.pgp',
                            '--cleartext','--output',str(authenticated),str(path)],check=True,
                           stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,env=environment())
            releases[base] = fresh_release(authenticated.read_text(),codename)
    indexes = {}
    for url,row in urls.items():
        base = next((base for base in releases if url.startswith(base)),None)
        if not base or url == base+'InRelease': continue
        signed = digest_rows(releases[base]['SHA256'])
        matches = [name for name,value in signed.items() if value == (row['sha256'],row['size_bytes'])]
        relative = url.removeprefix(base)
        if relative not in matches and not ('/by-hash/SHA256/' in relative and relative.rsplit('/',1)[1] == row['sha256'] and matches):
            raise ValueError('repository index not authenticated by fresh signature')
        for name in matches:
            if base == SECURITY and name in ('main/binary-arm64/Packages.xz','main/binary-arm64/Packages.gz','main/source/Sources.xz','main/source/Sources.gz'):
                raw=(transport/row['path']).read_bytes()
                indexes[name.rsplit('/',1)[1].split('.')[0]] = (lzma.decompress(raw) if name.endswith('.xz') else gzip.decompress(raw)).decode()
    binary = next(fields(s) for s in indexes['Packages'].split('\n\n') if fields(s).get('Package')=='mkvtoolnix')
    source = next(fields(s) for s in indexes['Sources'].split('\n\n') if fields(s).get('Package')=='mkvtoolnix' and fields(s).get('Version')==VERSION)
    if binary['Version'] != VERSION or binary['Architecture'] != 'arm64': raise ValueError('unreviewed binary delta')
    admitted = {POOL+binary['Filename']:(binary['SHA256'],int(binary['Size']))}
    admitted.update({POOL+source['Directory']+'/'+name:value for name,value in digest_rows(source['Checksums-Sha256']).items()})
    admitted = match_packages(urls,admitted)
    # New pool inputs are limited to the admitted security update and full source.
    for url in set(urls)-set(previous_urls):
        if url.startswith(SECURITY) or url == UPDATES+'InRelease': continue
        if url not in admitted: raise ValueError('unreviewed extra acquisition')
    return urls, admitted, {base:{key:data[key] for key in ('Date','Valid-Until','Codename')} for base,data in releases.items()}
