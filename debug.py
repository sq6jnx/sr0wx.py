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
# *********
# debug.py
# *********
#
# Special module for showing/storing debug informations. Log is saved in
# debug.path (stored in config) as yy-mm-dd.log. 

from config import debug as config
import datetime, os


# When module wants to log something it should give its name, message 
# to be logged and buglevel. debug.log() will "make decision" (basing
# config) if this message should be shown on screen and saved or just
# saved. Default buglevel is 0 (verbose).

def log(moduleName, message, buglevel=0):
    dt = datetime.datetime.utcnow()
    prefix = "%s [%s]:\t"%(dt.strftime("%y-%m-%d %X UTC"),moduleName )
    message = prefix + message.replace("\n","".join( ("\r\n",prefix) ))

    if buglevel>=config.showLevel:
        print message
    if buglevel>=config.writeLevel:
        filename = dt.strftime("%y-%m-%d")+".log"
        if not os.path.exists(filename):
            logfile = open(filename, 'w')
        else:
            logfile = open(filename, 'a+')
        try:
            logfile.write(message + '\n')
        except:
            print dt.strftime("%x %X UTC")+" [DEBUG]:\tCan't write to file!"
        finally:
            logfile.close()

