#!/usr/env/python -tt
# -*- encoding=utf8 -*-
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

import re
import urllib
from config import prospect_mp as config
import datetime
import debug
lang=None


def bezpiecznaNazwa(s):
    """Zwraca "bezpieczną" nazwę dla nazwy danej rzeki/danego
    wodowskazu. Ze względu na to, że w Polsce zarówno płynie
    rzeka Ślęza jak i Ślęża oznaczany jest każdy niełaciński
    znak"""
    return unicode(s, 'utf-8').lower().replace(u'ą',u'a_').replace(u'ć',u'c_').\
        replace(u'ę',u'e_').replace(u'ł',u'l_').\
        replace(u'ń',u'n_').replace(u'ó',u'o_').\
        replace(u'ś',u's_').replace(u'ź',u'x_').\
        replace(u'ż',u'z_').replace(u' ',u'_').\
        replace(u'-',u'_').replace(u'(',u'').\
        replace(u')',u'')

def downloadFile(url):
    webFile = urllib.urlopen(url)
    return webFile.read()

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def last(list):
    if len(list)==0:
        return None
    else:
        return list[-1]

_przekroczenie = re.compile('(Delta)(?:(?:.{1,}?)Przekroczony\ stan\ (ostrzegawczy|alarmowy))?')

def pobierzOstrzezenia(domena,stacja):
    global przekroczenie,debug
    domena,stacja = (domena.lower(), stacja.upper())
    # testowe -- nie używać na produkcji! nie siać zamętu!
    #url = "http://www.biala.prospect.pl/wizualizacja/punkt_pomiarowy.php?"+\
    #      "prze=TUBI&rok=2010&miesiac=06&dzien=04&godzina=19&minuta=-3"
    #url = "http://www.biala.prospect.pl/wizualizacja/punkt_pomiarowy.php?"+\
    #      "prze=TUBI&rok=2010&miesiac=06&dzien=03&godzina=23&minuta=27"

    url = "http://www.%s.prospect.pl/wizualizacja/punkt_pomiarowy.php?prze=%s"%(domena,stacja)
    plik = downloadFile(url)
    wynik = _przekroczenie.findall(plik)

    try:
       if wynik[0]==('Delta', ''):
           return None
       elif wynik[0][1] in ('ostrzegawczy','alarmowy'):
           return wynik[0][1]
       else:
           debug.log('PROSPECT-MP', u'Regex nie zwrócił oczekiwanych danych')
    except:
        debug.log('PROSPECT-MP', u'Regex nie zwrócił oczekiwanych danych')
        raise


def getData(l):
    data = {"data":"", "needCTCSS":False, "allOK":True}

    stanyOstrzegawcze = {}
    stanyAlarmowe = {}

    for w in config.wodowskazy:
        try:
            domena, rzeka, wodowskaz, stacja = w
            debug.log('PROSPECT-MP', ', '.join((domena,stacja,)))
            stan = pobierzOstrzezenia(domena,stacja)
            rzeka=bezpiecznaNazwa(rzeka)
            wodowskaz=bezpiecznaNazwa(wodowskaz)

            if stan ==  'ostzegawczy':
                if not stanyOstrzegawcze.has_key(rzeka):
                    stanyOstrzegawcze[rzeka]=[wodowskaz,]
                else:
                    stanyOstrzegawcze[rzeka].append(wodowskaz)
            elif stan == 'alarmowy': 
                if not stanyAlarmowe.has_key(rzeka):
                    stanyAlarmowe[rzeka]=[wodowskaz,]
                else:
                    stanyAlarmowe[rzeka].append(wodowskaz)
        except:
            pass

        
        # Chłyt debugowy sprawdzjący, czy mamy wszytkie sample: wszystkie rzeki
        # przełączamy na stan ostrzegawczy -- nie zapomnij wyłączyć!
        #w['przekroczenieStanu']='alarmowy'
        # Koniec chłytu

    if stanyOstrzegawcze!={} or stanyAlarmowe!={}:
        data['data'] += 'lokalny_komunikat_hydrologiczny '

        if stanyAlarmowe!={}:
            # Sprawdzenie dla których wodowskazów mamy przekroczone 
            # stany alarmowe -- włącz ctcss
            data['needCTCSS']=True
            data['data']+=' przekroczenia_stanow_alarmowych '
            for rzeka in sorted(stanyAlarmowe.keys()):
                data['data']+='rzeka %s wodowskaz %s '%(rzeka, \
                    " wodowskaz ".join(sorted(stanyAlarmowe[rzeka])),)

        if stanyOstrzegawcze!={}:
            data['data']+='_ przekroczenia_stanow_ostrzegawczych '
            for rzeka in sorted(stanyOstrzegawcze.keys()):
                data['data']+='rzeka %s wodowskaz %s '%(format(rzeka), \
                    " wodowskaz ".join([format(w) for w in sorted(stanyOstrzegawcze[rzeka])]),)

    debug.log("PODEST_MP", "finished...")

    return data

def show_help():
    print u"""
Uruchamiając ten skrypt z linii komend możesz wygenerować w łatwy sposób 
fragment słownika sr0wx dla rzek i wodowskazów wskazanych w pliku config.py

Należy uruchomić prospect_mp podając jako parametr gen., np.

python prospect_mp.py gen > pl_google/prospect_mp_dict.py

a następnie

python google_tts_downloader.py prospect_mp_dict.py

aby dociągnąć niezbędne pliki."""

if __name__ == '__main__':
    class DummyDebug:
        def log(self,module,message,buglevel=None):
            pass

    debug = DummyDebug()
    import sys
    # tak, wiem, że można to zrobić bardziej elegancko (getopt), ale dla 2
    # opcji nie ma chyba sensu...
    if len(sys.argv)==2 and sys.argv[1]=='gen':
        from config import prospect_mp as config
        
        # generowanie listy słów słownika; ostatnie słowo (rozielone spacją)
        # jest nazwą pliku docelowego
	
        print """#!/usr/bin/python
# -*- coding: utf-8 -*-

# Caution! I am not responsible for using these samples. Use at your own risk
# Google, Inc. is the copyright holder of samples downloaded with this tool.

# Generated automatically by imgw_podest.py. Feel free to modify it SLIGHTLY.

LANGUAGE = 'pl'

START_MARKER = 'ę. '
END_MARKER = ' k'

CUT_START = 0.9
CUT_END=0.7

download_list = [ """

        frazy = []
        for wpis in config.wodowskazy:
            frazy.append(wpis[1])
            frazy.append(wpis[2])

        for fraza in set(frazy):
            print "\t['ę. %s', '%s'],"%(fraza, str(bezpiecznaNazwa(fraza)),)


        print """'lokalny komunikat hydrologiczny', 'przekroczenia stanów ostrzegawczych',
            'przekroczenia stanów alarmowych', 'rzeka', 'wodowskaz',"""

	print ']'
    else:
        show_help()
