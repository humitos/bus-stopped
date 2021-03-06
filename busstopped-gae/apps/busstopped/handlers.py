# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Hello, World!: the simplest tipfy app.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE for more details.
"""

import pytz
import datetime

# We MUST import this file (filters.py) because it's required by LOADERS
import filters
import settings
import utils

from models import BusStop, News, BusDirection, BusPath
from forms import ViewBusStopLinesForm
from dateutil.relativedelta import relativedelta

# App Engine Imports
from google.appengine.ext import db

# TypFy imports
from tipfy import RequestHandler, render_json_response, cached_property
from tipfy.ext.jinja2 import render_response

from django.utils import simplejson

def request_context(context):
    def js_string(value):
        return '\'' + value + '\''

    now = datetime.datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
    # TODO: convert this to a JSON file
    js_settings = {
        'MEDIA_URL': js_string(settings.MEDIA_URL),
        'INITIAL_LOCATION': settings.INITIAL_LOCATION,
        'WEEKDAY': js_string(utils.get_weekday_display()),
        'CLOCK': simplejson.dumps({
                'year': now.year, 'month': now.month, 'day': now.day,
                'hour': now.hour, 'minute': now.minute, 'second': now.second
                })
        }

    context.update({
            'MEDIA_URL': settings.MEDIA_URL,
            'JS_SETTINGS': js_settings,
            'news': News.all().order('-date')[:5],
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

        ds = BusDirection.all()
        ds.filter('bus_line =', line)
        ds.filter('direction =', direction)

        # TODO: improve this feature
        directions_html = ''
        for d in ds:
            directions_html += '<strong>%s:</strong><ul><li>Desde: <em>%s</em></li><li>Hasta: <em>%s</em></li></ul>' % (d.direction,
                                                                                                  d.from_direction,
                                                                                                  d.to_direction)
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
        data = {'points': points,
                'directions_html': directions_html}
        return render_json_response(data)

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

        bus_direction = BusDirection.all()
        bus_direction.filter('direction =', directions)
        # README
        # BadValueError: Filtering on lists is not supported
        # We can't use "bus_direction.filter('bus_line =', bus_stop.lines)"
        # So, in the while we will use "bus_stop.lines[0]" because a BusStop only
        # has one line for the moment
        bus_direction.filter('bus_line =', bus_stop.lines[0])
        bus_direction = bus_direction.fetch(1)
        bus_direction = bus_direction[0]


        info_content = '<b>%s</b><br /> %s<br /><em style="font-size: 10px">%s / Hacia: %s (%s)</em>' % \
            (bus_stop.name, bus_stop.address, utils.get_weekday_display(), bus_direction.to_direction, bus_direction.direction)
        for bus_time in bus_times:
            left_time = relativedelta(bus_time.time_1970(), utils.now_time()).minutes
            bus_already_gone = False
            if left_time < 0:
                if bus_time.time_1970().hour == 0:
                    # Time over 00hs
                    next_day = bus_time.time_1970() + datetime.timedelta(days=1)
                    left_time = relativedelta(next_day, utils.now_time()).minutes
                else:
                    # This bus has already gone by
                    bus_already_gone = True
            time = bus_time.time.strftime('%H:%M')

            time_content = '<br /><b>%s min:</b><span> %s hs</span>' % (left_time, time)

            if bus_already_gone:
                info_content += '<span style="color: red">' + time_content + '</span>'
            else:
                info_content += time_content

            if bus_time.comments:
                info_content += '<em> ('
                for comment in bus_time.comments:
                    info_content += '%s, ' % comment
                info_content = info_content[:-2]
                info_content += ')</em>'

        return render_json_response({
                'info_content': info_content
                })


class AjaxGetBusPath(RequestHandler):
    def get(self, line=None, direction=None, **kwargs):

        form = ViewBusStopLinesForm()
        lines = form.lines.choices
        response = {}
        for l in lines:
            response[l[0]] = {}

        print response
        bus_paths = BusPath.all()
        for bp in bus_paths:
            response[bp.bus_line][bp.direction] = {
                'bus_line': bp.bus_line,
                'filename': bp.filename,
                'url': settings.MEDIA_URL + 'kml/' + bp.filename,
                'direction': bp.direction,
                }
        return render_json_response(response)


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
            'all_news': News.all().order('-date'),
            }

        context = request_context(context)

        return render_response('news.html', **context)


class InfoPage(RequestHandler):
    def get(self, **kwargs):
        context = {
            }

        context = request_context(context)

        return render_response('info.html', **context)

class AddPointDocPage(RequestHandler):
    def get(self, **kwargs):
        context = {
            }

        context = request_context(context)

        return render_response('add_point_doc.html', **context)

