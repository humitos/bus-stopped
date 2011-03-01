import sys
sys.path.insert(0, './busstopped')

# We HAVE TO import this model so appcfg.py could recognize it
from models import BusStop

from google.appengine.tools import bulkloader


class BusStopLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'BusStop',
                                   [('name', str),
                                    ('point', str),
                                    ('address', str),
                                    ('bus_line', int)
                                    ])

loaders = [BusStopLoader]

# import datetime
# lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date()),
