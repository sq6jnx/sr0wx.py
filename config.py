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
goodbyeMsg = ["_","tu_sp6yre",cw('sp6yre')]

modules = ["worldweatheronline", "meteoalarm", "imgw_podest", "prospect_mp", "y_weather"]

class m:
    pass

y_weather = m()
y_weather.zipcode = 526363
# it would be nice to give one ability to parse it via template engine
# http://wiki.python.org/moin/Templating
y_weather.template = """stan_pogody_z_dnia {PUB_DATE_HOUR} _ temperatura 
    {CURR_TEMP} wilgotnosc {HUMIDITY} 
    {CURRENT_CONDITION} _ kierunek_wiatru {WIND_DIR_NEWS} 
    {WIN_DIR_DEG} predkosc_wiatru {WIND_SPEED} _
    cisnienie {PRESSURE} {PRESSURE_TENDENTION}
    temperatura_odczuwalna {TEMP_WIND_CHILL} _
    
    prognoza_na_nastepne piec godzin 
    {FORECAST0_CONDITION} temperatura_minimalna
    {FORECAST0_MIN_TEMP_SHORT} maksymalna {FORECAST0_MAX_TEMP} 
    
    _ nastepnie {FORECAST1_CONDITION} temperatura_minimalna
    {FORECAST1_MIN_TEMP_SHORT} maksymalna {FORECAST1_MAX_TEMP} _
    """

# ----------
# sms_qst
# ----------

sms_qst = m()
sms_qst.max_sim_capacity = 255
sms_qst.db_file = 'sms_qst.sqlite' # or ':memory:' for on-memory db
sms_qst.temp_file = '/tmp/sms_qst_{ID}.wav'
sms_qst.leave_messages_on_sim = True # You can delete or leave SMS on SIMCard after reading

# command in subprocess.Popen form
# espeak
sms_qst.tts_command = [ 
    ['/usr/bin/espeak', '-a', '200', '-p', '64', 
    '-s', '170', '{MESSAGE}', '-g', '5', '-v', 'pl', '-w', 
    sms_qst.temp_file,]
    ]
# festival with mbrola voice -- ugly
# you need fest.conf file with two lines in it:
# (voice_pjwstk_pl_ks_mbrola)
# (Parameter.set 'Duration_Stretch 1.25)
#sms_qst.tts_command = [
#    ['echo', '{MESSAGE}',],
#    ['iconv', '-f', 'UTF-8', '-t', 'ISO_8859-2'],
#    ['text2wave', '-o', sms_qst.temp_file, '-eval', 'fest.conf']
#]

# espeak with mbrola -- doesn't work??
#sms_qst.tts_command = [
#    ['/usr/bin/espeak', '-a', '100', '-p', '64', 
#    '-s', '170', '-g', '10', '-v', 'mb-pl1', '{MESSAGE}'], 
#
#    ['/usr/bin/mbrola', '-e', '/usr/share/mbrola/pl1/pl1', 
##    '-t', '2', 
#     '-', sms_qst.temp_file]
#]
sms_qst.template = """komunikat_specjalny_od {CALL} _ {MESSAGE} _ 
    powtarzam_komunikat _ {MESSAGE}"""
sms_qst.authorized_senders = {
   '+48501805277': 'sq6jnx',
   '+48603186430': 'sq6jnq' }

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

