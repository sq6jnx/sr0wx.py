#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
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
 
# 
#
# ********
# sr0wx.py
# ********
#
# This is main program file for automatic weather station project;
# codename SR0WX.
#
# (At the moment) SR0WX can read METAR [#]_ weather informations and
# is able to read them aloud in Polish. SR0WX is fully extensible, so
# it's easy to make it read any other data in any language (I hope).
#
# .. [#] http://en.wikipedia.org/wiki/METAR
#
# =====
# About
# =====
#
# Every automatic station's callsign in Poland (SP) is prefixed by "SR".
# This software is intended to read aloud weather informations (mainly).
# That's why we (or I) called it SR0WX.
#
# Extensions (mentioned above) are called ``modules`` (or ``languages``).
# Main part of SR0WX is called ``core``.
#
# SR0WX consists quite a lot of independent files so I (SQ6JNX) suggest
# reading other manuals (mainly configuration- and internationalization
# manual) in the same time as reading this one. Really.
#
# ============
# Requirements
# ============
#
# SR0WX (core) requires the following packages:

import os,sys
import pygame
import time
import getopt
import lib.cw as cw
import debug, traceback

# ``os``, ``sys`` and ``time`` doesn't need further explanation, these are
# syandard Python packages.
#
# ``pygame`` [#]_ is a library helpful for game development, this project
# uses it for reading (playing) sound samples. ``config`` is just a
# SR0WX configuration file and it is described seperately.
#
# ..[#] www.pygame.org
#
# =========
# Let's go!
# =========
#
# For infrmational purposes script says hello and gives local time/date,
# so it will be possible to find out how long script was running.

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

debug.log("CORE", "sr0wx.py started")
debug.log("LEGAL","")
debug.log("LEGAL","Copyright 2009-2012 Michal Sadowski (sq6jnx at hamradio dot pl)")
debug.log("LEGAL","")
debug.log("LEGAL","Licensed under the Apache License, Version 2.0 (the \"License\");")
debug.log("LEGAL","you may not use this file except in compliance with the License.")
debug.log("LEGAL","You may obtain a copy of the License at")
debug.log("LEGAL","")
debug.log("LEGAL","    http://www.apache.org/licenses/LICENSE-2.0")
debug.log("LEGAL","")
debug.log("LEGAL","Unless required by applicable law or agreed to in writing, software")
debug.log("LEGAL","distributed under the License is distributed on an \"AS IS\" BASIS,")
debug.log("LEGAL","WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.")
debug.log("LEGAL","See the License for the specific language governing permissions and")
debug.log("LEGAL","limitations under the License.")

# 
# All datas returned by SR0WX modules will be stored in ``data`` variable.

data = " "

# Information about which modules are to be executed is written in SR0WX
# config file. Programm starts every single of them and appends it's return
# value in ``data`` variable. As you can see every module is started with
# language variable, which is also defined in configuration.
# Refer configuration and internationalization manuals for further
# informations.
#
# Modules may be also given in commandline, separated by a comma.

config=None
try:                                
    opts, args = getopt.getopt(sys.argv[1:], "c:", ["config="])
except getopt.GetoptError:
    pass
for opt, arg in opts:
    if opt in ("-c", "--config"):
        if arg[-3:]=='.py':
            arg=arg[:-3]
        config = __import__(arg)

if config is None:
    import config

if len(args)>0:
    modules = args[0].split(",")
else:
    modules=config.modules

needCTCSS = False
lang = my_import('.'.join((config.lang, config.lang)) )
sources = [lang.source,]

for m in modules:
    try:
        debug.log("CORE","starting %s..."%(m) )
        module = __import__(m)
        moduleData = module.getData(config.lang)
        data = " ".join( (data, moduleData["data"]) )
        needCTCSS = needCTCSS or moduleData["needCTCSS"]
        if moduleData["data"]!='' and moduleData.has_key('source')\
            and moduleData['source']!='':
            sources.append(moduleData['source'])
    except:
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        debug.log("CORE", traceback.format_exc(),6)

# When all the modules finished its' work it's time to ``.split()`` returned
# data. Every element of returned list is actually a filename of a sample.

