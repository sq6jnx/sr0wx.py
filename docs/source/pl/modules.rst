Moduły
======

``sr0wx.py`` nie istniałby gdyby nie jego moduły. Tu znajdziesz zwarty opis
każdego z nich.

Moduły językowe
---------------

Moduły językowe są niezbędne, aby ``sr0wx.py`` mówił w Twoim języku

==========   ===========
Nazwa        Opis
==========   ===========
pl           Pierwszy pakiet językowy języka polskiego. Korzysta z wcześniej
             przygotowanych sampli
pl_google    Druga wersja języka polskiego, korzysta z sampli wygenerowanych za
             pomocą narzędzia TTS (np. translate.google.com)
==========   ===========

Obecnie bardzo poszukiwane są osoby mówiące biegle po czesku i/lub niemiecku
(tak samo programiści posługujący się tymi językami) do pomocy w uruchomieniu
stacji u styku trzech granic.

Moduły danych
-------------

==========           ===========
Nazwa                Opis
==========           ===========
gopr_lawiny          Ostrzeżenia lawinowe wydawane przez GOPR
hscr_laviny          Ostrzeżenia lawinowe wydawane przez HSCR (Horská služba
                     ČR), czeski GOPR
meteoalarm           Informacje o zagrożeniach meteorologicznych ze strony
                     www.meteoalarm.eu
imgw_podest          Ostrzeżenia hydrologiczne dla Polski 
                     (z www.pogodynka.pl/podest)
povodi_cz            Ostrzeżenia hydrologiczne dla Czech i terenów 
                     przygranicznych (w tym części Polski)
prospect_mp          Ostrzeżenia hydrologiczne dla południowo-wschodniej 
                     części Polski (zobacz 
                     http://www.prospect.pl/index.php?a=article&art_id=83&m=13)
sms_qst              Moduł odczytywania głosowego i dystrybucji informacji SMS 
                     (na dzień 2011-09-05 wciąż w fazie alpha).
sunriset             Godziny wschodu i zachodu słońca dla danych współrzędnych
                     geograficznych
worldweatheronline   Bieżące obserwacje meteo i prognoza krótkoterminowa (moduł
                     konkurencyjny dla y_weather, w teorii pogoda dla podanych
                     współrzędnych geograficznych)
wview                Bieżące obserwacje meteo ze stacji pogodowej podłączonej do
                     komputera (za pomocą oprogramowania wview)                     
y_weather            Informacje o pogodzie z serwisu Yahoo! Weather
===========          ===========

Biblioteki
----------

=====   ===========
Nazwa   Opis
=====   ===========
cw      Generowanie telegrafii np. na potrzeby znamiennika stacji
ctcss   Generator tonu CTCSS
=====   ===========


Moduły narzędziowe
------------------

=================  ===========
Nazwa              Opis
=================  ===========
google_downloader  Narzędzie do pobierania sampli głosowych z 
                   ``translate.google.com`` (wg. nieoficjalnego API Google)
=================  ===========


Moduły przestarzałe
-------------------

============  ===========
Nazwa         Opis
============  ===========
metar         Bieżące informacje pogodowe z lotnisk międzynarodowych
taf           Krótkoterminowa prognoza pogody z lotnisk międzynarodowych.

Więcej modułów
--------------

Jeśli chcesz opisać jakiś moduł proszę, skorzystaj z **szablonu**.

