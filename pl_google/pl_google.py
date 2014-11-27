# -*- coding: utf-8 -*-
#
#   Copyright 2009-2012, 2014 Michal Sadowski (sq6jnx at hamradio dot pl)
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

# *********
# pl_google/pl_google.py
# *********
#
# This file defines language dependent functions and variables. Probably
# this is the most important file in whole package.
#
# ============
# Requirements
# ============
#
# This package *may* import some other packages, it is up to you (and your
# needs).
#
# BUT: this package **must** define the following functions:
# * ``direction()`` which "translates" direction given by letters into
#    its word representation
# * ``removeDiacritics()`` which removes diacritics
# * ``readISODT()`` "translates" date and time into its word representation
# * ``cardinal()``  which changes numbers into words (1 -> one)
#
# As you probably can see all of these functions are language-dependent.
#
# ======================
# Implementation example
# ======================
#
# Here is implementation example for Polish language. Polish is interesting
# because it uses diacritics and 7 (seven) grammatical cases[#]_ (among many
# other features ;)
#
# .. [*] http://pl.wikipedia.org/wiki/Przypadek#Przypadki_w_j.C4.99zyku_polskim
#
# There *may* be some issues with diacritics because there are many
# implementations [#]. For example, Windows uses its own coding system while
# Linux uses UTF-8 (I think). And, when moving files (which are named with
# diacritics) from one platform to another results may (will) be
# unexpectable.
#
# .. [#] http://pl.wikipedia.org/wiki/Kodowanie_polskich_znak%C3%B3w
#
# =====================
# Polish dictionary
# =====================
#
# Concept: to make things clear, easy to debug and to
# internationalize. Program *doesn't use words* but *filenames*.
# So, if somewhere in program variable's value or function returns
# ie. *windy* it should be regarded as a *filename*, ``windy.ogg``.
#
# Beware too short words, it will be like machine gun rapid fire or
# will sound like a cyborg from old, cheap sci-fi movie. IMO the good way
# is to record longer phrases, like *"the temperature is"*, save it as
# ``the_temperature_is.ogg`` and use it's filename (``the_temperature_is``)
# as a return value.
#
# This dictionary is used by all SR0WX modules.

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
if not os.path.isfile(pyliczba_init):
    with open(pyliczba_init, 'w') as f:
        f.write("from kwotaslownie import *")

# It works!

from six import u
import pyliczba

fake_gettext = lambda(s): s
_ = fake_gettext

# Units and grammar cases
hrs = ["", "godziny", "godzin"]
hPa = ["hektopaskal", "hektopaskale", "hektopaskali"]
percent = ["procent", "procent", "procent"]
mPs = ["metr_na_sekunde", "metry_na_sekunde", "metrow_na_sekunde"]
kmPh = ["kilometr_na_godzine", "kilometry_na_godzine", "kilometrow_na_godzine"]
MiPh = ["", "", ""] # miles per hour -- not used
windStrength = "sila_wiatru"
deg = ["stopien", "stopnie", "stopni"]
C = ["stopien_celsjusza", "stopnie_celsjusza", "stopni_celsjusza"]
km = ["kilometr", "kilometry", "kilometrow"]
mns = ["minuta", "minuty", "minut"]
tendention = ['tendencja_spadkowa', '', 'tendencja_wzrostowa']


# We need also local names for directions to convert two- or three letters
# long wind direction into words (first is used as prefix, second as suffix):
directions = {"N": (u("północno "),   u("północny")),
              "E": (u("wschodnio "),  u("wschodni")),
              "W": (u("zachodnio "),  u("zachodni")),
              "S": (u("południowo "), u("południowy")),
              }


# As you remember, ``cardinal()`` must be defined, this is the function which
# will be used by SR0WX modules. This functions was also written by dowgrid,
# modified by me. (Is function's name proper?)
def cardinal(no, units=[u"",u"",u""]):
    """Zamienia liczbę zapisaną cyframi na zapis słowny, opcjonalnie z jednostkami
w odpowiednim przypadku. Obsługuje liczby ujemne."""
    if no<0:
        rv = (u"minus " + pyliczba.cosslownie(-no, units)).replace(u("jeden tysiąc"), u("tysiąc"), 1)
    else:
        rv = pyliczba.cosslownie(no, units).replace(u("jeden tysiąc"), u("tysiąc"), 1)
    return removeDiacritics(rv)

# This one tiny simply removes diactrics (lower case only). This function
# must be defined even if your language doesn't use diactrics (like English),
# for example as a simple ``return text``.

# TODO: replace with pyliczba ends here


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

# The last one changes ISO structured date time into word representation.
# It doesn't return year value.

# TODO: this methods sucks. Replace with proper datetime use
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


def readHour(dt):
    return removeDiacritics(readISODT('0000-00-00 '
                                      + str(dt.hour).rjust(2, '0')
                                      + ':'
                                      + str(dt.minute).rjust(2, '0')
                                      + ':00'))


def readHourLen(hour):
    ss = hour.seconds
    hh = ss/3600
    mm = (ss-hh*3600)/60
    return removeDiacritics(" ".join((cardinal(hh, hrs),
                                      cardinal(mm, mns))))


def readCallsign(call):
    rv = ''
    for c in call.lower():
        if c in 'abcdefghijklmnopqrstuvwxyz':
            rv = rv + c + ' '
        elif c in '0123456789':
            rv = rv + removeDiacritics(cardinal(int(c))) + ' '
        elif c == '/':
            rv = rv + 'lamane '
    return rv


def readFraction(number, precision):
    try:
        integer, fraction = str(round(number, precision)).split('.')
    except TypeError:
        return None
        pass

    rv = ' '.join((cardinal(int(integer)), comma))

    while fraction[0] == '0':
        rv = ' '.join((rv, cardinal(0)),)
        fraction.pop(0)

    rv = ' '.join((rv, cardinal(int(fraction)),))
    return rv

# ##########################################
#
# module dependant words
# #############################################

class m:
    pass


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

river = 'rzeka'
station = 'wodowskaz'

comma = 'przecinek'
uSiph = 'mikrosiwerta_na_godzine'
radiation_level = 'promieniowanie_tla'
radiation_levels = ['w_normie', 'podwyzszone', 'wysokie']

source = 'zrodlo'
