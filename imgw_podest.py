#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
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


# TODO: sprawdzanie, dla których wodowskazów możemy czytać komunikaty 

import os
import urllib
import re
import unicodedata

import pl.pl as lang

def format(string):
    return unicodedata.normalize('NFKD', unicode(string.replace('ł','l').replace('Ł','l'), 'utf-8')).\
        encode('ascii','ignore').strip().lower().\
        replace(' ', '_').replace('-','_').replace('.','')

wodowskazy={}

_wodowskaz=re.compile('Stacja\:\ (.{1,}?)\<')
_rzeka=re.compile('Rzeka\:\ (.{1,}?)\<')
_stan=re.compile('Stan\ Wody\ H\ \[cm\]\:\ (.{1,}?)\<')
_nnw=re.compile('NNW\:(\d{1,})')
_ssw=re.compile('SSW\:(\d{1,})')
_www=re.compile('WWW\:(\d{1,})')
_przeplyw=re.compile('Przepływ\ Q\ \[m3/s\]:\ (.{1,}?)\<')
_czas=re.compile('Czas\(UTC\)\:\ (\d{4}-\d{2}-\d{2}\ \d{2}\:\d{2}\:\d{2})')

_przekroczenieStanu=re.compile('stan\ (ostrzegawczy|alarmowy)')
_przekroczenieStanuStan=re.compile('stan\ (?:ostrzegawczy|alarmowy)\</b\>\ \((\d{1,})cm\)')

def getFile(url):
    webFile = urllib.urlopen(url)
    contents = webFile.read()
    webFile.close()
    return contents

def flatten(x): # przerobić na lambda?
    """flatten(table) -> table[0] or None"""
    if x==[]:
        return None
    else:
        return x[0]

def zaladujRegion(region):
    """Funckcja służy do pobierania listy dostępnych wodowskazów ze strony IMGW
    dla danego regionu.


    Korzystamy tutaj z faktu, że 1. Hash tables w JS mają składnię identyczną do pythonowych
    słowników; 2. W pliku są 2 słowniki a nas interesuje tylko pierwszy; 3. Python potrafi 
    interpretować sam siebie :)"""

    global wodowskazy

    try:
        debug.log("IMGW-HYDRO", 'Pobieram dane dla regionu %s'%region)
        dane = getFile('http://www.pogodynka.pl/http/assets/products/podest/podest/hydro/mapy/dane%s.js'%str(region))
        debug.log("IMGW-HYDRO", 'Przetwarzam...')
        # NOTE: teraz trochę zabawnych rzeczy: następna linijka zadziała poprawnie tylko wtedy,
        # kiedy w następnej będzie coś w rodzaju "print"
        # wodowskazy.update(eval('{'+dane.split('{')[1].split('}')[0]+'}'))
        # print wodowskazy
        # próbujemy inaczej:
        wodowskazy = dict(eval('{'+dane.split('{')[1].split('}')[0]+'}'), **wodowskazy)
    except:
        debug.log("IMGW-HYDRO", 'Nie udało się pobrać danych o wodowskazach dla regionu %s'%region, buglevel=6)
        pass
    
def pobierzDaneWodowskazu(wodowskaz):
    global wodowskazy
    if '.' in wodowskaz:
        wodowskaz = wodowskaz.split('.')[1] # pozbywamy się numeru regionu
    dane = wodowskazy[wodowskaz] # po co cały czas mieszać słownikiem
    
    return {'numer':wodowskaz,
        'nazwa':flatten(_wodowskaz.findall(dane)),
        'rzeka':flatten(_rzeka.findall(dane)).split('->')[0],
        'stan':flatten(_stan.findall(dane)),
        'nnw':flatten(_nnw.findall(dane)),
        'ssw':flatten(_ssw.findall(dane)),
        'www':flatten(_www.findall(dane)),
        'przeplyw':flatten(_przeplyw.findall(dane)),
        'czas':flatten(_czas.findall(dane)),
        'przekroczenieStanu':flatten(_przekroczenieStanu.findall(dane)),
        'przekroczenieStanuStan':flatten(_przekroczenieStanuStan.findall(dane)),}

