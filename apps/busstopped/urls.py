# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE.txt for more details.
"""
from tipfy import Rule


def get_rules(app):
    """Returns a list of URL rules for the Hello, World! application.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        Rule('/', endpoint='home', handler='apps.busstopped.handlers.MainPage'),
        Rule('/ajax/busstopped', endpoint='ajax-busstopped', handler='apps.busstopped.handlers.AjaxGetBusStopped'),
        Rule('/ajax/point', endpoint='ajax-point', handler='apps.busstopped.handlers.AjaxGetBusStopTimes'),
        Rule('/faq', endpoint='faq', handler='apps.busstopped.handlers.FAQPage'),
        Rule('/changelog', endpoint='change-log', handler='apps.busstopped.handlers.ChangeLogPage'),
        Rule('/news', endpoint='news', handler='apps.busstopped.handlers.NewsPage'),
    ]

    return rules