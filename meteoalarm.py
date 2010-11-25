#!/usr/env/python -tt
# -*- encoding=utf8 -*-

import re
import urllib

from config import meteoalarm as config
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

def getData(l):
    global lang
    lang = my_import(l+"."+l)

    data = {"data":"", "needCTCSS":False, "debug":None, "allOK":True}
    
    today=tomorrow=""
    if config.showToday == True:
        today    = getAwareness(config.region, tomorrow=False)
    if config.showTomorrow == True:
        tomorrow = getAwareness(config.region, tomorrow=True)

    if today== "" and tomorrow== "":
        #data["data"] = " ".join( (lang.meteoalarmNoAwareness, lang.meteoalarmRegions[config.region]) )
        pass # silence is golden
    elif today!= "" and tomorrow=="":
        data["data"] =  " ".join( (lang.meteoalarmAwareness, lang.meteoalarmRegions[config.region], lang.today, today) )
        data["needCTCSS"] = True
    elif today== "" and tomorrow!="":
        data["data"] =  " ".join( (lang.meteoalarmAwareness, lang.meteoalarmRegions[config.region], lang.tomorrow, tomorrow) )
        data["needCTCSS"]= True
    else:
        data["data"] = " ".join( (lang.meteoalarmAwareness, lang.meteoalarmRegions[config.region], lang.today, today, lang.tomorrow,tomorrow) )
        data["needCTCSS"]= True 

    return data

def getAwareness(region, tomorrow=False):
# tommorow = False -- awareness for today
# tommorow = True  -- awareness for tommorow
    r =   re.compile('intranet/images/aw(\d[01]?)([0234]).jpg')
    url = "http://www.meteoalarm.eu/area.asp?lang=EN&ShowDate="+\
        ("tomorrow"*tomorrow)+"&area="+str(region)

    a = ""

    for line in downloadFile(url).split('\n'):
        f = r.findall(line)
        if len(f) is not 0 and int(f[0][0])!=0:
            a = " ".join( (a, lang.meteoalarmAwarenesses[int(f[0][0])],\
                lang.meteoalarmAwarenessLevel, lang.meteoalarmAwarenessLvl[int(f[0][1])]) )

    return a
