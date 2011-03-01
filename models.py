from google.appengine.ext import db

class BusStop(db.Model):
    name = db.StringProperty()
    point = db.GeoPtProperty(required=True)
    address = db.StringProperty()
    bus_line = db.IntegerProperty(int)

    def __repr__(self):
        return '%s' % self.name

    def get_bus_times(self):
        query = BusTime.gql('WHERE bus_stop = :1 ORDER BY time DESC', self.key())
        return query.fetch(query.count())


class BusTime(db.Model):
    bus_stop = db.ReferenceProperty(BusStop)
    days = db.StringProperty(required=True, choices=set(['Habiles', 'Sabados', 'Domingos']))
    time = db.TimeProperty(required=True)


    def __repr__(self):
        return '%s' % self.time
