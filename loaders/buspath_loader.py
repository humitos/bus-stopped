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

def get_string(s):
    return s.decode('utf-8')

class BusPathLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'BusPath',
                                   [
                ('bus_line', get_string),
                ('direction', get_string),
                ('filename', get_string),
                ])

    def generate_key(self, i, values):
        return values[0]

loaders = [BusPathLoader]
