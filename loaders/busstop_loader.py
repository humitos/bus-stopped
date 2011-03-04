# Import the app's data models directly into
# this namespace. We must add the app
# directory to the path explicitly.
import sys
import os.path
dirpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(dirpath))

# We HAVE TO import this model so appcfg.py could recognize it
from apps.busstopped.models import *

from google.appengine.tools import bulkloader


def parse_list(d):
    return d.split(',')

class BusStopLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'BusStop',
                                   [('name', str),
                                    ('point', str),
                                    ('address', str),
                                    ('lines', parse_list),
                                    ('directions', parse_list),
                                    ])

    def generate_key(self, i, values):
        return values[0]

loaders = [BusStopLoader]

# import datetime
# lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date()),
