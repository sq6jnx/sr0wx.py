#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import logging, logging.handlers

log_line_format = '%(asctime)s %(name)s %(levelname)s: %(message)s'
log_handlers = [
    {
        'log_level': logging.INFO,
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

serial_port = '/dev/ttyS0'
serial_baud_rate = 9600

import pl_microsoft.pl_microsoft as pl_microsoft
lang = "pl_microsoft"

pygame_bug = 0

hello_msg = ["tu_eksperymentalna_automatyczna_stacja_pogodowa", "sr0wx", ]
goodbye_msg = ["_", "tu_sr0wx"]

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
    language=pl_microsoft,
    message_template="""\
stan_pogody_z_godziny {OBSERVATION_TIME}
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
