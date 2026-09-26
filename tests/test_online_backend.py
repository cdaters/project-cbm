"""Synthetic protocol/security tests; never contacts providers or downloads titles."""
import io
import json
from pathlib import Path
import socket
import sys
import unittest
import urllib.error
from email.message import Message
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from project_cbm import online_backend as o
from project_cbm.ingestion import Item

class Response(io.BytesIO):
    status=200
    def __init__(self, body=b'{}', kind='application/json', **headers):
        super().__init__(body);self.headers=Message();self.headers['Content-Type']=kind
        for k,v in headers.items():self.headers[k.replace('_','-')]=v
    def read1(self,n):return self.read(n)
class Opener:
    def __init__(self, response):self.response=response;self.requests=[]
    def open(self,request,timeout):
        self.requests.append(request)
        if isinstance(self.response,Exception):raise self.response
        return self.response
class Fixtures:
    def __init__(self,data):self.data=data;self.calls=[]
    def get(self,path,limit,cancelled):
        self.calls.append(path)
        if cancelled():raise o.OnlineError('cancelled')
        return 'application/json',json.dumps(self.data[path]).encode()

class Backend(unittest.TestCase):
    def test_identity_origin_and_transport_framing(self):
        op=Opener(Response());t=o.Transport(opener=op)
        self.assertEqual(t.get('search/categories',100)[1],b'{}')
        r=op.requests[0]
        self.assertEqual(r.get_header('Client-id'),'cbm')
        self.assertTrue(r.get_header('User-agent').startswith('Project-CBM/'))
        self.assertEqual(r.full_url,o.CENTRAL.base+'search/categories')
        for p in ('/evil','https://evil','../evil'):
            with self.assertRaises(o.OnlineError):t.get(p,1)

    def test_http_failures_redirects_and_rate_cooldown(self):
        for status,code in [(302,'backend_unavailable'),(401,'admission'),(403,'admission'),(464,'admission'),(500,'backend_unavailable'),(429,'rate_limit')]:
            error=urllib.error.HTTPError('https://fixture',status,'fixture',{'Retry-After':'30'},io.BytesIO(b'private'))
            op=Opener(error);t=o.Transport(opener=op,clock=lambda:10)
            with self.assertRaisesRegex(o.OnlineError,code):t.get('a',10)
            if status==429:
                with self.assertRaisesRegex(o.OnlineError,'rate_limit'):t.get('a',10)
                self.assertEqual(len(op.requests),1)
        self.assertIsNone(o.NoRedirect().redirect_request(None,None,None,None,None,None))

    def test_stream_bounds_length_encoding_and_cancel(self):
        for response in (Response(b'123',Content_Length='100'),Response(b'123',Content_Length='2'),Response(b'123',Content_Encoding='gzip'),Response(b'123')):
            with self.assertRaises(o.OnlineError):o.Transport(opener=Opener(response)).get('a',2)
        with self.assertRaisesRegex(o.OnlineError,'cancelled'):o.Transport().get('a',10,lambda:True)
        for error,code in [(TimeoutError(),'timeout'),(urllib.error.URLError(socket.gaierror()),'offline'),(OSError(),'connection')]:
            with self.assertRaisesRegex(o.OnlineError,code):o.Transport(opener=Opener(error)).get('a',10)

    def test_queries_cannot_inject_or_broaden(self):
        self.assertEqual(o.query({'name':'Last Ninja','group':'System 3'}),'name:"Last Ninja" & group:"System 3"')
        for fields in ({},{'unknown':'x'},{'name':'x | repo:csdb'},{'name':'x"'},{'name':'x\\y'},{'name':'x\x1b'},{'date':'1980-2000'}):
            with self.assertRaises(o.OnlineError):o.query(fields)

    def test_json_contract_and_error_envelope(self):
        for kind,body in [('text/html',b'{}'),('application/json',b'{"x":1,"x":2}'),('application/json',b'{"x":NaN}'),('application/json',b'x')]:
            with self.assertRaisesRegex(o.OnlineError,'incompatible'):o.json_body(kind,body)
        with self.assertRaisesRegex(o.OnlineError,'admission'):o.json_body('application/json',b'{"errorCode":464}')

    def test_metadata_file_mapping_cache_and_unsupported(self):
        release={'id':'123','category':1,'name':'Fixture'}
        transport=Fixtures({'search/meta/123/1':release,'search/entries/123/1':{'contentEntry':[
            {'id':0,'path':'disk1/a.prg','size':4},{'id':1,'path':'disk2/a.prg','size':4},{'id':2,'path':'rom.bin','size':8},{'id':3,'path':'._disk.prg','size':8}]}})
        backend=o.Backend(transport=transport)
        self.assertEqual(backend.metadata(release),release);backend.metadata(release)
        items,unsupported=backend.files(release)
        self.assertEqual([i.id for i in items],['0','1']);self.assertEqual(unsupported,2)
        self.assertEqual(len(transport.calls),2)
        transport.data['search/entries/123/1']['contentEntry'][0]['path']='../evil.prg'
        backend.cache.clear()
        with self.assertRaises(o.OnlineError):backend.files(release)

    def test_discovery_is_not_selection_or_failover(self):
        transport=Fixtures({'homeserver/all-public-servers':[{'id':1,'descr':'Fixture','url':'http://example.invalid'}]})
        backend=o.Backend(transport=transport)
        found=backend.discovery();self.assertFalse(found[0]['available'])
        self.assertEqual(backend.profile,o.CENTRAL)
        self.assertEqual(transport.calls,['homeserver/all-public-servers'])

    def test_profile_filters_are_scoped_and_preset_validated(self):
        transport=Fixtures({'search/aql/presets':[{'type':'repo','values':[{'aqlKey':'csdb','name':'CSDB'}]}]})
        backend=o.Backend(transport=transport)
        with self.assertRaisesRegex(o.OnlineError,'query'):backend.search({'repo':'invented'})
        self.assertEqual(len(transport.calls),1)

    def test_raw_and_multipart_never_save_envelope(self):
        item=Item('0','disk/test.prg',4,'fixture');raw=b'\x01\x08ab'
        self.assertEqual(o.payload('application/octet-stream',raw,item),raw)
        part=b'--BOUND\r\nContent-Type: application/octet-stream\r\nContent-Disposition: attachment; filename="test.prg"\r\n\r\n'+raw+b'\r\n'
        envelope=part+b'--BOUND--\r\n'
        self.assertEqual(o.payload('multipart/mixed; boundary=BOUND',envelope,item),raw)
        for bad in (part+part+b'--BOUND--\r\n',envelope.replace(b'test.prg',b'../evil.prg'),envelope.replace(b'test.prg',b'other.prg'),envelope[:-10]):
            with self.assertRaises(o.OnlineError):o.payload('multipart/mixed; boundary=BOUND',bad,item)
        for kind,body in [('text/html',raw),('application/octet-stream',b'<html>'),('application/octet-stream',raw+b'x')]:
            with self.assertRaises(o.OnlineError):o.payload(kind,body,item)

    def test_payload_format_plausibility(self):
        with self.assertRaisesRegex(o.OnlineError,'invalid_payload'):
            o.payload('application/octet-stream',b'bad sid!',Item('1','a.sid',8,'fixture'))
