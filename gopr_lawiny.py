#!/usr/env/python -tt
# -*- encoding=utf8 -*-

import re
import urllib

from config import gopr_lawiny as config
lang=None

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

def pobierzOstrzezenia(region):
    url = "http://www.gopr.pl/index.php?action=zagrozenie_lawinowe&id=%d"%region

    print url

    _brak      = re.compile('w momencie zaistnienia adekwatnych')
    _stopien   = re.compile('img/lawina/stopnie/(\d)D.gif')
    _tendencja = re.compile("img/lawina/strzalka(\d).gif")
    _wystawa   = re.compile("img/lawina/pikto/roza(\d).gif")

    brak,stopien, tendencja, wystawa = False,False,False,False
    for line in downloadFile(url).split('\n'):
	if _brak.findall(line)!=[]:
	    return (-1,-1,-1)
        else:
            stopien   = stopien   or last(_stopien.findall(line))
            tendencja = tendencja or last(_tendencja.findall(line))
            wystawa   = wystawa   or last(_wystawa.findall(line))

    return (stopien, tendencja, wystawa)

def getData(l):
    global lang
    lang = my_import(l+"."+l)

    data = {"data":"", "needCTCSS":False, "debug":None, "allOK":True}

    stopien, tendencja, wystawa = pobierzOstrzezenia(config.region)

    if stopien == -1:
        return ""
    elif stopien > -1:
	data["needCTCSS"]=True

    data["data"] = " ".join( (data["data"], lang.gopr_region[config.region], lang.avalancheLevel[stopien]) )

    if config.podaj_tendencje==1:
        data["data"] = " ".join( (data["data"], lang.gopr_tendention[tendencja]) )

    # Profile i szczególnie niebezpieczne wystawy niezaimplementowane.

    return data	

if __name__ == '__main__':
    lang = 'pl'
    print getData(lang)

