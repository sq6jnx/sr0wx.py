#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# 
CTCSS = 88.8
playCTCSS = False
CTCSSVolume = 0.1
serialPort     = '/dev/ttyS0'
serialBaudRate = 9600

from lib.cw import *

lang = "pl_google"

pygameBug = 1

helloMsg = ["tu","eksperymentalna_automatyczna_stacja_pogodowa",\
    "sp6yre",]#"lokator","jo81ld"]
goodbyeMsg = ["_","tu","sp6yre"]

modules = ["y_weather"]

class m:
    pass


debug = m()
debug.writeLevel = None
debug.showLevel  = 0
