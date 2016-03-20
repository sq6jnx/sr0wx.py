#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import logging, logging.handlers

import pttlib

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

# There are three ways for PTT with sr0wx.
#
# This is the "null" option where your transmitter is turn on with VOX:
#
ptt = pttlib.vox()
#
# The other way is to use pySerial and PTT on one of two pins: DTR or RTS
#
#ptt = pttlib.serial('/dev/ttyUSB0', signal='DTR')
#
# The third way is to use GPIO from Raspberry PI:
# ptt = pttlib.gpio(17)

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
{FCAST_WEATHER} temperatura {FCAST_TEMP_C} stopni_celsjusza
kierunek_wiatru {FCAST_WIND_DIR} {FCAST_WIND_DIR_DEG} predkosc_wiatru
{FCAST_WIND_SPEED_MPS} {FCAST_WIND_SPEED_KMPH}""")

from open_weather_map import OpenWeatherMap
openweathermap = OpenWeatherMap(
    api_key="CHANGEME",
    latitude=52.71,
    longitude=19.11,
    language=pl_microsoft,
    message_template="""\
stan_pogody_z_godziny {OBSERVATION_TIME}
{CURRENT_WEATHER}
temperatura {CURRENT_TEMP_C} wilgotnosc {CURRENT_HUMIDITY}
kierunek_wiatru {CURRENT_WIND_DIR_DEG}
predkosc_wiatru {CURRENT_WIND_SPEED_MPS}
cisnienie {CURRENT_PRESSURE}
pokrywa_chmur {CURRENT_CLOUDCOVER}

prognoza_na_nastepne trzy godziny
{FCAST_WEATHER} temperatura {FCAST_TEMP_C}
kierunek_wiatru {FCAST_WIND_DIR_DEG} predkosc_wiatru
{FCAST_WIND_SPEED_MPS}""")

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
modules = [activitymap, worldweatheronline, openweathermap, ]
