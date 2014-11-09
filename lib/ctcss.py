#!/usr/env/python -tt
# -*- encoding=utf8 -*-
#
#   Copyright 2009-2014 Michal Sadowski (sq6jnx at hamradio dot pl)
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

# This is list of IARU Region I CTCSS tones
# (http://hamradio.pl/sq9jdo/_Kurs/Kurs%20operatora/CTCSS/system_ctcss.html).

CTCSSTones = {'A': 67.0,
              'B': 71.9,
              'C': 74.4,
              'D': 77.0,
              'E': 79.7,
              'F': 82.5,
              'G': 85.4,
              'H': 88.5,
              'I': 91.5,
              'J': 94.8,
              'K': 97.4,
              'L': 100.0,
              'M': 103.5,
              'N': 107.2,
              'O': 110.9,
              'P': 114.8,
              'Q': 118.8,
              'R': 123.0,
              'S': 127.3,
              'T': 131.8,
              'U': 136.5,
              'V': 141.3,
              'W': 146.2,
              'X': 151.4,
              'Y': 156.7,
              'Z': 162.2,
              'AA': 167.9,
              'AB': 173.8,
              'AC': 179.9,
              'AD': 186.2,
              'AE': 192.8,
              'AF': 203.5,
              'AG': 210.7,
              'AH': 218.1,
              'AI': 225.7,
              'AJ': 233.6,
              'AK': 241.8,
              'AL': 250.3,
              }

import numpy.oldnumeric as Numeric


def getCTCSS(tone, sampleRate=44100, peak=0.9):
    # http://www.nabble.com/Chord-player-td21350708.html
    if tone in CTCSSTones:
        tone = CTCSSTones[tone]
    length = sampleRate / float(tone)
    omega = Numeric.pi * 2 / length
    xvalues = Numeric.arange(int(length)) * omega
    oneCycle = ((peak * 32767) * Numeric.sin(xvalues)).astype(Numeric.Int16)
    return Numeric.transpose(Numeric.array((oneCycle, oneCycle)))


def main():
    import pygame
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.init(44100, -16, 2, 1024)
    print "Testing CTCSS capability"
    for tone in sorted(CTCSSTones.keys()):
        print "Tone %s, %s Hz..." % (tone, CTCSSTones[tone])
        s = pygame.sndarray.make_sound(getCTCSS(CTCSSTones[tone]))
        c = s.play(300)
        while c.get_busy():
            pygame.time.wait(25)

if __name__ == '__main__':
    main()
