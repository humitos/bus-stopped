import os
import csv
import glob
import datetime

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
        '1': {'Ida':    [],
              'Vuelta': [],
              },
        '5': {'Ida':    [(' (1)', 'Sale de Barrio 41 Viviendas'),
                         (' (3)', 'Sale de Seminario Parana')],
              'Vuelta': [(' (2)', 'Llega hasta Barrio 41 Viviendas'),
                         (' (4)', 'Llega hasta Seminario Parana')],},
        '6': {'Ida':    [],
              'Vuelta': [],
              },
        '10': {'Ida':    [(' (1)', 'Sale desde Barrio A.S.S.V.E.R.')],
               'Vuelta': [(' (2)', 'Llega hasta Barrio A.S.S.V.E.R.')],
              },
        '1121': {'Ida':    [(' (SL)', ''),
                            (' (DP)', ''),
                            (' (BH)', ''),
                            (' (DP)', ''),
                            (' (SR)', ''),
                            (' (LM)', ''),],
                 'Vuelta': [(' (BH)', ''),
                            (' (DP)', ''),
                            (' (SL)', ''),
                            (' (DP)', ''),
                            (' (SR)', ''),
                            (' (LM)', ''),],
              },
        '15': {'Ida':    [(' (1)', ''),
                          (' (2)', ''),],
               'Vuelta': [(' (3)', ''),
                          (' (4)', ''),]
              },
        # '1121': {'Ida':    [(' (SL)', 'Sale de Santa Lucia'),
        #                     (' (DP)', 'Sale de Divina Providencia'),
        #                     (' (BH)', 'Llega a Barrio Hernandarias'),
        #                     (' (DP)', 'Llega a Barrio La Milagrosa'),
        #                     (' (SR)', 'Sale de Cementerio Solar del Rio')],
        #          'Vuelta': [(' (BH)', 'Sale de Barrio Hernandarias'),
        #                     (' (DP)', 'Sale de Barrio La Milagrosa'),
        #                     (' (SL)', 'Llega a Santa Lucia'),
        #                     (' (DP)', 'Llega a Divina Providencia'),
        #                     (' (SR)', 'Llega a Cementerio Solar del Rio')],
        #       },
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

    # calculate estimates time from other Bus Stop
    data = [
        # 1 - IDA - HABILES
        {
            'line': '1',
            'direction': 'ida',
            'days': 'habiles',
            'bus_stop_name': '5 esquinas',
            'from_bus_stop_id': '31',
            'to_bus_stop_id': '32',
            'plus_time': 7,
         },
        {
            'line': '1',
            'direction': 'ida',
            'days': 'habiles',
            'bus_stop_name': 'B. Mitre y S. del Estero',
            'from_bus_stop_id': '33',
            'to_bus_stop_id': '17',
            'plus_time': 6,
         },

        # 1 - IDA - SABADOS
        {
            'line': '1',
            'direction': 'ida',
            'days': 'sabados',
            'bus_stop_name': '5 esquinas',
            'from_bus_stop_id': '31',
            'to_bus_stop_id': '32',
            'plus_time': 7,
         },
        {
            'line': '1',
            'direction': 'ida',
            'days': 'sabados',
            'bus_stop_name': 'B. Mitre y S. del Estero',
            'from_bus_stop_id': '33',
            'to_bus_stop_id': '17',
            'plus_time': 6,
         },

        # 1 - IDA - DOMINGOS
        {
            'line': '1',
            'direction': 'ida',
            'days': 'domingos',
            'bus_stop_name': '5 esquinas',
            'from_bus_stop_id': '31',
            'to_bus_stop_id': '32',
            'plus_time': 6,
         },

        #################################################

        # 5 - IDA - HABILES
        {
            'line': '5',
            'direction': 'ida',
            'days': 'habiles',
            'bus_stop_name': 'Don Bosco y Rondeau',
            'from_bus_stop_id': '9',
            'to_bus_stop_id': '10',
            'plus_time': 13,
         },
        {
            'line': '5',
            'direction': 'ida',
            'days': 'habiles',
            'bus_stop_name': 'P. Grella y Alte. Brown',
            'from_bus_stop_id': '10',
            'to_bus_stop_id': '11',
            'plus_time': 5,
         },

        # 5 - VUELTA - HABILES
        {
            'line': '5',
            'direction': 'vuelta',
            'days': 'habiles',
            'bus_stop_name': 'Casa de Gobierno',
            'from_bus_stop_id': '15',
            'to_bus_stop_id': '19',
            'plus_time': 7,
         },
        {
            'line': '5',
            'direction': 'vuelta',
            'days': 'habiles',
            'bus_stop_name': '5 esquinas',
            'from_bus_stop_id': '19',
            'to_bus_stop_id': '12',
            'plus_time': 13,
         },
        {
            'line': '5',
            'direction': 'vuelta',
            'days': 'habiles',
            'bus_stop_name': 'Don Bosco y Rondeau',
            'from_bus_stop_id': '12',
            'to_bus_stop_id': '10',
            'plus_time': 10,
         },

        # 5 - IDA - SABADOS
        {
            'line': '5',
            'direction': 'ida',
            'days': 'sabados',
            'bus_stop_name': 'Don Bosco y Rondeau',
            'from_bus_stop_id': '9',
            'to_bus_stop_id': '10',
            'plus_time': 12,
         },
        {
            'line': '5',
            'direction': 'ida',
            'days': 'sabados',
            'bus_stop_name': 'P. Grella y Alte. Brown',
            'from_bus_stop_id': '10',
            'to_bus_stop_id': '11',
            'plus_time': 5,
         },

        # 5 - VUELTA - SABADOS
        {
            'line': '5',
            'direction': 'vuelta',
            'days': 'sabados',
            'bus_stop_name': 'Don Bosco y Rondeau',
            'from_bus_stop_id': '12',
            'to_bus_stop_id': '10',
            'plus_time': 10,
         },

        # 5 - IDA - DOMINGOS
        {
            'line': '5',
            'direction': 'ida',
            'days': 'domingos',
            'bus_stop_name': 'Don Bosco y Rondeau',
            'from_bus_stop_id': '9',
            'to_bus_stop_id': '10',
            'plus_time': 12,
         },
        {
            'line': '5',
            'direction': 'ida',
            'days': 'domingos',
            'bus_stop_name': 'P. Grella y Alte. Brown',
            'from_bus_stop_id': '10',
            'to_bus_stop_id': '11',
            'plus_time': 5,
         },

        # 5 - VUELTA - DOMINGOS
        {
            'line': '5',
            'direction': 'vuelta',
            'days': 'domingos',
            'bus_stop_name': 'Don Bosco y Rondeau',
            'from_bus_stop_id': '12',
            'to_bus_stop_id': '10',
            'plus_time': 10,
         },

        #################################################

        # 6 - IDA - HABILES
        {
            'line': '6',
            'direction': 'ida',
            'days': 'habiles',
            'bus_stop_name': 'Av. Americas y M. Lebhenson',
            'from_bus_stop_id': '2',
            'to_bus_stop_id': '5',
            'plus_time': 12,
         },
        {
            'line': '6',
            'direction': 'ida',
            'days': 'habiles',
            'bus_stop_name': 'Av. Americas y Bv. Racedo',
            'from_bus_stop_id': '5',
            'to_bus_stop_id': '6',
            'plus_time': 7,
         },

        # 6 - VUELTA - HABILES
        {
            'line': '6',
            'direction': 'vuelta',
            'days': 'habiles',
            'bus_stop_name': 'Av. Americas y Bv. Racedo',
            'from_bus_stop_id': '8',
            'to_bus_stop_id': '6',
            'plus_time': 8,
         },

        # 6 - IDA - SABADOS
        {
            'line': '6',
            'direction': 'ida',
            'days': 'sabados',
            'bus_stop_name': 'Av. Americas y M. Lebhenson',
            'from_bus_stop_id': '2',
            'to_bus_stop_id': '5',
            'plus_time': 12,
         },
        {
            'line': '6',
            'direction': 'ida',
            'days': 'sabados',
            'bus_stop_name': 'Av. Americas y Bv. Racedo',
            'from_bus_stop_id': '5',
            'to_bus_stop_id': '6',
            'plus_time': 7,
         },

        # 6 - VUELTA - SABADOS
        {
            'line': '6',
            'direction': 'vuelta',
            'days': 'sabados',
            'bus_stop_name': 'Av. Americas y Bv. Racedo',
            'from_bus_stop_id': '8',
            'to_bus_stop_id': '6',
            'plus_time': 7,
         },

        # 6 - IDA - DOMINGOS
        {
            'line': '6',
            'direction': 'ida',
            'days': 'domingos',
            'bus_stop_name': 'Av. Americas y M. Lebhenson',
            'from_bus_stop_id': '2',
            'to_bus_stop_id': '5',
            'plus_time': 12,
         },
        {
            'line': '6',
            'direction': 'ida',
            'days': 'domingos',
            'bus_stop_name': 'Av. Americas y Bv. Racedo',
            'from_bus_stop_id': '5',
            'to_bus_stop_id': '6',
            'plus_time': 7,
         },

        # 6 - VUELTA - DOMINGOS
        {
            'line': '6',
            'direction': 'vuelta',
            'days': 'domingos',
            'bus_stop_name': 'Av. Americas y Bv. Racedo',
            'from_bus_stop_id': '8',
            'to_bus_stop_id': '6',
            'plus_time': 7,
         },

        #################################################

        # 10 - IDA - HABILES
        {
            'line': '10',
            'direction': 'ida',
            'days': 'habiles',
            'bus_stop_name': 'Antonio Crespo y Av. Ramirez',
            'from_bus_stop_id': '38',
            'to_bus_stop_id': '20',
            'plus_time': 13,
         },
        {
            'line': '10',
            'direction': 'ida',
            'days': 'habiles',
            'bus_stop_name': 'Barrio Hernandarias',
            'from_bus_stop_id': '20',
            'to_bus_stop_id': '21',
            'plus_time': 5,
         },

        # 10 - VUELTA - HABILES
        {
            'line': '10',
            'direction': 'vuelta',
            'days': 'habiles',
            'bus_stop_name': 'Barrio Hernandarias',
            'from_bus_stop_id': '39',
            'to_bus_stop_id': '31',
            'plus_time': 8,
         },
        {
            'line': '10',
            'direction': 'vuelta',
            'days': 'habiles',
            'bus_stop_name': 'Antonio Crespo y Av. Ramirez',
            'from_bus_stop_id': '31',
            'to_bus_stop_id': '20',
            'plus_time': 6,
         },

        # 10 - IDA - SABADOS
        {
            'line': '10',
            'direction': 'ida',
            'days': 'sabados',
            'bus_stop_name': 'Antonio Crespo y Av. Ramirez',
            'from_bus_stop_id': '38',
            'to_bus_stop_id': '20',
            'plus_time': 13,
         },
        {
            'line': '10',
            'direction': 'ida',
            'days': 'habiles',
            'bus_stop_name': 'Barrio Hernandarias',
            'from_bus_stop_id': '20',
            'to_bus_stop_id': '21',
            'plus_time': 5,
         },

        # 10 - VUELTA - SABADOS
        {
            'line': '10',
            'direction': 'vuelta',
            'days': 'sabados',
            'bus_stop_name': 'Barrio Hernandarias',
            'from_bus_stop_id': '39',
            'to_bus_stop_id': '31',
            'plus_time': 8,
         },
        {
            'line': '10',
            'direction': 'vuelta',
            'days': 'habiles',
            'bus_stop_name': 'Antonio Crespo y Av. Ramirez',
            'from_bus_stop_id': '31',
            'to_bus_stop_id': '20',
            'plus_time': 6,
         },

        # 10 - IDA - DOMINGOS
        {
            'line': '10',
            'direction': 'ida',
            'days': 'domingos',
            'bus_stop_name': 'Antonio Crespo y Av. Ramirez',
            'from_bus_stop_id': '38',
            'to_bus_stop_id': '20',
            'plus_time': 12,
         },
        {
            'line': '10',
            'direction': 'ida',
            'days': 'domingos',
            'bus_stop_name': 'Barrio Hernandarias',
            'from_bus_stop_id': '20',
            'to_bus_stop_id': '21',
            'plus_time': 5,
         },

        # 10 - VUELTA - DOMINGOS
        {
            'line': '10',
            'direction': 'vuelta',
            'days': 'domingos',
            'bus_stop_name': 'Barrio Hernandarias',
            'from_bus_stop_id': '39',
            'to_bus_stop_id': '31',
            'plus_time': 8,
         },
        {
            'line': '10',
            'direction': 'vuelta',
            'days': 'domingos',
            'bus_stop_name': 'Antonio Crespo y Av. Ramirez',
            'from_bus_stop_id': '31',
            'to_bus_stop_id': '20',
            'plus_time': 6,
         },


        ]

    for d in data:
        rows = []
        filename = 'bustime_linea_%s_%s_%s.csv' % (d['line'], d['days'], d['direction'])
        path = os.path.join('../fixtures', filename)
        if os.path.exists(path):
            csv_reader = csv.reader(open(path, 'r'))
            for row in csv_reader:
                if row[1] != d['from_bus_stop_id']:
                    continue

                hour, minute, second = map(int, row[4].split(':'))
                original_time = datetime.datetime(1970, 1, 1, hour, minute, 0)
                plus_time = original_time + datetime.timedelta(minutes=d['plus_time'])
                plus_time = plus_time.time().strftime('%H:%M:%S')
                new_row = d['bus_stop_name'], d['to_bus_stop_id'], d['line'], d['days'].title(), plus_time, row[5].strip(), row[6]
                rows.append(new_row)

        fp = open(path, 'a')
        csv_writer = csv.writer(fp)
        csv_writer.writerows(rows)
        fp.close()
        print 'Rows added to: %s' % path
