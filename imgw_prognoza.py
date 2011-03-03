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

import urllib
import re
import datetime, time, pytz
from config import imgw_prognoza as config
import pl.pl as pl

import debug
    
#poczatek = """:00"""
#koniec   = """Noc"""

# read the sorce, Luke ;) http://www.pogodynka.pl/miasto.php?miasto=Wroc%B3aw&wojewodztwo=dolno%B6l%B1skie&powiat=Wroc%B3aw&gmina=Wroc%B3aw&czas=&model=Aladin , linia 529
# Muszę szczerze przyznać, że gdyby nie przypadek to w życiu bym tego tak dobrze nie rozkodował.
# Teraz wystarczy przeparsować to do wersji zgodnej z METAR/TAF, co niniejszym czynię:

zjawiskaIMGW = {
    # Bezchmurnie => 
      "n0z00": pl.clouds['SKC'],
    # Pogodnie => 
      "n1z00": pl.clouds['SKC'],
    # Pogodnie, możliwe słabe opady deszczu => 
      "n1z60": pl.clouds['SKC'] + " slaby deszcz",
    # Pogodnie, okresami wzrost zachmurzenia do umiarkowanego => 
      "n3z00": pl.clouds['SKC'],
    # Pochmurno, okresami przejaśnienia => 
      "n6z00": pl.clouds['SCT'],
    # Zachmurzenie całkowite => 
      "n8z00": pl.clouds['OVC'],
    # Zachmurzenie małe, możliwe słabe opady deszczu => 
      "n3z60": pl.clouds['FEW'] + " slaby deszcz",
    # Zachmurzenie małe, możliwe opady deszczu => 
      "n3z61": pl.clouds['FEW'] + " deszcz",
    # Pochmurno z przejaśnieniami, słabe opady deszczu => 
      "n6z60": pl.clouds['SCT'] + " slaby deszcz",
    # Pochmurno, słabe opady deszczu => 
      "n8z60": pl.clouds['BKN'] + " slaby deszcz",
    # Zachmurzenie male, możliwe słabe opady marznącego deszczu => 
      "n3z66": pl.clouds['FEW'] + " slaby marznacy deszcz",
    # Zachmurzenie male, możliwe słabe opady  deszczu ze śniegiem => 
      "n3z68": pl.clouds['FEW'] + " slaby deszcz snieg",
    # Zachmurzenie małe, opady śniegu => 
      "n3z71": pl.clouds['FEW'] + " snieg",
    # Pochmurno z przejaśnieniami, opady marznącego deszczu => 
      "n6z66": pl.clouds['SCT'] + " marznacy snieg",
    # Pochmurno, opady marznącego deszczu => 
      "n8z66": pl.clouds['BKN'] + " marznacy deszcz",
    # Pochmurno z przejaśnieniami, intensywne opady deszczu => 
      "n6z61": pl.clouds['SCT'] + " silny deszcz",
    # Pochmurno, intensywne opady deszczu => 
      "n8z61": pl.clouds['BKN'] + " silny deszcz",
    # Zachmurzenie małe, możliwe słabe opady śniegu => 
      "n3z70": pl.clouds['FEW'] + " slaby snieg",
    # Pochmurno z przejaśnieniami, słabe opady śniegu => 
      "n6z70": pl.clouds['SCT'] + " slaby snieg",
    # Pochmurno, słabe opady śniegu => 
      "n8z70": pl.clouds['BKN'] + " slaby snieg",
    # Pochmurno z przejaśnieniami, intensywne opady śniegu => 
      "n6z71": pl.clouds['SCT'] + " silny snieg",
    # Pochmurno, intensywne opady śniegu => 
      "n8z71": pl.clouds['BKN'] + " silny snieg",
    # Pochmurno z przejaśnieniami, opady deszczu ze śniegiem => 
      "n6z68": pl.clouds['SCT'] + " deszcz snieg",
    # Pochmurno, opady deszczu ze śniegiem => 
      "n8z68": pl.clouds['BKN'] + " deszcz snieg",
    # Pochmurno z przejaśnieniami, okresami przelotny deszcz ze śniegiem => 
      "n6z83": pl.clouds['SCT'] + " przelotny deszcz snieg",
    # Pochmurno, opady przelotnego deszczu ze śniegiem => 
      "n8z83": pl.clouds['BKN'] + " przelotny deszcz snieg",
    # Pochmurno z przejaśnieniami, opady mżawki => 
      "n6z50": pl.clouds['SCT'] + " mzawka",
    # Pochmurno, opady mżawki => 
      "n8z50": pl.clouds['BKN'] + " mzawka",
    # Pochmurno z przejaśnieniami, opady marznącej mżawki => 
      "n6z56": pl.clouds['SCT'] + " marznaca mzawka",
    # Pochmurno, opady marznącej mżawki => 
      "n8z56": pl.clouds['BKN'] + " marznaca mzawka",
    # Pogodnie, możliwe opady deszczu przelotnego => 
      "n3z80": pl.clouds['SKC'] + " przelotny deszcz",
    # Pochmurno z przejaśnieniami, okresami deszcz przelotny => 
      "n6z80": pl.clouds['SCT'] + " przelotny deszcz",
    # Pochmurno, opady deszczu przelotnego => 
      "n8z80": pl.clouds['BKN'] + " przelotny deszcz",
    # Pochmurno z przejaśnieniami, możliwość burz => 
      "n6z90": pl.clouds['SCT'] + " burza",
    # Pochmurno, możliwość burz => 
      "n8z90": pl.clouds['BKN'] + " burza",
    # Pogodnie, możliwe opady śniegu przelotnego => 
      "n3z85": pl.clouds['SKC'] + " przelotny snieg",
    # Pochmurno z przejaśnieniami,okresami opady śniegu przelotnego => 
      "n6z85": pl.clouds['SCT'] + " przelotny snieg",
    # Pochmurno, śnieg przelotny => 
      "n8z85": pl.clouds['BKN'] + " przelotny snieg",
}

