"""Read-only tree inventory. SHA-256 covers file bytes and xattrs; never follows symlinks."""
import argparse, collections, ctypes, datetime, hashlib, json, os, pathlib, stat, sys

def xattrs(path):
    if hasattr(os,'listxattr'):
        return {n:os.getxattr(path,n,follow_symlinks=False) for n in os.listxattr(path,follow_symlinks=False)}
    if sys.platform != 'darwin': raise RuntimeError('Extended attribute support required')
    libc=ctypes.CDLL(None,use_errno=True)
    libc.listxattr.restype=ctypes.c_ssize_t
    libc.getxattr.restype=ctypes.c_ssize_t
    name=os.fsencode(path)
    length=libc.listxattr(name,None,0,1)
    if length<0: raise OSError(ctypes.get_errno(),str(path))
    buf=ctypes.create_string_buffer(length)
    if libc.listxattr(name,buf,length,1)!=length: raise RuntimeError('xattr names changed')
    result={}
    for attr in buf.raw.split(b'\0'):
        if not attr: continue
        size=libc.getxattr(name,attr,None,0,0,1)
        if size<0: raise OSError(ctypes.get_errno(),str(path))
        value=ctypes.create_string_buffer(size)
        if libc.getxattr(name,attr,value,size,0,1)!=size: raise RuntimeError('xattr changed')
        result[os.fsdecode(attr)]=value.raw
    return result

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''): h.update(block)
    return h.hexdigest()

def classify(path):
    s=str(path).lower()
    if any(x in s for x in ['.img', '.git/', '.bundle', 'dotgit', 'build.log', 'diar', '.ds_store', 'releases-', 'repository-']):
        return 'PRIVATE-HISTORICAL'
    if any(x in s for x in ['/cover/', '/covers/', '/demos/', '/theverysecond', '.zip', '.tar.gz', '/fonts/']):
        return 'PROVENANCE-UNKNOWN'
    if any(x in s for x in ['license','sha256sums','/scripts/pcbm-', '/docs/pcbm-v1.0.0-docs/']):
        return 'PUBLIC/REDISTRIBUTABLE'
    return 'PRIVATE-HISTORICAL'

def inventory(root):
    paths=[root]
    for directory, dirs, files in os.walk(root, followlinks=False):
        paths.extend(pathlib.Path(directory)/n for n in dirs+files)
    result=[]
    for p in sorted(paths):
        s=p.lstat()
        e={'path':p.relative_to(root).as_posix(),'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,
           'classification':classify(p),'xattrs':{}}
        for attr,value in sorted(xattrs(p).items()):
            e['xattrs'][attr]={'bytes':len(value),'sha256':hashlib.sha256(value).hexdigest()}
        if stat.S_ISREG(s.st_mode):
            e.update(type='file',bytes=s.st_size,sha256=digest(p))
        elif stat.S_ISDIR(s.st_mode): e['type']='directory'
        elif stat.S_ISLNK(s.st_mode):
            e.update(type='symlink',target_sha256=hashlib.sha256(os.fsencode(os.readlink(p))).hexdigest())
        else: raise ValueError('Special file: '+str(p))
        after=p.lstat()
        assert (s.st_size,s.st_mtime_ns,s.st_mode)==(after.st_size,after.st_mtime_ns,after.st_mode), 'Changed during read: '+str(p)
        result.append(e)
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='action',required=True)
    c=sub.add_parser('create'); c.add_argument('root',type=pathlib.Path); c.add_argument('manifest',type=pathlib.Path)
    v=sub.add_parser('verify'); v.add_argument('manifest',type=pathlib.Path)
    args=ap.parse_args()
    if args.action=='create':
        assert args.root.is_dir() and args.root.is_absolute()
        assert not args.manifest.is_relative_to(args.root), 'Manifest must be outside inventoried tree'
        entries=inventory(args.root)
        data={'schema':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(args.root),
              'scope':'content, type, mode, mtime, xattr hashes; no atime/ACL/ownership guarantee; classifications provisional, not license grants',
              'entries':entries}
        with args.manifest.open('x') as f: json.dump(data,f,indent=2); f.write('\n')
        print(json.dumps({'manifest':str(args.manifest),'entries':len(entries),'bytes':sum(e.get('bytes',0) for e in entries),'sha256':digest(args.manifest),'classifications':dict(collections.Counter(e['classification'] for e in entries))}),flush=True)
    else:
        data=json.loads(args.manifest.read_text()); actual=inventory(pathlib.Path(data['root']))
        expected={e['path']:e for e in data['entries']}; got={e['path']:e for e in actual}
        differences=[p for p in sorted(expected.keys()|got.keys()) if expected.get(p)!=got.get(p)]
        print(json.dumps({'manifest':str(args.manifest),'verified':not differences,'entries':len(actual),'changed_paths':differences}),flush=True)
        raise SystemExit(bool(differences))

if __name__=='__main__': main()
