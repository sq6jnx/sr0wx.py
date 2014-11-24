#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import logging, logging.handlers

log_line_format = '%(asctime)s %(name)s %(levelname)s: %(message)s'
log_handlers = [
    {
        'log_level': logging.DEBUG,
        'class': logging.StreamHandler,
        'config': {'stream': None},
    },
    {
        'log_level': logging.DEBUG,
        'class': logging.handlers.TimedRotatingFileHandler,
        'config': {
            'filename': 'sr0wx.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
            'delay': True,
            'utc': True,
        }
    }
]

CTCSS = 88.8
playCTCSS = False
CTCSSVolume = 0.1
serialPort = '/dev/ttyS0'
serialBaudRate = 9600

from lib.cw import *

import pl_google.pl_google as pl_google
lang = "pl_google"

pygameBug = 0

helloMsg = ["tu_eksperymentalna_automatyczna_stacja_pogodowa", "sp6yre", ]
goodbyeMsg = ["_", "tu_sp6yre", cw('sp6yre')]

modules = ["activity_map", "worldweatheronline",]

# world weather online

world_weather_online = {
    'api_key': "CHANGEME",
    'latitude': 52.71,
    'longitude': 19.11,
    'language': pl_google,
    'message_template': """\
stan_pogody_z_dnia {OBSERVATION_TIME}
_ {CURRENT_WEATHER}
temperatura {CURRENT_TEMP_C} wilgotnosc {CURRENT_HUMIDITY}
_ kierunek_wiatru {CURRENT_WIND_DIR}
{CURRENT_WIND_DIR_DEG} predkosc_wiatru {CURRENT_WIND_SPEED_MPS}
{CURRENT_WIND_SPEED_KMPH} _ cisnienie {CURRENT_PRESSURE}
pokrywa_chmur {CURRENT_CLOUDCOVER} _

prognoza_na_nastepne trzy godziny
{FCAST0_WEATHER} temperatura_minimalna
{FCAST0_TEMP_MIN_C} maksymalna {FCAST0_TEMP_MAX_C}
kierunek_wiatru {FCAST0_WIND_DIR} {FCAST0_WIND_DIR_DEG} predkosc_wiatru
{FCAST0_WIND_SPEED_MPS} {FCAST0_WIND_SPEED_KMPH}

_ jutro {FCAST1_WEATHER} temperatura_minimalna
{FCAST1_TEMP_MIN_C} maksymalna {FCAST1_TEMP_MAX_C} kierunek_wiatru
{FCAST1_WIND_DIR} {FCAST1_WIND_DIR_DEG} predkosc_wiatru
{FCAST1_WIND_SPEED_MPS} {FCAST1_WIND_SPEED_KMPH} _ """,
}


# -------------
# activity_map
# ------------

activity_map = {
    "service_url": "http://test.ostol.pl/?base=",
    "callsign": None,
    "latitude": 0,
    "longitude": 0,
    "hour_quarter": 5,
    "above_sea_level": 118,
    "above_ground_level": 20,
    "station_range": 30,
    "additional_info": "",
}