prospect_mp = m()
prospect_mp.wodowskazy = [
# obowiązuje ścisła kolejność! domena, rzeka, wodowskaz, stacja
    ['jaslo',    'Ropa',          'Biecz',             'BIRO'],
    ['jaslo',    'Jasiołka',      'Jasło',             'JAJA'],
    ['jaslo',    'Jasiołka',      'Jedlicze',          'JEJA'],
    ['jaslo',    'Wisloka',       'ulica Mickiewicza', 'JSWI'],
    ['jaslo',    'Kąty',          'Wisłoka',           'KAWI'],
    ['jaslo',    'Kotań',         'Wisłoka',           'KOWI'],
    ['jaslo',    'Ropa',          'Łosie',             'LORO'],
    ['jaslo',    'Wisłoka',       'Majscowa',          'MAWI'],
    ['jaslo',    'Wisłoka',       'Nowy Żmigród',      'NZWI'],
    ['jaslo',    'Wisłoka',       'Osiek Jasielski',   'OJWI'],
    ['jaslo',    'Ropa',          'Skoloszyn',         'SKRO'],
    ['jaslo',    'Jasiołka',      'Szczepańcowa',      'SZJA'],
    ['jaslo',    'Ropa',          'Szymbark',          'SZRO'],
    ['jaslo',    'Jasiołka',      'Tarnowiec',         'TAJA'],
    ['jaslo',    'Ropa',          'Trzczcinica',       'TRRO'],
    ['mielec',   'Wisłoka',       'Gawluszowice',      'GAWI'],
    ['mielec',   'Potok Zgórski', 'Podborze',          'POPZ'],
    ['mielec',   'Wisłoka',       'Przeclaw',          'PRWI'],
    ['mielec',   'Breń Stary',    'Sadkowa Gora',      'SABR'],
    ['mielec',   'Wisłoka',       'Wola Mielceka',     'WMWI'],
    ['mielec',   'Breń',          'Zabrnie',           'ZABR'],
    ['mielec',   'Wisła',         'Zaduszniki',        'ZAWI'],
    ['mielec',   'Breń',          'Ziempiniów',        'ZIBR'],
    ['ropczyce', 'Wielopolka',    'Glinik',            'GLWI'],
    ['ropczyce', 'Bystrzyca',     'Iwierzyce',         'IWBY'],
    ['ropczyce', 'Wielopolka',    'Kozodrza',          'KZWI'],
    ['ropczyce', 'Wielopolka',    'Łączki Kucharskie', 'LKWI'],
    ['ropczyce', 'Wielopolka',    'Okonin',            'OKWI'],
    ['ropczyce', 'Bystrzyca',     'Sielec',            'SIBY'],
    ['ropczyce', 'Budzisz',       'Zagorzyce',         'ZABU'],
    ['biala',    'Biała',         'Grybów',            'GRBI'],
    ['biala',    'Biała',         'Pławna',            'PWBI'],
    ['biala',    'Biała',         'Golanka',           'GOBI'],
    ['biala',    'Biała',         'Tuchów',            'TUBI'],
    ['biala',    'Biała',         'Pleśna',            'PLBI'],
    ['biala',    'Biała',         'Tarnów',            'TABI'],
    ['sanok',    'Osława',        'Czaszyn',           'CZOS'],
    ['sanok',    'Pielnica',      'Nowosielce',        'NOPI'],
    ['sanok',    'San',           'Sanok',             'SASA'],
    ['lososina', 'Łososina',      'Wronowice',         'WRLO'],
]

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

# world weather online

world_weather_online = m()
world_weather_online.api_key = '4bd98a1060131251112011'
world_weather_online.latitude = 52.71
world_weather_online.longitude=19.11
world_weather_online.template = """stan_pogody_z_dnia {OBSERVATION_TIME} 
    _ {CURRENT_WEATHER}
    temperatura {CURRENT_TEMP_C} wilgotnosc {CURRENT_HUMIDITY} 
    _ kierunek_wiatru {CURRENT_WIND_DIR} 
    {CURRENT_WIND_DIR_DEG} predkosc_wiatru {CURRENT_WIND_SPEED_MPS} 
    {CURRENT_WIND_SPEED_KMPH} _ cisnienie {CURRENT_PRESSURE} 
    pokrywa_chmur {CURRENT_CLOUDCOVER} _
    
    prognoza_na_nastepne piec godzin 
    {FCAST0_WEATHER} temperatura_minimalna
    {FCAST0_TEMP_MIN_C} maksymalna {FCAST0_TEMP_MAX_C} 
    kierunek_wiatru {FCAST0_WIND_DIR} {FCAST0_WIND_DIR_DEG} predkosc_wiatru 
    {FCAST0_WIND_SPEED_MPS} {FCAST0_WIND_SPEED_KMPH}
    
    _ jutro {FCAST1_WEATHER} temperatura_minimalna
    {FCAST1_TEMP_MIN_C} maksymalna {FCAST1_TEMP_MAX_C} kierunek_wiatru 
    {FCAST1_WIND_DIR} {FCAST1_WIND_DIR_DEG} predkosc_wiatru 
    {FCAST1_WIND_SPEED_MPS} {FCAST1_WIND_SPEED_KMPH} _ """


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
gopr_lawiny.podajWystawe = 1 # not yet implemented

