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

modules = ["worldweatheronline", "meteoalarm", "y_weather", 'ibles']

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
    #['mielec',   'Wisłoka',       'Gawluszowice',      'GAWI'],
    #['mielec',   'Potok Zgórski', 'Podborze',          'POPZ'],
    #['mielec',   'Wisłoka',       'Przeclaw',          'PRWI'],
    #['mielec',   'Breń Stary',    'Sadkowa Gora',      'SABR'],
    #['mielec',   'Wisłoka',       'Wola Mielceka',     'WMWI'],
    #['mielec',   'Breń',          'Zabrnie',           'ZABR'],
    #['mielec',   'Wisła',         'Zaduszniki',        'ZAWI'],
    #['mielec',   'Breń',          'Ziempiniów',        'ZIBR'],
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
    #['sanok',    'Osława',        'Czaszyn',           'CZOS'],
    #['sanok',    'Pielnica',      'Nowosielce',        'NOPI'],
    #['sanok',    'San',           'Sanok',             'SASA'],
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
world_weather_online.api_key = 'changeme'
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
# Niestety, dla Śnieżnika Kłodzkiego odsyła na stronę Horska Sluzba CZ, dla 
# Pienin nie podaje komunikatów wogóle. Zagrożenia dla Tatr podaje TOPR.

gopr_lawiny.region = 1
gopr_lawiny.podajTendencje = 1
gopr_lawiny.podajWystawe = 1 # not yet implemented

# -------------
# ibles
# ------------

# Numer swojej strefy najłatwiej sprawdzić na
# http://bazapozarow.ibles.pl/zagrozenie/ . Możesz podać jedną lub kilka stref,
# którymi jesteś zainteresowany; w tym drugim przypadku odczytane zostanie
# najwyższe z występujących zagrożenie nawet jeśli w strefie "obok" zagrożenie
# nie występuje. Ważne, aby numery stref podać w tablicy.

ibles = m()
ibles.strefy = [37,38,16]



# -------------
# activity_map
# ------------

activity_map = m()
activity_map.service_url="http://test.ostol.pl/?base="
activity_map.data = {
        "callsign":"SR0WX",
        "lat":     0,
        "lon":     0,
        "q":       5,
        "asl":     118,
        "agl":     20,
        "range":   30,
        "info":    u"Additional informations",
        } 


# -------------
# radAtHome
# ------------

radAtHome = m()
radAtHome.file_path = '/tmp/data.bin'
radAtHome.n_hours = 3
radAtHome.medium_tresh = 0.3
radAtHome.high_tresh   = 0.8
#radAtHome.database    = ':memory:' # for testing
radAtHome.database     = 'radathome.sqlite3' # for normal use

# ------
# wview
# ------
wview = m()
wview.path = '/var/lib/wview/archive/wview-archive.sdb'
wview.template = """stan_pogody_z_dnia {OBSERVATION_TIME}
temperatura {CURRENT_TEMP_C} wilgotnosc {CURRENT_HUMIDITY}
_ kierunek_wiatru
{CURRENT_WIND_DIR_DEG} predkosc_wiatru {CURRENT_WIND_SPEED_MPS}
_ cisnienie {CURRENT_PRESSURE} """
