import datetime

from fixture import DataSet

class BusStopData(DataSet):
    class line_6__thompson:
        name = 'Balneario Thompson'
        point = '0,0'
        lines = ['6']
        directions = 'Ida,Vuelta'.split(',')
        address = 'Soler y Bravard'


class BusTimeData(DataSet):
    class tarde1__sabados__line_6__thompson:
        bus_stop = BusStopData.line_6__thompson
        bus_line = '6'
        days = 'Sabados'
        time = datetime.time(18, 51)
        direction = 'Ida'

    class tarde2__sabados__line_6__thompson:
        bus_stop = BusStopData.line_6__thompson
        bus_line = '6'
        days = 'Sabados'
        time = datetime.time(19, 7)
        direction = 'Ida'


class BusDirectionData(DataSet):
    class line_6__ida:
        bus_line = '6'
        direction = 'Ida'
        from_direction = 'Oro Verde'
        to_direction = 'Balneario Thompson'


