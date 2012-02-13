How does it work?
=================

We belive that simple is beautifull. The concept of ``sr0wx.py`` is trivial
*but* in some cases it may be quite tricky to tell it what do you want from
it. 

The concept was:
  #. It has to be modular: it has to be able to read and parse data from many
  sources, mainly from the Internet, but with ability to read data from any
  source we could imagine.
  #. It has to be international: we don't know if it will be succesfull, but
  if anyone, **ANYONE**, would like to run such station should be able to do so
  in his or her language.
  #. It has to be free (both as in freedom and as in free beer) and
  #. ... it has to be understandable: there are no good and free (see above)
  Text-to-Speech synthesizers for polish language; in my opinion all of
  them[#]_ are barely understandable. 

.. [#] espeak, mbrola (with default voice), festival and milena. The only good
  one (for festival) was the one created by Krzysztof Szklanny, but it weights
  over 500 MB and I have no idea how to get it work...

Hang on, I see that this is going quite long...

So as you will see on the other pages of this documentation[#]_ use prerecorded
wave samples (I personally call them *phrases*). Recording such phases is a
nontrivial task.

(a misplaced) NOTE: you can't record all phrases well during one session. you 
won't remember to record all of them. these samples won't be clear. Every 
recording session will sound differently so after 2 years you'll be able to 
tell which samples where recorded first, and which were recorded later. 
**DO NOT CARE ABOUT IT!** I'm pretty sure NO ONE will notice it "on the air"!

.. [#] you'll definitelly see it during ``git clone`` process when you'll be
  downloading almost 100 MB of ``ogg`` files. O Gee...


But **how** does it work?
=========================

So when you run ``./sr0wx.py`` the main module (I call it core) loads its 
config. It finds out what language
it should speak, which modules should it run (or *ask*), which is your
favourite CTCSS tone and how to play your callsign on CW, how to press PTT and what playlist
should it play to make you feel like it is saying *hello* and *goodbye*.

That last part is the most important one. Hello-, goodbye-, and module given
informations are, in fact, playlists of ogg samples which are played in the
given order. Core concatenates them in order to create one, longer message.

How modules are told about what should they say and which language should they
use? Well, language is given to them from core and they read their config from
``config.py`` which is shared. Yes, this is quite redundant and looks buggy.
The other informations are retrieved from source or sources where modules
*know* to point to [#]_.

.. [#] this is usually called *business logic* but I state that modules are
  intelligent creatures as business and logic are usually antonyms.

Modules can't play sound by themselves, but they give their playlist back to
the core. What they also give back is the optional information that there's
something bad happening (hydro- or meteo awareness) so it asks core to play a
predefined tone.

If module fails to give back data to the core core shows Python traceback and
carries on collecting data from other modules. This traceback is usually send
back to station's operator by ``cron``. If core fails to find a phrase
(remember? ``ogg`` file) is echoes to stdout and replaces missing sound with
eight CW dots. 

All informations (including verbose chats) informations are stored by 
``debug`` module which is
a piece of... poor code... and should be replaced with something better.

Back to the core. When it has collected all needed data it turns PTT on,
starts playing CTCSS and then the whole playlist.

That's, basicly, all.
