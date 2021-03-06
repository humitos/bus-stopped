# Import the app's data models directly into
# this namespace. We must add the app
# directory to the path explicitly.
import sys
import os.path
dirpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(os.path.dirname(dirpath), 'busstopped-gae'))

# We HAVE TO import this model so appcfg.py could recognize it
from apps.busstopped.models import *
from google.appengine.tools import bulkloader

def get_date(d):
    return datetime.datetime.strptime(d, '%d/%m/%Y').date()

def get_string(s):
    return s.decode('utf-8')

class NewsLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'News',
                                   [('date', get_date),
                                    ('title', get_string),
                                    ('text', get_string),
                                    ])

loaders = [NewsLoader]
