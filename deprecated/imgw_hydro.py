#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# 
# Copyright 2009-2011 Michal Sadowski (sq6jnx at hamradio dot pl).
#  
# Future versions of this software will probably be licensed under
# some open source license, but this experimental version is not.
# Copying and distribution without the author's explicit permission.
# is not allowed.
# 
# Przyszle wersje tego oprogramowania beda prawdopodobnie udostepniane
# na jednej z open source'owych licencji, jednakze ta, eksperymentalna
# wersja nie jest. Kopiowanie i dystrybuowanie tego oprogramowania bez
# wyraznej zgody autora jest zabronione.
# 
#
# TEN MODUŁ JEST PRZESTARZAŁY A IMGW NIE PODAJE JUZ DANYCH W TYM FORMACIE
#
# NALEZY KORZYSTAC Z MODUŁU imgw_podest
#

from config import imgw_hydro as config

import os
import debug

import pl.pl as lang

# ** NOTE **
#
# This module uses links [http://links.sourceforge.net/] (text mode) 
# for downlading and pre-parsing poor HTML code.
#
# pomysl: pamietac wodowskazy i sprawdzic czy nie doszly jakies nowe

def format(string):
    return string.strip().lower().replace("ą","a").\
        replace("ć","c").replace("ę","e").replace("ł","l").\
        replace("ń","n").replace("ó","o").replace("ś","s").\
        replace("ź","z").replace("ż","z").replace(' ', '_').\
        replace('-','_').replace('.','')

def getData(l):

    data = {"data":"", "needCTCSS":True, "allOK":True}
    # Pobieranie danych o wodowskazach
    debug.log("IMGW-HYDRO", "downloading data...")
    command = 'links -dump http://pogodynka.pl/hydrobiuletyn.php > /tmp/imgw-hydro.tmp'
    if os.system(command) != 0:
        debug.log("IMGW-HYDRO", "Couldn't download data!", 6)
        return {"data":"", "needCTCSS":False, "allOK":False}

    hydroFile = open('/tmp/imgw-hydro.tmp')
    hydrobiuletyn = hydroFile.readlines()
    hydroFile.close()




    dane = []
    dostepneWodowskazy = []

    # odczyt danych z pliku (parsowanie)
    debug.log("IMGW-HYDRO", "parsing...")
    for line in hydrobiuletyn:
        if "|" in line:
            columns = line.split("|")
            if "Zbiornik" in columns[1]:
                break
            elif len(columns[2].strip())>0 and "-+-" not in columns[1]:
                if len(columns[1].strip())>0:
                    dane.append( {                          \
                        "rzeka"       : columns[1].strip(), \
                        "wodowskaz"   : columns[2].strip(), \
                        "stanAlarmowy": columns[4].strip(), \
                        "stanWody"    : columns[6].strip(), \
                        "dobowaZmiana": columns[7].strip()  \
                      })
                else: dane[-1]["wodowskaz"]+=" " + columns[2].strip()

    # czyszczenie nazw wodowskazów (z pliku i z konfiguracji) = ustawianie jednolitego formatu
    for i in range(0, len(dane)):
        dane[i]["rzeka"]    = format(dane[i]["rzeka"])
        dane[i]["wodowskaz"]= format(dane[i]["wodowskaz"])
        dostepneWodowskazy.append(dane[i]["wodowskaz"])

    # czy pojawiły się jakieś nowe wodowskazy? Jeśli tak to informacja idzie na debug
    try:
       # if os.path.isfile('/tmp/wodowskazy.tmp'):
        wodowskazyFile = open('/tmp/wodowskazy.tmp')
        zapisaneWodowskazy = wodowskazyFile.readlines()[0].split()
        noweWodowskazy = set(dostepneWodowskazy) - set(zapisaneWodowskazy)
        if len(noweWodowskazy) > 0: 
            debug.log('IMGW-HYDRO', 'nowe wodowskazy: '+" ".join( (noweWodowskazy) ),1)
    except:
        debug.log('IMGW-HYDRO', 'Nie można było porównać listy wodowskazów. Było to albo wynikiem wcześniejszych błędów albo świeżej instalacji.',1)
    finally:
        # lista dostepnych wodowskazów ląduje w pliku
        wodowskazyFile = open('/tmp/wodowskazy.tmp', 'w')
        wodowskazyFile.write(" ".join( (dostepneWodowskazy) ))
        wodowskazyFile.close()


    # jeśli w konfigu podano jakiś nieistniejący w danych wodowskaz info o tym ląduje w logu i wyświetlana jest lista poprawnych nazw wodowskazów
    if not set(config.wodowskazy).issubset(dostepneWodowskazy):
        debug.log("IMGW-HYDRO", "brak danych dla wodowskazów %s"%( set(config.wodowskazy)-set(dostepneWodowskazy) ),3)
        debug.log("IMGW-HYDRO", "dostępne wodowskazy: %s"%(" ".join( (dostepneWodowskazy) )), 1)
 
   # przy pierwszym ostrzeżeniu wyswietlany jest nagłówek
   # pierwszeOstrzezenie = True

    rzeki = {}

    for wodowskaz in config.wodowskazy:
        for linia in dane:
            if wodowskaz in linia["wodowskaz"] and 'brak' not in linia.values(): 
                if int(linia["stanWody"]) >= int(linia["stanAlarmowy"]):
                    if not rzeki.has_key(linia["rzeka"]):
                        rzeki[linia["rzeka"]]=""
                    rzeki[linia["rzeka"]] += " wodowskaz %s"%(linia["wodowskaz"])
                    if config.podajStan and len(linia["stanWody"])>0:
                        rzeki[linia["rzeka"]] += " " + lang.removeDiacritics(lang.cardinal(int(linia["stanWody"])))
                    if config.podajTendencje and len(linia["dobowaZmiana"])>0:
                        if int(linia["dobowaZmiana"])<0:
                            rzeki[linia["rzeka"]] += " tendencja_spadkowa "
                        elif int(linia["dobowaZmiana"])>0:
                            rzeki[linia["rzeka"]] += " tendencja_wzrostowa "

    # niewinny trick: jeśli było pierwsze ostrzezenie, to znaczy ze byly ostrzezenia i nalezy pod danymi podpisac IMGW
    # if rzeki != {}:
    #     data["data"] = "komunikat_hydrologiczny imgw przekroczenia_stanow_alarmowych "
    #     for rzeka in rzeki.keys():
    #         data["data"]+='rzeka ' + rzeka + rzeki[rzeka]
                        
    debug.log("IMGW-HYDRO", "finished...")

    return data

