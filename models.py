import datetime

from google.appengine.ext import db

class BusStop(db.Model):
    name = db.StringProperty()
    point = db.GeoPtProperty(required=True)
    address = db.StringProperty()
    bus_line = db.IntegerProperty(int)

    def __repr__(self):
        return '%s' % self.name

    def get_bus_times(self):
        query = BusTime.gql('WHERE bus_stop = :1 ORDER BY time ASC', self.key())
        return query.fetch(query.count())

    @classmethod
    def now_time(self):
        now_time = datetime.datetime.now()
        now_1970 = datetime.datetime(1970, 1, 1, now_time.hour, now_time.minute, 0)
        return now_1970

    def get_next_bus_times(self, next_minutes):
        now = self.now_time()
        next_minutes = now + datetime.timedelta(minutes=next_minutes)
        query = db.Query(BusTime)
        query.filter('bus_stop =', self.key())
        query.filter('time <=', next_minutes)
        query.filter('time >=', now)
        return query.fetch(query.count())


class BusTime(db.Model):
    bus_stop = db.ReferenceProperty(BusStop)
    days = db.StringProperty(required=True, choices=set(['Habiles', 'Sabados', 'Domingos']))
    time = db.TimeProperty(required=True)


    def __repr__(self):
        return '%s' % self.time
