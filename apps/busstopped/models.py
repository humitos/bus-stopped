import sys
import logging
import datetime

import utils
from google.appengine.ext import db

# To make sure you're seeing all debug output:
logger = logging.getLogger('busstopped')
STDOUT = logging.StreamHandler(sys.stdout)
logger.addHandler(STDOUT)
logger.setLevel(logging.DEBUG)

class BusStop(db.Model):
    name = db.StringProperty(required=True)
    point = db.GeoPtProperty(required=True)
    address = db.StringProperty(required=True)
    lines = db.StringListProperty(required=True)
    directions = db.StringListProperty(required=True)

    def __repr__(self):
        return '%s' % self.name

    def get_bus_times(self):
        query = BusTime.gql('WHERE bus_stop = :1 ORDER BY time ASC', self.key())
        return query.fetch(query.count())

    def get_next_bus_times(self, next_minutes, direction=None):
        weekday = utils.get_weekday_display()

        now = utils.now_time()
        next_minutes = now + datetime.timedelta(minutes=next_minutes)

        query = db.Query(BusTime)
        query.filter('bus_stop =', self.key())
        query.filter('time <=', next_minutes)
        query.filter('time >=', now)
        query.filter('days =', weekday)
        if direction:
            query.filter('direction =', direction)
        query.order('time')
        results = query.fetch(query.count())
        return results


class BusTime(db.Model):
    bus_stop = db.ReferenceProperty(BusStop)
    bus_line = db.StringProperty(required=True)
    days = db.StringProperty(required=True, choices=set(['Habiles', 'Sabados', 'Domingos']))
    time = db.TimeProperty(required=True)
    direction = db.StringProperty(choices=set(['Ida', 'Vuelta']))
    comment = db.StringProperty()

    def time_1970(self):
        return datetime.datetime(1970, 1, 1, self.time.hour,
                                 self.time.minute, self.time.second)

    def __repr__(self):
        return '%s' % self.time


class News(db.Model):
    date = db.DateProperty(required=True)
    text = db.TextProperty(required=True)
    title = db.StringProperty(required=True)


    def __repr__(self):
        return '(%s) %s' % (self.date, self.title)
