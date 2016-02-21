#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
#
#   Copyright 2009-2016 Michal Sadowski (sq6jnx at hamradio dot pl)
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
    """Class for downloading and parsing worldweatheronline.com weather data
(www.worldweatheronline.com/api/docs/local-city-town-weather-api.aspx).

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
        l = self.__language
        wc = self.__language.wwo_weather_codes

        REQ_URL = "https://api.worldweatheronline.com/free/v2/weather.ashx?"\
                + "q={LAT},{LON}&format=json&num_of_days=2&key={API_KEY}"

        params = {
            'LAT': str(self.__latitude),
            'LON': str(self.__longitude),
            'API_KEY': self.__api_key,
        }

        url = REQ_URL.format(**params)
        logger.info("Sending query")
        raw_data = urllib2.urlopen(url).read()
        response = json.loads(raw_data)
        d = response['data']

        # TODO: this is a configuration parameter!
        timezone = pytz.timezone('Europe/Warsaw')

        observation_datetime_utc = ' '.join((
            d['weather'][0]['date'],
            d['current_condition'][0]['observation_time']))

        observation_datetime_utc = datetime.datetime.strptime(
            observation_datetime_utc,
            '%Y-%m-%d %I:%M %p')

        observation_localtime = (pytz.utc.localize(observation_datetime_utc)
                                .astimezone(timezone))

        cc = d['current_condition'][0]

        # calculating index for weather forecast for the next few hours is
        # tricky. 
        datetime_3hrs = observation_datetime_utc + datetime.timedelta(hours=3)
        fcast_day_index = 1 if datetime_3hrs.day != observation_datetime_utc else 0
        fcast_hour_index = int(datetime_3hrs.hour / 3)

        fcast = d["weather"][fcast_day_index]["hourly"][fcast_hour_index]


        data = {
            'OBSERVATION_TIME': l.read_datetime(observation_localtime, '%H %M'),
            'CURRENT_CLOUDCOVER': l.read_percent(int(cc['cloudcover'])),
            'CURRENT_HUMIDITY': l.read_percent(int(cc['humidity'])),
            'CURRENT_PRESSURE': l.read_pressure(int(cc['pressure'])),
            'CURRENT_TEMP_C': l.read_temperature(int(cc['temp_C'])),
            'CURRENT_WEATHER': l.ra(wc[cc['weatherCode']]),
            'CURRENT_WIND_DIR': l.read_direction(cc['winddir16Point'], short=True),
            'CURRENT_WIND_DIR_DEG': l.read_degrees(int(cc['winddirDegree'])),
            'CURRENT_WIND_SPEED_KMPH': l.read_speed(int(cc['windspeedKmph']), unit='kmph'),
            'CURRENT_WIND_SPEED_MPS': l.read_speed(self.kmph2mps(cc['windspeedKmph'])),

            'FCAST_TEMP_C': l.read_number(int(fcast['tempC'])),
            'FCAST_WEATHER': l.ra(wc[fcast['weatherCode']]),
            'FCAST_WIND_DIR': l.read_direction(fcast['winddir16Point'], short=True),
            'FCAST_WIND_DIR_DEG': l.read_degrees(int(fcast['winddirDegree'])),
            'FCAST_WIND_SPEED_KMPH': l.read_speed(int(fcast['windspeedKmph']), unit='kmph'),
            'FCAST_WIND_SPEED_MPS': l.read_speed(self.kmph2mps(fcast['windspeedKmph'])),
        }

        # (temporary?) fix for reading wind directions -- elements are separated
        # with hyphen, but for purposes of reading by sr0wx core these should be
        # separated by space.
        data.update(dict(tuple((k, data[k].replace('-', ' '))
                               for k in ('CURRENT_WIND_DIR',
                                         'FCAST_WIND_DIR',
                                         ))))

        return {
            "message": self.__message_template.format(**data),
            "source": "worldweatheronline",
        }
