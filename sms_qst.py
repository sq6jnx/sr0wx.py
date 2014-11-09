#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
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
# **********
# sms_qst.py
# **********


from config import sms_qst as config
import datetime
import gammu
import os
import re
import sqlite3
import subprocess

global conn, lang

_validity = re.compile("^(!|\d{1,})\.")


def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def create_db():
    """Creates database for storing send/received SMS messages"""
    global conn
    c = conn.cursor()
    # TODO: these are not primary SQLite types
    c.execute("""\
CREATE TABLE sms_rcvd (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender CHAR(12) NOT NULL,
    message VARCHAR(160) NOT NULL,
    date_rcvd DATETIME NOT NULL,
    valid_until date
);""")
    conn.commit()


def get_validity_date(message, sms_date_time=datetime.date.today()):
    """For each message we've to check if it starts with an
exclamation mark or number followed by a dot (.). Exclamation mark
means that we'll be reading this message until next message arrives.
Number is the number of days when the message will be read aloud
(until tomorrow 23:59:59 is 1, day after tomorrow is 2, etc.)

This function returns datetime of message validity; if none supplied
this is until today, forever is None."""
    head = _validity.findall(message)

    if head == []:
        return (False, str(datetime.datetime.date(sms_date_time)),)
    elif head == ['!']:
        return (True, None,)
    else:
        return (True, str(datetime.datetime.date(sms_date_time\
                                                 + datetime.timedelta(days=int(head[0])))),)


def add_sms_to_db(sender, message, date_rcvd):
    valid_until = get_validity_date(message, date_rcvd)
    if valid_until[0]:
        message = message.split('.', 1)[1]

    c = conn.cursor()
    # TODO: this is debug message
    # print (sender, message, date_rcvd, valid_until[1],)
    # TODO change to SQLite placeholders
    c.execute("""\
INSERT INTO sms_rcvd (sender, message, date_rcvd, valid_until)
VALUES (?,?,?,?);""", (sender, message, date_rcvd, valid_until[1], ))
    conn.commit()


def get_sms_messages():
    sm = gammu.StateMachine()
    sm.ReadConfig()
    sm.Init()

    for f in enumerate(sm.GetSMSFolders()):
        if f[1]['Inbox'] == 1:  # folder is inbox
            for pos in range(config.max_sim_capacity):
                try:
                    sms = sm.GetSMS(f[0], pos)[0]
                    # Debug prints should be logged!
                    # print 'nadawca ', sms['Number']
                    # print 'tresc ', sms['Text']
                    # print 'data otrz ', sms['DateTime']
                    # print 'SMSCDateTime ', sms['SMSCDateTime']
                    # print '----------------------------------------'
                    add_sms_to_db(sms['Number'], sms['Text'],\
                                  sms['DateTime'] or sms['SMSCDateTime'])
                    if not config.leave_messages_on_sim:
                        sm.DeleteSMS(f[0], pos)
                    pos += 1
                except Exception:
                    raise


def get_last_authorized_message():
    global lang, conn
    c = conn.cursor()
    c.execute("""\
SELECT id, sender, message
FROM sms_rcvd
WHERE COALESCE(valid_until, date()) >= date()
ORDER BY date_rcvd DESC;""")

    # TODO: if **last_authorized_message** then for loop in not necessary here
    for sms in c.fetchall():
        if sms[1] in config.authorized_senders.keys():
            callsign = lang.readCallsign(config.authorized_senders[sms[1]])
            return {'id': sms[0],
                    'callsign': callsign,
                    'message': sms[2],
                    }
    return None


def getData(l):
    global lang, conn
    lang = my_import(l + "." + l)
    if config.db_file == ':memory:' or not os.path.isfile(config.db_file):
        conn = sqlite3.connect(config.db_file)
        create_db()
    else:
        conn = sqlite3.connect(config.db_file)

    data = {"data": "",
            "needCTCSS": True,
            "allOK": True,
            }

    get_sms_messages()
    sms = get_last_authorized_message()

    # Empty message means that there is no new message.
    # THIS IS A DIRTY TRICK 'CAUSE I'VE FORGOT ABOUT IT AND I'M LAZY
    if sms is None or sms['message'] == '':
        return {"data": "",
                "needCTCSS": True,
                "allOK": True}
    # END OF DIRTY TRICK

    # TODO: template strings
    config.temp_file = config.temp_file.replace('{ID}', str(sms['id']))
    if not os.path.isfile(config.temp_file):
        for i, command in enumerate(config.tts_command):
            args = []
            for arg in command:
                if arg == '{MESSAGE}':
                    args.append(sms['message'])
                else:
                    arg = arg.replace('{ID}', str(sms['id']))
                    args.append(arg)
            if i == 0:
                p = subprocess.Popen(args, stdout=subprocess.PIPE)
            elif i == len(config.tts_command)-1:
                p = subprocess.Popen(args, stdin=subprocess.PIPE)
            else:
                p = subprocess.Popen(args, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE)

    data['data'] = config.template.format(**{'CALL': sms['callsign'],
                                             'MESSAGE': 'file://%s' % config.temp_file,
                                             })
    return data
