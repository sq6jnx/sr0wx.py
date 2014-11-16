Core configuration
==================

This is the place where you can find information about how to configure the
``core`` module of ``sr0wx.py`` project. This is actually my personal
``config.py`` with some additional informations.

What you **won't** find here is how to configure modules. Of course, you can
find it on modules' description pages.

**Warning**: there are some things which I am not proud of. You can probably
find them (and fix them!) on your own. If you will, please send me a patch.

We can divide ``core`` part of ``sr0wx.py`` configuration into several, but
very small, parts:

First, CTCSS (aka subtone). This is going to be easy and self-explanatory: ::

  CTCSS = 88.8
  playCTCSS = False
  CTCSSVolume = 0.1

First line states, that station will be using CTCSS at 88.8 Hz (other possible
values include whole spectrum of floating point numbers or character code from
``'A'`` to ``'AL'``). 

``playCTCSS = False`` means, that CTCSS will be played in
background **only** if any of modules (see below) will ask for it. Other
values include ``True`` (CTCSS is played always) and ``None`` (never).

Next we define how Push-To-Talk is pressed. We do it by sending an RTS signal
(pin 7 on RS232) which is plugged as ``/dev/ttyS0``. ``SerialBaudRate`` is not
used at the moment, but may be usefull in future.::

  serialPort     = '/dev/ttyS0'
  serialBaudRate = 9600
  
As the station is going to speak polish using samples downloaded from Google
Translator we define: (see languages page for mor info) ::
  
  lang = "pl_google"
  
  
Next step is defining how the transmission starts and ends. These are
so-called hello and goodbye messages. As the station is going to give its
callsign in CW we import tiny module to translate text to morse code: ::
 
  from lib.cw import *
  
  helloMsg = ["tu_eksperymentalna_automatyczna_stacja_pogodowa",\
      "sp6yre",cw('sp6yre),]
  goodbyeMsg = ["_","tu_sp6yre",]

Almost done. Defining which modules should be run at each start and in which
order is self explanatory: ::
  
  modules = ["module_a", "module_b"]

Actually, that's all for the ``core``. Next lines (and this is probably 75% of
the whole ``config.py`` are **modules** configuration. This starts from a
dirty hack ...: ::
  
  class m:
      pass

... and usually looks like: ::
  
  foo_module = m()
  foo_module.option_1 = 'bar'
  

Last, but not least, recent versions on ``PyGame`` and/or ``Numeric`` have a
bug which makes CW and CTCSS played twice as fast as it should be and at
doubled frequency. We try to cope with it with: ::

  pygameBug = 1

Oh, almost forget. The values **must** be written in the ``config`` file.
