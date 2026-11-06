"""Local-only smoke tests for the Windows host, no GUI or Internet required."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0,str(Path(__file__).resolve().parents[1] / 'windows'))
from host import DeviceHost, PORT

class ProtocolTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix='conectatudo_')
        cls.server=DeviceHost(folder=cls.tmp.name)
        cls.server.start()
        cls.base=f'http://127.0.0.1:{PORT}'

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()
        cls.tmp.cleanup()

    def get(self,path):
        with urlopen(self.base+path+('&' if '?' in path else '?')+'pin='+self.server.pin,timeout=8) as r:
            return json.load(r)

    def post(self,path,body=b'',headers=None):
        r=Request(self.base+path+('&' if '?' in path else '?')+'pin='+self.server.pin,body,method='POST',headers=headers or {})
        with urlopen(r,timeout=8) as response: return json.load(response)

    def test_messages(self):
        self.post('/api/message','mensagem teste'.encode())
        self.assertEqual(self.get('/api/messages')['messages'][-1]['text'],'mensagem teste')

    def test_control_is_disabled(self):
        self.assertFalse(self.get('/api/control/status')['enabled'])
        with self.assertRaises(HTTPError) as error:
            self.post('/api/control/input',json.dumps({'action':'click'}).encode())
        self.assertEqual(error.exception.code,403)

    def test_resumable_upload(self):
        content=b'arquivo teste' * 60000
        identity='upTESTabcdef0123456789'
        item={'id':identity,'name':'smoke.txt','size':len(content)}
        self.assertEqual(self.post('/api/upload/init',json.dumps(item).encode())['offset'],0)
        first=262144
        self.assertEqual(self.post('/api/upload/chunk?id='+identity+'&offset=0',content[:first])['offset'],first)
        self.assertEqual(self.get('/api/upload/status?id='+identity)['offset'],first)
        self.assertEqual(self.post('/api/upload/init',json.dumps(item).encode())['offset'],first)
        self.assertEqual(self.post('/api/upload/chunk?id='+identity+'&offset='+str(first),content[first:])['offset'],len(content))
        self.assertTrue(self.post('/api/upload/finish?id='+identity)['ok'])
        self.assertEqual((Path(self.tmp.name)/'smoke.txt').read_bytes(),content)
        self.assertEqual(len(self.get('/api/files')['files']),1)

if __name__=='__main__':unittest.main()
