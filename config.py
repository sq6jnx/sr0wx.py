#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# *********
# config.py
# *********
#
# ==================
# Core configuration
# ==================
#
# This file stores whole configuration of SR0WX. It's simple and
# self-explanatory, but... here is documentation:
#
# Variable ``lang`` defines which language files will be used by whole
# application. ``"pl"`` for Polish, ``"en"`` for English, ``"kli"`` for
# Klingon ;)
lang = "pl"

# Here you can select your subtone, both as channel name (``'A'`` to
# ``'AL'``) and frequency in Hz. Please remember about decimal dot (``.``)
# ie. 88.8.
#
# Set ``playCTCSS = True`` if you want CTCSS even if modules didn't asked for it.
CTCSS = 88.8
playCTCSS = False
#CTCSS = None

# CTCSS volume should be greater than 0.0 (which is silence); ``pygame``
# will accept any decimal value, default 0.1

CTCSSVolume = 0.1

# Here you can define serial port for PTT (default is ``None``) and baud rate.
# Refer your TRX manual.

serialPort = None
#serialPort     = '/dev/ttyS0'
#serialBaudRate = 9600

# Welcome and Goodbye messages. Quite easy, too. It's just a playlist of files
# which will be played as a welcome message. Remember -- don't write ``.ogg``
# here. Remember (2): these files *must* be in catalogue named after
# ``lang`` value.
#
# Remember (3), that there is also special makrer, ``"_"`` for 0.5 second long
# silence.
#
# If you'd like to generate cw automatically you can do it with ``cw("text")``
# but the following line must be uncommented. You don't have to know what does
# it mean until it works ;)

from lib.cw import *

helloMsg = [cw('test'), "tu","eksperymentalna","automatyczna_stacja_pogodowa",\
    "sp6yre",cw("sp6yre"),"lokator","jo81ld"]
goodbyeMsg = ["_","tu","sp6yre",cw("sp6yre")]

# There is a bug, probably in pygame, which makes cw played twice.
# There is also a workaround of this problem

playHalf = 1

# This one informes which modules will be used by SR0WX. These *must*
# be stored as an array (possibly as a tuple, too).
modules = ["metar","taf","meteoalarm","imgw_hydro","sunriset"]

# =====================
# Modules configuration
# =====================
#
# Here we have setting for SR0WX modules. Every module has its configuration
# dictionary.
#
# Now dirty trick to make config reading easy:

class m:
    pass

# -----
# debug
# -----

debug = m()

# debug module is used for showing/logging debug informations.
# There are several debug levels (see bug#30):
# * [9] Critical/Fatal, the program can't possible continue, normally the user lost it.
# * [6] Error, something really wrong, used data can be corrupt, but you can be lucky.
# * [3] Warning, this is not right, I can continue, but please have a look.
# * [1] Hint/Information, i like to say something, but I don't expect you to listen.
# * [0] Debug, all information only interesting for programmers (verbose).
#
# Normally all debug informations are stored (level 0), but you can change it here:

debug.writeLevel = 0

# You can also show on screen debug infos of specified level (or higher):

debug.showLevel  = 1

# ------
# metar
# ------
metar = m()
#
# Gee. It's so easy, that it's make me smile when I think about writing about
# it. OK. First of all you have to find ICAO code of airport in your
# neightbourhood. You can find it on
# http://www.airlinecodes.co.uk/aptcodesearch.asp
#
# If you are lucky you will be able to download your ``metar`` weather info
# from NOAA's servers[#]_. If not, you can always check your weather on
# http://www.aviador.es/metar.php , but ``metar`` module is not yet able to
# download you weather report from there.
#
# .. [#] http://weather.noaa.gov/weather/metar.shtml

metar.ICAOAirportCode= "EPWR"

# Here you *have to* define your timezone. You can find yours by:
# >>> import pytz
# >>> print pytz.all_timezones

metar.timeZone= "Europe/Warsaw"
# Here you can define which informations will be retrieved from
# METAR report. If you want SR0WX to read it, type ``1`` after variable's
# name, if not, type ``0``.
#
# Please remember, that when line starts with ``##`` (double hash) option is
# not yet implemented. Remember also, that if report doesn't mention
# about, ie. humidity, it won't be mentioned.