def getData(l):
    data = {"data":"", "needCTCSS":False, "allOK":True}

    stanyOstrzegawcze = {}
    stanyAlarmowe = {}

    # Sprawdzenie w config jakie regiony będziemy spawdzać. Wodowskazy zapisane
    # są jako region.wodowskaz, np. rzeka Bystrzyca wodowskaz Jarnołtów będzie
    # zapisany jako 3.151160190. Ładujemy regiony

    zaladowaneRegiony = []
    for wodowskaz in config.wodowskazy:
        region = wodowskaz.split('.')[0]
        if region not in zaladowaneRegiony:
            zaladujRegion(region)
            zaladowaneRegiony.append(region)
        w = pobierzDaneWodowskazu(wodowskaz)
        
        # Chłyt debugowy sprawdzjący, czy mamy wszytkie sample: wszystkie rzeki
        # przełączamy na stan ostrzegawczy -- nie zapomnij wyłączyć!
        #w['przekroczenieStanu']='alarmowy'
        # Koniec chłytu

        # Repolonizacja nazw rzek:
        if w['nazwa'] == 'Kudowa Zdrój - Zakrze':
            w['nazwa']='kudowa_zdroj_zakrze'
        elif w['nazwa']=='Opole - Groszowice':
            w['nazwa']='opole_groszowice'
        elif w['nazwa']=='Ślęża':
            w['nazwa']='slez_a'

        if w['przekroczenieStanu']=='ostrzegawczy':
            if not stanyOstrzegawcze.has_key(w['rzeka']):
                stanyOstrzegawcze[w['rzeka']]=[w['nazwa']]
            else:
                stanyOstrzegawcze[w['rzeka']].append(w['nazwa'])
        elif w['przekroczenieStanu']=='alarmowy':
            if not stanyAlarmowe.has_key(w['rzeka']):
                stanyAlarmowe[w['rzeka']]=[w['nazwa']]
            else:
                stanyAlarmowe[w['rzeka']].append(w['nazwa'])


#            stanyOstrzegawcze+=' wodowskaz %s %s'%(w['rzeka'],format(w['nazwa']),)
#        elif w['przekroczenieStanu']=='alarmowy':
#            stanyAlarmowe+=' rzeka %s wodowskaz %s'%(w['rzeka'],format(w['nazwa']),)

    if stanyOstrzegawcze!={} or stanyAlarmowe!={}:
        data['data'] += 'komunikat_hydrologiczny_imgw _ '

        if stanyAlarmowe!={}:
            # Sprawdzenie dla których wodowskazów mamy przekroczone 
            # stany alarmowe -- włącz ctcss
            data['needCTCSS']=True
            data['data']+=' przekroczenia_stanow_alarmowych '
            for rzeka in sorted(stanyAlarmowe.keys()):
                data['data']+='rzeka %s wodowskaz %s '%(format(rzeka), \
                    " wodowskaz ".join([format(w) for w in sorted(stanyAlarmowe[rzeka])]),)

        if stanyOstrzegawcze!={}:
            data['data']+='_ przekroczenia_stanow_ostrzegawczych '
            for rzeka in sorted(stanyOstrzegawcze.keys()):
                data['data']+='rzeka %s wodowskaz %s '%(format(rzeka), \
                    " wodowskaz ".join([format(w) for w in sorted(stanyOstrzegawcze[rzeka])]),)


    debug.log("IMGW-HYDRO", "finished...")

    return data

def show_help():
    print u"""
Lista wodowskazów danej zlewni dostępna po podaniu parametru:

 1. Zlewnia Sanu
 2. Zlewnia Górnej Wisły
 3. Zlewnia Górnej Odry
 4. Zlewnia górej Odry i środkowej Odry
 5. Zlewnia Bugu
 6. Zlewnia Środkowej Wisły
 7. Zlewnia Warty do Poznania
 8. Zlewnia Noteci
 9. Zlewnia Nawii
10. Zlewnia Zalewu Wiślenego
11. Zlewnia Dolnej Wisły do Torunia
12. Zlewnia Dolnej Wisły od Torunia
13. Zlewnia rzek przymorza i Zalewu Gdańskiego
14. Zlewnia dolnej Odry do Kostrzynia i zalewu Szczecińskiego

Mapę zlewni można zobaczyć na stronie:
http://www.pogodynka.pl/polska/podest/"""


def podajListeWodowskazow(region):
    for wodowskaz in wodowskazy.keys():
        w = pobierzDaneWodowskazu(wodowskaz)
        print "'%s.%s',   # Nazwa: %s, rzeka: %s"%(str(region), w['numer'], w['nazwa'], w['rzeka'])

if __name__ == '__main__':
    class DummyDebug:
        def log(self,module,message,buglevel=None):
            print message

    debug = DummyDebug()
    import sys
    if len(sys.argv)==2 and int(sys.argv[1]) in range(1,14+1):
        zaladujRegion(int(sys.argv[1]))
        podajListeWodowskazow(int(sys.argv[1]))
    else:
        show_help()
else:
    import debug
    from config import imgw_podest as config
