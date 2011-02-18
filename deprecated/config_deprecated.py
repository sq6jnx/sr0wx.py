#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
#
# ********************
# config_deprecated.py
# ********************

# This module shows how deprecated modules were configured. Just for reference.

# -----------
# imgw-hydro
# -----------

imgw_hydro = m()

# Nie chce mi się pisać po angielsku. Nie ma to chyba większego 
# sensu, z racji tego, że IMGW podaje informacje hydro tylko dla
# regionu Polski. Dane są pobierane ze strony 
# [http://pogodynka.pl/hydrobiuletyn.php], jednak nazwy wodowskazów
# są z pewnych względów zmodyfikowane na potrzeby modułu.
#
# Najlepszym sposobem na sprawdzenie jakie wodowskazy są dostępne
# jest wpisanie jakiejś niepoprawnej nazwy wodowskazu (np. potocznej 
# nazwy określającej część ciała poniżej pleców), np:
# 
# imgw_hydro.wodowskazy = ['uda']
#
# moduł zwróci błąd, ale wyświetli dostępne nazwy. Nazwy wodowskazów
# powinny być w formie Pythonowej tablicy.

imgw_hydro.wodowskazy = ['chalupki', 'miedonia', 'kozle', 'krapkowice', 'opole', 'ujscie_nysy', 'trestno', 'brzeg_dolny', 'malczyce', 'scinawa', 'glogow', 'klodzko', 'skorogoszcz', 'jarnoltow', 'piatnica', 'osetno', 'zagan', 'zgorzelec', 'gubin']

imgw_hydro.podajStan = 1
imgw_hydro.podajTendencje = 0 
