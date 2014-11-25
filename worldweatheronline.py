#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
#
#   Copyright 2009-2014 Michal Sadowski (sq6jnx at hamradio dot pl)
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

from sr0wx_module import SR0WXModule


class WorldWeatherOnline(SR0WXModule):
    """Class for downloading and parsing worldweatheronline.com weather data.

    You should obtain your (version 2) `api_key` for the site. `latitude` and
`longitude` define your position on the globe. `message template` is the most
tricky part, so best see example config."""
    def __init__(self, api_key, latitude, longitude, language, message_template):
        self.__api_key = api_key
        self.__latitude = latitude
        self.__longitude = longitude
        self.__language = language
        self.__message_template = message_template

    def __wind_direction(self, direction, short=False):
        # TODO: `move to lang package`
        retval = ""
        if len(direction) == 3 and short:
            direction = direction[1:3]
        for i in range(0, len(direction) - 1):
            retval = retval + self.__language.directions[direction[i]][0]
        retval = retval + self.__language.directions[direction[-1]][1]
        return retval

    # TODO: Do I need this?
    kmph2mps = lambda self, s: int(round(float(s)*(5.0/18.0)))


    def get_data(self):
        logger = logging.getLogger(__name__)

        rv = {
            'message': '',
            "need_ctcss": False,
            "source": "worldweatheronline",
        }

        REQ_URL = "http://api.worldweatheronline.com/free/v2/weather.ashx?"\
                + "q={LAT},{LON}&format=json&num_of_days=2&key={API_KEY}"

        params = {
            'LAT': str(self.__latitude),
            'LON': str(self.__longitude),
            'API_KEY': self.__api_key,
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
        wc = self.__language.wwo_weather_codes

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

        # What a mess!
        # TODO: lang.read_temperature_celsius
        # TODO: lang.`read datetime function` (no idea for name and
        # functionality now)
        # TODO: lang.read_pressure
        # TODO: read_wind_direction (see def __wind_direction() above)
        # TODO: read_wind_direction_degrees
        # TODO: read_speed_kmph
        # TODO: and so on to clear this mess below.
        data = {
            'OBSERVATION_TIME': self.__language.readISODT(utc_dt.astimezone(local).strftime('%Y-%m-%d %H:%M:%S')),
            'CURRENT_CLOUDCOVER': self.__language.cardinal(int(w['cloudcover']), self.__language.percent),
            'CURRENT_HUMIDITY': self.__language.cardinal(int(w['humidity']), self.__language.percent),
            'CURRENT_PRESSURE': self.__language.cardinal(int(w['pressure']), self.__language.hPa),
            'CURRENT_TEMP_C': self.__language.cardinal(int(w['temp_C']), self.__language.C),
            'CURRENT_WEATHER': self.__language.removeDiacritics(wc[w['weatherCode']], remove_spaces=True),
            'CURRENT_WIND_DIR': self.__wind_direction(w['winddir16Point'], short=True),
            'CURRENT_WIND_DIR_DEG': self.__language.cardinal(int(w['winddirDegree']), self.__language.deg),
            'CURRENT_WIND_SPEED_KMPH': self.__language.cardinal(int(w['windspeedKmph']), self.__language.kmPh),
            'CURRENT_WIND_SPEED_MPS': self.__language.cardinal(self.kmph2mps(int(w['windspeedKmph'])), self.__language.mPs),
            'CURRENT_WIND_SPEED_MI': self.__language.cardinal(int(w['windspeedMiles']), self.__language.MiPh),
            'FCAST0_TEMP_MIN_C': self.__language.cardinal(int(f0['mintempC'])),
            'FCAST0_TEMP_MAX_C': self.__language.cardinal(int(f0['maxtempC']), self.__language.C),
            'FCAST0_WEATHER': self.__language.removeDiacritics(wc[f00['weatherCode']], remove_spaces=True),
            'FCAST0_WIND_DIR': self.__wind_direction(f00['winddir16Point']),
            'FCAST0_WIND_DIR_DEG': self.__language.cardinal(int(f00['winddirDegree']), self.__language.deg),
            'FCAST0_WIND_SPEED_KMPH': self.__language.cardinal(int(f00['windspeedKmph']), self.__language.kmPh),
            'FCAST0_WIND_SPEED_MPS': self.__language.cardinal(self.kmph2mps(int(f00['windspeedKmph'])), self.__language.mPs),
            'FCAST0_WIND_SPEED_MI': int(f00['windspeedMiles']),
            'FCAST1_TEMP_MIN_C': self.__language.cardinal(int(f1['mintempC'])),
            'FCAST1_TEMP_MAX_C': self.__language.cardinal(int(f1['maxtempC']), self.__language.C),
            'FCAST1_WEATHER': self.__language.removeDiacritics(wc[f10['weatherCode']], remove_spaces=True),
            'FCAST1_WIND_DIR': self.__wind_direction(f10['winddir16Point']),
            'FCAST1_WIND_DIR_DEG': self.__language.cardinal(int(f10['winddirDegree']), self.__language.deg),
            'FCAST1_WIND_SPEED_KMPH': self.__language.cardinal(int(f10['windspeedKmph']), self.__language.kmPh),
            'FCAST1_WIND_SPEED_MPS': self.__language.cardinal(self.kmph2mps(int(f10['windspeedKmph'])), self.__language.mPs),
            'FCAST1_WIND_SPEED_MI': int(f10['windspeedMiles']),
            }

        rv['message'] = self.__language.removeDiacritics(self.__message_template.format(**data))

        return rv

def get_data(l):
    from config import world_weather_online as config
    wwo = WorldWeatherOnline(**config)
    return wwo.get_data()