#rozaWiatrow = {0:"północny", 1:"północno-wschodni", 2:"wschodni", 
#        3:"południowo-wschodni", 4:"południowy",
#        5:"południowo-zachodni", 6:"zachodni", 7:"północno-zachodni" }

rozaWiatrow = {0:"polnocny", 1:"polnocno wschodni", 2:"wschodni", 
        3:"poludniowo wschodni", 4:"poludniowy",
        5:"poludniowo zachodni", 6:"zachodni", 7:"polnocno zachodni" }

prognozy = []

def downloadFile(url):
    webFile = urllib.urlopen(url)
    return webFile.read()

def parseData(dane):
    prognozy = []
    dane = dane.split("\r\n")
    _data     = re.compile("\((\d{1,2})\.(\d{1,2})\.(\d\d\d\d)\)")
    _godzina  = re.compile("(\d{1,2})(:00)")
    _zjawiska = re.compile("n\dz\d\d")

    #temperatura, temperatura odczuwalna, ciśnienie
    _temp     = re.compile("(?<=>)((?:-)?\d{1,2})(<)")
    _tempOdcz = re.compile("(?<=\()(?:-)?\d{1,2}\.\d")
    _cisn     = re.compile("(\d{3,4})(\ hPa)")

    #sila wiatru, kierunek wiatru
    _silaWiatru = re.compile("(\d{1,2})(\sm/s)")
    _kierWiatru = re.compile("(?<=imgw/)(\d)(\.gif)")

    for i in range(0,len(dane)):
        if len(_data.findall(dane[i]))>0:
            data =_data.findall(dane[i])[0]
        elif ":00" in dane[i] and len(dane[i].split(">"))>2: 
            godzina  = _godzina.findall(dane[i])[0]

            zjawiska    = _zjawiska.findall(dane[i+1])[0]

            temp     = _temp.findall(dane[i+2])[0][0]
            tempOdcz = _tempOdcz.findall(dane[i+2])[0]
            cisn     = _cisn.findall(dane[i+2])[0][0]

            silaWiatru    = _silaWiatru.findall(dane[i+3])[0][0]
            kierWiatru    = _kierWiatru.findall(dane[i+3])[0][0] 
            
            # timestamp godziny, na którą jest prognoza
            ts = int(time.mktime(time.strptime("-".join( (data[2], data[1].rjust(2,'0'), data[0].rjust(2,'0')) ) 
                                   + ' ' + godzina[0].rjust(2,'0')+godzina[1], "%Y-%m-%d %H:%M" ) ))
                                          
            prognozy.append( { \
                "zjawiska":   zjawiskaIMGW[zjawiska], \
                "temp":       int(temp), \
                "tempOdcz":   int(float(tempOdcz)), \
                "silaWiatru": int(silaWiatru), \
                "kierWiatru": rozaWiatrow[int(kierWiatru)], \
                "cisn":       int(cisn), \
                "timestamp":  ts \
                } )

    return prognozy

