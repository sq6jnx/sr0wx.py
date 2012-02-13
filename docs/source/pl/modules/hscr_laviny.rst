``hscr_lawiny`` -- Ostrzeżenia lawinowe HS CR
=============================================

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

    hscr_laviny = m()
    hscr_laviny.region = "Jesen"
    hscr_laviny.giveTendention = 1
    hscr_laviny.giveExposition = 1   # not yet implemented

Gdzie ``region`` powinien być fragmentem napisu "Krkonoše" lub "Jeseníky"

Dla Karkonoszy, Babiej Góry i Bieszczad ostrzeżenia podaje GOPR, zagrożenia 
dla Tatr podaje TOPR.

Zależności językowe
--------------------

W pliku słownika powinny się znaleźć następujące frazy: ::

    ['komunikat czeskiej służby ratownictwa górskiego'],
    ['w karkonoszach'],['w jesionikach i masywie śnieżnika'], ['obowiązuje'],
    ["pierwszy"],["drugi"],["trzeci"],["czwarty"],
    ["piąty, najwyższy", 'piaty_najwyzszy'], ['stopień zagrożenia lawinowego'],
    ['tendencja wzrostowa'],['tendencja spadkowa'], 
    ['służba górska republiki czeskiej','hscr'],
