import sys
import os
sys.path.insert(1, '/usr/lib/google-cloud-sdk/platform/google_appengine')
sys.path.insert(1, '/usr/lib/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
if 'google' in sys.modules:
    del sys.modules['google']

os.environ['APPLICATION_ID'] = 'sillywalkplus'
from google.appengine.ext import testbed

def before_all(context):
    context.tb = testbed.Testbed()
    context.tb.activate()
    context.tb.init_datastore_v3_stub()
    context.tb.init_memcache_stub()

def after_all(context):
    context.tb.deactivate()
