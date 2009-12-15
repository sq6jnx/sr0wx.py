#!/usr/env/python -tt
# -*- encoding=utf8 -*-

from config import sunriset as config
import pytz, datetime
import lib.Sun
lang=None

# Moduł powinien podawać godzinę wschodu słońca przed jego wschodem danego dnia, zachodu na X godzin przed jego zachodem


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
        
        
        dt = datetime.datetime.utcnow()

        sun = lib.Sun.Sun()
        sunrise, sunset = sun.sunRiseSet(dt.year, dt.month, dt.day, config.location[0], config.location[1])

        sunrise, sunset = datetime.timedelta(hours=sunrise), datetime.timedelta(hours=sunset)

        print sunrise, sunset
        print sunrise > datetime.datetime.utcnow()
        

# Wschod slonca godzina 6:34 zachod slonca 16:45. dzien bedzie trwal 14h 34m. <-- jeśli przed świtem (w tym po zachodzie)
# Zachód słońca  godzina 15:45 <-- jeśli dzień trwa
# Długosc dnia....
