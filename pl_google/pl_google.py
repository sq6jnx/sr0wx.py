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

from six import u
import datetime
from functools import wraps

# #################
# CAUTION!
# DIRTY HACK BELOW
# #################
#
# for now `pyliczba` is not a Python module in terms like you can `pip` it or
# something. It's even impossibru to import it, because it does not have an
# `__init__  file. And the main file isn't even called `pyliczba`!
#
# ... so we create one...

import os

pyliczba_init = os.sep.join(('pl_google', 'pyliczba', '__init__.py'))
with open(pyliczba_init, 'w') as f:
    f.write("from .kwotaslownie import *")

# It works!

import pyliczba


def remove_accents(function):
    """unicodedata.normalize() doesn't work with ł and Ł"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)\
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
    return wrapper

def _(text):
    return text.replace(' ', '_')


@remove_accents
def read_number(value, units=None):
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
def read_pressure(value):
    hPa = ["hektopaskal", "hektopaskale", "hektopaskali"]
    return read_number(value, hPa)

@remove_accents
def read_percent(value):
    percent = ["procent", "procent", "procent"]
    return read_number(value, percent)

@remove_accents
def read_temperature(value):
    C = [_(u("stopień Celsjusza")), _("stopnie Celsjusza"), _("stopni Celsjusza")]
    return read_number(value, C)

@remove_accents
def read_speed(no, unit='mps'):
    units = {
        'mps': [_(u("metr na sekundę")), _(u("metry na sekundę")),
                _(u("metrów na sekundę"))],
        'kmph': [_(u("kilometr na godzinę")), _(u("kilometry na godzinę")),
                 _(u("kilometrów na godzinę"))]
    }
    return read_number(no, units[unit])

@remove_accents
def read_degrees(value):
    deg = [u("stopień"), u("stopnie"), u("stopni")]
    return read_number(value, deg)


@remove_accents
def read_direction(value, short=False):
    directions = {
        "N": (u("północno"),   u("północny")),
        "E": (u("wschodnio"),  u("wschodni")),
        "W": (u("zachodnio"),  u("zachodni")),
        "S": (u("południowo"), u("południowy")),
    }
    if short:
        value = value[-2:]
    return '-'.join([directions[d][0 if i < 0 else 1]
                     for i, d in enumerate(value, -len(value)+1)])


@remove_accents
def read_datetime(value, in_fmt, out_fmt):
    MONTHS = [u(""),
              u("stycznia"), u("lutego"), u("marca"), u("kwietnia"), u("maja"),
              u("czerwca"), u("lipca"), u("sierpnia"), u("września"),
              u("października"), u("listopada"), u("grudnia"),
    ]

    DAYS_N0 = [u(""), u(""), u("dwudziestego"), u("trzydziestego"),]
    DAYS_N = [u(""),
              u("pierwszego"), u("drugiego"), u("trzeciego"), u("czwartego"),
              u("piątego"), u("szóstego"), u("siódmego"), u("ósmego"),
              u("dziewiątego"), u("dziesiątego"), u("jedenastego"),
              u("dwunastego"), u("trzynastego"), u("czternastego"),
              u("piętnastego"), u("szesnastego"), u("siedemnastego"),
              u("osiemnastego"), u("dziewiętnastego"),
    ]
    HOURS = [u("zero"), u("pierwsza"), u("druga"), u("trzecia"), u("czwarta"),
             u("piąta"), u("szósta"), u("siódma"), u("ósma"), u("dziewiąta"),
             u("dziesiąta"), u("jedenasta"), u("dwunasta"), u("trzynasta"),
             u("czternasta"), u("piętnasta"), u("szesnasta"),
             u("siedemnasta"), u("osiemnasta"), u("dziewiętnasta"),
             u("dwudziesta"),
    ]

    _, tm_mon, tm_mday, tm_hour, tm_min, _, _, _, _ = \
        datetime.datetime.strptime(value, in_fmt).timetuple()
    #import pdb; pdb.set_trace()
    retval = []
    for word in out_fmt.split(" "):
        if word == '%d':  # Day of the month
            if tm_mday <= 20:
                retval.append(DAYS_N[tm_mday])
            else:
                retval.append(DAYS_N0[tm_mday //10])
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
def read_callsign(value):
    # literowanie polskie wg. "Krótkofalarstwo i radiokomunikacja - poradnik",
    # Łukasz Komsta SQ8QED, Wydawnictwa Komunikacji i Łączności Warszawa, 2001,
    # str. 130 (z drobnymi modyfikacjami fonetycznymi)
    LETTERS = {
        'a': u('adam'), 'b': u('barbara'), 'c': u('celina'), 'd': u('dorota'),
        'e': u('edward'), 'f': u('franciszek'), 'g': u('gustaw'),
        'h': u('henryk'), 'i': u('irena'), 'j': u('józef'), 'k': u('karol'),
        'l': u('ludwik'), 'm': u('marek'), 'n': u('natalia'), 'o': u('olga'),
        'p': u('paweł'), 'q': u('quebec'), 'r': u('roman'), 's': u('stefan'),
        't': u('tadeusz'), 'u': u('urszula'), 'v': u('violetta'),
        'w': u('wacław'), 'x': u('xawery'), 'y': u('ypsilon'), 'z': u('zygmunt'),
        '/': u('łamane'),
    }
    retval = []
    for char in value.lower():
        try:
            retval.append(LETTERS[char])
        except KeyError:
            try:
                retval.append(read_number(int(char)))
            except ValueError:
                raise ValueError("\"%s\" is not a element of callsign", char)
    return ' '.join(retval)




# set of deprecated functions

def cardinal(no, units=[u"",u"",u""]):
    """Zamienia liczbę zapisaną cyframi na zapis słowny, opcjonalnie z jednostkami
