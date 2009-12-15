#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
#
# ********
# sr0wx.py
# ********
#
# This is METAR module for SR0WX project. It's quite simple, because
# ``pymetar`` (by Tobias Klausmann) does all the job (but not as good as it
# should and pymetar will be replaced by another module shortly).
#
# This file is based on ``pymetar`` example. Required packages are ``sys``
# and ``pymetar``, of course.

import sys
import lib.pymetar as pymetar

# We also import ``pytz`` and ``datetime`` because METAR gives us date-time
# info in UTC and we want it in local, as defined in ``metar``'s config file.
import pytz, datetime

# ``metar_config`` defines airport ICAO code and informations which you'd
# like retrieve form METAR reports.
from config import metar as config

# For debugging purposes:

import debug

# It will store ``metar`` language module.
lang = None

# Now the hardest part. As ``metar`` module doesn't know which language
# will it speak it has to import which is called same as value of
# SR0WX's language variable. As ``__import`` in Python 2.6 doesn't work as in
# 2.5 (bugfix) program has to import it in a different way. How? Consult
# http://www.wingware.com/psupport/python-manual/2.4/lib/built-in-funcs.html

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

# This tiny function is used to convert from UTC to local time. Code inspired
# by ``pytz`` manual, http://pytz.sourceforge.net/#example-usage .
def getLocalTimeFromISO(isoDT, timeZone=config.timeZone):
    y,m,d,hh,mm,ss= ( int(isoDT[0:4]),   int(isoDT[5:7]),   int(isoDT[8:10]),
                      int(isoDT[11:13]), int(isoDT[14:16]), int(isoDT[17:19]) )

    utc = datetime.datetime(y, m, d, hh, mm, ss, tzinfo=pytz.timezone("UTC"))
    loc = utc.astimezone(pytz.timezone(timeZone))

# Returning simple str(loc) should be safe, but in case something will go
# wrong someday we do it another way:

    return loc.strftime("%Y-%m-%d %H:%M:%S %Z%z")

# Another function is used to change direction written as symbols (ie. "NNE")
# into its full-word representation, ie. "nothern northern eastern". This
# is used by METAR module.

def direction(dir, short=False):
    global lang
    _dir = ""
    if len(dir)==3 and short==True:
        dir = dir[1:3]
    for i in range(0,len(dir)-1):
        _dir = _dir + lang.directions[dir[i]][0]
    _dir = _dir + lang.directions[dir[-1]][1]

    return _dir


# OK. This function **must** be defined in every module. I think it's quite easy 
# to find out what's happening in here.
#
# `lang` is a language module, it contains doctionary and language-dependent fuctions.
def getData(l):
    data = {"data":"", "needCTCSS":False, "allOK":True}

    global lang
    lang = my_import(l+"."+l)
    try:
        rf=pymetar.ReportFetcher(config.ICAOAirportCode)
        rep=rf.FetchReport()
    except Exception, e:
        sys.stderr.write("Something went wrong when fetching the report.\n")
        sys.stderr.write("These usually are transient problems if the station ")
        sys.stderr.write("ID is valid. \nThe error encountered was:\n")
        sys.stderr.write(str(e)+"\n")
        sys.exit(1)

    rp=pymetar.ReportParser()
    pr=rp.ParseReport(rep)

    debug.log("METAR", "METAR report: %s"%(pr.getRawMetarCode()) )

    if config.lastUpdate==1:
        _weather = " ".join( (lang.weatherDate,\
            lang.readISODT(getLocalTimeFromISO(pr.getISOTime()))) )

    _weather=_weather + "_"

    if config.temperatureCelsius==1:
        _weather = " ".join( (_weather, lang.temperature,\
            lang.cardinal(int(pr.getTemperatureCelsius()), lang.C) ) )

    if config.humidity==1:
        _weather = " ".join( (_weather, lang.humidity, \
            lang.cardinal(int(pr.getHumidity()),lang.percent)) )

# There are three possible situations with wind:
# * when wind speed != None and wind direction != None
# * when wind speed != None and wind direction == None (variable wind directions)
# * when wind speed == None and wind direction == None (silence==no wind)

# First situation, most typical:
    if pr.getWindSpeed() != 0 and pr.getWindCompass() is not None:
        if config.windDirectionCompass==1:
            _weather = " ".join( (_weather, lang.windDirection,\
                direction(pr.getWindCompass(),config.shortenWindDirection)) )
        if config.windDirectionDegrees==1:
            _weather = " ".join( (_weather,\
                lang.cardinal(int(pr.getWindDirection()), lang.deg)) )

        if config.windSpeedMPS==1:
            _weather = " ".join( (_weather, lang.windSpeed,\
                lang.cardinal(int(pr.getWindSpeed()),lang.mPs)) )
        if config.windStrengthBeaufort==1:
            _weather = " ".join( (_weather, lang.windStrength,\
            lang.cardinal(int(pr.getWindSpeedBeaufort()),lang.B)) )

    elif pr.getWindSpeed() !=0 and pr.getWindCompass() is None:
        if config.windDirectionCompass==1 or config.windDirectionDegrees==1:
            _weather = " ".join( (_weather, lang.variableWindDirection) )

        if config.windSpeedMPS==1:
            _weather = " ".join( (_weather, lang.windSpeed,\
                lang.cardinal(int(pr.getWindSpeed()),lang.mPs)) )
        if config.windStrengthBeaufort==1:
            _weather = " ".join( (_weather, lang.windStrength,\
            lang.cardinal(int(pr.getWindSpeedBeaufort()),lang.B)) )

    elif pr.getWindSpeed() == 0 and pr.getWindCompass() is None:
        if config.windDirectionCompass==1 or config.windDirectionDegrees==1 or\
            config.windSpeedMPS==1 or config.windStrengthBeaufort==1:
            _weather = " ".join( (_weather, lang.noWind) )
    else:
        debug.log("METAR", "unsupported wind conditions")

    if config.pressureHPa==1 and pr.getPressure() is not None:
        _weather = " ".join( (_weather, lang.pressure,\
            lang.cardinal(int(pr.getPressure()),lang.hPa)) )

    if config.dewPointCelsius==1:
        _weather = " ".join( (_weather, lang.dewPoint,\
            lang.cardinal(int(pr.getDewPointCelsius()), lang.C)) )

    if config.visibilityKilometers==1 and pr.getVisibilityKilometers() is not None:
        _weather = " ".join( (_weather, lang.visibility,\
            lang.cardinal(int(pr.getVisibilityKilometers()),lang.km)) )

# ``pymetar`` doesn't give proper informations about clouds and weather
# conditions (snow, rain, etc), so we don't show these.

    debug.log("METAR", "finished")
    data["data"] = lang.removeDiacritics(_weather)
    return data
