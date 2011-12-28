``sms_qst`` -- reading aloud SMS messages
=========================================

Purpose
-------

``sr0wx.py`` is not an emeregency communication/informing package, but in some circumstances it may be useful. These circumstances include situations, when there is or there is no internet connection and someone (with efficient privileges, see below) wants to spread a message around. He or she can d this by sending a text message (sms). Of course, we assume, that GSM networks are still up and running.

Dependiences
------------

There are quite a lot of dependiences. As we may be functioning without any internet connection station needs *any* standalone Text-To-Speech software. There are few of them in Debian-like OSes packages (eSpeak, festival, Mbrola). All of these are free (of charge) and are... understandable. Of course, you can use any paid TTS system if you like.

So first of all you have to have a TTS system installed plus *voice* for your language. This TTS has to be able to produce ``.wav`` or ``.ogg`` file.

Another dependiency is ``python-gammu`` package for reading (and in future) sending SMS messages. Plus, you'll need a cell phone (or, as I did, Internet over a GSM modem) and a SIM card.
  
As I am lazy ``sms_qst`` uses ``sqlite3`` database for collecting SMSes (both received and sent). ``sqlite`` is included in recent distributions of Python, but it would be nice to have it available via command line.

Configuration
--------------

Configuration is a real pain in the bottom.

You'll need a ``.gammurc`` file to let gammu know what kind of device you're going to use. See http://wammu.eu/ for details. My ``.gammurc`` file looks like: ::
  [gammu]
  port=/dev/ttyUSB1
  connection = at19200
  name=huawei unknown

Most of the following will be also OK for you, but let's see what configuration you can make in ``config.py``: ::
  sms_qst = m()
  sms_qst.max_sim_capacity = 255
  sms_qst.leave_messages_on_sim = False 

I have to say that I have no idea how to check how many text messages can fit on a given SIM card, so I've kinda hard-coded it. I don't think that there are bigger cards. Next we have an option for leaving or deleting SMS after receiving. I suggest deleting due to limited capacity and a fact that all messages will be imported again on next run. ::

  sms_qst.db_file = 'sms_qst.sqlite' 
  sms_qst.temp_file = '/tmp/sms_qst_{ID}.wav'

You should probably leave this as is; this is just a filename of database file. More, you should rather leave another option too; this is just an information where sound files will be saved by TTS system and if it will be ``.wav`` or ``ogg``. ``{ID}`` is a placeholder and must be specified in ``temp_file`` variable.

Of course, not everyone should be able to have his or her text message red aloud, so you have to specify phone numbers of these people and therir callsigns::
  
  sms_qst.authorized_senders = {
     '+485018052xx': 'sq6jnx',
     '+486031864xx': 'sq6jnq' }

Now, you should specify what message should be played if there are any new informations ::

  sms_qst.template = """komunikat_specjalny_od {CALL} _ {MESSAGE} _ 
      powtarzam_komunikat _ {MESSAGE}"""

This is *Special message from <callsign> <message goes here>. I repeat <message goes here>*.

That was easy. Now the harder part.

You have to find a way how to convert text to speech with TTS software and save it as a wavefile. Sounds easy, but...

In espeak what you have to do is, for example:

``/usr/bin/espeak -a 200 -p 64 -s 170 "Resistance is futile" -g 10 -v en -w out.wav``

Amazingly, on Festival, when using utf-8 encoded characters and writing in Polish you have to:

``echo "Resistance..." | iconv -f UTF-8 -t ISO_8859-2 | text2wave -o out.wav -eval fest.conf``

The ``-eval`` part is optional and is usefull when you want i.e. to load non-standard voice. In this situation my ``fest.conf`` file looks like: ::
  (voice_pjwstk_pl_ks_mbrola)
  (Parameter.set 'Duration_Stretch 1.25)

This command line fugue has to be written as separate ``subprocess.Popen``-like arrays of arguments, so for example for espeak you'll need something like: ::

  sms_qst.tts_command = [ 
      ['/usr/bin/espeak', '-a', '200', '-p', '64', 
      '-s', '170', '{MESSAGE}', '-g', '10', '-v', 'pl', '-w', 
      sms_qst.temp_file,]
      ]

... and for Festival ::

  sms_qst.tts_command = [
      ['echo', '{MESSAGE}',],
      ['iconv', '-f', 'UTF-8', '-t', 'ISO_8859-2'],
      ['text2wave', '-o', sms_qst.temp_file, '-eval', 'fest.conf']
  ]

... where ``{MESSAGE}`` is a placeholder for SMS text.

Handling text messages
----------------------

Before we start: **ONLY** the lastly received message from configured sender is handled. **ONLY**.

We have three cases in text messages:

  #. ``This is the message`` -- will be read aloud until the end of today (== the day it was sent)

  #. ``2.This is the message`` -- will be played today, tommorow and the day after tommorow.

  #. ``!.This is the message`` -- will be played for ever and it can be stopped by...

  #. *an empty message* -- which is never read and is used to cancel any previous message.

This means that you can cancel *any* message with an empty message.

Language dependant issues
-------------------------

There are no language dependant issues/samples/texts except these defined in ``sms_qst.template`` and ``sms_qst.authorized_senders``.
