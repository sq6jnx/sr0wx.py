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

    # TODO: Is it the best place for this function?
    kmph2mps = lambda self, s: int(round(float(s)*(5.0/18.0)))


    def get_data(self):
        logger = logging.getLogger(__name__)


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

        # observation time gives us time in UTC, like '09:50 PM', but it gives
        # no date. Since we want it as a whole datetime, like '1970-01-01 21:50'
        # we have to get it from the API (from first forecast, to be exact)
        # and merge it with the observation time 

        # TODO: this is a configuration parameter!
        timezone = pytz.timezone('Europe/Warsaw')

        utc = pytz.utc
        observation_time_utc = response['data']['current_condition'][0]['observation_time']
        observation_date_utc = response['data']['weather'][0]['date']
        
        observation_string_utc = observation_date_utc + ' ' + observation_time_utc

        observation_datetime_utc = datetime.datetime.strptime(observation_string_utc,
                                                              '%Y-%m-%d %I:%M %p')

        utc_dt = utc.localize(observation_datetime_utc)
        obs_localtime = utc_dt.astimezone(timezone)

        l = self.__language
        wc = self.__language.wwo_weather_codes
        data = {
            'OBSERVATION_TIME': l.read_datetime(obs_localtime, '%H %M'),
            'CURRENT_CLOUDCOVER': l.read_percent(int(w['cloudcover'])),
            'CURRENT_HUMIDITY': l.read_percent(int(w['humidity'])),
            'CURRENT_PRESSURE': l.read_pressure(int(w['pressure'])),
            'CURRENT_TEMP_C': l.read_temperature(int(w['temp_C'])),
            'CURRENT_WEATHER': l.ra(wc[w['weatherCode']]),
            'CURRENT_WIND_DIR': l.read_direction(w['winddir16Point'], short=True),
            'CURRENT_WIND_DIR_DEG': l.read_degrees(int(w['winddirDegree'])),
            'CURRENT_WIND_SPEED_KMPH': l.read_speed(int(w['windspeedKmph']), unit='kmph'),
            'CURRENT_WIND_SPEED_MPS': l.read_speed(self.kmph2mps(w['windspeedKmph'])),
            'FCAST0_TEMP_MIN_C': l.read_number(int(f0['mintempC'])),
            'FCAST0_TEMP_MAX_C': l.read_temperature(int(f0['maxtempC'])),
            'FCAST0_WEATHER': l.ra(wc[f00['weatherCode']]),
            'FCAST0_WIND_DIR': l.read_direction(f00['winddir16Point'], short=True),
            'FCAST0_WIND_DIR_DEG': l.read_degrees(int(f00['winddirDegree'])),
            'FCAST0_WIND_SPEED_KMPH': l.read_speed(int(f00['windspeedKmph']), unit='kmph'),
            'FCAST0_WIND_SPEED_MPS': l.read_speed(self.kmph2mps(f00['windspeedKmph'])),
            'FCAST1_TEMP_MIN_C': l.read_number(int(f1['mintempC'])),
            'FCAST1_TEMP_MAX_C': l.read_temperature(int(f1['maxtempC'])),
            'FCAST1_WEATHER': l.ra(wc[f10['weatherCode']]),
            'FCAST1_WIND_DIR': l.read_direction(f10['winddir16Point']),
            'FCAST1_WIND_DIR_DEG': l.read_degrees(int(f10['winddirDegree'])),
            'FCAST1_WIND_SPEED_KMPH': l.read_speed(int(f10['windspeedKmph']), unit='kmph'),
            'FCAST1_WIND_SPEED_MPS': l.read_speed(self.kmph2mps(f10['windspeedKmph'])),
        }

        # (temporary?) fix for reading wind directions -- elements are separated
        # with hyphen, but for purposes of reading by sr0wx core these should be
        # separated by space.
        data.update(dict(tuple((k, data[k].replace('-', ' '))
                               for k in ('CURRENT_WIND_DIR',
                                         'FCAST0_WIND_DIR',
                                         'FCAST1_WIND_DIR',
                                         ))))

        return {
            "message": self.__message_template.format(**data),
            "source": "worldweatheronline",
        }
