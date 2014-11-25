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

ctcss_tone = 88.8
play_ctcss = False
ctcss_volume = 0.1
serial_port = '/dev/ttyS0'
serial_baud_rate = 9600

from lib.cw import *

import pl_google.pl_google as pl_google
lang = "pl_google"

pygame_bug = 0

hello_msg = ["tu_eksperymentalna_automatyczna_stacja_pogodowa", "sp6yre", ]
goodbye_msg = ["_", "tu_sp6yre", cw('sp6yre')]

#
# Modules configuration
#
# List of activated modules is at the very bottom of this file
#

# world weather online

from world_weather_online import WorldWeatherOnline
worldweatheronline = WorldWeatherOnline(
    api_key="CHANGEME",
    latitude=52.71,
    longitude=19.11,
    language=pl_google,
    message_template="""\
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
)


# -------------
# activity_map
# ------------

from activity_map import ActivityMap
activitymap = ActivityMap(
    service_url="http://test.ostol.pl/?base=",
    callsign=None,
    latitude=0,
    longitude=0,
    hour_quarter=5,
    above_sea_level=118,
    above_ground_level=20,
    station_range=30,
    additional_info="",
)

# List of modules to query on program run
modules = [activitymap, worldweatheronline, ]
