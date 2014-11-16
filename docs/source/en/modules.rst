Modules
=======

``sr0wx.py`` is nothing without its modules. Here you can find short list of them:

Language modules
----------------

Language modules are needed to tell ``sr0wx.py`` how to speak in your language.

=========   ===========
Code        Description
=========   ===========
pl          First (and poorly implemented) language. Utilizes previously recorded samples
pl_google   Second impression, utilizes ``translate.google.com`` samples. As of 2011-09-05 still in alpha-stage.
=========   ===========





We're currently looking for czech and german native
speakers/programmers to help us develop these languages (as we're going 
to run a station on polish/czech/german border). If you'd like to develop 
your language (any language, even klingon) you're are very welcome.

Data modules
------------

===========   ===========
Name          Description
===========   ===========
metar         Current weather conditions on the nearest international airport
taf           Short-term weather forecast from nearest international airport 
              weather service
meteoalarm    Regional meteo awarenesses as listed on ``www.meteoalarm.eu``
imgw_podest   Hydrological awarenesses for Poland (via www.pogodynka.pl/podest)
y_weather     World-wide weather forecast from Yahoo! Weather
===========   ===========

Library modules
---------------

=====   ===========
Name    Description
=====   ===========
cw      CW sound generation (jak to napisać że na potrzeby znamiennika stajci automatycznej?)
ctcss   CTCSS tone generation
=====   ===========


Utility modules
---------------

=================  ===========
Name               Description
=================  ===========
google_downloader  Utility to download all needed samples from
                   ``translate.google.com`` instead of recording and cutting them
=================  ===========

More modules
------------

If you'd like to write your own module please fill in the gaps in **module
description template**.

