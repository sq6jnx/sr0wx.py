# -*- coding: utf-8 -*-
# 
#   Copyright 2009-2011 Michal Sadowski (sq6jnx at hamradio dot pl)
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
# BUT: this packahe **must** define the following functions:
# * ``direction()`` which "translates" direction given by letters into
#    its word representation
# * ``removeDiacritics()`` which removes diacritics
# * ``readISODT()`` "translates" date and time into its word representation
# * ``cardinal()``  which changes numbers into words (1 -> one)
#
# As you probably can see all of these functions are language-dependant.
#
# ======================
# Implementation example
# ======================
#
# Here is implementation example for Polish language. Polish is interresting
# because it uses diacritics and 7 (seven) gramatical cases[#]_ (among many
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
# So, if somewhere in programme variable's value or function returnes 
# ie. *windy* it should be regarded as a *filename*, ``windy.ogg``.
#
# Beware too short words, it will be like machine gun rapid fire or
# will sound like a cyborg from old, cheap sci-fi movie. IMO the good way
# is to record longer phrases, like *"the temperature is"*, save it as
# ``the_temperature_is.ogg`` and use it's filename (``the_temperature_is``)
# as a return value.
#
# This dictionary is used by all SR0WX modules.

fake_gettext = lambda(s): s
_ = fake_gettext

# Units and grammar cases
hrs = ["","godziny","godzin"]
hPa = ["hektopaskal", "hektopaskale", "hektopaskali"]
percent = [u"procent",u"procent",u"procent"]
mPs    = ["metr_na_sekunde", "metry_na_sekunde", "metrow_na_sekunde"]
windStrength  = "sila_wiatru"
deg = [u"stopien","stopnie","stopni"]
C   = ["stopien_celsjusza", "stopnie_celsjusza", "stopni_celsjusza"]
km  = ["kilometr", "kilometry", u"kilometrow"]
mns = ["minuta","minuty","minut"]
tendention = ['tendencja_spadkowa','', 'tendencja_wzrostowa']


# We need also local names for directions to convert two- or three letters
# long wind direction into words (first is used as prefix, second as suffix):
directions = { "N": ("północno ",   "północny"),
               "E": ("wschodnio ",  "wschodni"),
               "W": ("zachodnio ",  "zachodni"),
               "S": ("południowo ", "południowy") }

# numbers
jednostkiM = [u""] + u"jeden dwa trzy cztery pięć sześć siedem osiem dziewięć".split()
jednostkiF = [u""] + u"jedną dwie trzy cztery pięć sześć siedem osiem dziewięć".split()
dziesiatki = [u""] + u"""dziesięć dwadzieścia  trzydzieści czterdzieści
     pięćdziesiąt sześćdziesiąt siedemdziesiąt osiemdziesiąt dziewięćdziesiąt""".split()
nastki = u"""dziesięć jedenaście dwanaście trzynaście czternaście piętnaście
        szesnaście siedemnaście osiemnaście dziewiętnaście""".split()
setki = [u""]+ u"""sto dwieście trzysta czterysta pięćset sześćset siedemset osiemset
              dziewięćset""".split()

ws=u"""x x x
   tysiąc tysiące tysięcy
   milion miliony milionów
   miliard miliardy miliardów
   bilion biliony bilionów"""
wielkie = [ l.split() for l in ws.split('\n') ]

##zlotowki=u"""złoty złote złotych""".split()
##grosze=u"""grosz grosze groszy""".split()

# There are also some functions, by dowgird, so I haven't even looked into
# them.

