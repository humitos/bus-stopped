import os
import simplejson

from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from utils import buildmap

# from google.appengine.dist import use_library
# use_library('django', '1.0')

class BusStop(db.Model):
  name = db.StringProperty()
  point = db.GeoPtProperty()
  address = db.StringProperty()


class MainPage(webapp.RequestHandler):
    def get(self):
        bus_stops = BusStop.all()

        points = []
        for bs in bus_stops:
          points.append({
            'title': bs.name,
            'address': bs.address,
            'icon': 'info',
            'latitude': bs.point.lat,
            'longitude': bs.point.lon,
            'description': 'Here are a description example',
            })
        gmap = buildmap(points)

        template_values = {
          'bus_stops': bus_stops,
          'gmap': gmap
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
            'address': bs.address,
            'icon': '/static/img/gmarkers/info.png',
            'shadow': '/static/img/gmarkers/shadow.png',
            'latitude': bs.point.lat,
            'longitude': bs.point.lon,
            'description': '<b>' + bs.name + '</b>',
            })
        points = simplejson.dumps(points)
        self.response.out.write(points)


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
        bus_stop = BusStop()
        bus_stop.point = '%s,%s' % (self.request.get('latitude'), self.request.get('longitude'))
        bus_stop.name = self.request.get('name')
        bus_stop.address = self.request.get('address')

        bus_stop.put()

        self.redirect('/')

application = webapp.WSGIApplication(
    [
        ('/', MainPage),
        ('/map', MapPage),
        ('/point/insert', InsertPointPage),
        ('/ajax/busstopped', AjaxGetBusStopped),
    ],
     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

