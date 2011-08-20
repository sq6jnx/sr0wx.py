#!/usr/bin/python
# -*- coding: utf-8 -*-

# Caution! I am not responsible for using these samples. Use at your own risk
# Google, Inc. is the copyright holder of samples downloaded with this tool.

language = 'pl'

CUT_START = 0.9
CUT_END=0.7

download_list = [
# say... and save output file as...
["tu eksperymentalna automatyczna stacja pogodowa k",],
["ę. Stanisław Paweł 6 Jokohama - Roman, Ewa", "sp6yre"],

["stan pogody z dnia k",],

["pierwszego"], ["drugiego"], ["trzeciego"], ["czwartego"],
["piątego"], ["szóstego"], ["siódmego"], 
["ę. ósmego", 'osmego'], ["dziewiątego"], ["dziesiątego"], 
["jedenastego"], ["dwunastego"],
["trzynastego"], ["czternastego"], ["piętnastego"],
["szesnastego"], ["siedemnastego"], ["osiemnastego"],
["dziewiętnastego"], ["dwudziestego"], ["trzydziestego"],

["stycznia"],
["lutego"], ["marca"], ["kwietnia"], ["maja"], ["czerwca"],
["lipca"], ["sierpnia"], ["września"], ["października"],
["listopada"], ["grudnia"],


["jeden"],
["dwa"], ["trzy"], ["cztery"], ["pięć"], ["sześć"],
["siedem"], ["osiem"], ["dziewięć"], ["dziesięć"],
["jedenaście"], ["dwanaście"], ["trzynaście"],
["czternaście"], ["piętnaście"], ["szesnaście"],
["siedemnaście"], ["osiemnaście"], ["dziewiętnaście"],
["dwadzieścia"], ["trzydzieści"], ["czterdzieści"],
["pięćdziesiąt"], ["sześćdziesiąt"], ["siedemdziesiąt"],
["osiemdziesiąt"], ["dziewięćdziesiąt"], ["sto"], 
["dwieście"], ["trzysta"], ["czterysta"], ["pięćset"],
["sześćset"], ["siedemset"], ["osiemset"], ["dziewięćset"],
["tysiąc"],

# nazwy zjawisk pogodowych (Y!)
["bezchmurnie"], ["burza"], ["burza tropikalna"],
["burze"], ["częściowe zachmurzenie"],
["deszcz"], ["deszcz ze śniegiem"], ["huragan"],
["intensywne opady śniegu"],
["marznące opady"], ["deszcz"], ["snieg"],
["marznacy deszcz"], ["mgła"], ["mrzawka"],
["przelotne_opady"], ["deszcz"], ["śnieg"],
["przymrozki"], ["pył"], ["silne burze"],
["silny wiatr"], ["słabe zachmurzenie"],
["smog"], ["śnieg"], ["śnieg z deszczem"],
["trąba powietrzna"], ["wysokie temperatury"],
["zachmurzenie całkowite"], 
["zachmurzeniełumiarkowane"],
["zamieć"], ["zawieje i zamiecie śniezne"],
#
## różne
["temperatura"], ["stopień celsjusza"],
["minus"], ["stopnie celsjusza"], ["stopni celsjusza"],
["kierunek wiatr"], ["północny"], ["północno"], ["wschodni"],
["wschodnio"], ["zachodni"], ["zachodnio"], ["południowy"],
["południowo"], ["wilgotność"], ["procent"], ["prędkość wiatru"],
["metr na sekundę"], ["metrów na sekundę"], ["stopni"],
["widoczność"], ["kilometr"], ["kilometry"],
["kilometrów"], ["temperatura odczuwalna"],
["prognoza na następne"], ["godzin"],["godzina"],
["godziny"], ["temperatura od"], ["do"],

["pierwsza"],
["druga"],
["trzecia"],
["czwarta"],
["piąta"],
["szósta"],
["siódma"],
["ósma","osma"],
["dziewiąta"],
["dziesiąta"],
["jedenasta"],
["dwunasta"],
["trzynasta"],
["czternasta"],
["piętnasta"],
["szesnasta"],
["siedemnasta"],
["osiemnasta"],
["dziewiętnasta"],
["dwudziesta"],
["kierunek wiatru"],

["metr na sekundę"],
["metry na sekundę"],
["metrów na sekunde"],
["ciśnienie"],
["hektopaskal"],
["hektopaskale"],
["hektopaskali"],
["tendencja spadkowa"],
["tendencja wzrostowa"],
["temepatura odczuwalna"],
["od"],
["tu"],
["do"],
["następnie"],

]

import urllib
import os
import subprocess


for word in download_list:
    phrase = word[0]
    if len(word)==1:
        filename = phrase.replace(' ','_').replace("ą","a").replace("ć","c").replace("ę","e").\
		replace("ł","l").replace("ń","n").replace("ó","o").replace("ś","s").\
		replace("ź","z").replace("ż","z")
        if phrase[0:3]=="ę.":
            filename=filename[4:]
        if phrase[-1] == "k":
            filename = filename[0:-2]
    else:
        filename = word[1]

    if not os.path.exists("%s.ogg"%filename):
        start, end = (0,0.4575)
        if phrase[0:3]=="ę.":
            start = 0.5
        if phrase[-1] == "k":
            end = 0.73

        url = "\"http://translate.google.com/translate_tts?tl=pl&q=%s\""%urllib.quote_plus(phrase+" .")
        os.system("wget -q -U \"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6\" -O %s.mp3 %s"%(filename,url))
        os.system("lame --decode %s.mp3 %s.wav"%(filename,filename))
        length = float(subprocess.Popen(["soxi", "-D", "%s.wav"%filename], stdout=subprocess.PIPE).communicate()[0])
    
        os.system("sox %s.wav %s.ogg trim %s %s"%(filename,filename, str(start), str(length-end)))
        
        #os.system("mplayer %s.ogg"%filename)
        os.remove(filename+".wav")
        os.remove(filename+".mp3")
