#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

LICENSE = """

Copyright 2009-2014 Michal Sadowski (sq6jnx at hamradio dot pl)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

-----------------------------------------------------------

You can find full list of contributors on github.com/sq6jnx/sr0wx.py

"""


import getopt
import os
import pygame
import sys
import logging, logging.handlers


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

message = " "
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
logger.info(LICENSE)


modules = config.modules

lang = my_import('.'.join((config.lang, config.lang)))
sources = [lang.source, ]

for module in modules:
    try:
        logger.info("starting %s...", module)
        module_data = module.get_data()
        module_message = module_data.get("message", "")
        module_source = module_data.get("source", "")

        message = " ".join((message, module_message))
        if module_message != "" and module_source != "":
            sources.append(module_data['source'])
    except:
        logger.exception("Exception when running %s", module)

message = config.hello_msg + message.split()
if len(sources) > 1:
    message += sources
message += config.goodbye_msg

pygame.mixer.init(16000, -16, 2, 1024)

playlist = []

for el in message:
    if "upper" in dir(el):
        playlist.append(el)
    else:
        playlist.append("[sndarray]")

logger.info("playlist elements: %s", " ".join(playlist))
logger.info("loading sound samples...")

logger.info("playing sound samples")

sound_samples = {}
for el in message:
    if "upper" in dir(el):
        if el[0:7] == 'file://':
            sound_samples[el] = pygame.mixer.Sound(el[7:])
        if el is not "_" and el not in sound_samples:
            if not os.path.isfile(config.lang + "/" + el + ".ogg"):
                logger.warn("Couldn't find %s" % (config.lang + "/" + el + ".ogg"))
            else:
                sound_samples[el] = pygame.mixer.Sound(config.lang + "/" + el + ".ogg")


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

for el in message:
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

logger.info("finishing...")

pygame.time.delay(1000)

try:
    if config.serial_port is not None:
        ser.close()
except NameError:
    logging.exception("Couldn't close serial port")


pygame.mixer.quit()

logging.info("goodbye")
