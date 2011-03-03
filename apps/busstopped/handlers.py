# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Hello, World!: the simplest tipfy app.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE for more details.
"""

import os
import settings
import datetime

from models import BusStop, BusTime, News

from dateutil.relativedelta import relativedelta

# App Engine Imports
from google.appengine.ext import db

# TypFy imports
from tipfy import RequestHandler, render_json_response
from tipfy.ext.jinja2 import render_response

def request_context(context):
    context.update({
            'news': News.all(),
            })
    return context


class MainPage(RequestHandler):
    def get(self, **kwargs):
        news = News.all()

        context = {
          'news': news,
          }

        return render_response('index.html', **context)

class AjaxGetBusStopped(RequestHandler):
    def get(self, **kwargs):
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
        return render_json_response(points)

class AjaxGetBusStopTimes(RequestHandler):
    def get(self, **kwargs):
        bs = db.get(self.request.values.get('busstop_key'))
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
        return render_json_response(times)


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
        news = News.all()
        context = {
            'news': news,
            }

        return render_response('news.html', **context)

