import unittest
import requests
import sys
import os
sys.path.insert(1, '/usr/lib/google-cloud-sdk/platform/google_appengine')
sys.path.insert(1, '/usr/lib/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
if 'google' in sys.modules:
    del sys.modules['google']

os.environ['APPLICATION_ID'] = 'sillywalkplus'
from google.appengine.ext import testbed


class FlowsTestCase(unittest.TestCase):

    def setUp(self):
        self.tb = testbed.Testbed()
        self.tb.activate()
        self.tb.init_datastore_v3_stub()
        self.tb.init_memcache_stub()
        self.base_url = 'http://127.0.0.1:8080'


    def build_url(self, url):
        return '{}/{}'.format(self.base_url, url)

    def test_flow_1(self):
        """
        1.      Input: http://_your-app-id_.appspot.com/set?name=ex&value=10
        Output:`
        """
        url = self.build_url('set?name=ex&value=10')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)
        """
        2.      Input: http://_your-app-id_.appspot.com/get?name=ex
        Output: 10
        """
        url = self.build_url('get?name=ex')
        res = requests.get(url)
        self.assertEqual(res.content, '10')
        """
        3.      Input: http://_your-app-id_.appspot.com/unset?name=ex
        Output:
        """
        url = self.build_url('unset?name=ex')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)
        """
        4.      Input: http://_your-app-id_.appspot.com/get?name=ex
        Output: None

        """
        url = self.build_url('get?name=ex')
        res = requests.get(url)
        self.assertEqual(res.content, 'None')
        """
        5.      Input: http://_your-app-id_.appspot.com/end
        Output:

        """
        url = self.build_url('end')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)

    def test_flow_2(self):
        """
        1.      Input: http://_your-app-id_.appspot.com/set?name=a&value=10
        Output:
        """
        url = self.build_url('set?name=a&value=10')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)
        """
        2.      Input: http://_your-app-id_.appspot.com/set?name=b&value=10
        Output:
        """
        url = self.build_url('set?name=b&value=10')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)
        """
        3.      Input: http://_your-app-id_.appspot.com/numequalto?value=10
        Output: 2
        """
        url = self.build_url('numequalto?value=10')
        res = requests.get(url)
        self.assertEqual(res.content, '2')
        """
        4.      Input: http://_your-app-id_.appspot.com/numequalto?value=20
        Output: 0
        """
        url = self.build_url('numequalto?value=20')
        res = requests.get(url)
        self.assertEqual(res.content, '0')
        """
        5.      Input: http://_your-app-id_.appspot.com/set?name=b&value=30
        Output:
        """
        url = self.build_url('set?name=b&value=30')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)
        """
        6.      Input: http://_your-app-id_.appspot.com/numequalto?value=10
        Output: 1
        """
        url = self.build_url('numequalto?value=10')
        res = requests.get(url)
        self.assertEqual(res.content, '1')
        """
        7.      Input: http://_your-app-id_.appspot.com/end
        Output: 
        """
        url = self.build_url('end')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)

    def test_flow_3(self):
        """
        1.      Input: http://_your-app-id_.appspot.com/set?name=a&value=10
        Output:
        """
        url = self.build_url('set?name=a&value=10')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)
        """
        2.      Input: http://_your-app-id_.appspot.com/set?name=b&value=20
        Output:
        """
        url = self.build_url('set?name=b&value=20')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)
        """
        3.      Input: http://_your-app-id_.appspot.com/get?name=a
        Output: 10
        """
        url = self.build_url('get?name=a')
        res = requests.get(url)
        self.assertEqual(res.content, '10')
        """
        4.      Input: http://_your-app-id_.appspot.com/get?name=b
        Output: 20
        """
        url = self.build_url('get?name=b')
        res = requests.get(url)
        self.assertEqual(res.content, '20')
        """
        5.      Input: http://_your-app-id_.appspot.com/undo
        Output:
        """
        url = self.build_url('undo')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)
        """
        6.      Input: http://_your-app-id_.appspot.com/get?name=a
        Output: 10
        """
        url = self.build_url('get?name=a')
        res = requests.get(url)
        self.assertEqual(res.content, '10')
        """
        7.      Input: http://_your-app-id_.appspot.com/get?name=b
        Output: None
        """
        url = self.build_url('get?name=b')
        res = requests.get(url)
        self.assertEqual(res.content, 'None')
        """
        8.      Input: http://_your-app-id_.appspot.com/set?name=a&value=40
        Output:
        """
        url = self.build_url('set?name=a&value=40')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)
        """
        9.      Input: http://_your-app-id_.appspot.com/get?name=a
        Output: 40
        """
        url = self.build_url('get?name=a')
        res = requests.get(url)
        self.assertEqual(res.content, '40')
        """
        10.   Input: http://_your-app-id_.appspot.com/undo
        Output:
        """
        url = self.build_url('undo')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)
        """
        11.   Input: http://_your-app-id_.appspot.com/get?name=a
        Output: 10
        """
        url = self.build_url('get?name=a')
        res = requests.get(url)
        self.assertEqual(res.content, '10')
        """
        12.   Input: http://_your-app-id_.appspot.com/undo
        Output:
        """
        url = self.build_url('undo')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)
        """
        13.   Input: http://_your-app-id_.appspot.com/get?name=a
        Output: None
        """
        url = self.build_url('get?name=a')
        res = requests.get(url)
        self.assertEqual(res.content, 'None')
        """
        14.   Input: http://_your-app-id_.appspot.com/undo
        Output: NO COMMANDS
        """
        url = self.build_url('undo')
        res = requests.get(url)
        self.assertEqual(res.content, "NO COMMANDS")
        """
        15.   Input: http://_your-app-id_.appspot.com/end
        Output:
        """
        url = self.build_url('end')
        res = requests.get(url)
        self.assertEqual(len(res.content), 0)

    def tearDown(self):
        self.tb.deactivate()