metar.temperatureCelsius= 1
## metar.temperatureFahrenheit = 0
metar.dewPointCelsius= 0
## metar.dewPointFahrenheit   = 0
metar.windSpeedMPS         = 1 
## metar.windSpeedMiPH"    = 0
metar.windStrengthBeaufort = 0
metar.windDirectionDegrees = 1
metar.windDirectionCompass = 1
metar.visibilityKilometers = 1
metar.visibilityMiles        = 0
metar.humidity             = 1
metar.pressureHPa          = 1
## metar.pressureMMHg      = 1
## metar.weather              = 1
## metar.clouds               = 1
metar.lastUpdate           = 1

# Some people find three-letters long wind direction, here you can shorten
# it to max 2 last letters (default=False, which is "do not shorten")

metar.shortenWindDirection=   True

# ---------
# taf
# ---------
taf = m()

taf.forecastingPeriod = 3 # in hours, keep this value small but >1
taf.ICAOAirportCode= "EPWR"
taf.temperatureCelsius = 0 # not implemented, but must be here!
## taf.temperatureFahrenheit = 0
##taf.dewPointCelsius= 0
## taf.dewPointFahrenheit   = 0
taf.windSpeedMPS         = 1 
## metar.windSpeedMiPH"    = 0
##taf.windStrengthBeaufort = 0
taf.windDirectionDegrees = 1
##taf.windDirectionCompass = 1
taf.visibilityKilometers = 1
##taf.visibilityMiles        = 0
##taf.humidity             = 1
taf.pressureHPa          = 0 # not implemented, but must be here!
## taf.pressureMMHg      = 1
taf.weather              = 1
taf.skyConditions               = 1
taf.lastUpdate           = 1

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
# 483: Łódzkie                  479: Śląskie
# 482: Świętokrzyskie           477: Dolnośląskie 
# 485: Kujawsko-pomorskie       487: Lubelskie
# 474: Lubuskie                 480: Małopolskie 
# 489: Mazowieckie              478: Opolskie
# 481: Podkarpackie             488: Podlaskie
# 476: Pomorskie                486: Warmińsko-mazurskie 
# 484: Wielkopolskie            475: Zachodniopomorskie 

meteoalarm.region = 477 
meteoalarm.showToday = 1
meteoalarm.showTomorrow = 1

# ----------------
# zagrozenia-imgw -- not yet implemented!
# ----------------

zagrozenia_imgw = m()

# IMGW dzieli kraj na regiony i podaje zagrożenia w podziale na te regiony.
# Niestety, podział na regiony jest niejednoznaczny, regiony dzielą się, etc.
# Poniżej lista regionów oraz ich oznaczeń używanych zarówno przez IMGW jak 
# i na potrzeby tego modułu.
#
# Regiony nadmorskie:
# "bs": Zatoka Pomorska, in. strefa brzegowa woj. zachodniopomorskiego
# "sz": Zalew Szczeciński 
# "bg": strefa brzegowa wojewodztwa pomorskiego
# "26": całe wybrzeże, region nieużywany, opcja niepolecana
#
# Miasta
# "sc": Szczecin                     "by": Bydgoszcz
# "gd": trójmiasto                   "wa": Warszawa
# "ol": Olszyn                       "wr": Wrocław
# "bi": Białystok                    "oe": Opole
# "gw": Gorzów Wielkopolski          "kr": Kraków
# "zg": Zielona Góra                 "lo": Łódź
# "po": Poznań
# 
# Województwa:
# "zp": zachodniopomorskiego
# "pm": pomorskiego",
# "wm": warminsko_mazurskiego",
# "pd": podlaskiego",
# "lb": lubuskiego",
# "wp": "wojewodztwa wielkopolskiego",
# "kp": "wojewodztwa kujawsko_pomorskiego",
# "mz": "wojewodztwa mazowieckiego",
# "lu": "wojewodztwa lubuskiego",
# "ld": "wojewodztwa lodzkiego",
# "ds": "wojewodztwa dolnoslaskiego",
# "op": "wojewodztwa opolskiego",
# "sl": "wojewodztwa slaskiego",
# "sk": "wojewodztwa swietokrzyskiego",
# "ma": "wojewodztwa malopolskiego",
# "pk": "wojewodztwa podkarpackiego",
#
# "kk": "kotliny_klodzkiej",
# "su": "przedgorza_sudeckiego_i_sudetow",
# "eb": "powiatu_elblaskiego"

