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

fake_gettext = lambda(s): s
_ = fake_gettext

from config import wview as config

# There are no bebug informations!

import sqlite3

lang = None


def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def getWeather():
    """Retrieves last (newest) record from archive.sdb. Possibly, this function
    should recalculate units (metric/imperial) or maybe calculate no-peak
    average of x number of values...

    For now it just ``select``s all columns from ``archive``."""
    # TODO: Do I really need all this data?

    conn = sqlite3.connect(config.path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
SELECT DATETIME(dateTime, 'unixepoch', 'localtime') AS dateTime,
    usUnits, interval, barometer, pressure, altimeter, inTemp, outTemp,
    inHumidity, outHumidity, windSpeed, windDir, windGust, windGustDir,
    rainRate, rain, dewpoint, windchill, heatindex, ET, radiation, UV,
    extraTemp1, extraTemp2, extraTemp3, soilTemp1, soilTemp2, soilTemp3,
    soilTemp4, leafTemp1, leafTemp2, extraHumid1, extraHumid2, soilMoist1,
    soilMoist2, soilMoist3, soilMoist4, leafWet1, leafWet2, rxCheckPercent,
    txBatteryStatus, consBatteryVoltage, hail, hailRate, heatingTemp,
    heatingVoltage, supplyVoltage, referenceVoltage, windBatteryStatus,
    rainBatteryStatus, outTempBatteryStatus, inTempBatteryStatus
FROM archive
ORDER BY datetime DESC
LIMIT 1;""")

    return c.fetchone()

# Probably this is the beginning of the metcalc module for meteorological
# calculations... we'll see.

fahrenheit2celsius = lambda f: int((f-32) * (5/9.0))
miph2mps = lambda miph: int(miph * 0.44704)
inHg2hPa = lambda inHg2hPa: int(inHg2hPa * 33.7685)


def getData(l):
    rv = {'data': '',
          "needCTCSS": False,
          "source": ""
          }

    lang = my_import(l+"."+l)
    w = getWeather()

    data = {'OBSERVATION_TIME': lang.readISODT(w['dateTime']),
            'CURRENT_TEMP_C': lang.cardinal(fahrenheit2celsius(w['outTemp']), lang.C),
            'CURRENT_HUMIDITY': lang.cardinal(int(w['outHumidity']), lang.percent),
            'CURRENT_WIND_DIR_DEG': lang.cardinal(int(w['windDir']) or 0, lang.deg),
            'CURRENT_WIND_SPEED_MPS': lang.cardinal(miph2mps(w['windSpeed']), lang.mPs),
            'CURRENT_PRESSURE': lang.cardinal(inHg2hPa(w['pressure']), lang.hPa),
            'TEMP_WIND_CHILL': lang.cardinal(fahrenheit2celsius(w['windchill']), lang.C),
            }

    rv['data'] = lang.removeDiacritics(config.template.format(**data))
    return rv

if __name__ == '__main__':
    getWeather()
