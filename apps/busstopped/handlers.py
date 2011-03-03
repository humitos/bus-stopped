# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Hello, World!: the simplest tipfy app.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE for more details.
"""

import re
import settings

from models import BusStop, News

from dateutil.relativedelta import relativedelta

# App Engine Imports
from google.appengine.ext import db

# TypFy imports
from tipfy import RequestHandler, render_json_response
from tipfy.ext.jinja2 import get_jinja2_instance, Jinja2Mixin, render_response

from django.utils.text import truncate_html_words

def filter_date(value, format):
    return value.strftime(format)

def filter_truncate_html_words(value, length):
    return truncate_html_words(value, length)

def filter_slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

# Templating functions
env = get_jinja2_instance()
env.filters['date'] = filter_date
env.filters['truncatewords_html'] = filter_truncate_html_words
env.filters['slugify'] = filter_slugify


def request_context(context):
    context.update({
            'news': News.all(),
            })
    return context


class MainPage(RequestHandler, Jinja2Mixin):
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

