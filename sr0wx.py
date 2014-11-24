#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
#
#   Copyright 2009-2011, 2014 Michal Sadowski (sq6jnx at hamradio dot pl)
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

import getopt
import lib.cw as cw
import os
import pygame
import sys
import logging, logging.handlers

# ``os``, ``sys`` and ``time`` doesn't need further explanation, these are
# syandard Python packages.
#
# ``pygame`` [#]_ is a library helpful for game development, this project
# uses it for reading (playing) sound samples. ``config`` is just a
# SR0WX configuration file and it is described separately.
#
# ..[#] www.pygame.org
#
# =========
# Let's go!
# =========
#
# For infrmational purposes script says hello and gives local time/date,
# so it will be possible to find out how long script was running.

# Logging configuration
def setup_logging(config):
    # create formatter and add it to the handlers
    formatter = logging.Formatter(config.log_line_format)

    # Creating logger with the lowest log level in config handlers
    min_log_level = min([h['log_level'] for h in config.log_handlers])
    logger = logging.getLogger()
    logger.setLevel(min_log_level)

    # create logging handlers according to its definitions
    for handler_definition in config.log_handlers:
        handler = handler_definition['class'](**handler_definition['config'])
        handler.setLevel(handler_definition['log_level'])
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

#
# All datas returned by SR0WX modules will be stored in ``data`` variable.

data = " "

# Information about which modules are to be executed is written in SR0WX
# config file. Program starts every single of them and appends it's return
# value in ``data`` variable. As you can see every module is started with
# language variable, which is also defined in configuration.
# Refer configuration and internationalization manuals for further
# informations.
#
# Modules may be also given in commandline, separated by a comma.

config = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "c:", ["config="])
except getopt.GetoptError:
    pass
for opt, arg in opts:
    if opt in ("-c", "--config"):
        if arg[-3:] == '.py':
            arg = arg[:-3]
        config = __import__(arg)

if config is None:
    import config

logger = setup_logging(config)

logger.info("sr0wx.py started")
logger.info('''
Copyright 2009-2014 Michal Sadowski (sq6jnx at hamradio dot pl)

Licensed under the Apache License, Version 2.0 (the \"License\");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an \"AS IS\" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.''')
logger.info("sr0wx.py started")


if len(args) > 0:
    modules = args[0].split(",")
else:
    modules = config.modules

need_ctcss = False
lang = my_import('.'.join((config.lang, config.lang)))
sources = [lang.source, ]

for m in modules:
    try:
        logger.info("starting %s...", m)
        module = __import__(m)
        module_data = module.get_data(config.lang)
        data = " ".join((data, module_data["data"]))
        need_ctcss = need_ctcss or module_data["need_ctcss"]
        if module_data["data"] != '' and module_data.has_key('source') \
                and module_data['source'] != '':
            sources.append(module_data['source'])
    except:
        logger.exception("Exception when running %s", m)

# When all the modules finished its' work it's time to ``.split()`` returned
# data. Every element of returned list is actually a filename of a sample.

data = config.hello_msg + data.split()
if len(sources) > 1:
    data += sources
data += config.goodbye_msg

# It's time to init ``pygame``'s mixer (and ``pygame``). Possibly defined
# sound quality is far-too-good (44kHz 16bit, stereo), so you can change it.

pygame.mixer.init(16000, -16, 2, 1024)

# Next (as a tiny timesaver & memory eater ;) program loads all necessary
# samples into memory. I think that this is better approach than reading
# every single sample from disk in the same moment when it's time to play it.

# Just for debug: our playlist (whole message as a list of filenames)

playlist = []

for el in data:
    if "upper" in dir(el):
        playlist.append(el)
    else:
        playlist.append("[sndarray]")

logger.info("playlist elements: %s", " ".join(playlist))
logger.info("loading sound samples...")

logger.info("playing sound samples")

sound_samples = {}
for el in data:
    if "upper" in dir(el):
        if el[0:7] == 'file://':
            sound_samples[el] = pygame.mixer.Sound(el[7:])
        if el is not "_" and el not in sound_samples:
            if not os.path.isfile(config.lang + "/" + el + ".ogg"):
                logger.warn("Couldn't find %s" % (config.lang + "/" + el + ".ogg"))
                sound_samples[el] = pygame.sndarray.make_sound(cw.cw("^"))
                if config.pygame_bug == 1:
                    sound_samples[el] = pygame.sndarray.make_sound(pygame.sndarray.array(sound_samples[el])[:len(pygame.sndarray.array(sound_samples[el]))/2])
            else:
                sound_samples[el] = pygame.mixer.Sound(config.lang + "/" + el + ".ogg")

# If program configuration specifies CTCSS subtone frequency this tone
# will be played as long as the message.

if config.ctcss_tone is not None and (need_ctcss or config.play_ctcss):
    import lib.ctcss as ctcss

    subtone_channel = pygame.sndarray.make_sound(ctcss.getCTCSS(config.ctcss_tone)).play(-1)
    subtone_channel.set_volume(config.ctcss_volume)

# Program should be able to "press PTT" via RSS232. See ``config`` for
# details.

if config.serial_port is not None:
    import serial
    try:
        ser = serial.Serial(config.serial_port, config.serial_baud_rate)
        if config.serial_signal == 'DTR':
            ser.setDTR(0)
            ser.setRTS(1)
        else:
            ser.setDTR(1)
            ser.setRTS(0)
    except:
        log = "Failed to open serial port %s@%i"
        logger.error(log, config.serial_port, config.serial_baud_rate)

pygame.time.delay(1000)

# OK, data prepared, samples loaded, let the party begin!
#
# Take a look at ``while`` condition -- program doesn't check if the
# sound had finished played all the time, but only 25 times/sec (default).
# It is because I don't want 100% CPU usage. If you don't have as fast CPU
# as mine (I think you have, though) you can always lower this value.
# Unfortunately, there may be some pauses between samples so "reading
# aloud" will be less natural.

for el in data:
    if el == "_":
        pygame.time.wait(500)
    else:
        if "upper" in dir(el):
            voice_channel = sound_samples[el].play()
        elif "upper" not in dir(el):
            sound = pygame.sndarray.make_sound(el)
            if config.pygame_bug == 1:
                sound = pygame.sndarray.make_sound(pygame.sndarray.array(sound)[:len(pygame.sndarray.array(sound))/2])
            voice_channel = sound.play()
        while voice_channel.get_busy():
            pygame.time.Clock().tick(25)

# Possibly the argument of ``pygame.time.Clock().tick()`` should be in
# config file...
#
# The following four lines give us a one second break (for CTCSS, PTT and
# other stuff) before closing the ``pygame`` mixer and display some debug
# informations.

logger.info("finishing...")

pygame.time.delay(1000)

# If we've opened serial it's now time to close it.
try:
    if config.serial_port is not None:
        ser.close()
except NameError:
    logging.exception("Couldn't close serial port")


pygame.mixer.quit()

logging.info("goodbye")

# Documentation is a good thing when you need to double or triple your
# Lines-Of-Code index ;)
