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
#modules = ["metar","taf","meteoalarm"]#,"gopr_lawiny","hscr_laviny","sunriset"]
modules = ["imgw_podest"]

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
    '3.149180020', # Nazwa: Chałupki, rzeka: Odra
    '3.150160180', # Nazwa: Kłodzko, rzeka: Nysa Kłodzka
    '3.150170120', # Nazwa: Niemodlin, rzeka: Ścinawa Niemodlińska
    '3.150170130', # Nazwa: Ujście Nysy Kłodzkiej, rzeka: Odra
    '3.150170130', # Nazwa: Ujście Nysy Kłodzkiej, rzeka: Odra
    '3.150170140', # Nazwa: Skorogoszcz, rzeka: Nysa Kłodzka
    '3.150170240', # Nazwa: Krapkowice, rzeka: Odra
    '3.150170290', # Nazwa: Opole - Groszowice, rzeka: Odra
    '3.150180030', # Nazwa: Koźle, rzeka: Odra
    '3.150180060', # Nazwa: Racibórz Miedonia, rzeka: Odra
    '3.151150070', # Nazwa: Żagań , rzeka: Czerna Wielka
    '3.151150080', # Nazwa: Żagań, rzeka: Bóbr
    '3.151160060', # Nazwa: Głogów, rzeka: Odra
    '3.151160100', # Nazwa: Piątnica, rzeka: Kaczawa
    '3.151160130', # Nazwa: Ścinawa, rzeka: Odra
    '3.151160140', # Nazwa: Osetno, rzeka: Barycz
    '3.151160150', # Nazwa: Malczyce, rzeka: Odra
    '3.151160170', # Nazwa: Brzeg Dolny, rzeka: Odra
    '3.151160190', # Nazwa: Jarnołtów, rzeka: Bystrzyca
    '3.151170030', # Nazwa: Trestno, rzeka: Odra
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

