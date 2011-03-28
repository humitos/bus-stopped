# Parse Times from "lavictoriasrl.com.ar"

import urllib2

from utils import UnicodeWriter
from BeautifulSoup import BeautifulSoup

from config import LA_VICTORIA

def download_times(line, day, url, config):
    r = urllib2.urlopen(url).read()
    soup = BeautifulSoup(r)
    table = soup.find('table')

    filename_ida = 'lavictoriasrl/line_%s_%s_ida.csv' % (line.lower(), day.lower())
    filename_vuelta = 'lavictoriasrl/line_%s_%s_vuelta.csv' % (line.lower(), day.lower())

    csv_writer_ida = UnicodeWriter(open(filename_ida, 'w'))
    csv_writer_vuelta = UnicodeWriter(open(filename_vuelta, 'w'))

    csv_writer_ida.writerow([n for n, i in config['row_titles']['ida']])
    csv_writer_ida.writerow([i for n, i in config['row_titles']['ida']])
    csv_writer_vuelta.writerow([n for n, i in config['row_titles']['vuelta']])
    csv_writer_vuelta.writerow([i for n, i in config['row_titles']['vuelta']])

    for tr in table.findAll('tr')[config['exclude_start_rows']:-config['exclude_end_rows']]:
        row_ida = []
        row_vuelta = []
        all_times = tr.findAll('td')[:-1]
        for ida, vuelta in zip(all_times[:config['nro_cols_ida']],
                               all_times[config['nro_cols_ida']:]):
            text_ida = ida.text
            text_vuelta = vuelta.text
            for r in ('&nbsp;', ):
                text_ida = text_ida.replace(r, '')
                text_vuelta = text_vuelta.replace(r, '')
            row_ida.append(text_ida)
            row_vuelta.append(text_vuelta)
        if not config['has_comments']:
            row_ida.append('')
            row_vuelta.append('')
        csv_writer_ida.writerow(row_ida)
        csv_writer_vuelta.writerow(row_vuelta)
    csv_writer_ida.close()
    csv_writer_vuelta.close()

for line, days in LA_VICTORIA.iteritems():
    for key, value in days.iteritems():
        if line != '1':
            continue
        if key == 'config':
            continue
        print line, key, value
        download_times(line, key, value, days['config'])