def getForecast(t):
    global prognozy
    prognoza = {}
    t     = int(time.mktime(t.timetuple()))
    # delta powinna być w miarę dużą liczbą; tu jest to timestamp danej chwili
    delta = int(time.mktime(datetime.datetime.now( tz=pytz.timezone("Europe/Warsaw") ).timetuple()))

    for p in prognozy:
        if abs(t-p["timestamp"]) < delta and t-p["timestamp"]<0:
            delta = abs(t - p["timestamp"])
            prognoza = p
        #else:
        #    break
    
    return prognoza

def getCurrWeather():
    global prognozy
    pogoda = {}
    t = datetime.datetime.now( tz=pytz.timezone("Europe/Warsaw") ) # teraz
    t     = int(time.mktime(t.timetuple()))

    # delta powinna być w miarę dużą liczbą; tu jest to timestamp danej chwili
    delta = int(time.mktime(datetime.datetime.now( tz=pytz.timezone("Europe/Warsaw") ).timetuple()))

    for p in prognozy:
        if t-p["timestamp"] < delta and t-p["timestamp"]>0:
            delta = abs(t - p["timestamp"])
            pogoda = p
        #else:
        #    break
    
    return pogoda

def readWeather(fcast):
    rv = ""
    if config.podajTemp:       rv = " ".join( (rv, "temperatura", pl.cardinal(fcast["temp"], pl.C)) )
    if config.podajTempOdcz:   rv = " ".join( (rv, "temperatura_odczuwalna ", pl.cardinal(fcast["tempOdcz"], pl.C)) )
    if config.podajZjawiska:   rv = " ".join( (rv, fcast["zjawiska"]) )
    if config.podajCisnHpa:    rv = " ".join( (rv, "cisnienie", pl.cardinal(fcast["cisn"], pl.hPa)) )
    if config.podajSileWiatru: rv = " ".join( (rv, "predkosc_wiatru", pl.cardinal(fcast["silaWiatru"], pl.mPs)) )
    if config.podajKierWiatru: rv = " ".join( (rv, "kierunek_wiatru", fcast["kierWiatru"]) )

    return rv + " zrodlo imgw"

def getData(l):
    data = {"data":"", "needCTCSS":None, "allOK":True}

    global prognozy, zjawiskaIMGW
    prognozy = parseData( downloadFile(config.url) )

    teraz = datetime.datetime.now( tz=pytz.timezone("Europe/Warsaw") )
    potem = teraz + datetime.timedelta(hours=config.czasPrognozy)

    if config.podajStanPogody:
        data["data"] = readWeather(getCurrWeather())
    data["data"] = " ".join( (data["data"], "prognoza_na_nastepne trzy godziny", readWeather(getForecast(potem))) )

    data["data"] = pl.removeDiacritics(data["data"])

    return data
