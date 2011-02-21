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

#serialPort = None
serialPort     = '/dev/ttyS0'
serialBaudRate = 9600

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

# Pygame has a bug which effects in playing cw twice. set pygameBug=1

pygameBug = 1

helloMsg = ["tu","eksperymentalna","automatyczna_stacja_pogodowa",\
    "sp6yre",cw("sp6yre"),]#"lokator","jo81ld"]
goodbyeMsg = ["_","tu","sp6yre",cw("sp6yre qra jo81mc")]

# This one informes which modules will be used by SR0WX. These *must*
# be stored as an array
modules = ["metar","taf","meteoalarm","gopr_lawiny","hscr_laviny","sunriset", "imgw_podest"]
#modules = ["imgw_podest"]

# You can also start selected modules via commandline, ie:
# python sr0wx.py metar,taf,sunriset

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
# Normally all debug informations are stored (level 0), but you can change it here. Setting this to None is the most pythonic way to disable writing to file.

debug.writeLevel = None

# You can also show on screen debug infos of specified (or higher) level.
# What comes to stdout should be sent by cron.

debug.showLevel  = 0

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
metar.weather              = 1
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


# -----------
# imgw-podest
# -----------

imgw_podest = m()

imgw_podest.wodowskazy = [
'3.149180010',   # Nazwa: Krzyżanowice, rzeka: Odra
'3.149180020',   # Nazwa: Chałupki, rzeka: Odra
'3.149180030',   # Nazwa: Łaziska, rzeka: Olza
'3.149180060',   # Nazwa: Cieszyn, rzeka: Olza
'3.149180070',   # Nazwa: Cieszyn, rzeka: Olza-Młynówka
'3.149180130',   # Nazwa: Istebna, rzeka: Olza
'3.149180300',   # Nazwa: Olza, rzeka: Odra
'3.150150010',   # Nazwa: Mirsk, rzeka: Kwisa
'3.150150020',   # Nazwa: Mirsk, rzeka: Czarny Potok
'3.150150030',   # Nazwa: Jakuszyce, rzeka: Kamienna
'3.150150040',   # Nazwa: Barcinek, rzeka: Kamienica
'3.150150050',   # Nazwa: Piechowice, rzeka: Kamienna
'3.150150060',   # Nazwa: Pilchowice, rzeka: Bóbr
'3.150150070',   # Nazwa: Jelenia Góra, rzeka: Kamienna
'3.150150080',   # Nazwa: Jelenia Góra, rzeka: Bóbr
'3.150150090',   # Nazwa: Łomnica, rzeka: Łomnica
'3.150150100',   # Nazwa: Wojanów, rzeka: Bóbr
'3.150150110',   # Nazwa: Kowary, rzeka: Jedlica
'3.150150120',   # Nazwa: Bukówka, rzeka: Bóbr
'3.150150130',   # Nazwa: Błażkowa, rzeka: Bóbr
'3.150150190',   # Nazwa: Podgórzyn, rzeka: Podgórna
'3.150150200',   # Nazwa: Sosnówka, rzeka: Czerwonka
'3.150160010',   # Nazwa: Kamienna Góra, rzeka: Bóbr
'3.150160020',   # Nazwa: Świebodzice, rzeka: Pełcznica
'3.150160030',   # Nazwa: Chwaliszów, rzeka: Strzegomka
'3.150160040',   # Nazwa: Kudowa Zdrój - Zakrze, rzeka: Klikawa
'3.150160060',   # Nazwa: Jugowice, rzeka: Bystrzyca
'3.150160070',   # Nazwa: Lubachów, rzeka: Bystrzyca
'3.150160080',   # Nazwa: Tłumaczów, rzeka: Ścinawka
'3.150160090',   # Nazwa: Łazany, rzeka: Strzegomka
'3.150160100',   # Nazwa: Gorzuchów, rzeka: Ścinawka
'3.150160110',   # Nazwa: Szalejów Dolny, rzeka: Bystrzyca Dusznicka
'3.150160120',   # Nazwa: Krasków, rzeka: Bystrzyca
'3.150160130',   # Nazwa: Mościsko, rzeka: Piława
'3.150160140',   # Nazwa: Dzierżoniów, rzeka: Piława
'3.150160150',   # Nazwa: Bystrzyca Kłodzka , rzeka: Bystrzyca Łomnicka
'3.150160160',   # Nazwa: Mietków, rzeka: Bystrzyca
'3.150160170',   # Nazwa: Bystrzyca Kłodzka, rzeka: Nysa Kłodzka
'3.150160180',   # Nazwa: Kłodzko, rzeka: Nysa Kłodzka
'3.150160190',   # Nazwa: Międzylesie, rzeka: Nysa Kłodzka
'3.150160200',   # Nazwa: Żelazno, rzeka: Biała Lądecka
'3.150160210',   # Nazwa: Wilkanów, rzeka: Wilczka
'3.150160220',   # Nazwa: Bardo, rzeka: Nysa Kłodzka
'3.150160230',   # Nazwa: Lądek Zdrój, rzeka: Biała Lądecka
'3.150160250',   # Nazwa: Białobrzezie, rzeka: Ślęza
'3.150160270',   # Nazwa: Kamieniec Ząbkowicki, rzeka: Budzówka
'3.150160280',   # Nazwa: Borów, rzeka: Ślęza
'3.150160290',   # Nazwa: Gniechowice, rzeka: Czarna Woda
'3.150170010',   # Nazwa: Zborowice, rzeka: Oława
'3.150170030',   # Nazwa: Oława, rzeka: Oława
'3.150170040',   # Nazwa: Oława, rzeka: Odra
'3.150170050',   # Nazwa: Biała Nyska, rzeka: Biała Głuchołaska
'3.150170060',   # Nazwa: Nysa, rzeka: Nysa Kłodzka
'3.150170070',   # Nazwa: Głuchołazy, rzeka: Biała Głuchołaska
'3.150170090',   # Nazwa: Brzeg, rzeka: Odra
'3.150170100',   # Nazwa: Kopice, rzeka: Nysa Kłodzka
'3.150170110',   # Nazwa: Prudnik, rzeka: Prudnik
'3.150170120',   # Nazwa: Niemodlin, rzeka: Ścinawa Niemodlińska
'3.150170130',   # Nazwa: Ujście Nysy Kłodzkiej, rzeka: Odra
'3.150170140',   # Nazwa: Skorogoszcz, rzeka: Nysa Kłodzka
'3.150170150',   # Nazwa: Karłowice, rzeka: Stobrawa
'3.150170160',   # Nazwa: Branice, rzeka: Opawa
'3.150170170',   # Nazwa: Branice, rzeka: Opawa-Młynówka
'3.150170180',   # Nazwa: Racławice Śląskie, rzeka: Osobłoga
'3.150170220',   # Nazwa: Dobra, rzeka: Biała
'3.150170240',   # Nazwa: Krapkowice, rzeka: Odra
'3.150170290',   # Nazwa: Opole - Groszowice, rzeka: Odra
'3.150180020',   # Nazwa: Turawa, rzeka: Mała Panew
'3.150180030',   # Nazwa: Koźle, rzeka: Odra
'3.150180040',   # Nazwa: Bojanów, rzeka: Psina
'3.150180050',   # Nazwa: Ozimek, rzeka: Mała Panew
'3.150180060',   # Nazwa: Racibórz Miedonia, rzeka: Odra
'3.150180070',   # Nazwa: Lenartowice, rzeka: Kłodnica
'3.150180080',   # Nazwa: Grabówka, rzeka: Bierawka
'3.150180100',   # Nazwa: Staniszcze Wielkie, rzeka: Mała Panew
'3.150180110',   # Nazwa: Ruda Kozielska, rzeka: Ruda
'3.150180130',   # Nazwa: Rybnik Stodoły, rzeka: Ruda
'3.150180150',   # Nazwa: Pyskowice Dzierżno, rzeka: Kłodnica
'3.150180160',   # Nazwa: Pyskowice Dzierżno, rzeka: Drama
'3.150180170',   # Nazwa: Pyskowice, rzeka: Drama
'3.150180180',   # Nazwa: Gliwice-Łabędy, rzeka: Kłodnica
'3.150180190',   # Nazwa: Krupski Młyn, rzeka: Mała Panew
'3.150180220',   # Nazwa: Gliwice, rzeka: Kłodnica
'3.150180280',   # Nazwa: Gotartowice, rzeka: Ruda
'3.151150030',   # Nazwa: Iłowa, rzeka: Czerna Mała
'3.151150040',   # Nazwa: Nowogród Bobrzański, rzeka: Bóbr 
'3.151150050',   # Nazwa: Dobroszów Wielki, rzeka: Bóbr
'3.151150060',   # Nazwa: Leśna, rzeka: Kwisa
'3.151150070',   # Nazwa: Żagań , rzeka: Czerna Wielka
'3.151150080',   # Nazwa: Żagań, rzeka: Bóbr
'3.151150090',   # Nazwa: Łozy, rzeka: Kwisa
'3.151150100',   # Nazwa: Nowogrodziec, rzeka: Kwisa
'3.151150110',   # Nazwa: Gryfów Śląski, rzeka: Kwisa
'3.151150120',   # Nazwa: Szprotawa, rzeka: Bóbr
'3.151150130',   # Nazwa: Szprotawa, rzeka: Szprotawa
'3.151150140',   # Nazwa: Dąbrowa Bolesławiecka, rzeka: Bóbr
'3.151150150',   # Nazwa: Nowa Sól, rzeka: Odra
'3.151150160',   # Nazwa: Zagrodno, rzeka: Skora
'3.151150170',   # Nazwa: Świerzawa, rzeka: Kaczawa
'3.151150180',   # Nazwa: Chojnów, rzeka: Skora
'3.151160020',   # Nazwa: Rzymówka, rzeka: Kaczawa
'3.151160040',   # Nazwa: Bukowna, rzeka: Czarna Woda
'3.151160050',   # Nazwa: Dunino, rzeka: Kaczawa
'3.151160060',   # Nazwa: Głogów, rzeka: Odra
'3.151160070',   # Nazwa: Winnica, rzeka: Nysa Szalona
'3.151160080',   # Nazwa: Rzeszotary, rzeka: Czarna Woda
'3.151160090',   # Nazwa: Jawor, rzeka: Nysa Szalona
'3.151160100',   # Nazwa: Piątnica, rzeka: Kaczawa
'3.151160120',   # Nazwa: Prochowice, rzeka: Kaczawa
'3.151160130',   # Nazwa: Ścinawa, rzeka: Odra
'3.151160140',   # Nazwa: Osetno, rzeka: Barycz
'3.151160150',   # Nazwa: Malczyce, rzeka: Odra
'3.151160160',   # Nazwa: Rydzyna, rzeka: Polski Rów
'3.151160170',   # Nazwa: Brzeg Dolny, rzeka: Odra
'3.151160180',   # Nazwa: Bogdaszowice, rzeka: Strzegomka
'3.151160190',   # Nazwa: Jarnołtów, rzeka: Bystrzyca
'3.151160200',   # Nazwa: Korzeńsko, rzeka: Orla
'3.151160220',   # Nazwa: Kanclerzowice, rzeka: Sąsiecznica
'3.151160230',   # Nazwa: Ślęża, rzeka: Ślęza
'3.151170010',   # Nazwa: Krzyżanowice, rzeka: Widawa
'3.151170030',   # Nazwa: Trestno, rzeka: Odra
'3.151170040',   # Nazwa: Łąki, rzeka: Barycz
'3.151170050',   # Nazwa: Zbytowa, rzeka: Widawa
'3.151170060',   # Nazwa: Bogdaj, rzeka: Polska Woda
'3.151170070',   # Nazwa: Odolanów, rzeka: Barycz
'3.151170080',   # Nazwa: Odolanów, rzeka: Kuroch
'3.151170090',   # Nazwa: Namyslów, rzeka: Widawa
'3.152150020',   # Nazwa: Stary Raduszec, rzeka: Bóbr 
'3.152150050',   # Nazwa: Nietków, rzeka: Odra
'3.152150130',   # Nazwa: Cigacice, rzeka: Odra
]

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

# -------------
# hscr_laviny
# -------------

hscr_laviny = m()

# HS CR gives avalanche awarenesses for two regions: Krkonoše and Jeseníky.
# As a reference we use a little bit strange shorthand for these, so any
# string which matches "Krkonoše" or "Jeseníky" is valid, i.e. "Krk" or "Jesen".
# 

#hscr_laviny.region = "Krkono"
hscr_laviny.region = "Jesen"
hscr_laviny.giveTendention = 1
hscr_laviny.giveExposition = 1   # not yet implemented

# That's all for now.

