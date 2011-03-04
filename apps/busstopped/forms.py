# -*- coding: utf-8 -*-

from wtforms import Form, fields

from models import BusTime

class ViewBusStopLinesForm(Form):
    lines = fields.SelectField(u'Líneas')
    direction = fields.SelectField(u'Direccion', choices=[('Ida', 'Ida'),
                                                          ('Vuelta', 'Vuelta')])

    def __init__(self, *args, **kwargs):
        super(ViewBusStopLinesForm, self).__init__(*args, **kwargs)
        self.lines.choices = set([(bt.bus_line, u'Línea %s' % bt.bus_line) for bt in BusTime.all()])
