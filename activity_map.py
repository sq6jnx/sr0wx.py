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

from config import activity_map as config
import base64
import logging
import json
import urllib

def getData(l):
    """This module does NOT return any data! It is here just to say "hello" to
    map utility!"""

    logger = logging.getLogger(__name__)

    data = {"data": "",
            "needCTCSS": False,
            "debug": None,
            "allOK": True,
            }

    dump = json.dumps(config.data, separators=(',', ':'))
    b64data = base64.urlsafe_b64encode(dump)

    if urllib.urlopen(config.service_url + b64data).read() == 'OK':
        logger.info("Message sent, status OK")
    else:
        msg = "Non-OK response from %s"
        logger.info(msg, config.service_url + b64data)

    return data

if __name__ == '__main__':
    getData('pl_google')
