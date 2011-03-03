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

from config import gopr_lawiny as config
import datetime
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

    aktualny = True

    _date      = re.compile('(\d{4})-(\d{2})-(\d{2})\ (\d{2}):(\d{2}):(\d{2})')
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
	    if _date.findall(line)!=[]:
	        dt      = _date.findall(line)[0]
	        now     = datetime.datetime.now()
	        delta   = datetime.timedelta(hours=24)
	        infoDT  = datetime.datetime(int(dt[0]), int(dt[1]), int(dt[2]), int(dt[3]), int(dt[4]), int(dt[5]))
	        if infoDT+delta<now:
                     aktualny = False

    print (stopien, tendencja, wystawa, aktualny, infoDT)

    return (int(stopien), int(tendencja), int(wystawa), aktualny, infoDT)

def getData(l):
    global lang
    lang = my_import(l+"."+l)

    data = {"data":"", "needCTCSS":False, "debug":None, "allOK":True}

    stopien, tendencja, wystawa, aktualny, infoDT = pobierzOstrzezenia(config.region)

    if stopien == -1:
        return ""
    elif stopien > -1:
	data["needCTCSS"]=True

    data["data"] = " ".join( (data["data"], lang.gopr_region[config.region], lang.avalancheLevel[stopien]) )

    if config.podajTendencje==1:
        data["data"] = " ".join( (data["data"], lang.gopr_tendention[tendencja]) )

    if aktualny==False:
	data["data"] = " ".join( (data["data"], lang.info_at, lang.readISODT(infoDT.isoformat(' '))) )

    # Profile i szczególnie niebezpieczne wystawy niezaimplementowane.

    data["data"] = lang.removeDiacritics(data["data"])

    return data	

if __name__ == '__main__':
    lang = 'pl'
    print getData(lang)

