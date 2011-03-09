import sys

if 'lib' not in sys.path:
    # Add /lib as primary libraries directory, with fallback to /distlib
    # and optionally to distlib loaded using zipimport.
    sys.path[0:0] = ['../lib', '../distlib', '../distlib.zip']


import re
import urllib2
import datetime

from apps.busstopped.models import ExternalNews

from BeautifulSoup import BeautifulSoup

from google.appengine.api import mail



def send_mail(site=None, url=None):
    sender_address = user_address = 'humitos@gmail.com'
    subject = 'Nueva noticia en: %s' % site
    body = 'Se encontro un texto referido a "colectivos" en %s:\n  * %s' % (site, url)
    mail.send_mail(sender_address, user_address, subject, body)

def get_db_last_date(site=None):
    query = ExternalNews.all()
    query.filter('site =', site)
    query.order('date')
    last_news = query.fetch(1)
    if query.count():
        return last_news[0].date
    else:
        return None

def la_victoria_news():
    URL = 'http://usuarios.advance.com.ar/isti98/Novedades.htm'

    data = urllib2.urlopen(URL).read()
    soup = BeautifulSoup(data)

    last_new = soup.find('div', attrs={'id': 'container'}).find('td')
    text = last_new.text
    last_date = datetime.datetime.strptime(text.split(':')[0], '%d/%m/%Y').date()

    db_last_date = get_db_last_date(site='La Victoria')

    if (db_last_date == None) or (last_date > db_last_date):
        site = 'La Victoria'
        send_mail(site=site, url=URL)
        en = ExternalNews(site=site, date=last_date.date())
        en.put()

def diario_uno_parana_news():
    URL = 'http://edimpresa.unoentrerios.com.ar/v2/municipios/?municipio=1'

    data = urllib2.urlopen(URL).read()

    regex = re.compile('colectivo')
    if regex.match(data):
        send_mail(site='Diario Uno Parana', url=URL)

def diario_uno_entrerios_news():
    URL = 'http://www.unoentrerios.com.ar/'

    data = urllib2.urlopen(URL).read()

    regex = re.compile('colectivo')
    if regex.match(data):
        send_mail(site='Diario Uno Entre Rios', url=URL)

def el_diario_news():
    URL = 'http://www.eldiario.com.ar/'

    data = urllib2.urlopen(URL).read()

    regex = re.compile('colectivo')
    if regex.match(data):
        send_mail(site='El Diario', url=URL)


if __name__ == '__main__':
    la_victoria_news()
    diario_uno_parana_news()
    diario_uno_entrerios_news()
    el_diario_news()
