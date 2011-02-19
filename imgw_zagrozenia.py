#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from config import imgw_hydro as config

import os
import debug

import pl.pl as lang
import re

# archiwum ostrzezen: http://www3.imgw.pl/wl/internet/zz/zagrozenia/_ost_met/wszy.html
zagrozenia = {
    "nieznane.":                       "nieokreslone_zagrozenie",
    "silnywiatr.":                     "silny wiatr", 
    "intensywneopadydeszczu.":         "intensywne opady deszczu",
    "intensywneopadysniegu.":          "intensywne opady sniegu",
    "opadymarznace.":                  "marznace opady",
    "zawiejezamieciesniezne.":         "zawieje_zamiecie_sniezne",
    "silnamgla.":                      "silna mgla",
    "oblodzenie.":                     "obldzenie",
    "przymrozki.":                     "prymrozki",
    "roztopy.":                        "roztopy",
    "upaly.":                          "upaly",
    "silnemrozy.":                     "silne mrozy",
    "mglaintensywnieosadzajacaszadz.": "mgla intensywnie_osadzajaca_szadz",
    "burze.":                          "burze",
    "silneburze.":                     "sile burze",
    "burzezgradem.":                   "burze z_gradem",
    "silneburzezgradem.":              "silne burze z_gradem"}
_zagrozenia = re.compile("|".join( (zagrozenia.keys()) ))

poziomyZagrozen = {"green":"odwolane", "yellow":"niski","#FEA52":"sredni", "red":"wysoki"}
_poziomyZagrozen = re.compile("|".join( (poziomyZagrozen.keys()) ))


regiony = {
    "bs": "zatoki_pomorskiej", #"strefy brzegowej woj. zach-pom"
    "sz": "zalewu_szczecinskiego",
    "bg": "strefy brzegowej wojewodztwa pomorskiego",
    "26": "calego_wybrzeza", # nieuzywane

    "sc": "szczecina",
    "gd": "trojmiasta",
    "ol": "olsztyna",
    "bi": "bialegostoku",
    "gw": "gorzowa_wielkopolskiego",
    "zg": "zielonej_gory",
    "po": "poznania",
    "by": "bydgoszczy",
    "wa": "warszawy",
    "wr": "wroclawia",
    "oe": "opola",
    "kr": "krakowa",
    "lo": "lodzi",

    "zp": "wojewodztwa zachodniopomorskiego",
    "pm": "wojewodztwa pomorskiego",
    "wm": "wojewodztwa warminsko_mazurskiego",
    "pd": "wojewodztwa podlaskiego",
    "lb": "wojewodztwa lubuskiego",
    "wp": "wojewodztwa wielkopolskiego",
    "kp": "wojewodztwa kujawsko_pomorskiego",
    "mz": "wojewodztwa mazowieckiego",
    "lu": "wojewodztwa lubuskiego",
    "ld": "wojewodztwa lodzkiego",
    "ds": "wojewodztwa dolnoslaskiego",
    "op": "wojewodztwa opolskiego",
    "sl": "wojewodztwa slaskiego",
    "sk": "wojewodztwa swietokrzyskiego",
    "ma": "wojewodztwa malopolskiego",
    "pk": "wojewodztwa podkarpackiego",

    "kk": "kotliny_klodzkiej",
    "su": "przedgorza_sudeckiego_i_sudetow",
    "eb": "powiatu_elblaskiego"
}

def downloadFile(url):
    webFile = urllib.urlopen(url)
    return webFile.read()

def zagrozeniaDlaRegionu(z):
    global zagrozenia
    file = downloadFile('http://www3.imgw.pl/wl/internet/zz/zagrozenia/_ost_met/'+z+'.html').split('\n')
    zjawiska = ""
    for i in range(0, len(file)):
        if 'Zjawisko:' in file[i]:
            _z = _zagrozenia.findall(file[i+15])[0]
            _p = _poziomy.findall(file[i+9])[0]
            if _z!="" and _p!="":
                zjawiska = " ".join( (zagrozenia[_z], "poziom_zagrozenia", 
           
        
def getData(l):
    data = {"data":"", "needCTCSS":False, "allOK":True}
    for region in config.regiony:
        z =zagrozeniaDlaRegionu(region)
        if z is not "":
            data["data"]      += pl.removeDiacritics(z)
            data["needCTCSS"] =  True

    return data

print "|".join( (zagrozenia.keys()) )

print "|".join( (poziomyZagrozen.keys()) ) 

