#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

CTCSS = 88.8
playCTCSS = False
CTCSSVolume = 0.1
serialPort = '/dev/ttyS0'
serialBaudRate = 9600

from lib.cw import *

lang = "pl_google"

pygameBug = 0

helloMsg = ["tu_eksperymentalna_automatyczna_stacja_pogodowa", "sp6yre", ]
goodbyeMsg = ["_", "tu_sp6yre", cw('sp6yre')]

modules = ["worldweatheronline", "y_weather",]


class m:
    pass


y_weather = m()
y_weather.zipcode = 526363
# it would be nice to give one ability to parse it via template engine
# http://wiki.python.org/moin/Templating
y_weather.template = """\
    stan_pogody_z_dnia {PUB_DATE_HOUR} _ temperatura
    {CURR_TEMP} wilgotnosc {HUMIDITY}
    {CURRENT_CONDITION} _ kierunek_wiatru {WIND_DIR_NEWS}
    {WIN_DIR_DEG} predkosc_wiatru {WIND_SPEED} _
    cisnienie {PRESSURE} {PRESSURE_TENDENTION}
    temperatura_odczuwalna {TEMP_WIND_CHILL} _

    prognoza_na_nastepne piec godzin
    {FORECAST0_CONDITION} temperatura_minimalna
    {FORECAST0_MIN_TEMP_SHORT} maksymalna {FORECAST0_MAX_TEMP}

    _ nastepnie {FORECAST1_CONDITION} temperatura_minimalna
    {FORECAST1_MIN_TEMP_SHORT} maksymalna {FORECAST1_MAX_TEMP} _
    """

debug = m()
debug.writeLevel = None
debug.showLevel = 0

# world weather online

world_weather_online = m()
world_weather_online.api_key = 'CHANGEME'
world_weather_online.latitude = 52.71
world_weather_online.longitude = 19.11
world_weather_online.template = """\
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
    {FCAST1_WIND_SPEED_MPS} {FCAST1_WIND_SPEED_KMPH} _ """


# -------------
# activity_map
# ------------

activity_map = m()
activity_map.service_url = "http://test.ostol.pl/?base="
activity_map.data = {"callsign": "SR0WX",
                     "lat": 0,
                     "lon": 0,
                     "q": 5,
                     "asl": 118,
                     "agl": 20,
                     "range": 30,
                     "info": u"Additional information",
                     }

# ------
# wview
# ------
wview = m()
wview.path = '/var/lib/wview/archive/wview-archive.sdb'
wview.template = """\
stan_pogody_z_dnia {OBSERVATION_TIME}
temperatura {CURRENT_TEMP_C} wilgotnosc {CURRENT_HUMIDITY}
_ kierunek_wiatru
{CURRENT_WIND_DIR_DEG} predkosc_wiatru {CURRENT_WIND_SPEED_MPS}
_ cisnienie {CURRENT_PRESSURE} """
