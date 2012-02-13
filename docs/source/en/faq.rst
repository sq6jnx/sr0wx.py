(in)Frequently Asked Questions
==============================

General
-------

``SR0WX.py``? What is it?
  Oh, gosh... read first paragraph on the main page.

What kind of information can it read?
  Any which you can give to it: weather conditions, weather forecast, all
  kinds of awarenesses, etc. Please, see modules page. If its contents do
  not satisfy you you can always write new module.

Is it expensive?
  Software is licensed under Apache 2.0 License, so no, it is free. Of course,
  hardware may cost you some about 100 EUR (computer, transmitter, antenna...).

Where can I get it from?
  Check project's download page.

What system platforms does it run?
  Theoretically, any platform where current (2.6+) version of Python is
  available. This include all flavors of Linux and recent Windowses, but
  probably also MacOS, palette of BSDs, etc. Please note, that we are not able
  to test it on all possible platforms. We develop and run (and, occasionally
  even test) it under Ubuntu Server LTS.

I'm not a (put system name here) guru. Can you help?
  Probably, yes. Just email either of us and describe your problem. 

Can you assist me in running such station?
  Certainly. We can buy hardware for you, install software on it, configure
  and make some tests with it. We can do it if you'll pay us our money spent
  back. We may add few percent to it, but we won't bankrupt you. But first,
  you have to contact us.

Specific
--------

How to make ``sr0wx.py`` run every X minutes?
  On \*nixes you probably would like to use ``cron``. I've heard that Windows
  *Task manager* was made to do similar jobs.

Can ``sr0wx.py`` send me an email when something goes bad?
  Yes. You have to configure ``debug`` module properly. You probably won't
  install mail server on your computer, so you can use sendemail?

How can I change anything remotely?
  I'd suggest installing openssh server. On Windows machines there is a tool
  called Remote Desktop. I suppose there is such thing on Macs, too.

Stupid
------

It doesn't work!
  See http://i.imgur.com/jacoj.jpg
