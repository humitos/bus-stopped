from google.appengine.ext import db
from apps.busstopped.models import *

bt = BusTime.all()
db.delete(bt)


bs = BusStop.all()
db.delete(bs)

nw = News.all()
db.delete(nw)
