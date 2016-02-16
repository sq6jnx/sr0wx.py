#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
#
#   Copyright 2016 Michal Sadowski (sq6jnx at hamradio dot pl)
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

import contextlib

PYSERIAL_AVAILABLE = False
try:
    import serial as pyserial
    PYSERIAL_AVAILABLE = True
except ImportError:
    pass


RPI_GPIO_AVIALABLE = False
try:
    import RPi.GPIO
    RPI_GPIO_AVIALABLE = True
except ImportError:
    pass


def nullptt():
    @contextlib.contextmanager
    def ptt():
        yield
    return ptt

vox = nullptt


def serial(serial_port, signal='DTR'):
    if not PYSERIAL_AVAILABLE:
        raise ImportError("Could not import pyserial")
    if signal not in ('DTR', 'RTS'):
        raise ValueError("Expected DTR or RTS as signal")
    baudrate = 9600

    @contextlib.contextmanager
    def ptt():
        try:
            ser = pyserial.Serial(port=serial_port, baudrate=baudrate)
            if signal == 'DTR':
                ser.setDTR(0)
                ser.setRTS(1)
            else:
                ser.setDTR(1)
                ser.setRTS(0)
            yield
        except:
            raise
        finally:
            try:
                ser.close()
            except UnboundLocalError:
                raise UnboundLocalError("It seems serial port could " +
                                        "not be initialized. Please check " +
                                        "permissions to " + serial_port)
    return ptt


def gpio(bcm_port):
    if not RPI_GPIO_AVIALABLE:
        raise ImportError("Could not import pyserial")

    @contextlib.contextmanager
    def ptt():
        try:
            RPi.GPIO.setmode(RPi.GPIO.BCM)
            RPi.GPIO.setup(bcm_port, RPi.GPIO.OUT)
            RPi.GPIO.output(bcm_port, True)
            yield
        finally:
            RPi.GPIO.output(bcm_port, False)
            RPi.GPIO.cleanup()
    return ptt
