import os
import csv
import glob

def parse_times(filename, line, direction, days):
    rows = []

    csv_reader = csv.reader(open(filename , 'r'))

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

    # References to Replace
    references = {
        '5': {'Ida':    [(' (1)', 'Sale de Barrio 41 Viviendas'),
                         (' (3)', 'Sale de Seminario Parana')],
              'Vuelta': [(' (2)', 'Llega hasta Barrio 41 Viviendas'),
                         (' (4)', 'Llega hasta Seminario Parana')],},
        '1': {'Ida':    [],
              'Vuelta': [],
              },
        '6': {'Ida':    [],
              'Vuelta': [],
              },
        }


    for row in csv_reader:
        for i, column in enumerate(row[:-1]):
            comments = row[-1].strip()
            for n, message in references[line][direction]:
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

            r = [first_row[i], second_row[i], line, days, column, comments, direction]
            if column not in ('-', '\xc2\xa0', '', ' '):
                rows.append(r)

    rows = sorted(rows, key=lambda r: r.__getitem__(1))
    rows.insert(0, cabeceras)


    output_name = 'bustime_linea_%s_%s_%s.csv' % (line, days.lower(), direction.lower())
    print '"%s" -> CREATED' % output_name
    f = open(os.path.join('../fixtures/', output_name), 'w')
    csv_writer = csv.writer(f)
    csv_writer.writerows(rows)
    f.close()

    return rows

if __name__ == '__main__':
    for filename in glob.glob('../fixtures/scriptable/*.csv'):
        basename = os.path.basename(filename)
        line = basename.split('_')[0]
        direction = basename.split('_')[-1].split('.')[0].title()
        days = basename.split('_')[1].title()
        parse_times(filename, line, direction, days)