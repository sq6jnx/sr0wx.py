#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
#
#   Copyright 2009-2011 Michal Sadowski (sq6jnx at hamradio dot pl)
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

#from config import y_weather as config

yahoo_conditions = {
'0':  'traba_powietrzna',            # tornado
'1':  'burza_tropikalna',            # tropical storm
'2':  'huragan',                     # hurricane
'3':  'silne_burze',                 # severe thunderstorms
'4':  'burza',                       # thunderstorms
'5':  'deszcz snieg',                # mixed rain and snow
'6':  'marznace_opady deszczu',      # mixed rain and sleet
'7':  'marznace_opady sniegu',       # mixed snow and sleet
'8':  'marznace_opady deszczu',      # freezing drizzle
'9':  'mrzawka',                     # drizzle
'10': 'marznacy deszcz',             # freezing rain
'11': 'przelotne_opady deszczu',     # showers
'12': 'przelotne_opady deszczu',     # showers
'13': 'przelotne_opady sniegu',      # snow flurries
'14': 'przelotne_opady sniegu',      # light snow showers
'15': 'zawieje_i_zamiecie_sniezne',  # blowing snow
'16': 'snieg',                       # snow
'17': 'zamiec',                      # hail
'18': 'snieg deszcz',                # sleet
'19': 'pyl',                         # dust
'20': 'mgla',                        # foggy
'21': 'smog',                        # haze
'22': 'smog',                        # smoky
'23': 'silny_wiatr',                 # blustery
'24': 'silny_wiatr',                 # windy
'25': 'przymrozki',                  # cold
'26': 'zachmurzenie_calkowite',      # cloudy
'27': 'zachmurzenie_umiarkowane',    # mostly cloudy (night)
'28': 'zachmurzenie_umiarkowane',    # mostly cloudy (day)
'29': 'czesciowe zachmurzenie',      # partly cloudy (night)
'30': 'czesciowe zachmurzenie',      # partly cloudy (day)
'31': 'bezchmurnie',                 # clear (night)
'32': 'bezchmurnie',                 # sunny
'33': 'slabe zachmurzenie',          # fair (night)
'34': 'slabe zachmurzenie',          # fair (day)
'35': 'deszcz',                      # mixed rain and hail
'36': 'wysokie_temperatury',         # hot
'37': 'burza',                       # isolated thunderstorms
'38': 'burza',                       # scattered thunderstorms
'39': 'burza',                       # scattered thunderstorms
'40': 'deszcz',                      # scattered showers
'41': 'intensywne_opady sniegu',     # heavy snow
'42': 'snieg',                       # scattered snow showers
'43': 'intensywne_opady sniegu',     # heavy snow
'44': 'czesciowe zachmurzenie',      # partly cloudy
'45': 'burza',                       # thundershowers
'46': 'mzawka',                      # snow showers
'47': 'burze',                       # isolated thundershowers
'3200': '',                          # not available
}

# For debugging purposes:

import debug
import urllib2

# It will store ``metar`` language module.
lang = None

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

# Taken from http://developer.yahoo.com/python/python-xml.html (SLIGHTLY modified)
# simple and elegant, but I HATE XML!

import urllib
from xml.dom import minidom
    

def weather_for_zip(zip_code):
    WEATHER_URL = 'http://weather.yahooapis.com/forecastrss?w=%s&u=c'
    #WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
    WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'

    url = WEATHER_URL % zip_code
    dom = minidom.parse(urllib.urlopen(url))
    forecasts = []
    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'forecast'):
        forecasts.append({
            'date': node.getAttribute('date'),
            'low': node.getAttribute('low'),
            'high': node.getAttribute('high'),
            'condition': node.getAttribute('text')
        })
    ycondition = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]
    return {
        'current_condition': ycondition.getAttribute('text'),
        'current_temp': ycondition.getAttribute('temp'),
        'forecasts': forecasts,
        'title': dom.getElementsByTagName('title')[0].firstChild.data
    }


def getData(l):
    print weather_for_zip(487947)

    global lang
    lang = my_import(l+"."+l)

    return data

getData('pl')