# -----------
# imgw-hydro
# -----------

imgw_hydro = m()

# Nie chce mi się pisać po angielsku. Nie ma to chyba większego 
# sensu, z racji tego, że IMGW podaje informacje hydro tylko dla
# regionu Polski. Dane są pobierane ze strony 
# [http://pogodynka.pl/hydrobiuletyn.php], jednak nazwy wodowskazów
# są z pewnych względów zmodyfikowane na potrzeby modułu.
#
# Najlepszym sposobem na sprawdzenie jakie wodowskazy są dostępne
# jest wpisanie jakiejś niepoprawnej nazwy wodowskazu (np. potocznej 
# nazwy określającej część ciała poniżej pleców), np:
# 
# imgw_hydro.wodowskazy = ['uda']
#
# moduł zwróci błąd, ale wyświetli dostępne nazwy. Nazwy wodowskazów
# powinny być w formie Pythonowej tablicy.

imgw_hydro.wodowskazy = ['chalupki', 'miedonia', 'kozle', 'krapkowice', 'opole', 'ujscie_nysy', 'trestno', 'brzeg_dolny', 'malczyce', 'scinawa', 'glogow', 'klodzko', 'skorogoszcz', 'jarnoltow', 'piatnica', 'osetno', 'zagan', 'zgorzelec', 'gubin']

imgw_hydro.podajStan = 1
imgw_hydro.podajTendencje = 0 

# -------------
# imgw_prognoza
# -------------

imgw_prognoza = m()

imgw_prognoza.url = """http://www.pogodynka.pl/miasto.php?miasto=Wroc%B3aw&gmina=Wroc%B3aw&powiat=Wroc%B3aw&wojewodztwo=dolno%B6l%B1skie&czas=&model="""

imgw_prognoza.podajStanPogody = 1
imgw_prognoza.czasPrognozy    = 3

imgw_prognoza.podajZjawiska   = 1
imgw_prognoza.podajTemp       = 1
imgw_prognoza.podajTempOdcz   = 1
imgw_prognoza.podajCisnHpa    = 1
imgw_prognoza.podajSileWiatru = 1
imgw_prognoza.podajKierWiatru = 1

# -------------
# sunRiseSet
# -------------

sunriset = m()

# As stated in Sun.py (around line 230):
# Eastern longitude positive, Western longitude negative       
# Northern latitude positive, Southern latitude negative 
sunriset.location = (17.03, 51.110) # Wroclaw
sunriset.timeZone = "Europe/Warsaw"

sunriset.giveSunRiseAfterSunRise = 1
sunriset.giveSunSetAfterSunSet = 1
sunriset.giveDayLength = 1

# Na ile godzin przed wschodem/zachodem podajemy godzinę wschodu/zachodu (-1 = zawsze)
sunriset.hoursBeforeSunRise = 3 
sunriset.hoursBeforeSunSet = 3 

# -------------
# gopr_lawiny
# -------------

gopr_lawiny = m()

# GOPR podzielił Polskę na następujące regiony:
# 1 - Karkonosze
# 2 - Śnieżnik Kłodzki
# 3 - Babia Góra
# 4 - Pieniny
# 5 - Bieszczady
#
# Niestety, dla Śnieżnika Kłodzkiego odsyła na stronę Horska Sluzba CZ, dla Pienin nie podaje komunikatów wogóle.
# Zagrożenia dla Tatr podaje TOPR.

gopr_lawiny.region = 1
gopr_lawiny.podajTendencje = 1
gopr_lawiny.podajWystawe = 1   # not yet implemented

# That's all for now.
