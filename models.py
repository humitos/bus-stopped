from google.appengine.ext import db

class BusStop(db.Model):
    name = db.StringProperty()
    point = db.GeoPtProperty(required=True)
    address = db.StringProperty()
    bus_line = db.IntegerProperty(int)


class BusTime(db.Model):
    bus_stop = db.ReferenceProperty(BusStop)
    days = db.StringProperty(required=True, choices=set(['Habiles', 'Sabados', 'Domingos']))
    time = db.TimeProperty(required=True)

