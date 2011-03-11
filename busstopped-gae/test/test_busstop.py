import unittest


from google.appengine.ext import db

from apps.busstopped.models import BusStop

class TestBusStop(unittest.TestCase):

    def setUp(self):
        # NOTE: we have to fill the database
        # Line #283 gaeunit.py

        # TODO: how do we do to load a fixture here?
        bs = BusStop(name='test', address='test',
                     point='31,32', lines=['1'],
                     directions=['Ida', 'Vuelta'])
        bs.put()

    def test_line_1(self):
        # make sure that all BusStop exists into the database
        bs = BusStop.all()
        self.assertEqual(bs.count(), 1)

if __name__ == '__main__':
    unittest.main()
