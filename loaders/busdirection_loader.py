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


def get_string(s):
    return s.decode('utf-8')

class BusDirectionLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'BusDirection',
                                   [
                ('bus_line', get_string),
                ('from_direction', get_string),
                ('to_direction', get_string),
                ('direction', get_string),
                ])

loaders = [BusDirectionLoader]

# import datetime
# lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date()),