#imgw_podest.wodowskazy = [
#'10.153190040',   # Nazwa: Bągart, rzeka: Dzierzgoń
#'10.153200030',   # Nazwa: Kalisty, rzeka: Pasłęka
#'10.153200040',   # Nazwa: Tomaryny, rzeka: Pasłęka
#'10.153200070',   # Nazwa: Olsztyn, rzeka: Łyna
#'10.153200090',   # Nazwa: Szypry, rzeka: None
#'10.154190010',   # Nazwa: Nowy Dwór Gdański, rzeka: Święta
#'10.154190020',   # Nazwa: Tujsk, rzeka: Szkarpawa
#'10.154190030',   # Nazwa: Osłonka, rzeka: None
#'10.154190040',   # Nazwa: Dolna Kępa, rzeka: Nogat
#'10.154190050',   # Nazwa: Nowe Batorowo, rzeka: None
#'10.154190060',   # Nazwa: Elbląg, rzeka: Elbląg
#'10.154190080',   # Nazwa: Żukowo, rzeka: None
#'10.154190090',   # Nazwa: Tolkmicko, rzeka: None
#'10.154190100',   # Nazwa: Pasłęk, rzeka: Wąska
#'10.154190130',   # Nazwa: Nowa Pasłęka, rzeka: None
#'10.154190140',   # Nazwa: Braniewo, rzeka: Pasłęka
#'10.154190150',   # Nazwa: Pierzchały, rzeka: Jezioro Pierzchalski
#'10.154190160',   # Nazwa: Pierzchały, rzeka: Jezioro Pierzchalski
#'10.154190170',   # Nazwa: Łozy, rzeka: Pasłęka
#'10.154200010',   # Nazwa: Bornity, rzeka: Wałsza
#'10.154200020',   # Nazwa: Krosno, rzeka: Drwęca Warmińska
#'10.154200030',   # Nazwa: Smolajny, rzeka: Łyna
#'10.154210010',   # Nazwa: Sępopol, rzeka: Łyna
#'10.154210020',   # Nazwa: Prosna, rzeka: Guber
#'10.154210060',   # Nazwa: Przystań, rzeka: None
#'10.154210070',   # Nazwa: Węgorzewo, rzeka: Węgorapa
#'10.154210080',   # Nazwa: Prynowo, rzeka: Węgorapa
#'10.154210090',   # Nazwa: Giżycko, rzeka: Kanał Giżycki
#'10.154210100',   # Nazwa: Mieduniszki, rzeka: Węgorapa
#'10.154220010',   # Nazwa: Banie Mazurskie, rzeka: Gołdapa
#'10.154220040',   # Nazwa: Gołdap, rzeka: Gołdapa
#'10.154220050',   # Nazwa: Jurkiszki, rzeka: Jarka
#'11.152190030',   # Nazwa: Włocławek, rzeka: Wisła
#'11.152190050',   # Nazwa: Kwiatkówek, rzeka: Bzura
#'11.152190100',   # Nazwa: Bielawy, rzeka: Mroga
#'11.152190120',   # Nazwa: Kępa Polska, rzeka: Wisła
#'11.152200010',   # Nazwa: Kęszyce, rzeka: Rawka
#'11.152200030',   # Nazwa: Wyszogród, rzeka: Wisła
#'11.152200050',   # Nazwa: Żuków, rzeka: Bzura
#'11.152200090',   # Nazwa: Krubice, rzeka: Utrata
#'11.152200110',   # Nazwa: Modlin, rzeka: Wisła
#'11.153180140',   # Nazwa: Elgiszewo, rzeka: Drwęca
#'11.153190050',   # Nazwa: Brodnica, rzeka: Drwęca
#'11.153190090',   # Nazwa: Nowe Miasto Lubawskie, rzeka: Drwęca
#'11.153190120',   # Nazwa: Rodzone, rzeka: Drwęca
#'11.153190150',   # Nazwa: Lidzbark, rzeka: Wel
#'11.153190170',   # Nazwa: Ostróda, rzeka: None
#'1.149210110',   # Nazwa: Krosno, rzeka: Wisłok
#'1.149210120',   # Nazwa: Godowa, rzeka: Stobnica
#'1.149210130',   # Nazwa: Żarnowa, rzeka: Wisłok
#'1.149210140',   # Nazwa: Iskrzynia, rzeka: Morwawa
#'1.149210150',   # Nazwa: Puławy, rzeka: Wisłok
#'1.149210160',   # Nazwa: Sieniawa, rzeka: Wisłok
#'1.149220010',   # Nazwa: Nowosielce, rzeka: Pielnica
#'1.149220020',   # Nazwa: Szczawne, rzeka: Osława
#'1.149220030',   # Nazwa: Olchowce, rzeka: San
#'1.149220040',   # Nazwa: Dynów, rzeka: San
#'1.149220050',   # Nazwa: Zagórz, rzeka: Osława
#'1.149220060',   # Nazwa: Lesko, rzeka: San
#'1.149220070',   # Nazwa: Hoczew, rzeka: Hoczewka
#'1.149220080',   # Nazwa: Cisna, rzeka: Solinka
#'1.149220100',   # Nazwa: Terka, rzeka: Solinka
#'1.149220110',   # Nazwa: Kalnica, rzeka: Wetlina
#'1.149220130',   # Nazwa: Zatwarnica, rzeka: San
#'1.149220140',   # Nazwa: Polana, rzeka: Czarny
#'1.149220150',   # Nazwa: Dwernik, rzeka: San
#'1.149220160',   # Nazwa: Rybotycze, rzeka: Wiar
#'1.149220180',   # Nazwa: Stuposiany, rzeka: Wołosaty
#'1.149220190',   # Nazwa: Przemyśl, rzeka: San
#'1.149220200',   # Nazwa: Krówniki, rzeka: Wiar
#'1.149220210',   # Nazwa: Nienowice, rzeka: Wisznia
#'1.150210210',   # Nazwa: Radomyśl, rzeka: San
#'1.150220010',   # Nazwa: Rzeszów, rzeka: Wisłok
#'1.150220020',   # Nazwa: Ruda Jastkowska, rzeka: Bukowa
#'1.150220030',   # Nazwa: Nisko, rzeka: San
#'1.150220040',   # Nazwa: Sarzyna, rzeka: Trzebosnica
#'1.150220050',   # Nazwa: Harasiuki, rzeka: Tanew
#'1.150220060',   # Nazwa: Gorliczyna, rzeka: Mleczka
#'1.150220070',   # Nazwa: Rzuchów, rzeka: San
#'1.150220080',   # Nazwa: Tryńcza, rzeka: Wisłok
#'1.150220090',   # Nazwa: Leżachów, rzeka: San
#'1.150220100',   # Nazwa: Jarosław, rzeka: San
#'1.150220110',   # Nazwa: Biłgoraj, rzeka: Biała Łada
#'1.150220130',   # Nazwa: Zapałów, rzeka: Lubaczówka
#'1.150220140',   # Nazwa: Charytany, rzeka: Szkło
#'1.150220160',   # Nazwa: Osuchy, rzeka: Tanew
#'12.153170120',   # Nazwa: Tuchola, rzeka: Brda
#'12.153170140',   # Nazwa: Smukała, rzeka: Brda
#'12.153180010',   # Nazwa: Czarna Woda, rzeka: Wda
#'12.153180020',   # Nazwa: Fordon, rzeka: Wisła
#'12.153180030',   # Nazwa: Bożepole, rzeka: Wierzyca
#'12.153180060',   # Nazwa: Krąplewice, rzeka: Wda
#'12.153180080',   # Nazwa: Chełmno, rzeka: Wisła
#'12.153180090',   # Nazwa: Toruń, rzeka: Wisła
#'12.153180100',   # Nazwa: Grudziądz, rzeka: Wisła
#'12.153180110',   # Nazwa: Brody Pomorskie, rzeka: Wierzyca
#'12.154180150',   # Nazwa: Tczew, rzeka: Wisła
#'12.154180190',   # Nazwa: Przegalina, rzeka: Wisła
#'12.154180200',   # Nazwa: Świbno, rzeka: Wisła
#'12.154180210',   # Nazwa: Ujście Wisły, rzeka: Wisła
#'12.154180220',   # Nazwa: Gdańska Głowa, rzeka: Wisła
#'13.153160020',   # Nazwa: Tychówko, rzeka: Parsęta
#'13.153180120',   # Nazwa: Hel, rzeka: None
#'13.154150010',   # Nazwa: Trzebiatów, rzeka: Rega
#'13.154150030',   # Nazwa: Kołobrzeg, rzeka: Morze Bałtyckie
#'13.154150040',   # Nazwa: Bardy, rzeka: Parsęta
#'13.154150050',   # Nazwa: Białogard, rzeka: Parsęta
#'13.154160020',   # Nazwa: Białogórzyno, rzeka: Radew
#'13.154160070',   # Nazwa: Stary Kraków, rzeka: Wieprza
#'13.154160110',   # Nazwa: Ustka, rzeka: None
#'13.154160120',   # Nazwa: Korzybie, rzeka: Wieprza
#'13.154160140',   # Nazwa: Charnowo, rzeka: Słupia
#'13.154170010',   # Nazwa: Słupsk, rzeka: Słupia
#'13.154170060',   # Nazwa: Smołdzino, rzeka: Łupawa
#'13.154170080',   # Nazwa: Łupawa, rzeka: Łupawa
#'13.154170100',   # Nazwa: Łeba, rzeka: None
#'13.154170120',   # Nazwa: Soszyca, rzeka: Słupia
#'13.154170160',   # Nazwa: Lębork, rzeka: Łeba
#'13.154180020',   # Nazwa: Miłoszewo, rzeka: Łeba
#'13.154180060',   # Nazwa: Goręczyno, rzeka: Radunia
#'13.154180080',   # Nazwa: Wejherowo, rzeka: Reda
#'13.154180090',   # Nazwa: Puck, rzeka: None
#'13.154180100',   # Nazwa: Władysławowo, rzeka: None
#'13.154180120',   # Nazwa: Gdynia, rzeka: None
#'13.154180130',   # Nazwa: Juszkowo, rzeka: Radunia
#'13.154180140',   # Nazwa: Gdańsk, rzeka: None
#'13.154180160',   # Nazwa: Sobieszewo, rzeka: Martwa Wisła
#'13.154180170',   # Nazwa: Wiślina, rzeka: Motława
#'13.154180180',   # Nazwa: Suchy Dąb, rzeka: Motława
#'13.156150050',   # Nazwa: Resko, rzeka: Rega
#'14.152140010',   # Nazwa: Bielinek, rzeka: Odra
#'14.152140020',   # Nazwa: Gozdowice, rzeka: Odra
#'14.152140060',   # Nazwa: Kostrzyn, rzeka: Odra
#'14.153140010',   # Nazwa: Świnoujście, rzeka: None
#'14.153140020',   # Nazwa: Widuchowa, rzeka: Odra
#'14.153140030',   # Nazwa: Gryfino, rzeka: Odra
#'14.153140040',   # Nazwa: Trzebież, rzeka: None
#'14.153140050',   # Nazwa: Szczecin, rzeka: Odra
#'14.153140060',   # Nazwa: Wolin, rzeka: None
#'14.153140070',   # Nazwa: Dziwnów, rzeka: Dziwna
#'14.153140090',   # Nazwa: Goleniów, rzeka: Ina
#'14.153140190',   # Nazwa: Szczecin Podjuchy, rzeka: Regalica
#'14.153150010',   # Nazwa: Stargard Szczeciński, rzeka: Ina
#'2.149180080',   # Nazwa: Drogomyśl, rzeka: Wisła
#'2.149180090',   # Nazwa: Borki Mizerów, rzeka: Pszczynka 
#'2.149180100',   # Nazwa: Skoczów, rzeka: Wisła
#'2.149180110',   # Nazwa: Ustroń Obłaziec, rzeka: Wisła
#'2.149180120',   # Nazwa: Górki Wielkie, rzeka: Brennica 
#'2.149180160',   # Nazwa: Wisła Czarne, rzeka: Wisła
#'2.149180180',   # Nazwa: Wisła Czarne, rzeka: Biała Wisełka
#'2.149180200',   # Nazwa: Wisła Czarne, rzeka: Czarna Wisełka
#'2.149180210',   # Nazwa: Zabrzeg, rzeka: Wisła
#'2.149180220',   # Nazwa: Pszczyna, rzeka: Pszczynka
#'2.149180250',   # Nazwa: Czechowice Dziedzice, rzeka: Iłowica
#'2.149190010',   # Nazwa: Czechowice-Bestwina, rzeka: Biała
#'2.149190020',   # Nazwa: Kamesznica, rzeka: Bystra
#'2.149190040',   # Nazwa: Ujsoły, rzeka: WodaUjsolska
#'2.149190050',   # Nazwa: Rajcza, rzeka: Soła
#'2.149190060',   # Nazwa: Jawiszowice, rzeka: Wisła
#'2.149190070',   # Nazwa: Łodygowice, rzeka: Żylica
#'2.149190080',   # Nazwa: Cięcina, rzeka: Soła
#'2.149190090',   # Nazwa: Żabnica, rzeka: Zabniczanka
#'2.149190100',   # Nazwa: Żywiec, rzeka: Soła
#'2.149190120',   # Nazwa: Czaniec (Kobiernice), rzeka: Soła
#'2.149190140',   # Nazwa: Łękawica, rzeka: Łękawka
#'2.149190150',   # Nazwa: Pewel Mała, rzeka: Koszarawa
#'2.149190160',   # Nazwa: Rudze, rzeka: Wieprzówka
#'2.149190170',   # Nazwa: Zator, rzeka: Skawa
#'2.149190180',   # Nazwa: Wadowice, rzeka: Skawa
#'2.149190200',   # Nazwa: Sucha Beskidzka, rzeka: Stryszawka
#'2.149190210',   # Nazwa: Sucha Beskidzka, rzeka: Skawa
#'2.149190220',   # Nazwa: Skawica Dolna, rzeka: Skawica
#'2.149190230',   # Nazwa: Czernichów-Prom, rzeka: Wisła
#'2.149190260',   # Nazwa: Osielec, rzeka: Skawa
#'2.149190270',   # Nazwa: Radziszów, rzeka: Skawinka
#'2.149190280',   # Nazwa: Koniówka, rzeka: Czarny Dunajec
#'2.149190290',   # Nazwa: Jordanów, rzeka: Skawa
#'2.149190300',   # Nazwa: Kościelisko-Kiry, rzeka: Potok Kościeliski
#'2.149190310',   # Nazwa: Stróża, rzeka: Raba
#'2.149190340',   # Nazwa: Rabka, rzeka: Raba
#'2.149190350',   # Nazwa: Krzczonów, rzeka: Krzczonówka
#'2.149190360',   # Nazwa: Ludźmierz, rzeka: Lepietnica
#'2.149190370',   # Nazwa: Lubień, rzeka: Lubienka
#'2.149190380',   # Nazwa: Zakopane Harenda, rzeka: Cicha Woda
#'2.149190390',   # Nazwa: Ludźmierz, rzeka: Wielki Rogoźnik
#'2.149200010',   # Nazwa: Poronin, rzeka: Poroniec
#'2.149200020',   # Nazwa: Szaflary, rzeka: Biały Dunajec
#'2.149200030',   # Nazwa: Nowy Targ, rzeka: Czarny Dunajec
#'2.149200040',   # Nazwa: Kasinka Mała, rzeka: Raba
#'2.149200050',   # Nazwa: Nowy Targ Kowaniec, rzeka: Dunajec
#'2.149200060',   # Nazwa: Mszana Dolna, rzeka: Raba
#'2.149200080',   # Nazwa: Mszana Dolna, rzeka: Mszanka
#'2.149200090',   # Nazwa: Dobczyce, rzeka: Raba
#'2.149200100',   # Nazwa: Łysa Polana, rzeka: Białka
#'2.149200110',   # Nazwa: Trybsz, rzeka: Białka
#'2.149200120',   # Nazwa: Niedzica, rzeka: Niedziczanka
#'2.149200130',   # Nazwa: Stradomka, rzeka: Stradomka
#'2.149200140',   # Nazwa: Sromowce Wyżne, rzeka: Dunajec
#'2.149200150',   # Nazwa: Tylmanowa, rzeka: Ochotnica
#'2.149200160',   # Nazwa: Krościenko, rzeka: Dunajec
#'2.149200170',   # Nazwa: Proszówki, rzeka: Raba
#'2.149200190',   # Nazwa: Gołkowice, rzeka: Dunajec
#'2.149200200',   # Nazwa: Jakubkowice, rzeka: Łososina
#'2.149200220',   # Nazwa: Stary Sącz, rzeka: Poprad
#'2.149200230',   # Nazwa: Czchów, rzeka: Dunajec
#'2.149200240',   # Nazwa: Nowy Sącz, rzeka: Dunajec
#'2.149200250',   # Nazwa: Nowy Sącz, rzeka: Kamienica
#'2.149200260',   # Nazwa: Nowy Sącz, rzeka: Łubinka
#'2.149200270',   # Nazwa: Łabowa, rzeka: Kamienica
#'2.149200280',   # Nazwa: Zgłobice, rzeka: Dunajec
#'2.149200290',   # Nazwa: Muszyna, rzeka: Poprad
#'2.149200310',   # Nazwa: Grybów, rzeka: Biała Tarnowska
#'2.149200320',   # Nazwa: Koszyce Wielkie, rzeka: Biała Tarnowska
#'2.149200330',   # Nazwa: Ciężkowice, rzeka: Biała Tarnowska
#'2.149200360',   # Nazwa: Lipnica Murowana, rzeka: Uszwica
#'2.149200370',   # Nazwa: Okocim, rzeka: Uszwica
#'2.149210010',   # Nazwa: Ropa, rzeka: Ropa
#'2.149210030',   # Nazwa: Klęczany, rzeka: Ropa
#'2.149210040',   # Nazwa: Łabuzie, rzeka: Wisłoka
#'2.149210050',   # Nazwa: Krajowice, rzeka: Wisłoka
#'2.149210060',   # Nazwa: Topoliny, rzeka: Ropa
#'2.149210070',   # Nazwa: Żółków, rzeka: Wisłoka
#'2.149210080',   # Nazwa: Jasło, rzeka: Jasiołka
#'2.149210090',   # Nazwa: Krempna-Kotań, rzeka: Wisłoka
#'2.149210100',   # Nazwa: Zboiska, rzeka: Jasiołka
#'2.150180270',   # Nazwa: Kozłowa Góra, rzeka: Brynica
#'2.150190010',   # Nazwa: Brynica, rzeka: Brynica
#'2.150190060',   # Nazwa: Bojszowy, rzeka: Gostynka
#'2.150190070',   # Nazwa: Szabelnia, rzeka: Brynica
#'2.150190080',   # Nazwa: Radocha, rzeka: Czarna Przemsza
#'2.150190100',   # Nazwa: Niwka, rzeka: Biała Przemsza
#'2.150190120',   # Nazwa: Przeczyce, rzeka: Czarna Przemsza
#'2.150190140',   # Nazwa: Nowy Bieruń, rzeka: Wisła
#'2.150190160',   # Nazwa: Oświęcim, rzeka: Soła
#'2.150190170',   # Nazwa: Pustynia, rzeka: Wisła
#'2.150190180',   # Nazwa: Jeleń, rzeka: Przemsza
#'2.150190190',   # Nazwa: Piwoń, rzeka: Czarna Przemsza
#'2.150190210',   # Nazwa: Kuźnica Sulikowska, rzeka: Mitręga
#'2.150190260',   # Nazwa: Smolice, rzeka: Wisła
#'2.150190310',   # Nazwa: Balice, rzeka: Rudawa
#'2.150190330',   # Nazwa: Ojców, rzeka: Prądnik
#'2.150190340',   # Nazwa: Kraków-Bielany, rzeka: Wisła
#'2.150190360',   # Nazwa: Gromiec, rzeka: Wisła
#'2.150200010',   # Nazwa: Mniszek, rzeka: Biała Nida
#'2.150200020',   # Nazwa: Bocheniec, rzeka: Łososina
#'2.150200030',   # Nazwa: Brzegi, rzeka: Nida
#'2.150200040',   # Nazwa: Tokarnia, rzeka: Czarna Nida
#'2.150200050',   # Nazwa: Michałów, rzeka: Mierzawa
#'2.150200060',   # Nazwa: Sierosławice, rzeka: Wisła
#'2.150200070',   # Nazwa: Biskupice, rzeka: Szreniawa
#'2.150200080',   # Nazwa: Pińczów, rzeka: Nida
#'2.150200090',   # Nazwa: Słowik, rzeka: Bobrza
#'2.150200100',   # Nazwa: Popędzynka, rzeka: Wisła
#'2.150200120',   # Nazwa: Morawica, rzeka: Czarna Nida
#'2.150200140',   # Nazwa: Borzęcin, rzeka: Uszwica
#'2.150200150',   # Nazwa: Karsy, rzeka: Wisła
#'2.150200160',   # Nazwa: Daleszyce, rzeka: Czarna Nida
#'2.150200170',   # Nazwa: Żabno, rzeka: Dunajec
#'2.150210010',   # Nazwa: Raków, rzeka: Czarna Staszowska
#'2.150210020',   # Nazwa: Szczucin, rzeka: Wisła
#'2.150210030',   # Nazwa: Mocha, rzeka: Łagowica
#'2.150210060',   # Nazwa: Staszów, rzeka: Czarna Staszowska
#'2.150210070',   # Nazwa: Wampierzów, rzeka: Breń
#'2.150210100',   # Nazwa: Połaniec, rzeka: Czarna Staszowska
#'2.150210110',   # Nazwa: Głowaczowa, rzeka: Grabinianka
#'2.150210120',   # Nazwa: Mielec, rzeka: Wisłoka
#'2.150210130',   # Nazwa: Pustków, rzeka: Wisłoka
#'2.150210140',   # Nazwa: Brzeźnica, rzeka: Wielopolka
#'2.150210150',   # Nazwa: Koło, rzeka: Wisła
#'2.150210160',   # Nazwa: Koprzywnica, rzeka: Koprzywianka
#'2.150210170',   # Nazwa: Sandomierz, rzeka: Wisła
#'2.150210200',   # Nazwa: Grebów, rzeka: Łęg
#'3.149180010',   # Nazwa: Krzyżanowice, rzeka: Odra
#'3.149180020',   # Nazwa: Chałupki, rzeka: Odra
#'3.149180030',   # Nazwa: Łaziska, rzeka: Olza
#'3.149180060',   # Nazwa: Cieszyn, rzeka: Olza
#'3.149180070',   # Nazwa: Cieszyn, rzeka: Olza-Młynówka
#'3.149180130',   # Nazwa: Istebna, rzeka: Olza
#'3.149180300',   # Nazwa: Olza, rzeka: Odra
#'3.150150010',   # Nazwa: Mirsk, rzeka: Kwisa
#'3.150150020',   # Nazwa: Mirsk, rzeka: Czarny Potok
#'3.150150030',   # Nazwa: Jakuszyce, rzeka: Kamienna
#'3.150150040',   # Nazwa: Barcinek, rzeka: Kamienica
#'3.150150050',   # Nazwa: Piechowice, rzeka: Kamienna
#'3.150150060',   # Nazwa: Pilchowice, rzeka: Bóbr
#'3.150150070',   # Nazwa: Jelenia Góra, rzeka: Kamienna
#'3.150150080',   # Nazwa: Jelenia Góra, rzeka: Bóbr
#'3.150150090',   # Nazwa: Łomnica, rzeka: Łomnica
#'3.150150100',   # Nazwa: Wojanów, rzeka: Bóbr
#'3.150150110',   # Nazwa: Kowary, rzeka: Jedlica
#'3.150150120',   # Nazwa: Bukówka, rzeka: Bóbr
#'3.150150130',   # Nazwa: Błażkowa, rzeka: Bóbr
#'3.150150190',   # Nazwa: Podgórzyn, rzeka: Podgórna
#'3.150150200',   # Nazwa: Sosnówka, rzeka: Czerwonka
#'3.150160010',   # Nazwa: Kamienna Góra, rzeka: Bóbr
#'3.150160020',   # Nazwa: Świebodzice, rzeka: Pełcznica
#'3.150160030',   # Nazwa: Chwaliszów, rzeka: Strzegomka
#'3.150160040',   # Nazwa: Kudowa Zdrój - Zakrze, rzeka: Klikawa
#'3.150160060',   # Nazwa: Jugowice, rzeka: Bystrzyca
#'3.150160070',   # Nazwa: Lubachów, rzeka: Bystrzyca
#'3.150160080',   # Nazwa: Tłumaczów, rzeka: Ścinawka
#'3.150160090',   # Nazwa: Łazany, rzeka: Strzegomka
#'3.150160100',   # Nazwa: Gorzuchów, rzeka: Ścinawka
#'3.150160110',   # Nazwa: Szalejów Dolny, rzeka: Bystrzyca Dusznicka
#'3.150160120',   # Nazwa: Krasków, rzeka: Bystrzyca
#'3.150160130',   # Nazwa: Mościsko, rzeka: Piława
#'3.150160140',   # Nazwa: Dzierżoniów, rzeka: Piława
#'3.150160150',   # Nazwa: Bystrzyca Kłodzka , rzeka: Bystrzyca Łomnicka
#'3.150160160',   # Nazwa: Mietków, rzeka: Bystrzyca
#'3.150160170',   # Nazwa: Bystrzyca Kłodzka, rzeka: Nysa Kłodzka
#'3.150160180',   # Nazwa: Kłodzko, rzeka: Nysa Kłodzka
#'3.150160190',   # Nazwa: Międzylesie, rzeka: Nysa Kłodzka
#'3.150160200',   # Nazwa: Żelazno, rzeka: Biała Lądecka
#'3.150160210',   # Nazwa: Wilkanów, rzeka: Wilczka
#'3.150160220',   # Nazwa: Bardo, rzeka: Nysa Kłodzka
#'3.150160230',   # Nazwa: Lądek Zdrój, rzeka: Biała Lądecka
#'3.150160250',   # Nazwa: Białobrzezie, rzeka: Ślęza
#'3.150160270',   # Nazwa: Kamieniec Ząbkowicki, rzeka: Budzówka
#'3.150160280',   # Nazwa: Borów, rzeka: Ślęza
#'3.150160290',   # Nazwa: Gniechowice, rzeka: Czarna Woda
#'3.150170010',   # Nazwa: Zborowice, rzeka: Oława
#'3.150170030',   # Nazwa: Oława, rzeka: Oława
#'3.150170040',   # Nazwa: Oława, rzeka: Odra
#'3.150170050',   # Nazwa: Biała Nyska, rzeka: Biała Głuchołaska
#'3.150170060',   # Nazwa: Nysa, rzeka: Nysa Kłodzka
#'3.150170070',   # Nazwa: Głuchołazy, rzeka: Biała Głuchołaska
#'3.150170090',   # Nazwa: Brzeg, rzeka: Odra
#'3.150170100',   # Nazwa: Kopice, rzeka: Nysa Kłodzka
#'3.150170110',   # Nazwa: Prudnik, rzeka: Prudnik
#'3.150170120',   # Nazwa: Niemodlin, rzeka: Ścinawa Niemodlińska
#'3.150170130',   # Nazwa: Ujście Nysy Kłodzkiej, rzeka: Odra
#'3.150170140',   # Nazwa: Skorogoszcz, rzeka: Nysa Kłodzka
#'3.150170150',   # Nazwa: Karłowice, rzeka: Stobrawa
#'3.150170160',   # Nazwa: Branice, rzeka: Opawa
#'3.150170170',   # Nazwa: Branice, rzeka: Opawa-Młynówka
#'3.150170180',   # Nazwa: Racławice Śląskie, rzeka: Osobłoga
#'3.150170220',   # Nazwa: Dobra, rzeka: Biała
#'3.150170240',   # Nazwa: Krapkowice, rzeka: Odra
#'3.150170290',   # Nazwa: Opole - Groszowice, rzeka: Odra
#'3.150180020',   # Nazwa: Turawa, rzeka: Mała Panew
#'3.150180030',   # Nazwa: Koźle, rzeka: Odra
#'3.150180040',   # Nazwa: Bojanów, rzeka: Psina
#'3.150180050',   # Nazwa: Ozimek, rzeka: Mała Panew
#'3.150180060',   # Nazwa: Racibórz Miedonia, rzeka: Odra
#'3.150180070',   # Nazwa: Lenartowice, rzeka: Kłodnica
#'3.150180080',   # Nazwa: Grabówka, rzeka: Bierawka
#'3.150180100',   # Nazwa: Staniszcze Wielkie, rzeka: Mała Panew
#'3.150180110',   # Nazwa: Ruda Kozielska, rzeka: Ruda
#'3.150180130',   # Nazwa: Rybnik Stodoły, rzeka: Ruda
#'3.150180150',   # Nazwa: Pyskowice Dzierżno, rzeka: Kłodnica
#'3.150180160',   # Nazwa: Pyskowice Dzierżno, rzeka: Drama
#'3.150180170',   # Nazwa: Pyskowice, rzeka: Drama
#'3.150180180',   # Nazwa: Gliwice-Łabędy, rzeka: Kłodnica
#'3.150180190',   # Nazwa: Krupski Młyn, rzeka: Mała Panew
#'3.150180220',   # Nazwa: Gliwice, rzeka: Kłodnica
#'3.150180280',   # Nazwa: Gotartowice, rzeka: Ruda
#'3.151150030',   # Nazwa: Iłowa, rzeka: Czerna Mała
#'3.151150040',   # Nazwa: Nowogród Bobrzański, rzeka: Bóbr 
#'3.151150050',   # Nazwa: Dobroszów Wielki, rzeka: Bóbr
#'3.151150060',   # Nazwa: Leśna, rzeka: Kwisa
#'3.151150070',   # Nazwa: Żagań , rzeka: Czerna Wielka
#'3.151150080',   # Nazwa: Żagań, rzeka: Bóbr
#'3.151150090',   # Nazwa: Łozy, rzeka: Kwisa
#'3.151150100',   # Nazwa: Nowogrodziec, rzeka: Kwisa
#'3.151150110',   # Nazwa: Gryfów Śląski, rzeka: Kwisa
#'3.151150120',   # Nazwa: Szprotawa, rzeka: Bóbr
#'3.151150130',   # Nazwa: Szprotawa, rzeka: Szprotawa
#'3.151150140',   # Nazwa: Dąbrowa Bolesławiecka, rzeka: Bóbr
#'3.151150150',   # Nazwa: Nowa Sól, rzeka: Odra
#'3.151150160',   # Nazwa: Zagrodno, rzeka: Skora
#'3.151150170',   # Nazwa: Świerzawa, rzeka: Kaczawa
#'3.151150180',   # Nazwa: Chojnów, rzeka: Skora
#'3.151160020',   # Nazwa: Rzymówka, rzeka: Kaczawa
#'3.151160040',   # Nazwa: Bukowna, rzeka: Czarna Woda
#'3.151160050',   # Nazwa: Dunino, rzeka: Kaczawa
#'3.151160060',   # Nazwa: Głogów, rzeka: Odra
#'3.151160070',   # Nazwa: Winnica, rzeka: Nysa Szalona
#'3.151160080',   # Nazwa: Rzeszotary, rzeka: Czarna Woda
#'3.151160090',   # Nazwa: Jawor, rzeka: Nysa Szalona
#'3.151160100',   # Nazwa: Piątnica, rzeka: Kaczawa
#'3.151160120',   # Nazwa: Prochowice, rzeka: Kaczawa
#'3.151160130',   # Nazwa: Ścinawa, rzeka: Odra
#'3.151160140',   # Nazwa: Osetno, rzeka: Barycz
#'3.151160150',   # Nazwa: Malczyce, rzeka: Odra
#'3.151160160',   # Nazwa: Rydzyna, rzeka: Polski Rów
#'3.151160170',   # Nazwa: Brzeg Dolny, rzeka: Odra
#'3.151160180',   # Nazwa: Bogdaszowice, rzeka: Strzegomka
#'3.151160190',   # Nazwa: Jarnołtów, rzeka: Bystrzyca
#'3.151160200',   # Nazwa: Korzeńsko, rzeka: Orla
#'3.151160220',   # Nazwa: Kanclerzowice, rzeka: Sąsiecznica
#'3.151160230',   # Nazwa: Ślęża, rzeka: Ślęza
#'3.151170010',   # Nazwa: Krzyżanowice, rzeka: Widawa
#'3.151170030',   # Nazwa: Trestno, rzeka: Odra
#'3.151170040',   # Nazwa: Łąki, rzeka: Barycz
#'3.151170050',   # Nazwa: Zbytowa, rzeka: Widawa
#'3.151170060',   # Nazwa: Bogdaj, rzeka: Polska Woda
#'3.151170070',   # Nazwa: Odolanów, rzeka: Barycz
#'3.151170080',   # Nazwa: Odolanów, rzeka: Kuroch
#'3.151170090',   # Nazwa: Namyslów, rzeka: Widawa
#'3.152150020',   # Nazwa: Stary Raduszec, rzeka: Bóbr 
#'3.152150050',   # Nazwa: Nietków, rzeka: Odra
#'3.152150130',   # Nazwa: Cigacice, rzeka: Odra
#'4.150140010',   # Nazwa: Porajów, rzeka: Nysa Łużycka
#'4.150140020',   # Nazwa: Sieniawka, rzeka: Nysa Łużycka
#'4.150140030',   # Nazwa: Turoszów, rzeka: Miedzianka
#'4.151140010',   # Nazwa: Gubin, rzeka: Nysa Łużycka
#'4.151140020',   # Nazwa: Pleśno, rzeka: Lubsza
#'4.151140030',   # Nazwa: Przewoźniki, rzeka: Skroda
#'4.151140040',   # Nazwa: Przewóz, rzeka: Nysa Łużycka
#'4.151140050',   # Nazwa: Ręczyn, rzeka: Witka
#'4.151140060',   # Nazwa: Zgorzelec, rzeka: Nysa Łużycka
#'4.151150010',   # Nazwa: Zgorzelec, rzeka: Czerwona Woda
#'4.151150020',   # Nazwa: Ostróżno, rzeka: Witka
#'4.152140050',   # Nazwa: Słubice, rzeka: Odra
#'4.152140070',   # Nazwa: Kostrzyn, rzeka: Warta
#'4.152140090',   # Nazwa: Biała Góra, rzeka: Odra
#'4.152140130',   # Nazwa: Połęcko, rzeka: Odra
#'4.152150010',   # Nazwa: Świerkocin, rzeka: Warta
#'4.152150040',   # Nazwa: Gorzów Wielkopolski, rzeka: Warta
#'4.152150070',   # Nazwa: Borek, rzeka: Warta
#'4.152150080',   # Nazwa: Santok, rzeka: Warta
#'4.152150100',   # Nazwa: Bledzew, rzeka: Obra
#'4.152150110',   # Nazwa: Skwierzyna, rzeka: Warta
#'4.152150200',   # Nazwa: Międzychód, rzeka: Warta
#'4.152160050',   # Nazwa: Wronki  , rzeka: Warta
#'4.152160100',   # Nazwa: Oborniki , rzeka: Warta
#'4.152160110',   # Nazwa: Kowanówko, rzeka: Wełna
#'5.150240010',   # Nazwa: Strzyżów, rzeka: Bug
#'5.150240020',   # Nazwa: Kryłów, rzeka: Bug
#'5.151230040',   # Nazwa: Włodawa, rzeka: Bug
#'5.151230060',   # Nazwa: Dorohusk, rzeka: Bug
#'5.152210090',   # Nazwa: Wyszków, rzeka: Bug
#'5.152210120',   # Nazwa: Łochów, rzeka: Liwiec
#'5.152220010',   # Nazwa: Zaliwie-Piegawki, rzeka: Liwiec
#'5.152220050',   # Nazwa: Frankopol, rzeka: Bug
#'5.152220070',   # Nazwa: Brańsk, rzeka: Nurzec
#'5.152230070',   # Nazwa: Malowa Góra, rzeka: Krzna
#'5.152230080',   # Nazwa: Krzyczew, rzeka: Bug
#'6.150190280',   # Nazwa: Wąsosz, rzeka: Pilica
#'6.150190350',   # Nazwa: Januszewice, rzeka: Czarna Włoszczowska
#'6.150210040',   # Nazwa: Rzepin, rzeka: Świślina
#'6.150210080',   # Nazwa: Nietulisko Duże, rzeka: Świślina
#'6.150210090',   # Nazwa: Kunów, rzeka: Kamienna
#'6.150210190',   # Nazwa: Zawichost, rzeka: Wisła
#'6.150210220',   # Nazwa: Włochy, rzeka: Pokrzywianka
#'6.150220120',   # Nazwa: Zakłodzie, rzeka: Pór
#'6.150230010',   # Nazwa: Nielisz, rzeka: Wieprz
#'6.150230040',   # Nazwa: Krasnystaw, rzeka: Wieprz
#'6.150230080',   # Nazwa: Michalów, rzeka: Wieprz
#'6.151190080',   # Nazwa: Kłudzice, rzeka: Luciąża
#'6.151190090',   # Nazwa: Przedbórz, rzeka: Pilica
#'6.151190100',   # Nazwa: Sulejów, rzeka: Pilica
#'6.151190120',   # Nazwa: Dąbrowa, rzeka: Czarna Maleniecka
#'6.151200020',   # Nazwa: Spała, rzeka: Pilica
#'6.151200080',   # Nazwa: Odrzywół, rzeka: Drzewiczka
#'6.151200090',   # Nazwa: Nowe Miasto n. Pilicą, rzeka: Pilica
#'6.151200100',   # Nazwa: Bzin, rzeka: Kamienna
#'6.151200120',   # Nazwa: Białobrzegi, rzeka: Netta / Pilica
#'6.151210010',   # Nazwa: Wąchock, rzeka: Kamienna
#'6.151210020',   # Nazwa: Michałów, rzeka: Kamienna
#'6.151210040',   # Nazwa: Brody Iłżeckie, rzeka: Kamienna
#'6.151210050',   # Nazwa: Gusin, rzeka: Wisła
#'6.151210060',   # Nazwa: Rogożek, rzeka: Radomka
#'6.151210090',   # Nazwa: Czekarzewice, rzeka: Kamienna
#'6.151210120',   # Nazwa: Dęblin, rzeka: Wisła
#'6.151210190',   # Nazwa: Puławy, rzeka: Wisła
#'6.151220010',   # Nazwa: Kośmin, rzeka: Wieprz
#'6.151220080',   # Nazwa: Tchórzew, rzeka: Tyśmienica
#'6.151220090',   # Nazwa: Lubartów, rzeka: Wieprz
#'6.151220100',   # Nazwa: Sobianowice, rzeka: Bystrzyca
#'6.152210010',   # Nazwa: Warszawa, rzeka: Wisła
#'6.152210020',   # Nazwa: Piaseczno, rzeka: Jeziorka
#'6.152210070',   # Nazwa: Otwock - Wólka Mlądzka, rzeka: Świder
#'7.150180210',   # Nazwa: Niwki, rzeka: Liswarta
#'7.150190150',   # Nazwa: Poraj, rzeka: Warta
#'7.150190200',   # Nazwa: Lgota Nadwarcie, rzeka: Warta
#'7.150190240',   # Nazwa: Kręciwilk, rzeka: Warta
#'7.151170110',   # Nazwa: Bogusław, rzeka: Prosna
#'7.151180010',   # Nazwa: Ołobok , rzeka: Ołobok
#'7.151180020',   # Nazwa: Piwonice, rzeka: Prosna
#'7.151180030',   # Nazwa: Kuźnica Skakawska, rzeka: Niesób
#'7.151180040',   # Nazwa: Mirków, rzeka: Prosna
#'7.151180050',   # Nazwa: Dębe, rzeka: Swędrnia
#'7.151180060',   # Nazwa: Kraszewice, rzeka: Łużyca
#'7.151180070',   # Nazwa: Gorzów Śląski, rzeka: Prosna
#'7.151180080',   # Nazwa: Sieradz, rzeka: Warta
#'7.151180090',   # Nazwa: Niechmirów, rzeka: Oleśnica
#'7.151180100',   # Nazwa: Osjaków, rzeka: Warta
#'7.151180110',   # Nazwa: Uniejów, rzeka: Warta
#'7.151180120',   # Nazwa: Burzenin, rzeka: Warta
#'7.151180130',   # Nazwa: Działoszyn, rzeka: Warta
#'7.151180140',   # Nazwa: Podgórze, rzeka: Widawka
#'7.151180150',   # Nazwa: Widawa, rzeka: Nieciecz
#'7.151180160',   # Nazwa: Poddębice, rzeka: Ner
#'7.151180170',   # Nazwa: Rogóźno, rzeka: Widawka
#'7.151180180',   # Nazwa: Grabno, rzeka: Grabia
#'7.151190010',   # Nazwa: Kule, rzeka: Liswarta
#'7.151190020',   # Nazwa: Szczerców, rzeka: Widawka
#'7.151190030',   # Nazwa: Łask, rzeka: Grabia
#'7.151190040',   # Nazwa: Lutomiersk, rzeka: Ner
#'7.151190060',   # Nazwa: Bobry, rzeka: Warta
#'7.152160090',   # Nazwa: Kościan, rzeka: Kan. Kościański
#'7.152160130',   # Nazwa: Mosina, rzeka: Kan. Mosiński
#'7.152160140',   # Nazwa: Poznań Most Rocha, rzeka: Warta
#'7.152170010',   # Nazwa: Śrem, rzeka: Warta
#'7.152170060',   # Nazwa: Nowa Wieś Podgórna, rzeka: Warta
#'7.152170080',   # Nazwa: Pyzdry, rzeka: Warta
#'7.152170120',   # Nazwa: Samarzewo, rzeka: Wrześnica
#'7.152170130',   # Nazwa: Ląd, rzeka: Warta
#'7.152170150',   # Nazwa: Trąbczyn, rzeka: Czarna Struga
#'7.152180050',   # Nazwa: Sławsk, rzeka: Warta
#'7.152180060',   # Nazwa: Posoka, rzeka: Powa
#'7.152180110',   # Nazwa: Kościelec, rzeka: Kiełbaska
#'7.152180120',   # Nazwa: Koło, rzeka: Warta
#'7.152180140',   # Nazwa: Grzegorzew, rzeka: Rgilewka
#'7.152180150',   # Nazwa: Dąbie, rzeka: Ner
#'8.152150090',   # Nazwa: Santok, rzeka: Noteć
#'8.152150140',   # Nazwa: Gościmiec, rzeka: Noteć
#'8.152150190',   # Nazwa: Nowe Drezdenko, rzeka: Noteć
#'8.152150240',   # Nazwa: Drawiny, rzeka: Drawa
#'8.152160010',   # Nazwa: Krzyż, rzeka: Noteć
#'8.152160070',   # Nazwa: Czarnków, rzeka: Noteć
#'8.152180030',   # Nazwa: Pakość, rzeka: Noteć
#'8.153160170',   # Nazwa: Ujście, rzeka: Noteć
#'8.153160180',   # Nazwa: Piła, rzeka: Gwda
#'8.153160210',   # Nazwa: Ptusza, rzeka: Gwda
#'8.153170010',   # Nazwa: Białośliwie, rzeka: Noteć
#'8.153170040',   # Nazwa: Wyrzysk, rzeka: Łobżonka
#'8.153170100',   # Nazwa: Nakło Zachód , rzeka: Noteć
#'9.152200020',   # Nazwa: Trzciniec, rzeka: Wkra
#'9.152200120',   # Nazwa: Borkowo, rzeka: Wkra
#'9.152200130',   # Nazwa: Orzechowo, rzeka: Narew
#'9.152210030',   # Nazwa: Maków Mazowiecki, rzeka: Orzyc
#'9.152210040',   # Nazwa: Warszawa-Nadwilanówka, rzeka: Wisła
#'9.152210060',   # Nazwa: Zambski Kościelne, rzeka: Narew
#'9.152210100',   # Nazwa: Czarnowo, rzeka: Orz
#'9.152220080',   # Nazwa: Suraż, rzeka: Narew 
#'9.152230030',   # Nazwa: Chraboły, rzeka: Orlanka
#'9.152230040',   # Nazwa: Ploski, rzeka: Narew 
#'9.152230090',   # Nazwa: Narew, rzeka: Narew
#'9.152230100',   # Nazwa: Narewka, rzeka: Narewka
#'9.152230110',   # Nazwa: Bondary - Siemianówka, rzeka: Narew
#'9.152230120',   # Nazwa: Bondary - Siemianówka, rzeka: Narew
#'9.152230190',   # Nazwa: Białowieża, rzeka: Narewka
#'9.153200020',   # Nazwa: Szreńsk, rzeka: Mławka
#'9.153210070',   # Nazwa: Białobrzeg Bliższy, rzeka: Omulew
#'9.153210090',   # Nazwa: Ostrołęka, rzeka: Narew
#'9.153210120',   # Nazwa: Walery, rzeka: Rozoga
#'9.153210140',   # Nazwa: Szkwa, rzeka: Szkwa
#'9.153210170',   # Nazwa: Ptaki, rzeka: Pisa
#'9.153210180',   # Nazwa: Zaruzie, rzeka: Ruź
#'9.153210190',   # Nazwa: Pisz, rzeka: Pisa
#'9.153210200',   # Nazwa: Maldanin, rzeka: None
#'9.153210210',   # Nazwa: Nowogród, rzeka: Narew
#'9.153210220',   # Nazwa: Dobrylas, rzeka: Pisa
#'9.153220010',   # Nazwa: Piątnica-Łomża, rzeka: Narew
#'9.153220030',   # Nazwa: Gać, rzeka: Gać
#'9.153220050',   # Nazwa: Ełk, rzeka: None
#'9.153220060',   # Nazwa: Ełk, rzeka: Ełk
#'9.153220070',   # Nazwa: Wizna, rzeka: Narew
#'9.153220080',   # Nazwa: Prostki, rzeka: Ełk
#'9.153220090',   # Nazwa: Czachy, rzeka: Wissa
#'9.153220100',   # Nazwa: Burzyn, rzeka: Biebrza
#'9.153220130',   # Nazwa: Strękowa Góra, rzeka: Narew
#'9.153220140',   # Nazwa: Przechody, rzeka: Ełk-Kanał Rudzki
#'9.153220160',   # Nazwa: Osowiec, rzeka: Ełk-Kanał Rudzki
#'9.153220170',   # Nazwa: Osowiec, rzeka: Biebrza
#'9.153220180',   # Nazwa: Zawady, rzeka: Ślina
#'9.153220190',   # Nazwa: Rajgród, rzeka: Jezioro Rajgrodzkie
#'9.153220200',   # Nazwa: Rajgród, rzeka: Jegrznia
#'9.153220230',   # Nazwa: Kulesze Chobotki, rzeka: Nereśl
#'9.153220260',   # Nazwa: Dębowo, rzeka: Biebrza
#'9.153220270',   # Nazwa: Babino, rzeka: Narew 
#'9.153220280',   # Nazwa: Białobrzegi, rzeka: Netta
#'9.153230010',   # Nazwa: Fasty, rzeka: Supraśl
#'9.153230020',   # Nazwa: Karpowicze, rzeka: Brzozówka
#'9.153230060',   # Nazwa: Zawady, rzeka: Biała
#'9.153230070',   # Nazwa: Sztabin, rzeka: Biebrza
#'9.153230080',   # Nazwa: Sochonie, rzeka: Czarna
#'9.153230110',   # Nazwa: Supraśl, rzeka: Supraśl
#'9.153230130',   # Nazwa: Harasimowicze, rzeka: Sidra
#'9.153230140',   # Nazwa: Sokołda, rzeka: Sokołda
#'9.153230170',   # Nazwa: Nowosiółki, rzeka: Supraśl
#]
