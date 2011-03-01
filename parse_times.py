import urllib2

from BeautifulSoup import BeautifulSoup

class LaVictorialSRL(object):

    URL = 'http://usuarios.advance.com.ar/isti98/hor_linea_%(linea)s%(dia)s.htm'
    LINEA = {
        1: '01',
        6: '06',
        5: '05',
        22: '22',
        1121: '11',
        2222: '22bis'
        }
    DIA = {
        'habiles': 'h',
        'sabado': 's',
        'domingos': 'd',
        }


    def download_html(self, url):
        return urllib2.urlopen(url).read()

    def parse(self, dia, linea):
        url = self.URL % {'dia': self.DIA[dia],
                          'linea': self.LINEA[linea],
                          }
        rows = []

        soup = BeautifulSoup(self.download_html(url))

        for tr in soup.findAll('tr', attrs={'height': '26'}):
            row = []
            for td in tr.findAll('td'):
                row.append(td.text.replace('&nbsp;', '').strip())
            rows.append(row)

        return rows

if __name__ == '__main__':
    lvs = LaVictorialSRL()
    print lvs.parse('habiles', 6)
