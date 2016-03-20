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

from six import u
import datetime
from functools import wraps

import pyliczba


def ra(value):
    return value\
        .replace(u("ą"), "a").replace(u("Ą"), "a")\
        .replace(u("ć"), "c").replace(u("Ć"), "c")\
        .replace(u("ę"), "e").replace(u("Ę"), "e")\
        .replace(u("ł"), "l").replace(u("Ł"), "l")\
        .replace(u("ń"), "n").replace(u("Ń"), "n")\
        .replace(u("ó"), "o").replace(u("Ó"), "o")\
        .replace(u("ś"), "s").replace(u("Ś"), "s")\
        .replace(u("ź"), "z").replace(u("Ź"), "z")\
        .replace(u("ż"), "z").replace(u("Ż"), "z")\
        .lower()


def remove_accents(function):
    """unicodedata.normalize() doesn't work with ł and Ł"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        return ra(function(*args, **kwargs))
    return wrapper


def _(text):
    return text.replace(' ', '_')


class SR0WXLanguage(object):
    def __init__(self):
        """Nothing here for now."""
        pass


class PLMicrosoft(SR0WXLanguage):
    def __init__(self):
        super(PLMicrosoft, self).__init__()

    @remove_accents
    def read_number(self, value, units=None):
        """Converts numbers to text."""
        if units is None:
            retval = pyliczba.lslownie(abs(value))
        else:
            retval = pyliczba.cosslownie(abs(value), units)

        if retval.startswith(u("jeden tysiąc")):
            retval = retval.replace(u("jeden tysiąc"), u("tysiąc"))
        if value < 0:
            retval = " ".join(("minus", retval))
        return retval

    @remove_accents
    def read_pressure(self, value):
        hPa = ["hektopaskal", "hektopaskale", "hektopaskali"]
        return self.read_number(value, hPa)

    @remove_accents
    def read_percent(self, value):
        percent = ["procent", "procent", "procent"]
        return self.read_number(value, percent)

    @remove_accents
    def read_temperature(self, value):
        C = [_(u("stopień Celsjusza")),
             _("stopnie Celsjusza"),
             _("stopni Celsjusza")]
        return read_number(value, C)

    @remove_accents
    def read_speed(self, no, unit='mps'):
        units = {
            'mps': [_(u("metr na sekundę")), _(u("metry na sekundę")),
                    _(u("metrów na sekundę"))],
            'kmph': [_(u("kilometr na godzinę")), _(u("kilometry na godzinę")),
                     _(u("kilometrów na godzinę"))]
        }
        return read_number(no, units[unit])

    @remove_accents
    def read_degrees(self, value):
        deg = [u("stopień"), u("stopnie"), u("stopni")]
        return read_number(value, deg)

    @remove_accents
    def read_direction(self, value, short=False):
        directions = {
            "N": (u("północno"), u("północny")),
            "E": (u("wschodnio"), u("wschodni")),
            "W": (u("zachodnio"), u("zachodni")),
            "S": (u("południowo"), u("południowy")),
        }
        if short:
            value = value[-2:]
        return '-'.join([directions[d][0 if i < 0 else 1]
                         for i, d in enumerate(value, -len(value)+1)])

    @remove_accents
    def read_datetime(self, value, out_fmt, in_fmt=None):

        if type(value) != datetime.datetime and in_fmt is not None:
            value = datetime.datetime.strptime(value, in_fmt)
        elif type(value) == datetime.datetime:
            pass
        else:
            raise TypeError('Either datetime must be supplied or both '
                            'value and in_fmt')

        MONTHS = [u(""),
                  u("stycznia"), u("lutego"), u("marca"), u("kwietnia"),
                  u("maja"), u("czerwca"), u("lipca"), u("sierpnia"),
                  u("września"), u("października"), u("listopada"),
                  u("grudnia")]

        DAYS_N0 = [u(""), u(""), u("dwudziestego"), u("trzydziestego")]
        DAYS_N = [u(""),
                  u("pierwszego"), u("drugiego"), u("trzeciego"),
                  u("czwartego"), u("piątego"), u("szóstego"), u("siódmego"),
                  u("ósmego"), u("dziewiątego"), u("dziesiątego"),
                  u("jedenastego"), u("dwunastego"), u("trzynastego"),
                  u("czternastego"), u("piętnastego"), u("szesnastego"),
                  u("siedemnastego"), u("osiemnastego"), u("dziewiętnastego")]

        HOURS = [u("zero"), u("pierwsza"), u("druga"), u("trzecia"),
                 u("czwarta"), u("piąta"), u("szósta"), u("siódma"), u("ósma"),
                 u("dziewiąta"), u("dziesiąta"), u("jedenasta"), u("dwunasta"),
                 u("trzynasta"), u("czternasta"), u("piętnasta"),
                 u("szesnasta"), u("siedemnasta"), u("osiemnasta"),
                 u("dziewiętnasta"), u("dwudziesta")]

        _, tm_mon, tm_mday, tm_hour, tm_min, _, _, _, _ = value.timetuple()
        retval = []
        for word in out_fmt.split(" "):
            if word == '%d':  # Day of the month
                if tm_mday <= 20:
                    retval.append(DAYS_N[tm_mday])
                else:
                    retval.append(DAYS_N0[tm_mday // 10])
                    retval.append(DAYS_N[tm_mday % 10])
            elif word == '%B':  # Month as locale’s full name
                retval.append(MONTHS[tm_mon])
            elif word == '%H':  # Hour (24-hour clock) as a decimal number
                if tm_hour <= 20:
                    retval.append(HOURS[tm_hour])
                elif tm_hour > 20:
                    retval.append(HOURS[20])
                    retval.append(HOURS[tm_hour - 20])
            elif word == '%M':  # Minute as a decimal number
                if tm_min == 0:
                    retval.append(u('zero-zero'))
                else:
                    retval.append(read_number(tm_min))
            elif word.startswith('%'):
                raise ValueError("Token %s' is not supported!", word)
            else:
                retval.append(word)
        return ' '.join((w for w in retval if w != ''))

    @remove_accents
    def read_callsign(self, value):
        # literowanie polskie wg. "Krótkofalarstwo i radiokomunikacja
        # - poradnik", Łukasz Komsta SQ8QED, Wydawnictwa Komunikacji
        # i Łączności Warszawa, 2001, str. 130
        ICAO_LETTERS = {
            'a': u('adam'),
            'b': u('barbara'),
            'c': u('celina'),
            'd': u('dorota'),
            'e': u('edward'),
            'f': u('franciszek'),
            'g': u('gustaw'),
            'h': u('henryk'),
            'i': u('irena'),
            'j': u('józef'),
            'k': u('karol'),
            'l': u('ludwik'),
            'm': u('marek'),
            'n': u('natalia'),
            'o': u('olga'),
            'p': u('paweł'),
            'q': u('quebec'),
            'r': u('roman'),
            's': u('stefan'),
            't': u('tadeusz'),
            'u': u('urszula'),
            'v': u('violetta'),
            'w': u('wacław'),
            'x': u('xawery'),
            'y': u('ypsilon'),
            'z': u('zygmunt'),
            '/': u('łamane'),
        }
        retval = []
        for char in value.lower():
            try:
                retval.append(ICAO_LETTERS[char])
            except KeyError:
                try:
                    retval.append(read_number(int(char)))
                except ValueError:
                    msg = "'%s' may not a element of callsign" % (char, )
                    raise ValueError(msg)
        return ' '.join(retval)


# ##########################################
#
# module dependant words
# #############################################


# World Weather Online

wwo_weather_codes = {
    'Clear/Sunny': _(ra(u('bezchmurnie'))),
    'Partly Cloudy': _(ra(u('częściowe zachmurzenie'))),
    'Cloudy': _(ra(u('pochmurno'))),
    'Overcast': _(ra(u('zachmurzenie całkowite'))),
    'Mist': _(ra(u('zamglenia'))),
    'Patchy rain nearby': _(ra(u('lokalne przelotne opady deszczu'))),
    'Patchy snow nearby': _(ra(u('śnieg'))),
    'Patchy sleet nearby': _(ra(u('śnieg z deszczem'))),
    'Patchy freezing drizzle nearby':
        _(ra(u('lokalna przelotna marznąca mżawka'))),
    'Thundery outbreaks in nearby': _(ra(u('lokalne burze'))),
    'Blowing snow': _(ra(u('zamieć śnieżna'))),
    'Blizzard': _(ra(u('zamieć śnieżna'))),
    'Fog': _(ra(u('mgła'))),
    'Freezing fog': _(ra(u('marznąca mgła'))),
    'Patchy light drizzle': _(ra(u('mżawka'))),
    'Light drizzle': _(ra(u('mżawka'))),
    'Freezing drizzle': _(ra(u('marznąca mżawka'))),
    'Heavy freezing drizzle': _(ra(u('marznąca mżawka'))),
    'Patchy light rain': _(ra(u('lokalny słaby deszcz'))),
    'Light rain': _(ra(u('słaby deszcz'))),
    'Moderate rain at times': _(ra(u('przelotne opady deszczu'))),
    'Moderate rain': _(ra(u('umiarkowane opady deszczu'))),
    'Heavy rain at times': _(ra(u('przelotne ulewy'))),
    'Heavy rain': _(ra(u('ulewy'))),
    'Light freezing rain': _(ra(u('słabe opady marznącego deszczu'))),
    'Moderate or Heavy freezing rain':
        _(ra(u('umiarkowane opady marznącego deszczu'))),
    'Light sleet': _(ra(u('słabe opady śniegu z deszczem'))),
    'Moderate or heavy sleet':
        _(ra(u('umiarkowane lub ciężkie opady śniegu z deszczem'))),
    'Patchy light snow': _(ra(u('słabe opady śniegu'))),
    'Light snow': _(ra(u('słabe opady śniegu'))),
    'Patchy moderate snow': _(ra(u('umiarkowane opady śniegu'))),
    'Moderate snow': _(ra(u('umiarkowane opady śniegu'))),
    'Patchy heavy snow': _(ra(u('opady śniegu'))),
    'Heavy snow': _(ra(u('intensywne_opady_sniegu'))),
    'Ice pellets': _(ra(u('grad'))),
    'Light rain shower': _(ra(u('słabe przelotne opady deszczu'))),
    'Moderate or heavy rain shower': _(ra(u('przelotne opady deszczu'))),
    'Torrential rain shower': _(ra(u('ulewny deszcz'))),
    'Light sleet showers': _(ra(u('słabe opady śniegu z deszczem'))),
    'Moderate or heavy sleet showers':
        _(ra(u('umiarkowane opady śniegu z deszczem'))),
    'Light snow showers': _(ra(u('słabe opady śniegu'))),
    'Moderate or heavy snow showers': _(ra(u('umiarkowane opady śniegu'))),
    'Light showers of ice pellets': _(ra(u('słabe opady śniegu ziarnistego'))),
    'Moderate or heavy showers of ice pellets':
        _(ra(u('umiarkowane opady śniegu ziarnistego'))),
    'Patchy light rain in area with thunder': _(ra(u('burza'))),
    'Moderate or heavy rain in area with thunder': _(ra(u('burza'))),
    'Patchy light snow in area with thunder': _(ra(u('burza śnieżna'))),
    'Moderate or heavy snow in area with thunder': _(ra(u('burza śnieżna'))),
}

open_weather_map = {
    "thunderstorm with light rain":_(ra(u("burza z lekkimi opadami deszczu"))),
    "thunderstorm with rain":_(ra(u("burza z opadami deszczu"))),
    "thunderstorm with heavy rain":_(ra(u("burza z intensywnymi opadami deszczu"))),
    "light thunderstorm":_(ra(u("lekka burza"))),
    "thunderstorm":_(ra(u("burza"))),
    "heavy thunderstorm":_(ra(u("silna burza"))),
    "ragged thunderstorm":_(ra(u("burza"))),
    "thunderstorm with light drizzle":_(ra(u("burza z lekką mżawką"))),
    "thunderstorm with drizzle":_(ra(u("burza z mżawka"))),
    "thunderstorm with heavy drizzle":_(ra(u("burza z intensywną mżawką"))),
    "light intensity drizzle":_(ra(u("lekka mżawka"))),
    "drizzle":_(ra(u("mżawka"))),
    "heavy intensity drizzle":_(ra(u("intensywna mżawka"))),
    "light intensity drizzle rain":_(ra(u("lekkie opady drobnego deszczu"))),
    "drizzle rain":_(ra(u("deszcz przechodzący w mżawkę"))),
    "heavy intensity drizzle rain":_(ra(u("intensywny deszcz przechodzący w mżawkę"))),
    "shower rain and drizzle":_(ra(u("intensywny deszcz przechodzący w mżawkę"))),
    "heavy shower rain and drizzle":_(ra(u("intensywny deszcz przechodzący w mżawkę"))),
    "shower drizzle":_(ra(u("silna mżawka"))),
    "light rain":_(ra(u("lekki deszcz"))),
    "moderate rain":_(ra(u("umiarkowany deszcz"))),
    "heavy intensity rain":_(ra(u("intensywny deszcz"))),
    "very heavy rain":_(ra(u("bardzo silny deszcz"))),
    "extreme rain":_(ra(u("ulewa"))),
    "freezing rain":_(ra(u("marznący deszcz"))),
    "light intensity shower rain":_(ra(u("przelotne ulewy"))),
    "shower rain":_(ra(u("deszcz"))),
    "heavy intensity shower rain":_(ra(u("deszcz"))),
    "ragged shower rain":_(ra(u("deszcz"))),
    "light snow":_(ra(u("lekkie opady śniegu"))),
    "snow":_(ra(u("śnieg"))),
    "heavy snow":_(ra(u("mocne opady śniegu"))),
    "sleet":_(ra(u("deszcz ze śniegem"))),
    "shower sleet":_(ra(u("deszcz ze śniegem"))),
    "light rain and snow":_(ra(u("deszcz ze śniegem"))),
    "rain and snow":_(ra(u("deszcz ze śniegem"))),
    "light shower snow":_(ra(u("deszcz ze śniegem"))),
    "shower snow":_(ra(u("śnieżyca"))),
    "heavy shower snow":_(ra(u("śnieżyca"))),
    "mist":_(ra(u("zamglenia"))),
    "smoke":_(ra(u("smog"))),
    "haze":_(ra(u("zamglenia"))),
    "sand, dust whirls":_(ra(u("zamieć piaskowa"))),
    "fog":_(ra(u("mgła"))),
    "sand":_(ra(u("mgła"))),
    "dust":_(ra(u("mgła"))),
    "volcanic ash":_(ra(u("mgła"))),
    "squalls":_(ra(u("mgła"))),
    "tornado":_(ra(u("mgła"))),
    "clear sky":_(ra(u("bezchmurnie"))),
    "few clouds":_(ra(u("lekkie zachmurzenie"))),
    "scattered clouds":_(ra(u("zachmurzenie umiarkowane"))),
    "broken clouds":_(ra(u("pochmurno z przejaśnieniami"))),
    "overcast clouds":_(ra(u("pochmurno"))),
    "tornado":_(ra(u("tornado"))),
    "tropical storm":_(ra(u("burza tropikalna"))),
    "hurricane":_(ra(u("huragan"))),
    "cold":_(ra(u("chłodno"))),
    "hot":_(ra(u("gorąco"))),
    "windy":_(ra(u("wietrznie"))),
    "hail":_(ra(u("grad"))),
    "calm":_(ra(u("spokojnie"))),
    "light breeze":_(ra(u("lekka bryza"))),
    "gentle breeze":_(ra(u("delikatna bryza"))),
    "moderate breeze":_(ra(u("umiarkowana bryza"))),
    "fresh breeze":_(ra(u("świeża bryza"))),
    "strong breeze":_(ra(u("silna bryza"))),
    "high wind, near gale":_(ra(u("bardzo silny wiatr"))),
    "gale":_(ra(u("wichura"))),
    "severe gale":_(ra(u("silna wichura"))),
    "storm":_(ra(u("sztorm"))),
    "violent storm":_(ra(u("gwałtowny sztorm"))),
    "hurricane":_(ra(u("huragan"))),
}

# to be removed from code
source = 'zrodlo'

pl = PLMicrosoft()

read_number = pl.read_number
read_pressure = pl.read_pressure
read_percent = pl.read_percent
read_temperature = pl.read_temperature
read_speed = pl.read_speed
read_degrees = pl.read_degrees
read_direction = pl.read_direction
read_datetime = pl.read_datetime
read_callsign = pl.read_callsign
