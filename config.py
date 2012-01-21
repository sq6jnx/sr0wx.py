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

modules = ["worldweatheronline", "meteoalarm", "prospect_mp",\
        "y_weather","povodi_cz",'gopr_lawiny',
        #"ibles_pl",'imieniny','sms_qst', "imgw_podest",'sunriset',
        #'hscr_laviny'

    ]


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
# stacje Grześka SP6TPW
povodi_cz.stations = [
    ['pmo1','046'],	# Branná, station Jindřichov
    ['pmo1','035'],	# Desná, station Šumperk
    ['pmo1','001'],	# Morava, station Raškov
    ['pmo1','045'],	# Morava, station Vlaské
    ['pmo1','042'],	# Moravská Sázava, station Lupěné
    ['pod1','21'],	# Bělá, station Mikulovice
    ['pod1','14'],	# Moravice, station Valšov
    ['pod1','15'],	# Moravice, station Kružberk
    ['pod1','18'],	# Moravice, station Branka
    ['pod1','16'],	# Opava, station Krnov
    ['pod1','19'],	# Opava, station Opava
    ['pod1','17'],	# Opavice, station Krnov
    ['pod1','59'],	# Zlatý potok, station Zlaté Hory
]

#povodi_cz.stations = [
#    ['pla1','7'],	# Bystřice, station Rohoznice
#    ['pla1','2'],	# Bělá, station Častolovice
#    ['pla1','3'],	# Bělá, station Jedlová v Orlických horách
#    ['pla1','10'],	# Cidlina, station Sány
#    ['pla1','177'],	# Cidlina, station Jičín
#    ['pla1','9'],	# Cidlina, station Nový Bydžov
#    ['pla1','18'],	# Divoká Orlice, station Klášterec nad Orlicí
#    ['pla1','19'],	# Divoká Orlice, station Kostelec nad Orlicí
#    ['pla1','20'],	# Divoká Orlice, station Litice
#    ['pla1','21'],	# Divoká Orlice, station Nekoř
#    ['pla1','267'],	# Divoká Orlice, station Orlické Záhoří
#    ['pla1','15'],	# Dědina, station Chábory
#    ['pla1','16'],	# Dědina, station Mitrov
#    ['pla1','17'],	# Dědina, station Žákovec
#    ['pla1','25'],	# Dřevíč, station Velký Dřevíč
#    ['pla1','160'],	# Javorka, station Lázně Bělohrad
#    ['pla1','171'],	# Kalenský potok, station Dolní Olešnice
#    ['pla1','36'],	# Kněžná, station Rychnov nad Kněžnou
#    ['pla1','226'],	# Labe, station Brod
#    ['pla1','227'],	# Labe, station Vestřev
#    ['pla1','47'],	# Labe, station Hostinné - Labe
#    ['pla1','50'],	# Labe, station Jaroměř
#    ['pla1','55'],	# Labe, station Labská
#    ['pla1','56'],	# Labe, station Les Království
#    ['pla1','75'],	# Labe, station Špindlerův Mlýn
#    ['pla1','169'],	# Malé Labe, station Prosečné
#    ['pla1','228'],	# Malé Labe, station Horní Lánov
#    ['pla1','87'],	# Metuje, station Hronov
#    ['pla1','88'],	# Metuje, station Jaroměř
#    ['pla1','89'],	# Metuje, station Krčín
#    ['pla1','90'],	# Metuje, station Maršov nad Metují
#    ['pla1','92'],	# Mrlina, station Vestec
#    ['pla1','269'],	# Olešenka, station Peklo
#    ['pla1','97'],	# Orlice, station Hradec Králové
#    ['pla1','98'],	# Orlice, station Týniště nad Orlicí
#    ['pla1','170'],	# Pilníkovský potok, station Chotěvice
#    ['pla1','116'],	# Rokytenka, station Žamberk
#    ['pla1','117'],	# Rozkošský potok, station Rozkoš
#    ['pla1','141'],	# Stěnava, station Meziměstí
#    ['pla1','142'],	# Stěnava, station Otovice
#    ['pla1','158'],	# Zdobnice, station Slatina nad Zdobnicí
#    ['pla1','149'],	# Úpa, station Horní Maršov
#    ['pla1','150'],	# Úpa, station Slatina nad Úpou
#    ['pla1','151'],	# Úpa, station Zlíč
#    ['pla1','172'],	# Úpa, station Horní Staré Město
#    ['pla1','201'],	# Čistá, station Hostinné
#    ['pla1','221'],	# Štítarský potok, station Svídnice
#    ['pla2','11'],	# Chrudimka, station Hamry
#    ['pla2','13'],	# Chrudimka, station Nemošice
#    ['pla2','14'],	# Chrudimka, station Svídnice
#    ['pla2','159'],	# Chrudimka, station Padrty
#    ['pla2','173'],	# Chrudimka, station Lány
#    ['pla2','174'],	# Chrudimka, station Přemilov
#    ['pla2','175'],	# Doubrava, station Spačice
#    ['pla2','23'],	# Doubrava, station Pařížov
#    ['pla2','24'],	# Doubrava, station Žleby
#    ['pla2','268'],	# Doubrava, station Bílek
#    ['pla2','270'],	# Krounka, station Otradov
#    ['pla2','224'],	# Ležák, station Zaječice
#    ['pla2','163'],	# Loučná, station Litomyšl
#    ['pla2','85'],	# Loučná, station Cerekvice nad Loučnou
#    ['pla2','86'],	# Loučná, station Dašice
#    ['pla2','164'],	# Novohradka, station Úhřetice
#    ['pla2','273'],	# Novohradka, station Luže
#    ['pla2','143'],	# Tichá Orlice, station Čermná nad Orlicí
#    ['pla2','144'],	# Tichá Orlice, station Lichkov
#    ['pla2','145'],	# Tichá Orlice, station Sobkovice
#    ['pla2','222'],	# Tichá Orlice, station Dolní Libchavy
#    ['pla2','146'],	# Třebovka, station Hylváty
#    ['pla2','147'],	# Třebovka, station Třebovice
#    ['pla2','271'],	# Třebovka, station Opatov
#    ['pla2','166'],	# Vrchlice, station Vrchlice
#    ['pla2','176'],	# Vrchlice, station Malešov
#    ['pla3','188'],	# Albrechtický potok, station Mlýnice/odtok
#    ['pla3','187'],	# Fojtka, station Fojtka/odtok
#    ['pla3','184'],	# Harcovský potok, station Harcov/odtok
#    ['pla3','167'],	# Jeřice, station Mníšek
#    ['pla3','1026'],	# Jizera, station Bakov nad Jizerou
#    ['pla3','182'],	# Jizera, station Turnov
#    ['pla3','28'],	# Jizera, station Dolní Sytová
#    ['pla3','29'],	# Jizera, station Jablonec nad Jizerou
#    ['pla3','30'],	# Jizera, station Mladá Boleslav
#    ['pla3','31'],	# Jizera, station Předměřice
#    ['pla3','32'],	# Jizera, station Železný Brod
#    ['pla3','161'],	# Jizerka, station Dolní Štěpanice
#    ['pla3','33'],	# Kamenice, station Josefův Důl
#    ['pla3','34'],	# Kamenice, station Kristiánov
#    ['pla3','35'],	# Kamenice, station Plavy
#    ['pla3','168'],	# Lužická Nisa, station Proseč nad Nisou
#    ['pla3','83'],	# Lužická Nisa, station Hrádek nad Nisou
#    ['pla3','84'],	# Lužická Nisa, station Liberec
#    ['pla3','91'],	# Mohelka, station Chocnějovice
#    ['pla3','179'],	# Mumlava, station Harrachov
#    ['pla3','183'],	# Mšenský potok, station Mšeno
#    ['pla3','180'],	# Oleška, station Slaná
#    ['pla3','119'],	# Smědá, station Bílý Potok
#    ['pla3','120'],	# Smědá, station Frýdlant
#    ['pla3','121'],	# Smědá, station Předlánce
#    ['pla3','162'],	# Černá Desná, station Souš
#    ['pla3','181'],	# Černá Desná, station Jezdecká
#    ['pla3','185'],	# Černá Nisa, station Uhlířská
#    ['pla3','186'],	# Černá Nisa, station Rudolfov/odtok
#    ['pla3','189'],	# Řasnice, station Frýdlant v Č.
#    ['pla4','220'],	# Labe, station Pardubice
#    ['pla4','233'],	# Labe, station Kostelec nad Labem
#    ['pla4','37'],	# Labe, station Brandýs nad Labem
#    ['pla4','61'],	# Labe, station Němčice
#    ['pla4','63'],	# Labe, station Nymburk
#    ['pla4','65'],	# Labe, station Opatovice nad Labem
#    ['pla4','66'],	# Labe, station Obříství
#    ['pla4','71'],	# Labe, station Přelouč
#    ['pla4','80'],	# Labe, station Valy
#    ['pla4','157'],	# Výrovka, station Plaňany
#    ['pla5','1042'],	# Labe, station Děčín
#    ['pla5','1079'],	# Labe, station Ústí nad Labem
#    ['pla5','223'],	# Labe, station Litoměřice
#    ['pla5','45'],	# Labe, station Dolní Beřkovice
#    ['pla5','60'],	# Labe, station Mělník
#    ['pla5','74'],	# Labe, station Střekov
#    ['pla5','93'],	# Ohře, station Louny
#    ['pla5','154'],	# Vltava, station Vraňany
#    ['pmo1','006'],	# Bečva, station Dluhonice
#    ['pmo1','043'],	# Bečva, station Teplice nad Bečvou
#    ['pmo1','046'],	# Branná, station Jindřichov
#    ['pmo1','036'],	# Bystřice, station Bystřička nad přehradou
#    ['pmo1','051'],	# Bystřice, station Bystřička pod přehradou
#    ['pmo1','035'],	# Desná, station Šumperk
#    ['pmo1','053'],	# Hloučela, station VD Plumlov
#    ['pmo1','111'],	# Hloučela, station Soběsuky
#    ['pmo1','112'],	# Hloučela, station Plumlov – nad přehradou
#    ['pmo1','113'],	# Hloučela, station Plumlov – pod přehradou
#    ['pmo1','117'],	# Juhyně, station Rajnochovice
#    ['pmo1','001'],	# Morava, station Raškov
#    ['pmo1','002'],	# Morava, station Moravičany
#    ['pmo1','003'],	# Morava, station Olomouc
#    ['pmo1','007'],	# Morava, station Kroměříž
#    ['pmo1','045'],	# Morava, station Vlaské
#    ['pmo1','042'],	# Moravská Sázava, station Lupěné
#    ['pmo1','004'],	# Rožnovská Bečva, station Valašské Meziříčí
#    ['pmo1','116'],	# Rusava, station Chomýž
#    ['pmo1','050'],	# Stanovnice, station Karolinka pod přehradou
#    ['pmo1','110'],	# Velička, station Hranice
#    ['pmo1','005'],	# Vsetínská Bečva, station Jarcová
#    ['pmo2','038'],	# Balinka, station Baliny
#    ['pmo2','026'],	# Dyje, station Podhradí
#    ['pmo2','027'],	# Dyje, station Vranov-Hamry
#    ['pmo2','029'],	# Dyje, station Hevlín
#    ['pmo2','031'],	# Dyje, station Nové Mlýny
#    ['pmo2','032'],	# Dyje, station Ladná
#    ['pmo2','064'],	# Dyje, station Znojmo pod přehradou
#    ['pmo2','048'],	# Fryšávka, station Jimramov
#    ['pmo2','030'],	# Jevišovka, station Hrušovany nad Jeviš.
#    ['pmo2','120'],	# Jevišovka, station Výrovice
#    ['pmo2','011'],	# Jihlava, station Ivančice
#    ['pmo2','019'],	# Jihlava, station Dvorce
#    ['pmo2','020'],	# Jihlava, station Třebíč-Ptáčov
#    ['pmo2','021'],	# Jihlava, station Přibice
#    ['pmo2','067'],	# Jihlava, station Mohelno
#    ['pmo2','044'],	# Křetínka, station Prostřední Poříčí
#    ['pmo2','025'],	# Moravská Dyje, station Janov
#    ['pmo2','022'],	# Oslava, station Velké Meziříčí
#    ['pmo2','023'],	# Oslava, station Oslavany
#    ['pmo2','040'],	# Oslava, station Dolní Bory
#    ['pmo2','068'],	# Oslava, station Mostiště pod přehradou
#    ['pmo2','024'],	# Rokytná, station Moravský Krumlov
#    ['pmo2','016'],	# Svitava, station Letovice
#    ['pmo2','017'],	# Svitava, station Bílovice nad Svitavou
#    ['pmo2','012'],	# Svratka, station Borovnice
#    ['pmo2','014'],	# Svratka, station Veverská Bítýška
#    ['pmo2','015'],	# Svratka, station Brno-Poříčí
#    ['pmo2','018'],	# Svratka, station Židlochovice
#    ['pmo2','086'],	# Svratka, station Dalečín
#    ['pmo2','087'],	# Svratka, station Vír-pod přehr.
#    ['pmo2','041'],	# Želetavka, station Jemnice
#    ['pmo3','118'],	# Brumovka, station Brumov
#    ['pmo3','008'],	# Dřevnice, station Zlín
#    ['pmo3','034'],	# Dřevnice, station Kašava
#    ['pmo3','055'],	# Dřevnice, station Slušovice pod přehradou
#    ['pmo3','056'],	# Fryštácký potok, station VD Fryšták
#    ['pmo3','115'],	# Fryštácký potok, station Fryšták – pod přehradou
#    ['pmo3','121'],	# Fryštácký potok, station Výlanta
#    ['pmo3','123'],	# Januštica, station Dolní Ves
#    ['pmo3','049'],	# Kyjovka, station Koryčany nad přehradou
#    ['pmo3','060'],	# Kyjovka, station Koryčany pod přehradou
#    ['pmo3','122'],	# Lukovský potok, station Kostelec
#    ['pmo3','047'],	# Lutonínka, station Vizovice
#    ['pmo3','010'],	# Morava, station Strážnice
#    ['pmo3','037'],	# Morava, station Spytihněv
#    ['pmo3','081'],	# Morava, station Lanžhot
#    ['pmo3','124'],	# Morava, station Otrokovice – lávka
#    ['pmo3','009'],	# Olšava, station Uherský Brod
#    ['pmo3','119'],	# Vlára, station Popov
#    ['pod1','48'],	# Bílovka, station Bílovec
#    ['pod1','21'],	# Bělá, station Mikulovice
#    ['pod1','58'],	# Bělá, station Jeseník
#    ['pod1','29'],	# Husí potok, station Fulnek
#    ['pod1','28'],	# Hvozdnice, station Otice
#    ['pod1','46'],	# Jičínka, station Nový Jičín
#    ['pod1','11'],	# Lubina, station Petřvald
#    ['pod1','52'],	# Lubina, station Vlčovice
#    ['pod1','56'],	# Luha, station Jeseník nad Odrou
#    ['pod1','14'],	# Moravice, station Valšov
#    ['pod1','15'],	# Moravice, station Kružberk
#    ['pod1','18'],	# Moravice, station Branka
#    ['pod1','26'],	# Moravice, station Slezská Harta
#    ['pod1','27'],	# Moravice, station Podhradí
#    ['pod1','10'],	# Odra, station Odry
#    ['pod1','30'],	# Odra, station Bartošovice
#    ['pod1','31'],	# Ondřejnice, station Kozlovice
#    ['pod1','32'],	# Ondřejnice, station Brušperk
#    ['pod1','16'],	# Opava, station Krnov
#    ['pod1','19'],	# Opava, station Opava
#    ['pod1','20'],	# Opava, station Děhylov
#    ['pod1','24'],	# Opava, station Karlovice
#    ['pod1','17'],	# Opavice, station Krnov
#    ['pod1','23'],	# Osoblaha, station Osoblaha
#    ['pod1','54'],	# Podolský potok, station Rýmařov
#    ['pod1','49'],	# Sedlnice, station Sedlnice
#    ['pod1','57'],	# Sezina, station Bravantice
#    ['pod1','60'],	# Staříč, station Lipová-lázně
#    ['pod1','55'],	# Tichávka, station Tichá
#    ['pod1','22'],	# Vidnávka, station Vidnava
#    ['pod1','59'],	# Zlatý potok, station Zlaté Hory
#    ['pod1','47'],	# Černá Opava, station Mnichov
#    ['pod1','25'],	# Černý potok, station Mezina
#    ['pod2','35'],	# Baštice, station Baška
#    ['pod2','51'],	# Lomná, station Jablunkov Lomná
#    ['pod2','05'],	# Lučina, station Žermanice
#    ['pod2','36'],	# Lučina, station Bludovice
#    ['pod2','40'],	# Lučina, station Radvanice
#    ['pod2','53'],	# Mohelnice, station Raškovice
#    ['pod2','02'],	# Morávka, station Morávka
#    ['pod2','39'],	# Morávka, station Vyšní Lhoty
#    ['pod2','38'],	# Morávka (přítok), station Morávka
#    ['pod2','12'],	# Odra, station Svinov
#    ['pod2','13'],	# Odra, station Bohumín
#    ['pod2','37'],	# Olešná, station Olešná
#    ['pod2','50'],	# Olešná, station Palkovice
#    ['pod2','06'],	# Olše, station Jablunkov
#    ['pod2','07'],	# Olše, station Český Těšín
#    ['pod2','09'],	# Olše, station Věřňovice
#    ['pod2','43'],	# Olše, station Dětmarovice
#    ['pod2','01'],	# Ostravice, station Šance
#    ['pod2','03'],	# Ostravice, station Frýdek Místek
#    ['pod2','04'],	# Ostravice, station Ostrava
#    ['pod2','33'],	# Ostravice, station Staré Hamry
#    ['pod2','45'],	# Petrůvka, station Zebrzydowice
#    ['pod2','44'],	# Porubka, station Vřesina
#    ['pod2','41'],	# Ropičanka, station Smilovice
#    ['pod2','08'],	# Stonávka, station Těrlicko
#    ['pod2','42'],	# Stonávka, station Hradiště
#    ['pod2','34'],	# Čeladenka, station Čeladná
#    ['poh1','1430'],	# Bystřice, station Ostrov
#    ['poh1','1409'],	# Libocký potok, station Horka - odtok
#    ['poh1','1426'],	# Lomnický potok, station Stanovice - odtok
#    ['poh1','1994'],	# Odrava, station Jesenice - odtok
#    ['poh1','1404'],	# Ohře, station Cheb
#    ['poh1','1410'],	# Ohře, station Citice
#    ['poh1','1429'],	# Ohře, station Drahovice
#    ['poh1','1417'],	# Rolava, station Stará Role
#    ['poh1','1411'],	# Svatava, station Kraslice
#    ['poh1','1414'],	# Svatava, station Svatava
#    ['poh1','1419'],	# Teplá, station Podhora
#    ['poh1','1422'],	# Teplá, station Teplička
#    ['poh1','1423'],	# Teplá, station Březová - odtok
#    ['poh1','1427'],	# Teplá, station Jánský most
#    ['poh2','2423'],	# Bouřlivec, station Všechlapy - odtok
#    ['poh2','2414'],	# Bílina, station Újezd - odtok
#    ['poh2','2424'],	# Bílina, station Trmice
#    ['poh2','2443'],	# Bílina, station Jirkov - odtok
#    ['poh2','2473'],	# Bílina, station Bílina ČD
#    ['poh2','2449'],	# Bílý potok, station Bílý potok
#    ['poh2','2439'],	# Chomutovka, station III.mlýn
#    ['poh2','2475'],	# Chomutovka, station Chomutov MěÚ
#    ['poh2','2448'],	# Flájský potok, station Český Jiřetín
#    ['poh2','2407'],	# Hačka, station Hačka pod odlehčením
#    ['poh2','2446'],	# Loupnice, station Janov - odtok
#    ['poh2','2401'],	# Ohře, station Klášterec nad Ohří
#    ['poh2','2404'],	# Ohře, station Stranná
#    ['poh2','2433'],	# Přísečnice, station Přísečnice - odtok
#    ['poh3','3412'],	# Chřibská Kamenice, station Chřibská - odtok
#    ['poh3','3422'],	# Kamenice, station Srbská Kamenice
#    ['poh3','3424'],	# Mandava, station Varnsdorf
#    ['poh3','3401'],	# Ohře, station Žatec
#    ['poh3','3402'],	# Ohře, station Louny
#    ['poh3','3403'],	# Ohře, station Brozany
#    ['poh3','3426'],	# Paneský potok, station Pertoltice
#    ['poh3','3407'],	# Ploučnice, station Stráž pod Ralskem - město
#    ['poh3','3408'],	# Ploučnice, station Mimoň
#    ['poh3','3409'],	# Ploučnice, station Česká Lípa
#    ['poh3','3410'],	# Ploučnice, station Benešov nad Ploučnicí
#    ['poh3','3428'],	# Robečský potok, station Zahrádky
#    ['poh3','3421'],	# Svitávka, station Zákupy
#    ['poh3','3425'],	# Úštěcký potok, station Vědlice
#    ['pvl1','BPLL'],	# Bezdrevský potok, station Lékařova Lhota
#    ['pvl1','BPNE'],	# Bezdrevský potok, station Netolice
#    ['pvl1','BLBA'],	# Blanice, station Bavorov
#    ['pvl1','BLBM'],	# Blanice, station Blanický mlýn
#    ['pvl1','BLHE'],	# Blanice, station Heřmaň
#    ['pvl1','BLHS'],	# Blanice, station odtok VD Husinec
#    ['pvl1','BLPO'],	# Blanice, station Podedvorský mlýn
#    ['pvl1','BLPR'],	# Blanice, station Protivín
#    ['pvl1','SKHO'],	# Braunaubach (Skřemelice), station Hoheneich
#    ['pvl1','BPKO'],	# Bílinský potok, station Koloděje B
#    ['pvl1','CPCV'],	# Chvalšinský potok, station Chvalšiny
#    ['pvl1','DRKL'],	# Dračice, station Klikov
#    ['pvl1','DRNB'],	# Dračice, station Nová Bystřice
#    ['pvl1','DUDL'],	# Dubský potok, station Dubská Lhota
#    ['pvl1','HAAN'],	# Hamerský potok, station Antýgl
#    ['pvl1','HPOL'],	# Hamerský potok, station Oldříš
#    ['pvl1','KPKH'],	# Koštěnický potok, station Kosky-Hamr
#    ['pvl1','KRST'],	# Křemelná, station Stodůlky
#    ['pvl1','KPBR'],	# Křemžský potok, station Brloh
#    ['pvl1','LUEH'],	# Lainsitz (Lužnice), station Ehrendorf
#    ['pvl1','LOBL'],	# Lomnice, station Blatná
#    ['pvl1','LODO'],	# Lomnice, station Dolní Ostrovec
#    ['pvl1','LOPR'],	# Lomnice, station Předmíř
#    ['pvl1','LUBE'],	# Lužnice, station Bechyně
#    ['pvl1','LUFR'],	# Lužnice, station Frahelž
#    ['pvl1','LUKA'],	# Lužnice, station Kazdovna
#    ['pvl1','LUKL'],	# Lužnice, station Klenovice
#    ['pvl1','LUNV'],	# Lužnice, station Nová Ves
#    ['pvl1','LUPI'],	# Lužnice, station Pilař
#    ['pvl1','LURZ'],	# Lužnice, station Rožmberk
#    ['pvl1','MAKA'],	# Malše, station Kaplice
#    ['pvl1','MALE'],	# Malše, station Leopoldschlag
#    ['pvl1','MAPO'],	# Malše, station Pořešín
#    ['pvl1','MARE'],	# Malše, station Plav-Rechle
#    ['pvl1','MARM'],	# Malše, station Římov
#    ['pvl1','MARO'],	# Malše, station Roudné
#    ['pvl1','MPMI'],	# Milevský potok, station Milevsko
#    ['pvl1','MNHZ'],	# Mlýnský potok, station Horažďovice-Zářečí
#    ['pvl1','NEHA'],	# Nežárka, station Hamr
#    ['pvl1','NELA'],	# Nežárka, station Lásenice
#    ['pvl1','NERO'],	# Nežárka, station Rodvínov
#    ['pvl1','NRML'],	# Nová řeka, station Mláka
#    ['pvl1','OSKO'],	# Ostružná, station Kolínec
#    ['pvl1','OTHO'],	# Otava, station Horažďovice
#    ['pvl1','OTKA'],	# Otava, station Katovice
#    ['pvl1','OTPI'],	# Otava, station Písek
#    ['pvl1','OTRE'],	# Otava, station Rejštejn
#    ['pvl1','OTST'],	# Otava, station Strakonice
#    ['pvl1','OTSU'],	# Otava, station Sušice
#    ['pvl1','OTTO'],	# Otava, station Topělec
#    ['pvl1','POCK'],	# Polečnice, station Český Krumlov
#    ['pvl1','PONO'],	# Polečnice, station Novosedly
#    ['pvl1','SKVA'],	# Skalice, station Varvažov
#    ['pvl1','SKZP'],	# Skalice, station Zadní Poříčí
#    ['pvl1','SMBO'],	# Smutná, station Božetice
#    ['pvl1','SMRA'],	# Smutná, station Rataje
#    ['pvl1','SPBO'],	# Spůlka, station Bohumilice
#    ['pvl1','SCBO'],	# Stropnice, station Borovany
#    ['pvl1','SCHM'],	# Stropnice, station odtok VD Humenice
#    ['pvl1','SCHS'],	# Stropnice, station Horní Stropnice
#    ['pvl1','SCPA'],	# Stropnice, station Pašínovice-Komařice
#    ['pvl1','SPHP'],	# Studenský potok, station Horní Pole
#    ['pvl1','SVCK'],	# Studená Vltava, station Černý Kříž
#    ['pvl1','TVCH'],	# Teplá Vltava, station Chlum
#    ['pvl1','TVLE'],	# Teplá Vltava, station Lenora
#    ['pvl1','TVSM'],	# Teplá Vltava, station Soumarský most
#    ['pvl1','VLBR'],	# Vltava, station Březí
#    ['pvl1','VLCB'],	# Vltava, station České Budějovice
#    ['pvl1','VLHN'],	# Vltava, station odtok VD Hněvkovice
#    ['pvl1','VLKO'],	# Vltava, station odtok VD Kořensko
#    ['pvl1','VLKS'],	# Vltava, station Spolí
#    ['pvl1','VLVB'],	# Vltava, station Vyšší Brod
#    ['pvl1','VLZA'],	# Vltava, station Zátoň
#    ['pvl1','VONE'],	# Volyňka, station Němětice
#    ['pvl1','VOSU'],	# Volyňka, station Sudslavice
#    ['pvl1','VYMO'],	# Vydra, station Modrava
#    ['pvl1','ZPBO'],	# Zborovský potok, station Borovnice
#    ['pvl1','ZSPI'],	# Zlatá stoka, station Pilař-Zlatá stoka
#    ['pvl1','ZPHR'],	# Zlatý potok, station Hracholusky
#    ['pvl1','CPTU'],	# Černovický potok, station Tučapy
#    ['pvl1','CRLC'],	# Černá, station Líčov
#    ['pvl1','RCOT'],	# Řečička, station Otín
#    ['pvl1','ZPPR'],	# Živný potok, station Prachatice
#    ['pvl2','BPVE'],	# Bakovský potok, station Velvary
#    ['pvl2','BERA'],	# Berounka, station Praha - Radotín - lávka
#    ['pvl2','BLLO'],	# Blanice, station Louňovice
#    ['pvl2','BLRA'],	# Blanice, station Radonice - Zdebudeves
#    ['pvl2','BPBL'],	# Blažejovický potok, station Blažejovice
#    ['pvl2','BPSH'],	# Borovský potok, station Stříbrné Hory
#    ['pvl2','BRHR'],	# Brzina, station Hrachov
#    ['pvl2','BARA'],	# Bělá, station Radětín
#    ['pvl2','CPVL'],	# Cerekevský potok, station Vlásenice
#    ['pvl2','CHSL'],	# Chotýšanka, station Slověnice
#    ['pvl2','DPPR'],	# Dobřejovický potok, station Průhonice D
#    ['pvl2','JPMI'],	# Jankovský potok, station Milotice
#    ['pvl2','KPPA'],	# Kejtovský potok, station Pacov
#    ['pvl2','KOST'],	# Kocába, station Štěchovice
#    ['pvl2','KPPO'],	# Konopišťský potok (Bystrá), station Poříčí nad Sázavou
#    ['pvl2','LPOL'],	# Lučický potok, station Olešnice u Okrouhlice
#    ['pvl2','MPSE'],	# Martinický potok, station Senožaty
#    ['pvl2','MSRA'],	# Mastník, station Radíč
#    ['pvl2','OCPO'],	# Ochozský potok, station Polná
#    ['pvl2','RPPR'],	# Radotínský potok, station Praha - Radotín
#    ['pvl2','SPJE'],	# Sedlecký potok, station Jesenice u Sedlčan
#    ['pvl2','SPLM'],	# Sedlický potok, station Leský mlýn
#    ['pvl2','SACH'],	# Sázava, station Chlístov
#    ['pvl2','SACS'],	# Sázava, station Český Šternberk
#    ['pvl2','SAHB'],	# Sázava, station Pohledští Dvořáci - Havlíčkův Brod
#    ['pvl2','SAKA'],	# Sázava, station Kácov
#    ['pvl2','SANE'],	# Sázava, station Nespeky
#    ['pvl2','SASV'],	# Sázava, station Světlá nad Sázavou
#    ['pvl2','SASZ'],	# Sázava, station Sázava u Žďáru
#    ['pvl2','SAZD'],	# Sázava, station Žďár nad Sázavou
#    ['pvl2','SAZR'],	# Sázava, station Zruč nad Sázavou
#    ['pvl2','SZJD'],	# Sázavka, station Josefodol
#    ['pvl2','TLKR'],	# Tloskovský potok, station Krusičany
#    ['pvl2','TRCR'],	# Trnava, station Červená Řečice
#    ['pvl2','TRKO'],	# Trnava, station Želiv - Kocanda
#    ['pvl2','VLCH'],	# Vltava, station Praha - Malá Chuchle
#    ['pvl2','VLFR'],	# Vltava, station Praha - Na Františku
#    ['pvl2','VLKA'],	# Vltava, station odtok VD Kamýk
#    ['pvl2','VLOR'],	# Vltava, station odtok VD Orlík
#    ['pvl2','VLPB'],	# Vltava, station Praha - Bradáč
#    ['pvl2','VLSL'],	# Vltava, station odtok VD Slapy
#    ['pvl2','VLST'],	# Vltava, station odtok VD Štěchovice
#    ['pvl2','VLVE'],	# Vltava, station odtok VD Vrané
#    ['pvl2','VLVX'],	# Vltava, station Vraňany
#    ['pvl2','VLZB'],	# Vltava, station Zbraslav
#    ['pvl2','UPTU'],	# Únětický potok, station Tuchoměřice
#    ['pvl2','RIBE'],	# Říčanka, station Praha - Běchovice
#    ['pvl2','SLMI'],	# Šlapanka, station Mírovka
#    ['pvl2','HECA'],	# Želivka, station Čakovice
#    ['pvl2','HEKO'],	# Želivka, station Kojčice
#    ['pvl2','ZEPO'],	# Želivka, station Poříčí
#    ['pvl2','ZESO'],	# Želivka, station Soutice
#    ['pvl2','ZEVR'],	# Želivka, station Želiv-Vřesník
#    ['pvl3','BEBE'],	# Berounka, station Beroun B
#    ['pvl3','BECE'],	# Berounka, station VD Černošice
#    ['pvl3','BELI'],	# Berounka, station Liblín
#    ['pvl3','BEPL'],	# Berounka, station Plzeň-Bílá Hora
#    ['pvl3','BESR'],	# Berounka, station Srbsko
#    ['pvl3','BEZB'],	# Berounka, station Zbečno
#    ['pvl3','BRZA'],	# Bradava, station Žákava
#    ['pvl3','BBDB'],	# Bělá, station Dolní Bělá
#    ['pvl3','CMLI'],	# Chumava, station Libomyšl
#    ['pvl3','DPKL'],	# Drnový potok, station Klatovy
#    ['pvl3','DPNE'],	# Drnový potok, station Vrhaveč
#    ['pvl3','HPPL'],	# Hamerský potok, station Planá
#    ['pvl3','HPRO'],	# Holoubkovský potok, station Rokycany-Dvořákova
#    ['pvl3','JEJA'],	# Jelenka, station Janovice nad Úhlavou
#    ['pvl3','KLHA'],	# Klabava, station Hrádek u Rokycan
#    ['pvl3','KLKB'],	# Klabava, station odtok VD Klabava
#    ['pvl3','KLNH'],	# Klabava, station Nová Huť
#    ['pvl3','KLRO'],	# Klabava, station Rokycany-Na Pátku
#    ['pvl3','KLST'],	# Klabava, station Strašice
#    ['pvl3','KCKL'],	# Klíčava, station odtok VD Klíčava
#    ['pvl3','KCLM'],	# Klíčava, station Lány-Městečko
#    ['pvl3','KPCO'],	# Kosový potok, station Chotěnov
#    ['pvl3','KPST'],	# Kosový potok, station Svahy-Třebel
#    ['pvl3','LIBE'],	# Litavka, station Beroun L
#    ['pvl3','LICE'],	# Litavka, station Čenkov
#    ['pvl3','LILZ'],	# Litavka, station odtok VD Láz
#    ['pvl3','LIPR'],	# Litavka, station Příbram
#    ['pvl3','LDLD'],	# Loděnice, station Loděnice
#    ['pvl3','LPMY'],	# Lužní potok, station Mýto
#    ['pvl3','LPLB'],	# Lánský potok, station Lány-Běleč
#    ['pvl3','MEUJ'],	# Merklínka, station Újezdec
#    ['pvl3','MPSO'],	# Mochtínský potok, station Sobětice
#    ['pvl3','MZHY'],	# Mže, station odtok VD Hracholusky
#    ['pvl3','MZKO'],	# Mže, station Kočov
#    ['pvl3','MZLC'],	# Mže, station odtok VD Lučina
#    ['pvl3','MZOB'],	# Mže, station Obora M
#    ['pvl3','MZST'],	# Mže, station Stříbro M
#    ['pvl3','OPOC'],	# Obecnický potok, station Obecnice
#    ['pvl3','PIZA'],	# Pivoňka, station Šitboř
#    ['pvl3','PODO'],	# Poleňka, station Dolany
#    ['pvl3','RALH'],	# Radbuza, station Lhota
#    ['pvl3','RAST'],	# Radbuza, station Staňkov
#    ['pvl3','RATA'],	# Radbuza, station Tasnovice
#    ['pvl3','RAUD'],	# Radbuza, station odtok VD České Údolí
#    ['pvl3','RPRK'],	# Rakovnický potok, station Rakovník
#    ['pvl3','RPRA'],	# Ratibořský potok, station Ratiboř
#    ['pvl3','SPOB'],	# Sklářský potok, station Obora S
#    ['pvl3','SPMI'],	# Skořický potok, station Mirošov
#    ['pvl3','SPHV'],	# Stroupinský potok, station Hředle
#    ['pvl3','STCI'],	# Střela, station Čichořice
#    ['pvl3','STPL'],	# Střela, station Plasy
#    ['pvl3','STSO'],	# Střela, station Sovolusky
#    ['pvl3','STZC'],	# Střela, station odtok VD Žlutice
#    ['pvl3','SPHA'],	# Svinský potok, station Hamry S
#    ['pvl3','TPVI'],	# Točnický potok, station Vicenice
#    ['pvl3','TRNE'],	# Třemošná, station Nevřeň
#    ['pvl3','VPPS'],	# Vejprnický potok, station Skvrňany
#    ['pvl3','ZPZL'],	# Zelenský potok, station Zelená Lhota
#    ['pvl3','ZUDO'],	# Zubřina, station Domažlice
#    ['pvl3','UHHA'],	# Úhlava, station Hamry U
#    ['pvl3','UHJI'],	# Úhlava, station Jíno
#    ['pvl3','UHKL'],	# Úhlava, station Klatovy-Tajanov
#    ['pvl3','UHPR'],	# Úhlava, station Přeštice
#    ['pvl3','UHSL'],	# Úhlava, station odtok VD Nýrsko
#    ['pvl3','UHST'],	# Úhlava, station Štěnovice
#    ['pvl3','UKST'],	# Úhlavka, station Stříbro U
#    ['pvl3','USKO'],	# Úslava, station Plzeň-Koterov
#    ['pvl3','USPR'],	# Úslava, station Prádlo
#    ['pvl3','USZD'],	# Úslava, station Ždírec
#    ['pvl3','UPTR'],	# Úterský potok, station Trpisty
#    ['pvl3','CEKL'],	# Černý potok, station Klenčí
#    ['pvl3','CPHO'],	# Červený potok, station Hořovice
#    ['pvl3','REAL'],	# Řezná, station Alžbětín
#    ['pvl3','SPOO'],	# Ševcovský potok, station Obora V
#]

