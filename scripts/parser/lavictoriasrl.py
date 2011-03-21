# Parse Times from "lavictoriasrl.com.ar"

import csv
import urllib2
import cStringIO
import codecs

from BeautifulSoup import BeautifulSoup

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        if isinstance(f, str):
            self.file_name = f
            self.file = open(f, 'w')
        else:
            self.file = f

        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, delimiter=',',**kwds)
        self.stream = self.file
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

    def close(self):
        self.file.close()

URL = {
    '1': {
        'Habiles': 'http://usuarios.advance.com.ar/isti98/hor_linea_01h.htm',
        'Sabados': 'http://usuarios.advance.com.ar/isti98/hor_linea_01s.htm',
        'Domingos': 'http://usuarios.advance.com.ar/isti98/hor_linea_01d.htm',
        },
    '5': {
        'Habiles': 'http://usuarios.advance.com.ar/isti98/hor_linea_05h.htm',
        'Sabados': 'http://usuarios.advance.com.ar/isti98/hor_linea_05s.htm',
        'Domingos': 'http://usuarios.advance.com.ar/isti98/hor_linea_05d.htm',
        },
    '6': {
        'Habiles': 'http://usuarios.advance.com.ar/isti98/hor_linea_06h.htm',
        'Sabados': 'http://usuarios.advance.com.ar/isti98/hor_linea_06s.htm',
        'Domingos': 'http://usuarios.advance.com.ar/isti98/hor_linea_06d.htm',
        },
    '10': {
        'Habiles': 'http://usuarios.advance.com.ar/isti98/hor_linea_10h.htm',
        'Sabados': 'http://usuarios.advance.com.ar/isti98/hor_linea_10s.htm',
        'Domingos': 'http://usuarios.advance.com.ar/isti98/hor_linea_10d.htm',
        },
    '11-21': {
        'Habiles': 'http://usuarios.advance.com.ar/isti98/hor_linea_11h.htm',
        'Sabados': 'http://usuarios.advance.com.ar/isti98/hor_linea_11s.htm',
        'Domingos': 'http://usuarios.advance.com.ar/isti98/hor_linea_11d.htm',
        },
    '15': {
        'Habiles': 'http://usuarios.advance.com.ar/isti98/hor_linea_15h.htm',
        'Sabados': 'http://usuarios.advance.com.ar/isti98/hor_linea_15s.htm',
        'Domingos': 'http://usuarios.advance.com.ar/isti98/hor_linea_15d.htm',
        },
    '22': {
        'Habiles': 'http://usuarios.advance.com.ar/isti98/hor_linea_22h.htm',
        'Sabados': 'http://usuarios.advance.com.ar/isti98/hor_linea_22s.htm',
        'Domingos': 'http://usuarios.advance.com.ar/isti98/hor_linea_22d.htm',
        },
    '22 Bis': {
        'Habiles': 'http://usuarios.advance.com.ar/isti98/hor_linea_22bish.htm',
        }
    }

def download_times(line, day, url):
    r = urllib2.urlopen(url).read()
    soup = BeautifulSoup(r)
    table = soup.find('table')

    filename = 'lavictoriasrl/line_%s_%s.csv' % (line.lower(), day.lower())

    csv_writer = UnicodeWriter(open(filename, 'w'))
    for tr in table.findAll('tr')[5:-2]:
        row = []
        for td in tr.findAll('td')[:-1]:
            text = td.text
            for r in ('&nbsp;', ):
                text = text.replace(r, '')
            row.append(text)
        csv_writer.writerow(row)
    csv_writer.close()

for line, days in URL.iteritems():
    for day, url in days.iteritems():
        print line, day, url
        download_times(line, day, url)
