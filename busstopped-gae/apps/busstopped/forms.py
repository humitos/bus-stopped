# -*- coding: utf-8 -*-

from wtforms import Form, fields

from models import BusStop

class ViewBusStopLinesForm(Form):
    lines = fields.SelectField(u'Líneas')
    direction = fields.SelectField(u'Direccion', choices=[('Ida', 'Ida'),
                                                          ('Vuelta', 'Vuelta')])

    def __init__(self, *args, **kwargs):
        super(ViewBusStopLinesForm, self).__init__(*args, **kwargs)

        busses_stops = BusStop.all()
        busses_stops.order('lines')
        lines = set()
        for bs in busses_stops:
            for l in bs.lines:
                lines.add((l, u'Línea %s' % l))
        self.lines.choices = lines
