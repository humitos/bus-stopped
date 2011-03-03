import os
import settings
import datetime

from django.utils import simplejson

from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from models import BusStop, BusTime, News

import sys
sys.path.insert(0,
                os.path.join(os.path.dirname(__file__), 'lib'))
from dateutil.relativedelta import relativedelta

# from google.appengine.dist import use_library
# use_library('django', '1.0')

class MainPage(webapp.RequestHandler):
    def get(self):
        news = News.all()

        template_values = {
          'news': news,
          }

        path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        self.response.out.write(template.render(path, template_values))

class AjaxGetBusStopped(webapp.RequestHandler):
    def get(self):
        bus_stops = BusStop.all()

        points = []
        for bs in bus_stops:
            points.append({
                'title': bs.name,
                'key': str(bs.key()),
                'address': bs.address,
                'icon': '/static/img/gmarkers/red_bus.png',
                'shadow': '/static/img/gmarkers/shadow_bus.png',
                'latitude': bs.point.lat,
                'longitude': bs.point.lon,
                'description': '<b>' + bs.name + '</b>',
                })
        points = simplejson.dumps(points)

        self.response.headers["Content-Type"] = 'application/json'
        self.response.out.write(points)

class AjaxGetBusStopTimes(webapp.RequestHandler):
    def get(self):
        bs = db.get(self.request.get('busstop_key'))
        bus_times = bs.get_next_bus_times(settings.NEXT_BUS_TIME_MINUTES, direction='Vuelta')

        times = []
        for bt in bus_times:
          times.append({
              'bus_stop': str(bt.bus_stop.key()),
              'days': bt.days,
              'time': bt.time.strftime('%H:%M'),
              'direction': bt.direction,
              'time_left': relativedelta(bt.time_1970(), BusStop.now_time()).minutes,
              })
        times = simplejson.dumps(times)

        self.response.headers["Content-Type"] = 'application/json'
        self.response.out.write(times)


class MapPage(webapp.RequestHandler):
    def get(self):
        bus_stops = BusStop.all()

        template_values = {
          'bus_stops': bus_stops,
          }

        path = os.path.join(os.path.dirname(__file__), 'templates', 'map.html')
        self.response.out.write(template.render(path, template_values))

class InsertPointPage(webapp.RequestHandler):
    def get(self):
        template_values = {
            }

        path = os.path.join(os.path.dirname(__file__), 'templates', 'insert_point.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        point = '%s,%s' % (self.request.get('latitude'), self.request.get('longitude'))

        bus_stop = BusStop(point=point,
                           name=self.request.get('name'),
                           address=self.request.get('address'))
        bus_stop.put()

        time = self.request.get('time')
        time = datetime.time(*map(int, time.split(':')))

        bus_time = BusTime(bus_stop=bus_stop.key(),
                           days=self.request.get('days'),
                           time=time)
        bus_time.put()

        self.redirect('/')


class FAQPage(webapp.RequestHandler):
    def get(self):
        template_values = {
            }

        path = os.path.join(os.path.dirname(__file__), 'templates', 'faq.html')
        self.response.out.write(template.render(path, template_values))


class ChangeLogPage(webapp.RequestHandler):
    def get(self):
        template_values = {
            }

        path = os.path.join(os.path.dirname(__file__), 'templates', 'change_log.html')
        self.response.out.write(template.render(path, template_values))


class NewsPage(webapp.RequestHandler):
    def get(self):
        news = News.all()
        template_values = {
            'news': news,
            }

        path = os.path.join(os.path.dirname(__file__), 'templates', 'news.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
    [
        ('/', MainPage),
        ('/faq', FAQPage),
        ('/news', NewsPage),
        ('/changelog', ChangeLogPage),
        ('/point/insert', InsertPointPage),
        ('/ajax/busstopped', AjaxGetBusStopped),
        ('/ajax/point', AjaxGetBusStopTimes),
    ],
     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

