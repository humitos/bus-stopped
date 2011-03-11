import os
import sys

# add Python SDK to the package PATH
DIRNAME = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(DIRNAME, '../../google_appengine'))
sys.path.insert(0, os.path.join(DIRNAME, '../../google_appengine/lib/yaml/lib'))

for p in ['lib', 'distlib', 'distlib.zip']:
    sys.path.insert(0, os.path.join(DIRNAME, '../busstopped-gae/', p))

sys.path.insert(0, os.path.join(DIRNAME, '../busstopped-gae/'))

