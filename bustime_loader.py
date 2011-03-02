# Import the app's data models directly into
# this namespace. We must add the app
# directory to the path explicitly.
import sys
import os.path
sys.path.append(
os.path.abspath(
os.path.dirname(
os.path.realpath(__file__))))
# We HAVE TO import this model so appcfg.py could recognize it
from models import *

import datetime

from google.appengine.tools import bulkloader

def get_time(d):
    return datetime.datetime.strptime(d, '%H:%M:%S').time()

def handle_entity(i):
    bs_key = db.Key.from_path('BusStop', i)
    bus_stop = db.get(bs_key)
    return bus_stop


class BusTimeLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'BusTime',
                                   [('bus_stop', handle_entity),
                                    ('days', str),
                                    ('time', get_time),
                                    ])


loaders = [BusTimeLoader]

# import datetime
# lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date()),