w odpowiednim przypadku. Obsługuje liczby ujemne."""
    if no<0:
        rv = (u"minus " + pyliczba.cosslownie(-no, units)).replace(u("jeden tysiąc"), u("tysiąc"), 1)
    else:
        rv = pyliczba.cosslownie(no, units).replace(u("jeden tysiąc"), u("tysiąc"), 1)
    return removeDiacritics(rv)

def removeDiacritics(text, remove_spaces=False):
    rv = text\
        .replace(u("ą"), "a")\
        .replace(u("ć"), "c")\
        .replace(u("ę"), "e")\
        .replace(u("ł"), "l")\
        .replace(u("ń"), "n")\
        .replace(u("ó"), "o")\
        .replace(u("ś"), "s")\
        .replace(u("ź"), "z")\
        .replace(u("ż"), "z")

    if not remove_spaces:
        return rv
    else:
        return rv.replace(' ', '_')

def readISODT(ISODT):
    _rv = ()
    _, m, d, hh, mm, _ = (int(ISODT[0:4]), int(ISODT[5:7]), int(ISODT[8:10]),
                          int(ISODT[11:13]), int(ISODT[14:16]),
                          int(ISODT[17:19]))

    # miesiąc
    _M = [u(w) for w in ["", "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
          "lipca", "sierpnia", "września", "października", "listopada",
          "grudnia"]]
    Mslownie = _M[m]

    # dzień
    _j = [u(w) for w in ["", "pierwszego", "drugiego", "trzeciego", "czwartego", "piątego",
          "szóstego", "siódmego", "ósmego", "dziewiątego", "dziesiątego",
          "jedenastego", "dwunastego", "trzynastego", "czternastego",
          "piętnastego", "szesnastego", "siedemnastego", "osiemnastego",
          "dziewiętnastego"]]
    _d = ["", "", "dwudziestego", "trzydziestego"]

    if d < 20:
        Dslownie = _j[d]
    else:
        Dslownie = " ".join((_d[d/10], _j[d % 10]))

    _j = [u(w) for word in ["zero", "pierwsza", "druga", "trzecia", "czwarta", "piąta",
          "szósta", "siódma", "ósma", "dziewiąta", "dziesiąta", "jedenasta",
          "dwunasta", "trzynasta", "czternasta", "piętnasta", "szesnasta",
          "siedemnasta", "osiemnasta", "dziewiętnasta"]]

    if hh < 20:
        HHslownie = _j[hh]
    elif hh == 20:
        HHslownie = "dwudziesta"
    else:
        HHslownie = " ".join(("dwudziesta", _j[hh % 10]))

    MMslownie = cardinal(mm).replace("zero", "zero_zero")

    return removeDiacritics(" ".join((Dslownie, Mslownie, "z_godziny", HHslownie, MMslownie)))


# TODO: this methods sucks. Replace with proper datetime use
def readISODate(ISODate):
    _rv = ()
    _, m, d, _, _, _ = (int(ISODate[0:4]), int(ISODate[5:7]),
                        int(ISODate[8:10]), int(ISODate[11:13]),
                        int(ISODate[14:16]), int(ISODate[17:19]))

    # miesiąc
    _M = [u(w) for w in ("", "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
          "lipca", "sierpnia", "września", "października", "listopada",
          "grudnia")]
    Mslownie = _M[m]

    # dzień
    _j = [u(w) for w in ("", "pierwszego", "drugiego", "trzeciego", "czwartego", "piątego",
          "szóstego", "siódmego", "ósmego", "dziewiątego", "dziesiątego",
          "jedenastego", "dwunastego", "trzynastego", "czternastego",
          "piętnastego", "szesnastego", "siedemnastego", "osiemnastego",
          "dziewiętnastego")]
    _d = ["", "", "dwudziestego", "trzydziestego"]

    if d < 20:
        Dslownie = _j[d]
    else:
        Dslownie = " ".join((_d[d/10], _j[d % 10]))

    return removeDiacritics(" ".join((Dslownie, Mslownie)))


# ##########################################
#
# module dependant words
# #############################################


# World Weather Online

wwo_weather_codes = {
    '113': u('bezchmurnie'),                                      # Clear/Sunny
    '116': u('częściowe zachmurzenie'),                           # Partly Cloudy
    '119': u('pochmurno'),                                        # Cloudy
    '122': u('zachmurzenie całkowite'),                           # Overcast
    '143': u('zamglenia'),                                        # Mist
    '176': u('lokalne przelotne opady deszczu'),                  # Patchy rain nearby
    '179': u('śnieg'),                                            # Patchy snow nearby
    '182': u('śnieg z deszczem'),                                 # Patchy sleet nearby
    '185': u('lokalna przelotna marznąca mżawka'),                # Patchy freezing drizzle nearby
    '200': u('lokalne burze'),                                    # Thundery outbreaks in nearby
    '227': u('zamieć śnieżna'),                                   # Blowing snow
    '230': u('zamieć śnieżna'),                                   # Blizzard
    '248': u('mgła'),                                             # Fog
    '260': u('marznąca mgła'),                                    # Freezing fog
    '263': u('mżawka'),                                           # Patchy light drizzle
    '266': u('mżawka'),                                           # Light drizzle
    '281': u('marznąca mżawka'),                                  # Freezing drizzle
    '284': u('marznąca mżawka'),                                  # Heavy freezing drizzle
    '293': u('lokalny słaby deszcz'),                             # Patchy light rain
    '296': u('słaby deszcz'),                                     # Light rain
    '299': u('przelotne opady deszczu'),                          # Moderate rain at times
    '302': u('umiarkowane opady deszczu'),                        # Moderate rain
    '305': u('przelotne ulewy'),                                  # Heavy rain at times
    '308': u('ulewy'),                                            # Heavy rain
    '311': u('słabe opady marznącego deszczu'),                   # Light freezing rain
    '314': u('umiarkowane opady marznącego deszczu'),             # Moderate or Heavy freezing rain
    '317': u('słabe opady śniegu z deszczem'),                    # Light sleet
    '320': u('umiarkowane lub ciężkie opady śniegu z deszczem'),  # Moderate or heavy sleet
    '323': u('słabe opady śniegu'),                               # Patchy light snow
    '326': u('słabe opady śniegu'),                               # Light snow
    '329': u('umiarkowane opady śniegu'),                         # Patchy moderate snow
    '332': u('umiarkowane opady śniegu'),                         # Moderate snow
    '335': u('opady śniegu'),                                     # Patchy heavy snow
    '338': u('intensywne_opady_sniegu'),                          # Heavy snow
    '350': u('grad'),                                             # Ice pellets
    '353': u('słabe przelotne opady deszczu'),                    # Light rain shower
    '356': u('przelotne opady deszczu'),                          # Moderate or heavy rain shower
    '359': u('ulewny deszcz'),                                    # Torrential rain shower
    '362': u('słabe opady śniegu z deszczem'),                    # Light sleet showers
    '365': u('umiarkowane opady śniegu z deszczem'),              # Moderate or heavy sleet showers
    '368': u('słabe opady śniegu'),                               # Light snow showers
    '371': u('umiarkowane opady śniegu'),                         # Moderate or heavy snow showers
    '374': u('słabe opady śniegu ziarnistego'),                   # Light showers of ice pellets
    '377': u('umiarkowane opady śniegu ziarnistego'),             # Moderate or heavy showers of ice pellets
    '386': u('burza'),                                            # Patchy light rain in area with thunder
    '389': u('burza'),                                            # Moderate or heavy rain in area with thunder
    '392': u('burza śnieżna'),                                    # Patchy light snow in area with thunder
    '395': u('burza śnieżna'),                                    # Moderate or heavy snow in area with thunder
}


# Units and grammar cases -- to be removed from code
C = ["stopien_celsjusza", "stopnie_celsjusza", "stopni_celsjusza"]
source = 'zrodlo'

deg = ["stopien", "stopnie", "stopni"]
directions = {
    "N": (u("północno "),   u("północny")),
    "E": (u("wschodnio "),  u("wschodni")),
    "W": (u("zachodnio "),  u("zachodni")),
    "S": (u("południowo "), u("południowy")),
}
MiPh = ["", "", ""]
hPa = ["hektopaskal", "hektopaskale", "hektopaskali"]
kmPh = ["kilometr_na_godzine", "kilometry_na_godzine", "kilometrow_na_godzine"]
mPs = ["metr_na_sekunde", "metry_na_sekunde", "metrow_na_sekunde"]
percent = ["procent", "procent", "procent"]
