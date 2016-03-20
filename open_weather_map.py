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

import datetime
import json
import logging

from dateutil import tz

from sr0wx_module import SR0WXModule


class OpenWeatherMap(SR0WXModule):
    def __init__(self, api_key, latitude, longitude, language, message_template):
        self.__api_key = api_key
        self.__latitude = latitude
        self.__longitude = longitude
        self.__language = language
        self.__message_template = message_template

        self.__logger = logging.getLogger(__name__)
        self.API_URL = "http://api.openweathermap.org/data/2.5/{MODE}?"\
            + "lat={LAT}&lon={LON}&appid={API_KEY}"

    def _get_json(self, mode):
        supported_modes = ('weather', 'forecast')
        if mode not in supported_modes:
            raise ValueError("Supported modes are %s"
                             % (', '.join(supported_modes)))
        url = self.API_URL.format(**{
            'API_KEY': self.__api_key,
            'MODE': mode,
            'LAT': self.__latitude,
            'LON': self.__longitude,
        })

        return json.loads(self.download_file(url).decode())

    def get_current_conditions(self):
        return self._get_json('weather')

    def get_forecast(self):
        return self._get_json('forecast')

    def get_data(self):
        def kelvin2celsius(kelvin):
            return int(kelvin - 273.15)

        def unix2datetime(timestamp):
            return datetime.datetime.fromtimestamp(timestamp)

        l = self.__language
        wc = self.__language.open_weather_map

        c = self.get_current_conditions()
        f = self.get_forecast()["list"][1]

        observation_time = unix2datetime(c["dt"])

        data = {
            'OBSERVATION_TIME': l.read_datetime(observation_time, '%H %M'),
            'CURRENT_CLOUDCOVER': l.read_percent(int(c["clouds"]["all"])),
            'CURRENT_HUMIDITY': l.read_percent(int(c["main"]["humidity"])),
            'CURRENT_PRESSURE': l.read_pressure(int(c["main"]["grnd_level"])),
            'CURRENT_TEMP_C': l.read_temperature(kelvin2celsius(int(c["main"]["temp"]))),
            'CURRENT_WEATHER': l.ra(wc[c['weather'][0]['description']]),
            'CURRENT_WIND_DIR_DEG': l.read_degrees(int(c["wind"]["deg"])),
            'CURRENT_WIND_SPEED_MPS': l.read_speed(int(c["wind"]["speed"])),

            'FCAST_CLOUDCOVER': l.read_percent(int(f["clouds"]["all"])),
            'FCAST_HUMIDITY': l.read_percent(int(f["main"]["humidity"])),
            'FCAST_PRESSURE': l.read_pressure(int(f["main"]["grnd_level"])),
            'FCAST_TEMP_C': l.read_temperature(kelvin2celsius(int(f["main"]["temp"]))),
            'FCAST_WEATHER': l.ra(wc[f['weather'][0]['description']]),
            'FCAST_WIND_DIR_DEG': l.read_degrees(int(f["wind"]["deg"])),
            'FCAST_WIND_SPEED_MPS': l.read_speed(int(f["wind"]["speed"])),
        }

        return {
            "message": self.__message_template.format(**data),
            "source": "openweathermap",
        }