data = config.helloMsg + data.split()
if len(sources)>1:
    data+= sources
data+= config.goodbyeMsg

# It's time to init ``pygame``'s mixer (and ``pygame``). Possibly defined
# sound quality is far-too-good (44kHz 16bit, stereo), so you can change it.

pygame.mixer.init(16000,-16,2,1024)

# Next (as a tiny timesaver & memory eater ;) program loads all neccessary
# samples into memory. I think that this is better approach than reading
# every single sample from disk in the same moment when it's time to play it.

# Just for debug: our playlist (whole message as a list of filenames)

playlist=[]

for el in data:
    if "upper" in dir(el): playlist.append(el)
    else: playlist.append("[sndarray]")

debug.log("CORE", "playlist elements: %s"%(" ".join(playlist)) )
debug.log("CORE", "loading sound samples...")

debug.log("CORE", "playing sound samples")

soundSamples = {}
for el in data:
    if "upper" in dir(el):
        if el[0:7]=='file://':
            soundSamples[el] = pygame.mixer.Sound(el[7:])
        if el is not "_" and el not in soundSamples:
            if not os.path.isfile(config.lang+"/"+el+".ogg"):
                debug.log("CORE", "couldn't find %s"%(config.lang+"/"+el+".ogg"), 3)
                soundSamples[el] = pygame.sndarray.make_sound( cw.cw("^") )
                if config.pygameBug==1:
                    soundSamples[el] = pygame.sndarray.make_sound(pygame.sndarray.array(soundSamples[el])[:len(pygame.sndarray.array(soundSamples[el]))/2])
            else: soundSamples[el] = pygame.mixer.Sound(config.lang+"/"+el+".ogg")

# If programme configuration specifies CTCSS subtone frequency this tone
# will be played as long as the message.

if config.CTCSS is not None and (needCTCSS or config.playCTCSS):
    import lib.ctcss as ctcss

    subtoneChannel = pygame.sndarray.make_sound(ctcss.getCTCSS(config.CTCSS)).play(-1)
    subtoneChannel.set_volume(config.CTCSSVolume)

# Programme should be able to "press PTT" via RSS232. See ``config`` for
# details.

if config.serialPort is not None:
    import serial
    try:
        ser = serial.Serial(config.serialPort, config.serialBaudRate)
	if config.serialSignal=='DTR':
	    ser.setDTR(0); ser.setRTS(1)
        else:
	    ser.setDTR(1); ser.setRTS(0)
    except:
        debug.log("CORE", "Failed to open %s@%i"%(config.serialPort, config.serialBaudRate), 3)

pygame.time.delay(1000)

# OK, data prepared, samples loaded, let the party begin!
#
# Take a look at ``while`` condition -- programme doesn't check if the
# sound had finished played all the time, but only 25 times/sec (default).
# It is because I don't want 100% CPU usage. If you don't have as fast CPU
# as mine (I think you have, though) you can always lower this value.
# Unfortunatelly, there may be some pauses between samples so "reading
# aloud" will be less natural.

for el in data:
    if el == "_":
        pygame.time.wait(500)
    else:
        if "upper" in dir(el):
            voiceChannel = soundSamples[el].play()
        elif "upper" not in dir(el):
            sound = pygame.sndarray.make_sound(el)
            if config.pygameBug == 1:
                sound = pygame.sndarray.make_sound(pygame.sndarray.array(sound)[:len(pygame.sndarray.array(sound))/2])
            voiceChannel = sound.play()
        while voiceChannel.get_busy():
            pygame.time.Clock().tick(25)

# Possibly the argument of ``pygame.time.Clock().tick()`` should be in
# config file...
#
# The following four lines give us a one second break (for CTCSS, PTT and
# other stuff) before closing the ``pygame`` mixer and display some debug
# informations.

debug.log("CORE", "finishing...")

pygame.time.delay(1000)

# If we've opened serial it's now time to close it.
if config.serialPort is not None:
    ser.close()

pygame.mixer.quit()

debug.log("CORE", "goodbye")

# Documentation is a good thing when you need to double or triple your
# Lines-Of-Code index ;)
