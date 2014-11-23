#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
#
#   Copyright 2009-2011, 2014 Michal Sadowski (sq6jnx at hamradio dot pl)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import urllib2
import json
import datetime
import pytz
import logging
from config import world_weather_online as config


def wind_direction(direction, short=False):
    # TODO: need to find better place for this function
    global lang
    _dir = ""
    if len(direction) == 3 and short:
        direction = direction[1:3]
    for i in range(0, len(direction) - 1):
        _dir = _dir + lang.directions[direction[i]][0]
    _dir = _dir + lang.directions[direction[-1]][1]
    return _dir


def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

kmph2mps = lambda s: int(round(float(s)*(5.0/18.0)))


def getData(l):
    global lang
    lang = my_import(l + "." + l)
    logger = logging.getLogger(__name__)

    rv = {'data': '',
          "needCTCSS": False,
          "source": "worldweatheronline",
          }

    REQ_URL = "http://api.worldweatheronline.com/free/v2/weather.ashx?"\
              + "q={LAT},{LON}&format=json&num_of_days=2&key={API_KEY}"

    params = {'LAT': str(config.latitude),
              'LON': str(config.longitude),
              'API_KEY': config.api_key,
              }

    url = REQ_URL.format(**params)
    logger.info("Sending query")
    logger.debug("Query is: %s", url)
    response_data = urllib2.urlopen(url).read()
    response = json.loads(response_data)
    logger.debug("Response is: %s", response)

    # `w`, `f0` and `f1` are parts of big weather dictionary; we have to
    # unpack it for further formatting.
    w = response['data']['current_condition'][0]
    f0 = response['data']['weather'][0]
    f00 = f0['hourly'][0]
    f1 = response['data']['weather'][1]
    f10 = f1['hourly'][0]
    wc = lang.wwo_weather_codes

    # observation time gives us time in UTC, like '09:50 PM', but it gives
    # no date. Since we want it as a whole datetime, like '2011-12-28 21:50'
    # we have to make some transformations. We assume that the observation
    # was made today, but if resulting timestamp is in future we substract 1
    # day and convert it to local time.

    OBSERVATION_TIME = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    OBSERVATION_TIME = ' '.join((OBSERVATION_TIME, w['observation_time']))
    OBSERVATION_TIME = datetime.datetime.strptime(OBSERVATION_TIME,
                                                  '%Y-%m-%d %I:%M %p')
    if OBSERVATION_TIME > datetime.datetime.utcnow():
        OBSERVATION_TIME = OBSERVATION_TIME-datetime.timedelta(hours=24)
    utc = pytz.utc

    # TODO: this is a configuration parameter!
    local = pytz.timezone('Europe/Warsaw')
    utc_dt = utc.localize(OBSERVATION_TIME)

    data = {'OBSERVATION_TIME': lang.readISODT(utc_dt.astimezone(local).strftime('%Y-%m-%d %H:%M:%S')),
            'CURRENT_CLOUDCOVER': lang.cardinal(int(w['cloudcover']), lang.percent),
            'CURRENT_HUMIDITY': lang.cardinal(int(w['humidity']), lang.percent),
            'CURRENT_PRESSURE': lang.cardinal(int(w['pressure']), lang.hPa),
            'CURRENT_TEMP_C': lang.cardinal(int(w['temp_C']), lang.C),
            'CURRENT_WEATHER': lang.removeDiacritics(wc[w['weatherCode']], remove_spaces=True),
            'CURRENT_WIND_DIR': wind_direction(w['winddir16Point'], short=True),
            'CURRENT_WIND_DIR_DEG': lang.cardinal(int(w['winddirDegree']), lang.deg),
            'CURRENT_WIND_SPEED_KMPH': lang.cardinal(int(w['windspeedKmph']), lang.kmPh),
            'CURRENT_WIND_SPEED_MPS': lang.cardinal(kmph2mps(int(w['windspeedKmph'])), lang.mPs),
            'CURRENT_WIND_SPEED_MI': lang.cardinal(int(w['windspeedMiles']), lang.MiPh),
            'FCAST0_TEMP_MIN_C': lang.cardinal(int(f0['mintempC'])),
            'FCAST0_TEMP_MAX_C': lang.cardinal(int(f0['maxtempC']), lang.C),
            'FCAST0_WEATHER': lang.removeDiacritics(wc[f00['weatherCode']], remove_spaces=True),
            'FCAST0_WIND_DIR': wind_direction(f00['winddir16Point']),
            'FCAST0_WIND_DIR_DEG': lang.cardinal(int(f00['winddirDegree']), lang.deg),
            'FCAST0_WIND_SPEED_KMPH': lang.cardinal(int(f00['windspeedKmph']), lang.kmPh),
            'FCAST0_WIND_SPEED_MPS': lang.cardinal(kmph2mps(int(f00['windspeedKmph'])), lang.mPs),
            'FCAST0_WIND_SPEED_MI': int(f00['windspeedMiles']),
            'FCAST1_TEMP_MIN_C': lang.cardinal(int(f1['mintempC'])),
            'FCAST1_TEMP_MAX_C': lang.cardinal(int(f1['maxtempC']), lang.C),
            'FCAST1_WEATHER': lang.removeDiacritics(wc[f10['weatherCode']], remove_spaces=True),
            'FCAST1_WIND_DIR': wind_direction(f10['winddir16Point']),
            'FCAST1_WIND_DIR_DEG': lang.cardinal(int(f10['winddirDegree']), lang.deg),
            'FCAST1_WIND_SPEED_KMPH': lang.cardinal(int(f10['windspeedKmph']), lang.kmPh),
            'FCAST1_WIND_SPEED_MPS': lang.cardinal(kmph2mps(int(f10['windspeedKmph'])), lang.mPs),
            'FCAST1_WIND_SPEED_MI': int(f10['windspeedMiles']),
            }

    rv['data'] = lang.removeDiacritics(config.template.format(**data))

    return rv
