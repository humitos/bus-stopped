# Import the app's data models directly into
# this namespace. We must add the app
# directory to the path explicitly.
import sys
import os.path
dirpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(os.path.dirname(dirpath)))

# We HAVE TO import this model so appcfg.py could recognize it
from apps.busstopped.models import *

import datetime

from google.appengine.tools import bulkloader

def get_time(d):
    return datetime.datetime.strptime(d, '%H:%M:%S').time()

def bus_stop_key(i):
    bs_key = db.Key.from_path('BusStop', i)
    bus_stop = db.get(bs_key)
    return bus_stop

def get_string(s):
    return s.decode('utf-8')

def get_list(s):
    if s:
        return map(get_string, s.split(','))
    else:
        return []

class BusTimeLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'BusTime',
                                   [
                ('_UNUSED', lambda x: None),
                ('bus_stop', bus_stop_key),
                ('bus_line', get_string),
                ('days', get_string),
                ('time', get_time),
                ('comments', get_list),
                ('direction', get_string),
                ])


loaders = [BusTimeLoader]

# import datetime
# lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date()),
