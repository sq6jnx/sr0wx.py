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
#
# -----------------------
# How does it (will) work
# -----------------------
#
# Every module (incl. ``core``) has the same instance of ``debug`` module,
# where they report everything (verbose). If something wrong happens (it is
# error level >= ``showlevel``) information goes on screen.
#
# At the end of application ``__del__`` or ``gather()`` is run``collect()`` is run (by ``__del__()`` or
# standalone). This function simply counts md5 sum of message containing
# and adds this information to the end of file. This sum is used as a
# fingerprint and may be useful when there will be many emails sent
# automatically by cron.
# 
# Suggestion: as I suggested before, every module needs an instance of debug.
# It should be given as a parameter to module's getData() (now, afair, we give it lang,
# but lang may be derived from config, or both can be parameters to getData()).
#
# For sure, checksum (short one; maybe CRC not MD5?) has to be counted as fast as message
# "comes into" debug, not in the end. debug should be count only on messages shown
# on screen, not written into the log or ignored.

from config import debug as config
import datetime, os

config.baseURI = "127.0.0.1/"

class debug():
    filename = datetime.datetime.utcnow().strftime("%y-%m-%d")+".log"
    logGathered = False
    msgs=''

# When module wants to log something it should give its name, message 
# to be logged and buglevel. debug.log() will "make decision" (basing
# config) if this message should be shown on screen and saved or just
# saved. Default buglevel is 0 (verbose).

    def log(self, moduleName, message, buglevel=0):
        self.dt = datetime.datetime.utcnow()

        time = self.dt.strftime("%y-%m-%d %X UTC")
        formattedMessage = time + message

        prefix = "%s [%s]:\t"%(time,moduleName)
        formattedMessage = prefix + message.replace("\n","".join( ("\r\n",prefix) ))


        if buglevel>=config.showLevel:
            self.msgs = self.msgs + message
            print formattedMessage 
        if buglevel>=config.writeLevel:
            try:
                if not os.path.exists(self.filename):
                    logfile = open(self.filename, 'w')
                else:
                    logfile = open(self.filename, 'a+')
                logfile.write(formattedMessage + '\n')
            except:
                print dt.strftime("%x %X UTC")+" [DEBUG]:\tCan't write to file!"
            finally:
                logfile.close()

# Both gather() and  __del__() should do as less as possible, so __del__() does not 
# run gether(). Both functions do the same except 
    def gather(self):
        if not self.logGathered:
            print "\n\nHash of traceback is %s. Hope it helps in debugging. You can find whole log at %s ."%\
                ('%X'%(self.msgs.__hash__()+int('ffffffff',16)), "".join( (config.baseURI, self.filename) ) )
            self.logGathered = True

    def __del__(self):
        if not self.logGathered:
            print "\n\nHash of traceback is %s. Hope it helps in debugging. You can find whole log at %s ."%\
                ('%X'%(self.msgs.__hash__()+int('ffffffff',16)), "".join( (config.baseURI, self.filename) ) )
        pass

        
if __name__ == "__main__":
    # d = debug()
    # d.log("ja", "nic się nie stało", 9)
    # d.gather()
    pass

