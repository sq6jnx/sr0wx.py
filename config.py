#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# 

CTCSS = 88.8
playCTCSS = False
CTCSSVolume = 0.1
serialPort     = '/dev/ttyS0'
serialBaudRate = 9600

from lib.cw import *

lang = "pl_google"

pygameBug = 1

helloMsg = ["tu_eksperymentalna_automatyczna_stacja_pogodowa",\
    "sp6yre",]#"lokator","jo81ld"]
goodbyeMsg = ["_","tu_sp6yre",]

modules = ["imgw_podest", "y_weather"]

class m:
    pass

y_weather = m()
y_weather.zipcode = 526363
# it would be nice to give one ability to parse it via template engine
# http://wiki.python.org/moin/Templating
y_weather.template = """stan_pogody_z_dnia {PUB_DATE_HOUR} _ temperatura 
    {CURR_TEMP} wilgotnosc _ {HUMIDITY} 
    {CURRENT_CONDITION} _ kierunek_wiatru {WIND_DIR_NEWS} 
    {WIN_DIR_DEG} predkosc_wiatru {WIND_SPEED} _
    cisnienie {PRESSURE} {PRESSURE_TENDENTION}
    temperatura_odczuwalna {TEMP_WIND_CHILL}
    
    prognoza_na_nastepne piec godzin 
    {FORECAST0_CONDITION} temperatura_minimalna
    {FORECAST0_MIN_TEMP_SHORT} maksymalna {FORECAST0_MAX_TEMP} 
    
    _ nastepnie {FORECAST1_CONDITION} temperatura_minimalna
    {FORECAST1_MIN_TEMP_SHORT} maksymalna {FORECAST1_MAX_TEMP} 
    """


imgw_podest = m()

imgw_podest.wodowskazy = ["3.150160160"]

debug = m()
debug.writeLevel = None
debug.showLevel  = 0




# ----------
# meteoalarm
# ----------
meteoalarm = m()

# There are three things you should configure in meteoalarm module:
# region number, if module should show meteo awareness for today and
# and if it should show awareness for tommorow.
#
# Here is the list of region codes for Poland. You can find region
# numbers for other countries on www.meteoalarm.eu .
#
# PL011: Łódzkie                PL007: Śląskie
# PL010: Świętokrzyskie         PL005: Dolnośląskie 
# PL013: Kujawsko-pomorskie     PL015: Lubelskie
# PL002: Lubuskie               PL008: Małopolskie 
# PL001: Mazowieckie            PL007: Opolskie
# PL009: Podkarpackie           PL016: Podlaskie
# PL004: Pomorskie              PL014: Warmińsko-mazurskie 
# PL012: Wielkopolskie          PL003: Zachodniopomorskie 

meteoalarm.region = 'PL005'
meteoalarm.showToday = 1
meteoalarm.showTomorrow = 1
