#!/usr/env/python -tt
# -*- encoding=utf8 -*-
#
#   Copyright 2009-2014 Michal Sadowski (sq6jnx at hamradio dot pl)
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

lang = None


def downloadFile(url):
    webFile = urllib.urlopen(url)
    return webFile.read()


def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def last(l):
    if len(l) == 0:
        return None
    else:
        return l[-1]


def pobierzOstrzezenia(region):
    url = "http://www.gopr.pl/avalanche/pl/%d" % region

    _date = re.compile('(\d{4})-(\d{2})-(\d{2})\ (\d{2}):(\d{2}):(\d{2})')
    _brak = re.compile('w momencie zaistnienia adekwatnych')
    _stopien = re.compile('img/([1-5])\.gif')
    _tendencja = re.compile("img/lawina/strzalka(\d)\.gif")
    _wystawa = re.compile("img/lawina/pikto/roza(\d)\.gif")

    stopien, tendencja, wystawa = False
    line = downloadFile(url)
    if _brak.findall(line) != []:
        return (-1, -1, -1)
    else:
        stopien = stopien or stopien.findall(line)[0]
        tendencja = tendencja or _tendencja.findall(line)[0]
        wystawa = wystawa or _wystawa.findall(line)[0]
    return (int(stopien), int(tendencja), int(wystawa))


def getData(l):
    global lang
    lang = my_import(l + "." + l)

    data = {"data": "",
            "needCTCSS": False,
            "debug": None,
            "allOK": True,
            "source": ""}

    stopien, tendencja = pobierzOstrzezenia(config.region)

    if stopien == -1:
        return ""

    data["needCTCSS"] = True
    data["data"] = " ".join((data["data"],
                            lang.gopr_region[config.region],
                            lang.avalancheLevel[stopien]))

    if config.podajTendencje == 1:
        data["data"] = " ".join((lang.gopr_welcome, data["data"],
                                 lang.gopr_tendention[tendencja]))

    data["data"] = lang.removeDiacritics(data["data"])

    return data

if __name__ == '__main__':
    lang = 'pl'
    print getData(lang)
