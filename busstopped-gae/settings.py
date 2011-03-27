# -*- coding: utf-8 -*-
import os

PROJECT_ROOT = os.path.dirname(__file__)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_URL = '/static/'

NEXT_BUS_TIME_MINUTES = 30
PREVIOUS_BUS_TIME_MINUTES = 7

# Paraná - Entre Ríos
INITIAL_LOCATION = {
    'latitude': -31.74141804574782,
    'longitude': -60.51123228454588,
    }
