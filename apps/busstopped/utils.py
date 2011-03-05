import pytz
import datetime

def now_time():
    # This is a horrible hack because GAE saves time object in 01/01/1970
    now_time = datetime.datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
    now_1970 = datetime.datetime(1970, 1, 1, now_time.hour, now_time.minute, 0)
    return now_1970

def get_weekday_display():
    weekday = datetime.date.today().weekday()
    # Testing
    # weekday = 6
    if weekday == 5:
        weekday = 'Sabados'
    elif weekday == 6:
        weekday = 'Domingos'
    else:
        weekday = 'Habiles'
    return weekday


def parse_times(filename, lines, direction, days):
    import csv

    rows = []

    csv_reader = csv.reader(open('fixtures/scriptable/%s' % filename , 'r'))

    first_row = csv_reader.next()
    second_row = csv_reader.next()

    cabeceras = [
        'BusStop Name (ignored)',
        'BusStop ID',
        'Line',
        'Days',
        'Time',
        'Comment',
        'Direction',
        ]

    references = {
        '5': {'Ida': [(' (1)', 'Sale de Barrio 41 Viviendas'),
                      (' (2)', 'Sale de Seminario Parana')],
              }
        }


    for row in csv_reader:
        for i, column in enumerate(row[:-1]):
            comments = row[-1].strip()
            for n, message in references[lines][direction]:
                if len(comments) < 5:
                    comments = ''

                if n in column: # Lleva un comentario
                    column = column.replace(n, '')
                    if len(comments) < 5:
                        comments = ''
                    else:
                        comments += ','
                        comments += message
                    column += ':00'
                column = column.strip()

            r = [first_row[i], second_row[i], lines, days, column, comments, direction]
            if column not in ('-', '\xc2\xa0', '', ' '):
                rows.append(r)

    rows = sorted(rows, key=lambda r: r.__getitem__(1))
    rows.insert(0, cabeceras)
    return rows