# -------------
# povodi_cz
# -------------

povodi_cz = m()
povodi_cz.stations = [
    #['pla','7'],	# Bystřice, station Rohoznice
    #['pla','3'],	# Bělá, station Jedlová
    #['pla','11'],	# Chrudimka, station Hamry
    #['pla','13'],	# Chrudimka, station Nemošice
    #['pla','14'],	# Chrudimka, station Svídnice
    #['pla','159'],	# Chrudimka, station Padrty
    #['pla','174'],	# Chrudimka, station Přemilov
    #['pla','10'],	# Cidlina, station Sány
    #['pla','177'],	# Cidlina, station Jičín
    #['pla','9'],	# Cidlina, station Nový Bydžov
    #['pla','19'],	# D. Orlice, station Kostelec n. O.
    #['pla','21'],	# D. Orlice, station Nekoř
    #['pla','267'],	# D. Orlice, station Orlické Záhoří
    #['pla','23'],	# Doubrava, station Pařížov
    #['pla','24'],	# Doubrava, station Žleby
    #['pla','268'],	# Doubrava, station Bílek
    #['pla','15'],	# Dědina, station Chábory
    #['pla','16'],	# Dědina, station Mitrov
    #['pla','160'],	# Javorka, station Lázně Bělohrad
    #['pla','167'],	# Jeřice, station Mníšek
    #['pla','1026'],	# Jizera, station Bakov
    #['pla','28'],	# Jizera, station Dolní Sytová
    #['pla','29'],	# Jizera, station Jablonec nad Jizerou
    #['pla','32'],	# Jizera, station Železný Brod
    #['pla','161'],	# Jizerka, station Dolní Štěpanice
    #['pla','35'],	# Kamenice, station Plavy
    #['pla','36'],	# Kněžná, station Rychnov nad Kněžnou
    #['pla','168'],	# L. Nisa, station Proseč n. N.
    #['pla','83'],	# L. Nisa, station Hrádek
    #['pla','84'],	# L. Nisa, station Liberec
    #['pla','1079'],	# Labe, station Ústí nad Labem
    #['pla','223'],	# Labe, station Litoměřice
    #['pla','226'],	# Labe, station Brod
    #['pla','227'],	# Labe, station Vestřev
    #['pla','37'],	# Labe, station Brandýs nad Labem
    #['pla','55'],	# Labe, station Labská
    #['pla','56'],	# Labe, station Les Království
    #['pla','60'],	# Labe, station Mělník
    #['pla','61'],	# Labe, station Němčice
    #['pla','63'],	# Labe, station Nymburk
    #['pla','71'],	# Labe, station Přelouč
    #['pla','75'],	# Labe, station Špindlerův Mlýn
    #['pla','163'],	# Loučná, station Litomyšl
    #['pla','85'],	# Loučná, station Cerekvice nad Loučnou
    #['pla','86'],	# Loučná, station Dašice
    #['pla','228'],	# Malé Labe, station Horní Lánov
    #['pla','87'],	# Metuje, station Hronov
    #['pla','89'],	# Metuje, station Krčín
    #['pla','90'],	# Metuje, station Maršov nad Metují
    #['pla','92'],	# Mrlina, station Vestec
    #['pla','164'],	# Novohradka, station Úhřetice
    #['pla','273'],	# Novohradka, station Luže
    #['pla','93'],	# Ohře, station Louny
    #['pla','98'],	# Orlice, station Týniště nad Orlicí
    #['pla','119'],	# Smědá, station Bílý Potok
    #['pla','120'],	# Smědá, station Frýdlant
    #['pla','121'],	# Smědá, station Předlánce
    #['pla','141'],	# Stěnava, station Meziměstí
    #['pla','142'],	# Stěnava, station Otovice
    #['pla','143'],	# T. Orlice, station Čermná nad Orlicí
    #['pla','144'],	# T. Orlice, station Lichkov
    #['pla','222'],	# Tichá Orlice, station Dolní Libchavy
    #['pla','146'],	# Třebovka, station Hylváty
    #['pla','147'],	# Třebovka, station Třebovice
    #['pla','154'],	# Vltava, station Vraňany
    #['pla','166'],	# Vrchlice, station Vrchlice
    #['pla','157'],	# Výrovka, station Plaňany
    #['pla','158'],	# Zdobnice, station Slatina nad Zdobnicí
    #['pla','149'],	# Úpa, station Horní Maršov
    #['pla','151'],	# Úpa, station Zlič
    #['pla','162'],	# Černá Desná, station Souš
    #['pmo','038'],	# Balinka, station Baliny
    #['pmo','006'],	# Bečva, station Dluhonice
    #['pmo','043'],	# Bečva, station Teplice nad Bečvou
    ['pmo','046'],	# Branná, station Jindřichov
    #['pmo','118'],	# Brumovka, station Brumov
    #['pmo','036'],	# Bystřice, station Bystřička nad přehradou
    #['pmo','051'],	# Bystřice, station Bystřička pod přehradou
    ['pmo','035'],	# Desná, station Šumperk
    #['pmo','026'],	# Dyje, station Podhradí
    #['pmo','027'],	# Dyje, station Vranov-Hamry
    #['pmo','029'],	# Dyje, station Hevlín
    #['pmo','031'],	# Dyje, station Nové Mlýny
    #['pmo','032'],	# Dyje, station Ladná
    #['pmo','064'],	# Dyje, station Znojmo pod přehradou
    #['pmo','008'],	# Dřevnice, station Zlín
    #['pmo','034'],	# Dřevnice, station Kašava
    #['pmo','055'],	# Dřevnice, station Slušovice pod přehradou
    #['pmo','056'],	# Fryštácký potok, station Fryšták
    #['pmo','115'],	# Fryštácký potok, station Fryšták – pod přehradou
    #['pmo','121'],	# Fryštácký potok, station Výlanta
    #['pmo','048'],	# Fryšávka, station Jimramov
    #['pmo','053'],	# Hloučela, station Plumlov
    #['pmo','111'],	# Hloučela, station Soběsuky
    #['pmo','112'],	# Hloučela, station Plumlov – nad přehradou
    #['pmo','113'],	# Hloučela, station Plumlov – pod přehradou
    #['pmo','123'],	# Januštica, station Dolní Ves
    #['pmo','030'],	# Jevišovka, station Hrušovany nad Jeviš.
    #['pmo','120'],	# Jevišovka, station Výrovice
    #['pmo','011'],	# Jihlava, station Ivančice
    #['pmo','019'],	# Jihlava, station Dvorce
    #['pmo','020'],	# Jihlava, station Třebíč-Ptáčov
    #['pmo','021'],	# Jihlava, station Přibice
    #['pmo','067'],	# Jihlava, station Mohelno
    #['pmo','117'],	# Juhyně, station Rajnochovice
    #['pmo','049'],	# Kyjovka, station Koryčany nad přehradou
    #['pmo','060'],	# Kyjovka, station Koryčany pod přehradou
    #['pmo','044'],	# Křetínka, station Prostřední Poříčí
    #['pmo','122'],	# Lukovský potok, station Kostelec
    #['pmo','047'],	# Lutonínka, station Vizovice
    ['pmo','001'],	# Morava, station Raškov
    #['pmo','002'],	# Morava, station Moravičany
    #['pmo','003'],	# Morava, station Olomouc
    #['pmo','007'],	# Morava, station Kroměříž
    #['pmo','010'],	# Morava, station Strážnice
    #['pmo','037'],	# Morava, station Spytihněv
    ['pmo','045'],	# Morava, station Vlaské
    #['pmo','081'],	# Morava, station Lanžhot
    #['pmo','124'],	# Morava, station okovice – lávka
    #['pmo','025'],	# Moravská Dyje, station Janov
    ['pmo','042'],	# Moravská Sázava, station Lupěné
    #['pmo','009'],	# Olšava, station Uherský Brod
    #['pmo','022'],	# Oslava, station Velké Meziříčí
    #['pmo','023'],	# Oslava, station Oslavany
    #['pmo','040'],	# Oslava, station Dolní Bory
    #['pmo','068'],	# Oslava, station Mostiště pod přehradou
    #['pmo','024'],	# Rokytná, station Moravský Krumlov
    #['pmo','004'],	# Rožnovská Bečva, station Valašské Meziříčí
    #['pmo','116'],	# Rusava, station Chomýž
    #['pmo','050'],	# Stanovnice, station Karolinka pod přehradou
    #['pmo','016'],	# Svitava, station Letovice
    #['pmo','017'],	# Svitava, station Bílovice nad Svitavou
    #['pmo','012'],	# Svratka, station Borovnice
    #['pmo','014'],	# Svratka, station Veverská Bítýška
    #['pmo','015'],	# Svratka, station Brno-Poříčí
    #['pmo','018'],	# Svratka, station Židlochovice
    #['pmo','086'],	# Svratka, station Dalečín
    #['pmo','087'],	# Svratka, station Vír-pod přehr.
    #['pmo','110'],	# Velička, station Hranice
    #['pmo','119'],	# Vlára, station Popov
    #['pmo','005'],	# Vsetínská Bečva, station Jarcová
    #['pmo','041'],	# Želetavka, station Jemnice
    ['pod','21'],	# Bělá, station Mikulovice
    #['pod','11'],	# Lubina, station Petřvald
    #['pod','05'],	# Lučina, station Žermanice
    ['pod','14'],	# Moravice, station Valšov
    ['pod','15'],	# Moravice, station Kružberk
    ['pod','18'],	# Moravice, station Branka
    #['pod','02'],	# Morávka, station Morávka
    #['pod','10'],	# Odra, station Odry
    #['pod','12'],	# Odra, station Svinov
    #['pod','13'],	# Odra, station Bohumín
    #['pod','06'],	# Olše, station Jablunkov
    #['pod','07'],	# Olše, station Český Těšín
    #['pod','09'],	# Olše, station Věřňovice
    ['pod','16'],	# Opava, station Krnov
    ['pod','19'],	# Opava, station Opava
    #['pod','20'],	# Opava, station Děhylov
    ['pod','17'],	# Opavice, station Krnov
    #['pod','01'],	# Ostravice, station Šance
    #['pod','03'],	# Ostravice, station Frýdek Místek
    #['pod','04'],	# Ostravice, station Ostrava
    #['pod','08'],	# Stonávka, station Těrlicko
    #['poh','1430'],	# Bystřice, station Ostrov
    #['poh','2424'],	# Bílina, station Trmice
    #['poh','2473'],	# Bílina, station Bílina ČD
    #['poh','2449'],	# Bílý potok, station Bílý potok
    #['poh','2439'],	# Chomutovka, station III.mlýn
    #['poh','2448'],	# Flájský potok, station Český Jiřetín
    #['poh','3422'],	# Kamenice, station Srbská Kamenice
    #['poh','1409'],	# Libocký potok, station Horka - odtok
    #['poh','2446'],	# Loupnice, station Janov - odtok
    #['poh','3424'],	# Mandava, station Varnsdorf
    #['poh','1994'],	# Odrava, station Jesenice - odtok
    #['poh','1404'],	# Ohře, station Cheb
    #['poh','1410'],	# Ohře, station Citice
    #['poh','1429'],	# Ohře, station Drahovice
    #['poh','2401'],	# Ohře, station Klášterec nad Ohří
    #['poh','2404'],	# Ohře, station Stranná
    #['poh','3401'],	# Ohře, station Žatec
    #['poh','3402'],	# Ohře, station Louny
    #['poh','3407'],	# Ploučnice, station Stráž pod Ralskem - město
    #['poh','3408'],	# Ploučnice, station Mimoň
    #['poh','3409'],	# Ploučnice, station Česká Lípa
    #['poh','3410'],	# Ploučnice, station Benešov nad Ploučnicí
    #['poh','3428'],	# Robečský potok, station Zahrádky
    #['poh','1417'],	# Rolava, station Stará Role
    #['poh','1411'],	# Svatava, station Kraslice
    #['poh','1414'],	# Svatava, station Svatava
    #['poh','3421'],	# Svitávka, station Zákupy
    #['poh','1419'],	# Teplá, station Podhora
    #['poh','1422'],	# Teplá, station Teplička
    #['poh','1423'],	# Teplá, station Březová - odtok
    #['poh','3425'],	# Úštěcký potok, station Vědlice
    #['pvl','BPVE'],	# Bakovský potok, station Velvary
    #['pvl','BEBE'],	# Berounka, station Beroun B
    #['pvl','BELI'],	# Berounka, station Liblín
    #['pvl','BEPL'],	# Berounka, station Plzeň-Bílá Hora
    #['pvl','BEZB'],	# Berounka, station Zbečno
    #['pvl','BPNE'],	# Bezdrevský potok, station Netolice
    #['pvl','BLBA'],	# Blanice, station Bavorov
    #['pvl','BLBM'],	# Blanice, station Blanický mlýn
    #['pvl','BLHE'],	# Blanice, station Heřmaň
    #['pvl','BLHS'],	# Blanice, station odtok VD Husinec
    #['pvl','BLLO'],	# Blanice, station Louňovice
    #['pvl','BLPO'],	# Blanice, station Podedvorský mlýn
    #['pvl','BLRA'],	# Blanice, station Radonice - Zdebudeves
    #['pvl','BPSH'],	# Borovský potok, station Stříbrné Hory
    #['pvl','BARA'],	# Bělá, station Radětín
    #['pvl','CPCV'],	# Chvalšinský potok, station Chvalšiny
    #['pvl','DRKL'],	# Dračice, station Klikov
    #['pvl','HPOL'],	# Hamerský potok, station Oldříš
    #['pvl','HPPL'],	# Hamerský potok, station Planá
    #['pvl','JPMI'],	# Jankovský potok, station Milotice
    #['pvl','KLHA'],	# Klabava, station Hrádek u Rokycan
    #['pvl','KLNH'],	# Klabava, station Nová Huť
    #['pvl','KOST'],	# Kocába, station Štěchovice
    #['pvl','KPST'],	# Kosový potok, station Svahy-Třebel
    #['pvl','KRST'],	# Křemelná, station Stodůlky
    #['pvl','KPBR'],	# Křemžský potok, station Brloh
    #['pvl','LIBE'],	# Litavka, station Beroun L
    #['pvl','LICE'],	# Litavka, station Čenkov
    #['pvl','LIPR'],	# Litavka, station Příbram
    #['pvl','LDLD'],	# Loděnice, station Loděnice
    #['pvl','LOBL'],	# Lomnice, station Blatná
    #['pvl','LODO'],	# Lomnice, station Dolní Ostrovec
    #['pvl','LUBE'],	# Lužnice, station Bechyně
    #['pvl','LUFR'],	# Lužnice, station Frahelž
    #['pvl','LUKA'],	# Lužnice, station Kazdovna
    #['pvl','LUKL'],	# Lužnice, station Klenovice
    #['pvl','LUNV'],	# Lužnice, station Nová Ves
    #['pvl','LUPI'],	# Lužnice, station Pilař
    #['pvl','MAKA'],	# Malše, station Kaplice
    #['pvl','MAPO'],	# Malše, station Pořešín
    #['pvl','MARM'],	# Malše, station Římov
    #['pvl','MARO'],	# Malše, station Roudné
    #['pvl','MSRA'],	# Mastník, station Radíč
    #['pvl','MPMI'],	# Milevský potok, station Milevsko
    #['pvl','MZHY'],	# Mže, station odtok VD Hracholusky
    #['pvl','MZKO'],	# Mže, station Kočov
    #['pvl','MZLC'],	# Mže, station odtok VD Lučina
    #['pvl','MZST'],	# Mže, station Stříbro M
    #['pvl','NEHA'],	# Nežárka, station Hamr
    #['pvl','NELA'],	# Nežárka, station Lásenice
    #['pvl','NERO'],	# Nežárka, station Rodvínov
    #['pvl','NRML'],	# Nová řeka, station Mláka
    #['pvl','OSKO'],	# Ostružná, station Kolínec
    #['pvl','OTKA'],	# Otava, station Katovice
    #['pvl','OTPI'],	# Otava, station Písek
    #['pvl','OTRE'],	# Otava, station Rejštejn
    #['pvl','OTST'],	# Otava, station Strakonice
    #['pvl','OTSU'],	# Otava, station Sušice
    #['pvl','POCK'],	# Polečnice, station Český Krumlov
    #['pvl','PONO'],	# Polečnice, station Novosedly
    #['pvl','RALH'],	# Radbuza, station Lhota
    #['pvl','RAST'],	# Radbuza, station Staňkov
    #['pvl','RATA'],	# Radbuza, station Tasnovice
    #['pvl','RAUD'],	# Radbuza, station odtok VD České Údolí
    #['pvl','SKVA'],	# Skalice, station Varvažov
    #['pvl','SKZP'],	# Skalice, station Zadní Poříčí
    #['pvl','SMBO'],	# Smutná, station Božetice
    #['pvl','SMRA'],	# Smutná, station Rataje
    #['pvl','SPBO'],	# Spůlka, station Bohumilice
    #['pvl','SCBO'],	# Stropnice, station Borovany
    #['pvl','SCHM'],	# Stropnice, station odtok VD Humenice
    #['pvl','SCPA'],	# Stropnice, station Pašínovice-Komařice
    #['pvl','SPHV'],	# Stroupinský potok, station Hředle
    #['pvl','SVCK'],	# Studená Vltava, station Černý Kříž
    #['pvl','STCI'],	# Střela, station Čichořice
    #['pvl','STPL'],	# Střela, station Plasy
    #['pvl','STZC'],	# Střela, station odtok VD Žlutice
    #['pvl','SACH'],	# Sázava, station Chlístov
    #['pvl','SACS'],	# Sázava, station Český Šternberk
    #['pvl','SAHB'],	# Sázava, station Pohledští Dvořáci - Havlíčkův Brod
    #['pvl','SAKA'],	# Sázava, station Kácov
    #['pvl','SANE'],	# Sázava, station Nespeky
    #['pvl','SASV'],	# Sázava, station Světlá nad Sázavou
    #['pvl','SASZ'],	# Sázava, station Sázava u Žďáru
    #['pvl','SAZD'],	# Sázava, station Žďár nad Sázavou
    #['pvl','SAZR'],	# Sázava, station Zruč nad Sázavou
    #['pvl','SZJD'],	# Sázavka, station Josefodol
    #['pvl','TVCH'],	# Teplá Vltava, station Chlum
    #['pvl','TVLE'],	# Teplá Vltava, station Lenora
    #['pvl','TRCR'],	# Trnava, station Červená Řečice
    #['pvl','TRKO'],	# Trnava, station Želiv - Kocanda
    #['pvl','TRNE'],	# Třemošná, station Nevřeň
    #['pvl','VLBR'],	# Vltava, station Březí
    #['pvl','VLCB'],	# Vltava, station České Budějovice
    #['pvl','VLCH'],	# Vltava, station Praha - Malá Chuchle
    #['pvl','VLKS'],	# Vltava, station Spolí
    #['pvl','VLOR'],	# Vltava, station odtok VD Orlík
    #['pvl','VLSL'],	# Vltava, station odtok VD Slapy
    #['pvl','VLVB'],	# Vltava, station Vyšší Brod
    #['pvl','VLVE'],	# Vltava, station odtok VD Vrané
    #['pvl','VLVX'],	# Vltava, station Vraňany
    #['pvl','VLZA'],	# Vltava, station Zátoň
    #['pvl','VONE'],	# Volyňka, station Němětice
    #['pvl','VOSU'],	# Volyňka, station Sudslavice
    #['pvl','VYMO'],	# Vydra, station Modrava
    #['pvl','ZPHR'],	# Zlatý potok, station Hracholusky
    #['pvl','ZUDO'],	# Zubřina, station Domažlice
    #['pvl','UHKL'],	# Úhlava, station Klatovy-Tajanov
    #['pvl','UHPR'],	# Úhlava, station Přeštice
    #['pvl','UHSL'],	# Úhlava, station odtok VD Nýrsko
    #['pvl','UHST'],	# Úhlava, station Štěnovice
    #['pvl','UKST'],	# Úhlavka, station Stříbro U
    #['pvl','USKO'],	# Úslava, station Plzeň-Koterov
    #['pvl','USPR'],	# Úslava, station Prádlo
    #['pvl','USZD'],	# Úslava, station Ždírec
    #['pvl','UPTR'],	# Úterský potok, station Trpisty
    #['pvl','CPTU'],	# Černovický potok, station Tučapy
    #['pvl','CRLC'],	# Černá, station Líčov
    #['pvl','CEKL'],	# Černý potok, station Klenčí
    #['pvl','CPHO'],	# Červený potok, station Hořovice
    #['pvl','SLMI'],	# Šlapanka, station Mírovka
    #['pvl','HECA'],	# Želivka, station Čakovice
    #['pvl','ZEPO'],	# Želivka, station Poříčí
    #['pvl','ZESO'],	# Želivka, station Soutice
    #['pvl','ZEVR'],	# Želivka, station Želiv-Vřesník
]

