#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import subprocess
import sys
import tempfile

from six.moves import urllib

# To be extracted to separate module

class MicrosoftTranslator(object):
    def __init__(self, client_id, client_secret, language):
        self._name = "microsofttranslator"
        self.__client_id = client_id
        self.__client_secret = client_secret
        self._language = language

        self.__access_token = None

    def __get_access_token(self):
        """See https://msdn.microsoft.com/en-us/library/hh454950.aspx
        for details"""
        url = "https://datamarket.accesscontrol.windows.net/v2/OAuth2-13"
        params = {
            "client_id": self.__client_id,
            "client_secret": self.__client_secret,
            "scope": "http://api.microsofttranslator.com",
            "grant_type": "client_credentials"
        }

        data = urllib.parse.urlencode(params)
        data = data.encode('utf-8')
        request = urllib.request.Request(url)
        request.add_header("Content-Type",
                           "application/x-www-form-urlencoded;charset=utf-8")
        f = urllib.request.urlopen(request, data)

        data = json.loads(f.read().decode('utf-8'))
        self.__access_token = data['access_token']

    def speak(self, phrase):
        """https://msdn.microsoft.com/en-us/library/ff512420.aspx"""

        if self.__access_token is None:
            self.__get_access_token()

        app_id = " ".join(("Bearer", self.__access_token))
        params = {
            "appId": " ".join(["Bearer", self.__access_token]),
            "text": phrase,
            "language": self._language,
            "format": "audio/wav",  # or "audio/mp3"
            "options": "MaxQuality|female",  # or "MinSize|male"
        }

        url = "https://api.microsofttranslator.com/V2/Http.svc/Speak?"\
            + "text=" + urllib.parse.quote_plus(phrase.encode('utf-8')) \
            + "&appId=" + urllib.parse.quote_plus(app_id) \
            + "&language=" + params["language"] \
            + "&format=" + params["format"] \
            + "&options=" + params["options"]

        try:
            request = urllib.request.urlopen(url)
            return request.read()
        except urllib.error.HTTPError as e:
            print(e.read())


def main():
    # check if `sox` is available
    try:
        subprocess.call('sox --version'.split())
    except OSError:
        six.print_("It looks like sox is not available. Please install sox",
              file=sys.stderr)
        exit(1)


    # I hope this hacky import is temporary...
    import dictionary

    # Add your credencials here. For details visit
    # https://msdn.microsoft.com/en-us/library/hh454950.aspx
    CLIENT_ID = ""
    CLIENT_SECRET = ""

    tts = MicrosoftTranslator(CLIENT_ID,
                              CLIENT_SECRET,
                              language=dictionary.LANGUAGE)

    for phrase in dictionary.phrases:
        if os.path.exists("%s.wav" % phrase.save_as):
            print("%s already exists" % (phrase.save_as,))
            continue
        print("Downloading %s" % (phrase.save_as,))
        with tempfile.NamedTemporaryFile('wb') as tmp:
            tmp.write(tts.speak(phrase.sounds_like))
            sox_command = "sox {tmp} {save_as}.wav trim {trim_start} {trim_end}"
            sox_status = os.system(sox_command.format(
                tmp=tmp.name,
                save_as=phrase.save_as,
                trim_start=dictionary.TRIM_START,
                trim_end=-abs(dictionary.TRIM_END),
            ))

            if sox_status != 0:
                raise ValueError("sox returned with status %d, not good"
                                 % (sox_status,))



if __name__ == "__main__":
    main()
