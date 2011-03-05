# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Hello, World!: the simplest tipfy app.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE for more details.
"""

# We MUST import this file (filters.py) because it's required by LOADERS
import filters
import settings
import utils

from models import BusStop, News, BusTime
from forms import ViewBusStopLinesForm
from dateutil.relativedelta import relativedelta

# App Engine Imports
from google.appengine.ext import db

# TypFy imports
from tipfy import RequestHandler, render_json_response, cached_property
from tipfy.ext.jinja2 import render_response


def request_context(context):
    def js_string(value):
        return '\'' + value + '\''

    js_settings = {
        'MEDIA_URL': js_string(settings.MEDIA_URL),
        'INITIAL_LOCATION': settings.INITIAL_LOCATION,
        'WEEKDAY': js_string(utils.get_weekday_display()),
        }

    context.update({
            'MEDIA_URL': settings.MEDIA_URL,
            'JS_SETTINGS': js_settings,
            'news': News.all().order('-date'),
            })
    return context


class MainPage(RequestHandler):
    def get(self, **kwargs):
        context = {
            'form': self.form,
          }

        context = request_context(context)

        return render_response('index.html', **context)

    @cached_property
    def form(self):
        return ViewBusStopLinesForm(self.request.values)


class AjaxGetBusStopped(RequestHandler):
    def get(self, line=None, direction=None, **kwargs):
        bus_stops = BusStop.all()
        bus_stops.filter('lines =', line)
        bus_stops.filter('directions =', direction)

        points = []
        for bs in bus_stops:
            points.append({
                'name': bs.name,
                'key': str(bs.key()),
                'address': bs.address,
                'icon': '/static/img/gmarkers/red_bus.png',
                'shadow': '/static/img/gmarkers/shadow_bus.png',
                'latitude': bs.point.lat,
                'longitude': bs.point.lon,
                'directions': bs.directions,
                })
        return render_json_response(points)

class AjaxGetBusStopTimes(RequestHandler):
    def get(self, **kwargs):
        bus_stop = db.get(self.request.values.get('busstop_key'))
        directions = self.request.values.get('directions', '')

        if len(directions.split(',')) == 2:
            directions = None
        else:
            directions = directions
        bus_times = bus_stop.get_next_bus_times(settings.NEXT_BUS_TIME_MINUTES,
                                                direction=directions)

        info_content = '<b>%s</b><br /> %s<br /><em style="font-size: 10px">%s</em>' % \
            (bus_stop.name, bus_stop.address, utils.get_weekday_display())
        for bus_time in bus_times:
            info_content += '<br /><b>%s min:</b> %s <span>%s</span>' % \
                (relativedelta(bus_time.time_1970(), utils.now_time()).minutes,
                 bus_time.direction, bus_time.time.strftime('%H:%M'))

            if bus_time.comments:
                info_content += '<em> ('
                for comment in bus_time.comments:
                    info_content += '%s, ' % comment
                info_content = info_content[:-2]
                info_content += ')</em>'

        return render_json_response({
                'info_content': info_content
                })


class FAQPage(RequestHandler):
    def get(self, **kwargs):
        context = {
            }

        context = request_context(context)
        return render_response('faq.html', **context)


class ChangeLogPage(RequestHandler):
    def get(self, **kwargs):
        context = {
            }

        context = request_context(context)
        return render_response('change_log.html', **context)


class NewsPage(RequestHandler):
    def get(self, **kwargs):
        context = {
            }

        context = request_context(context)

        return render_response('news.html', **context)


# URL to generate the .csv data
# http://localhost:8007/parse?direction=Vuelta&days=Habiles&filename=1_habiles_vuelta.csv&lines=1
class ParseTimesPage(RequestHandler):
    def get(self, **kwargs):
        import cStringIO
        import csv
        from tipfy import Response
        from utils import parse_times

        direction = self.request.values.get('direction')
        days = self.request.values.get('days')
        filename = self.request.values.get('filename')
        lines = self.request.values.get('lines')

        bus_times = parse_times(filename, lines, direction, days)

        f = cStringIO.StringIO()
        csv_writer = csv.writer(f)
        csv_writer.writerows(bus_times)
        csv_file = f.getvalue()
        f.close()

        context = {
            'bus_times': bus_times,
            }

        context = request_context(context)
        response = Response()
        response.data = csv_file
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename="%s"' % ('parsed__' + filename)
        return response
