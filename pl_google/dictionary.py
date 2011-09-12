#!/usr/bin/python
# -*- coding: utf-8 -*-

# Caution! I am not responsible for using these samples. Use at your own risk
# Google, Inc. is the copyright holder of samples downloaded with this tool.
#
# Unfortunatelly, Google gives no license text for these samples. I hope
# they're made with free (beer)/open source/free (freedom) software,
# but I have no idea.

# This is the GENERAL download list and settings for polish language 

LANGUAGE = 'pl'

CUT_START = 0.9
CUT_END=0.7

CUT_PREFIX = 'ę. '
CUT_SUFFIX = ' k'

download_list = [
# welcome and goodbye messages
["tu eksperymentalna automatyczna stacja pogodowa k",],
["tu automatyczna stacja pogodowa powiatu brzeskiego"],

["ę. Stanisław Paweł 6 Jokohama - Roman, Ewa", "sp6yre"],
["ę. stanisław kłebek 6 jadwiga natalia kłebek ", "sq6jnq"],
["ę. stanisław kłebek 6 adam cezary maria", "sq6acm"],


["tu Stanisław Paweł 6 Jokohama, Roman, Ewa", 'tu_sp6yre'],
["tu stanisław kłebek 6 jadwiga natalia kłebek k", 'tu_sq6jnq'],
["tu stanisław kłebek 6 adam cezary maria", 'tu_sq6acm'],

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

["zero"],
["zero zero"], ["jeden"],
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

# nazwy zjawisk pogodowych (dla Yahoo! Weather)
['bezchmurnie'], ['burza'], ['burza tropikalna'], ['częściowe zachmurzenie'],
['deszcz'], ['deszcz i deszcz ze śniegiem'], ['deszcz i grad'],
['deszcz ze śniegiem'], ['grad'], ['huragan'], ['intensywne opady śniegu'],
['marznąca mżawka'], ['marznący deszcz'], ['mgła'], ['mżawka'], ['pochmurno'],
['przelotne opady'], ['przelotne opady śniegu'], ['przymrozki'],
['pył'], ['silne burze'], ['silny wiatr'], ['słabe zachmurzenie'],
['słaby śnieg'], ['smog'], ['śnieg'], ['śnieg i deszcz ze śniegiem'],
['tornado'], ['wietrznie'], ['wysokie temperatury'], ['zamglenia'],
['zawieje śnieżne'],


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
["godziny"], ["temperatura od"],

["pierwsza"], ["druga"], ["trzecia"], ["czwarta"], ["piąta"],
["szósta"], ["siódma"], ["ósma","osma"], ["dziewiąta"], ["dziesiąta"],
["jedenasta"], ["dwunasta"], ["trzynasta"], ["czternasta"],
["piętnasta"], ["szesnasta"], ["siedemnasta"], ["osiemnasta"],
["dziewiętnasta"], ["dwudziesta"],

["kierunek wiatru"], ["metr na sekundę"], ["metry na sekundę"],
["metrów na sekunde"], ["ciśnienie"], ["hektopaskal"],
["hektopaskale"], ["hektopaskali"], ["tendencja spadkowa"],
["tendencja wzrostowa"], ["temperatura odczuwalna"],
["temperatura minimalna"], ["maksymalna"],
["następnie"],

# literowanie polskie wg. "Krótkofalarstwo i radiokomunikacja - poradnik", 
# Łukasz Komsta SQ8QED, Wydawnictwa Komunikacji i Łączności Warszawa, 2001,
# str. 130 (z drobnymi modyfikacjami fonetycznymi)

['adam', 'a'],
['barbara', 'b'],
['celina', 'c'],
['dorota', 'd'],
['edward', 'e'],
['franciszek', 'f'],
['gustaw', 'g'],
['henryk', 'h'],
['irena', 'i'],
['józef', 'j'],
['karol', 'k'],
['ludwik', 'l'],
['marek', 'm'],
['natalia', 'n'],
['olga', 'o'],
['paweł', 'p'],
['kłebek', 'q'], # wł. Quebec
['roman', 'r'],
['stefan', 's'],
['tadeusz', 't'],
['urszula', 'u'],
['violetta', 'v'],
['wacław', 'w'],
['xawery', 'x'],
['ypsylon', 'y'], # wł. Ypsilon
['zygmunt', 'z'],

]
