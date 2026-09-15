#!/usr/bin/env python3
"""Private loopback acquisition/replay transport. APT signatures remain authoritative.

Resolve mode retains first-seen HTTPS bytes from an allowlisted upstream. Frozen
mode ONLY serves a separately hashed URL catalog; no upstream/network fallback.
Never use a resolving run as a release image. Run in Linux guest on ext4.
"""
import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import threading
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from urllib.error import HTTPError

HOSTS = {'deb.debian.org', 'security.debian.org', 'archive.raspberrypi.com', 'archive.raspberrypi.org'}


def canonical(url):
    parsed = urlsplit(url)
    if parsed.scheme not in ('http', 'https') or parsed.hostname not in HOSTS:
        raise ValueError('upstream origin outside allowlist')
    if parsed.username or parsed.password or parsed.port or parsed.query or parsed.fragment:
        raise ValueError('unsupported locator')
    return 'https://' + parsed.hostname + parsed.path


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--mode', choices=['resolve','frozen'], required=True)
    parser.add_argument('--port', type=int, default=3142)
    args=parser.parse_args()
    root=args.root.resolve(strict=True)
    catalog_path=root/'catalog.json'
    catalog=json.loads(catalog_path.read_text()) if catalog_path.exists() else {}
    if args.mode=='frozen' and not catalog: raise SystemExit('frozen catalog missing')
    mutex=threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path=='/':
                self.send_response(200); self.end_headers(); self.wfile.write(b'CBM retained APT transport\n'); return
            try:
                url=canonical(self.path)
                with mutex:
                    entry=catalog.get(url)
                    if entry is None:
                        if args.mode=='frozen':
                            self.send_error(404,'Absent frozen input'); return
                        name=hashlib.sha256(url.encode()).hexdigest()
                        target=root/name
                        temp=root/(name+'.partial')
                        with urlopen(Request(url, headers={'User-Agent':'Project-CBM-input-retention/1'}), timeout=120) as response:
                            # Reject redirection to unreviewed origins too.
                            canonical(response.url)
                            with temp.open('wb') as out: shutil.copyfileobj(response,out)
                        entry={'path':name,'sha256':sha256(temp),'size_bytes':temp.stat().st_size}
                        temp.rename(target); catalog[url]=entry
                        next_catalog=root/'catalog.next'
                        next_catalog.write_text(json.dumps(catalog,indent=2,sort_keys=True)+'\n')
                        next_catalog.replace(catalog_path)
                    path=root/entry['path']
                    if path.parent!=root or path.is_symlink() or not path.is_file(): raise ValueError('invalid retained path')
                    if path.stat().st_size!=entry['size_bytes'] or sha256(path)!=entry['sha256']:
                        raise ValueError('retained input checksum mismatch')
                self.send_response(200); self.send_header('Content-Length',str(entry['size_bytes'])); self.end_headers()
                with path.open('rb') as stream: shutil.copyfileobj(stream,self.wfile)
            except HTTPError as exc:
                self.send_error(exc.code,'Upstream unavailable')
            except (ValueError,OSError) as exc:
                print('retention rejected:',type(exc).__name__,str(exc),flush=True)
                self.send_error(502,'Acquisition or integrity failure')
        def do_CONNECT(self):
            self.send_error(405,'Use HTTP repository locators through this HTTPS-fetching transport')
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()


if __name__=='__main__': main()
