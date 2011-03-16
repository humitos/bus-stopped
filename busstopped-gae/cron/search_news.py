# -*- coding: utf-8 -*-

import os
import sys

if 'lib' not in sys.path:
    # Add /lib as primary libraries directory, with fallback to /distlib
    # and optionally to distlib loaded using zipimport.
    for p in ['lib', 'distlib', 'distlib.zip']:
        basedir = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(basedir, p)
        if path not in sys.path:
            sys.path.insert(0, path)

import re
import urllib2
import datetime

from apps.busstopped.models import ExternalNews

from BeautifulSoup import BeautifulSoup

from google.appengine.api import mail

WORDS = [
    u'colectivo',
    u'tránsito', u'transito',
    u'línea', u'linea',
    u'ersa',
    u'mariano moreno',
    u'transporte',
    u'recorrido',
]
regex_str = u'.*(%s).*' % '|'.join(WORDS)
regex = re.compile(regex_str, flags=re.IGNORECASE | re.UNICODE | re.DOTALL)
# http://docs.python.org/library/re.html#re.DOTALL
# http://docs.python.org/library/re.html#re.UNICODE
# http://docs.python.org/library/re.html#re.IGNORECASE

def send_mail(title, content, link, site=None, url=None):
    sender_address = user_address = 'humitos@gmail.com'
    subject = 'Nueva noticia en: %s' % site
    body = 'Se encontro un texto referido a "colectivos" en %s:\n  * %s\n\n**%s**\n * %s\n%s' % (site, url, title, link, content)
    en = ExternalNews(site=site,
                      date=datetime.date.today(),
                      title=title,
                      content=content,
                      link=link)
    en.put()
    mail.send_mail(sender_address, user_address, subject, body)

def get_db_last_date(site=None):
    query = ExternalNews.all()
    query.filter('site =', site)
    query.order('-date')
    last_news = query.fetch(1)
    if query.count():
        return last_news[0].date
    else:
        return None

def la_victoria_news():
    URL = 'http://usuarios.advance.com.ar/isti98/Novedades.htm'
    site = 'La Victoria'

    # <meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
    soup = BeautifulSoup(urllib2.urlopen(URL).read())

    last_new = soup.find('div', attrs={'id': 'container'}).find('td')
    text = last_new.text
    last_date = datetime.datetime.strptime(text.split(':')[0], '%d/%m/%Y').date()

    db_last_date = get_db_last_date(site=site)

    if (db_last_date == None) or (last_date > db_last_date):
        send_mail('Novedad La Victoria SRL', text, link=URL, site=site, url=URL)

def diario_uno_parana_news():
    URL = 'http://edimpresa.unoentrerios.com.ar/v2/municipios/?municipio=1'

    # THIS <meta> ISN'T VALID!!
    # <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    soup = BeautifulSoup(urllib2.urlopen(URL).read())
    all_content = soup.find('div', attrs={'class': 'content'})
    news = all_content.findAll('div', attrs={'class': None, 'style': None})

    for n in news:
        title = n.find('div', attrs={'class': 'h2'}).text
        content = n.find('div', attrs={'class': 'bajada'}).text
        link = URL.split('?')[0] + n.find('a', attrs={'class': 'h2'}).get('href')
        match = regex.match(content) or regex.match(title)
        if match:
            send_mail(title, content, link, site='Diario Uno Parana', url=URL)

def diario_uno_entrerios_news():
    URL = 'http://www.unoentrerios.com.ar/'

    # <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    soup = BeautifulSoup(urllib2.urlopen(URL).read())
    news = soup.findAll('div', attrs={'class': 'nota-portada'})

    for n in news:
        title = n.find('h2').text
        content = n.findAll('p')[1].text
        link = URL[:-1] + n.a.get('href')
        match = regex.match(content) or regex.match(title)
        if match:
            send_mail(title, content, link, site='Diario Uno Entre Rios', url=URL)

def el_diario_news():
    URL = 'http://www.eldiario.com.ar/'

    # <meta> is missing
    soup = BeautifulSoup(urllib2.urlopen(URL).read())
    content = soup.find('table', attrs={'bgcolor': '#FF0000'})
    all_news = content.findAll('table')[1]
    news = all_news.findAll('table')
    for n in news:
        try:
            title = n.findAll('font')[2].text
            content = n.findAll('font')[4].text
            link = n.findAll('a')[0].get('href')
            match = regex.match(content) or regex.match(title)
            if match:
                send_mail(title, content, link, site='El Diario', url=URL)
        except IndexError:
            pass


def el_once_news():
    URL = 'http://www.elonce.com/'

    # <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
    soup = BeautifulSoup(urllib2.urlopen(URL).read())
    news = soup.findAll('div', attrs={'class': 'noticia emptyall'})


    for n in news:
        title = n.h2.text
        content = n.div.text
        link = URL[:-1] + n.a.get('href')
        match = regex.match(content) or regex.match(title)
        if match:
            send_mail(title, content, link, site='El Once.com', url=URL)


if __name__ == '__main__':
    la_victoria_news()
    diario_uno_parana_news()
    diario_uno_entrerios_news()
    el_diario_news()
    el_once_news()