def _slownie3cyfry(liczba, plec='M'):
    if plec=='M':
        jednostki = jednostkiM
    else:
        jednostki = jednostkiF

    je = liczba % 10
    dz = (liczba//10) % 10
    se = (liczba//100) % 10
    slowa=[]

    if se>0:
        slowa.append(setki[se])
    if dz==1:
        slowa.append(nastki[je])
    else:
        if dz>0:
            slowa.append(dziesiatki[dz])
        if je>0:
            slowa.append(jednostki[je])
    retval = " ".join(slowa)
    return retval

def _przypadek(liczba):
    je = liczba % 10
    dz = (liczba//10)  % 10

    if liczba == 1:
        typ = 0       #jeden tysiąc"
    elif dz==1 and je>1:  # naście tysięcy
        typ = 2
    elif  2<=je<=4:
        typ = 1       # [k-dziesiąt/set] [dwa/trzy/czery] tysiące
    else:
        typ = 2       # x tysięcy

    return typ

def lslownie(liczba, plec='M'):
    """Liczba całkowita słownie"""
    trojki = []
    if liczba==0:
        return u'zero'
    while liczba>0:
        trojki.append(liczba % 1000)
        liczba = liczba // 1000
    slowa = []
    for i,n in enumerate(trojki):
        if n>0:
            if i>0:
                p = _przypadek(n)
                w = wielkie[i][p]
                slowa.append(_slownie3cyfry(n, plec)+u" "+w)
            else:
                slowa.append(_slownie3cyfry(n, plec))
    slowa.reverse()
    return ' '.join(slowa)

def cosslownie(liczba,cos, plec='M'):
    """Słownie "ileś cosiów"

    liczba - int
    cos - tablica przypadków [coś, cosie, cosiów]"""
    #print liczba
    #print cos[_przypadek(liczba)]
    return lslownie(liczba, plec)+" " + cos[_przypadek(liczba)]

##def kwotaslownie(liczba, format = 0):
##    """Słownie złotych, groszy.
##
##    liczba - float, liczba złotych z groszami po przecinku
##    format - jesli 0, to grosze w postaci xx/100, słownie w p. przypadku
##    """
##    lzlotych = int(liczba)
##    lgroszy = int (liczba * 100 + 0.5 ) % 100
##    if format!=0:
##        groszslownie = cosslownie(lgroszy, grosze)
##    else:
##        groszslownie = '%d/100' % lgroszy
##    return cosslownie(lzlotych, przypzl) + u" " +  groszslownie
##

# As you remember, ``cardinal()`` must be defined, this is the function which
# will be used by SR0WX modules. This functions was also written by dowgrid,
# modified by me. (Is function's name proper?)
def cardinal(no, units=[u"",u"",u""], gender='M'):
    """Zamienia liczbę zapisaną cyframi na zapis słowny, opcjonalnie z jednostkami
w odpowiednim przypadku. Obsługuje liczby ujemne."""
    if no<0:
        return (u"minus " + cosslownie(-no, units, plec=gender)).replace(u"jeden tysiąc", u"tysiąc",1).encode("utf-8")
    else:
        return cosslownie(no, units, plec=gender).replace(u"jeden tysiąc", u"tysiąc",1).encode("utf-8")

# This one tiny simply removes diactrics (lower case only). This function
# must be defined even if your language doesn't use diactrics (like English),
# for example as a simple ``return text``.
def removeDiacritics(text):
    return text.replace("ą","a").replace("ć","c").replace("ę","e").\
        replace("ł","l").replace("ń","n").replace("ó","o").replace("ś","s").\
        replace("ź","z").replace("ż","z")

# The last one changes ISO structured date time into word representation.
# It doesn't return year value.
def readISODT(ISODT):
    _rv=() # return value
    y,m,d,hh,mm,ss= ( int(ISODT[0:4]),   int(ISODT[5:7]),   int(ISODT[8:10]),
                      int(ISODT[11:13]), int(ISODT[14:16]), int(ISODT[17:19]) )

    # miesiąc
    _M = ["","stycznia","lutego","marca","kwietnia","maja","czerwca","lipca",
         "sierpnia","września","października","listopada","grudnia"]
    Mslownie = _M[m]
    # dzień
    _j = ["","pierwszego","drugiego","trzeciego","czwartego","piątego","szóstego",
        "siódmego","ósmego","dziewiątego","dziesiątego","jedenastego",
        "dwunastego","trzynastego","czternastego","piętnastego","szesnastego",
        "siedemnastego","osiemnastego","dziewiętnastego"]
    _d = ["","","dwudziestego","trzydziestego"]

    if d<20: Dslownie = _j[d]
    else: Dslownie = " ".join( (_d[d/10], _j[d%10]) )

    _j = ["zero","pierwsza","druga","trzecia","czwarta","piąta","szósta",
          "siódma","ósma","dziewiąta","dziesiąta","jedenasta","dwunasta",
          "trzynasta","czternasta","piętnasta","szesnasta","siedemnasta",
          "osiemnasta","dziewiętnasta"]

    if hh<20: HHslownie = _j[hh]
    elif hh==20: HHslownie="dwudziesta"
    else: HHslownie = " ".join( ("dwudziesta", _j[hh%10]) )

    MMslownie = cardinal(mm).replace("zero","zero_zero")

    return " ".join( (Dslownie, Mslownie, "godzina", HHslownie, MMslownie) )

def readISODate(ISODate):
    _rv=() # return value
    y,m,d,hh,mm,ss= ( int(ISODate[0:4]),   int(ISODate[5:7]),   int(ISODate[8:10]),
                      int(ISODate[11:13]), int(ISODate[14:16]), int(ISODate[17:19]) )

    # miesiąc
    _M = ["","stycznia","lutego","marca","kwietnia","maja","czerwca","lipca",
         "sierpnia","września","października","listopada","grudnia"]
    Mslownie = _M[m]
    # dzień
    _j = ["","pierwszego","drugiego","trzeciego","czwartego","piątego","szóstego",
        "siódmego","ósmego","dziewiątego","dziesiątego","jedenastego",
        "dwunastego","trzynastego","czternastego","piętnastego","szesnastego",
        "siedemnastego","osiemnastego","dziewiętnastego"]
    _d = ["","","dwudziestego","trzydziestego"]

    if d<20: Dslownie = _j[d]
    else: Dslownie = " ".join( (_d[d/10], _j[d%10]) )

    return " ".join( (Dslownie, Mslownie) )


def readHour(dt):
    return removeDiacritics(readISODT('0000-00-00 '+str(dt.hour).rjust(2, '0')+':'+str(dt.minute).rjust(2, '0')+':00'))

def readHourLen(hour):
    ss = hour.seconds
    hh = ss/3600
    mm = (ss-hh*3600)/60
    return removeDiacritics(" ".join( (cardinal(hh, hrs, gender='F'), cardinal(mm, mns, gender='F')) ))


# ##########################################
#
# module dependant words
# #############################################

class m:
    pass

y_weather = m()
y_weather.conditions = {
'0':  _('traba_powietrzna'),            # tornado
'1':  _('burza_tropikalna'),            # tropical storm
'2':  _('huragan'),                     # hurricane
'3':  _('silne_burze'),                 # severe thunderstorms
'4':  _('burza'),                       # thunderstorms
'5':  _('deszcz snieg'),                # mixed rain and snow
'6':  _('marznace_opady deszczu'),      # mixed rain and sleet
'7':  _('marznace_opady sniegu'),       # mixed snow and sleet
'8':  _('marznace_opady deszczu'),      # freezing drizzle
'9':  _('mrzawka'),                     # drizzle
'10': _('marznacy deszcz'),             # freezing rain
'11': _('przelotne_opady deszczu'),     # showers
'12': _('przelotne_opady deszczu'),     # showers
'13': _('przelotne_opady sniegu'),      # snow flurries
'14': _('przelotne_opady sniegu'),      # light snow showers
'15': _('zawieje_i_zamiecie_sniezne'),  # blowing snow
'16': _('snieg'),                       # snow
'17': _('zamiec'),                      # hail
'18': _('snieg deszcz'),                # sleet
'19': _('pyl'),                         # dust
'20': _('mgla'),                        # foggy
'21': _('smog'),                        # haze
'22': _('smog'),                        # smoky
'23': _('silny_wiatr'),                 # blustery
'24': _('silny_wiatr'),                 # windy
'25': _('przymrozki'),                  # cold
'26': _('zachmurzenie_calkowite'),      # cloudy
'27': _('zachmurzenie_umiarkowane'),    # mostly cloudy (night)
'28': _('zachmurzenie_umiarkowane'),    # mostly cloudy (day)
'29': _('czesciowe_zachmurzenie'),      # partly cloudy (night)
'30': _('czesciowe_zachmurzenie'),      # partly cloudy (day)
'31': _('bezchmurnie'),                 # clear (night)
'32': _('bezchmurnie'),                 # sunny
'33': _('slabe zachmurzenie'),          # fair (night)
'34': _('slabe zachmurzenie'),          # fair (day)
'35': _('deszcz'),                      # mixed rain and hail
'36': _('wysokie_temperatury'),         # hot
'37': _('burza'),                       # isolated thunderstorms
'38': _('burza'),                       # scattered thunderstorms
'39': _('burza'),                       # scattered thunderstorms
'40': _('deszcz'),                      # scattered showers
'41': _('intensywne_opady sniegu'),     # heavy snow
'42': _('snieg'),                       # scattered snow showers
'43': _('intensywne_opady sniegu'),     # heavy snow
'44': _('czesciowe zachmurzenie'),      # partly cloudy
'45': _('burza'),                       # thundershowers
'46': _('mzawka'),                      # snow showers
'47': _('burze'),                       # isolated thundershowers
'3200': '',                          # not available
}
