``gopr_lawiny`` -- Ostrzeżenia lawinowe GOPR
============================================

Przeznaczenie
-------------

Zima w górach bywa niebezpieczna, z tego też względu ``sr0wx.py`` został
wyposażony w możliwość podawania ostrzeżeń lawinowych tak polskiego GOPR jak i
czeskiej HSCR.

Zależności
----------

Nic niestandardowego.

Konfiguracja
------------

Konfiguracja nie powinna nastręczać, nawet laikowi, większych trudności. Należy
zadbać, aby w konfiguracji znalazł się wpis podobny do: ::

    gopr_lawiny = m()
    
    
    gopr_lawiny.region = 1
    gopr_lawiny.podajTendencje = 1
    gopr_lawiny.podajWystawe = 1 # not yet implemented

Gdzie ``region`` przyjmuje wartości jak w tabeli:

=======       ======
Wartość       Region
=======       ======
1             Karkonosze
2             Śnieżnik Kłodzki
3             Babia Góra
4             Pieniny
5             Bieszczady

Dla Śnieżnika Kłodzkiego ostrzeżenia podaje Horska Sluzba CZ (``hscr_laviny``), 
dla Tatr TOPR (właściwego modułu brak). Nie wiem kto podaje ostrzeżenia dla
Pienin, być może tam lawiny nie występują w ogóle?

Zależności językowe
--------------------

W pliku słownika powinny się znaleźć następujące frazy: ::

    ['ę.  komunikat górskiego ochotniczego pogotowia ratunkowego'],
    ["ę.  w karkonoszach"], ["w regionie babiej góry"],
    ["w pieninach"], ["w bieszczadach"], ["ę.  obowiązuje"],
    ["pierwszy"],["drugi"],["trzeci"],["czwarty"],
    ["ę. piąty, najwyższy", 'piaty_najwyzszy'], 
    ['ę.  stopień zagrożenia lawinowego'],
    ['tendencja wzrostowa'],['tendencja spadkowa'],['gopr'],

