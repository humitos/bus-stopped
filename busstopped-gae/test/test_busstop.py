import unittest
from fixture import GoogleDatastoreFixture, DataSet
from fixture.style import NamedDataStyle
from apps.busstopped import models
from webtest import TestApp
from datasets import BusStopData, BusTimeData, BusDirectionData

from main import app

# from google.appengine.ext import db

from apps.busstopped.models import BusStop

datafixture = GoogleDatastoreFixture(env=models, style=NamedDataStyle())

class TestBusStop(unittest.TestCase):

    def setUp(self):
        # NOTE: we have to fill the database
        # Line #283 gaeunit.py

        # TODO: how do we do to load a fixture here?
        # bs = BusStop(name='test', address='test',
        #              point='31,32', lines=['1'],
        #              directions=['Ida', 'Vuelta'])
        # bs.put()
        self.app = TestApp(app)
        self.data = datafixture.data(BusStopData, BusTimeData, BusDirectionData)
        self.data.setup()


    def test_line_1(self):
        # make sure that all BusStop exists into the database
        bs = BusStop.all()
        self.assertEqual(bs.count(), 1)


if __name__ == '__main__':
    unittest.main()
