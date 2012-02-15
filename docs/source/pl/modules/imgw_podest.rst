``imgw_podest`` -- Ostrzeżenia hydrologiczne dla Polski
=======================================================

``imgw_podest`` podaje ostrzeżenia hydrologiczne dla obszaru całego kraju na 
postawie informacji IMGW.

Przeznaczenie
-------------

IMGW monitoruje zdecydowaną większość wodowskazów w Polsce. Oczywiście, nie ma
żadnej potrzeby, aby ``sr0wx.py`` informował o przekroczeniach stanów
wodowskazów w zupełnie innej części kraju, stąd też opiekun stacji ma
możliwość zawężenia listy wodowskazów do tych, którymi jest najbardziej
zainteresowany.

``imgw_podest`` będzie prosić moduł główny o uruchomienie tonu CTCSS w
przypadku wystąpienia stanów alarmowcch na którymkolwiek z wodowskazów z
listy (patrz konfiguracja).

Zależności
----------

Nic niestandardowego.

Konfiguracja
------------

Konfiguracja ``imgw_podest`` do trywialnych nie należy, ale można przez nią
przejść w ciągu kwadransa (no, może trzech).

Po wejściu na stronę http://www.pogodynka.pl/polska/podest/ (i dalszych) 
zobaczysz mapę zlewni w Polsce. Zlokalizuj miejsce zainstalowania stacji na tej 
mapie i, najlepiej, zanotuj nazwy interesujących cię wodowskazów.
Po uruchomieniu ``python imgw_podest.py`` zobaczysz listę zlewni wykorzystywaną 
przez ``imgw_podest``.

Kolejnym krokiem jest wygenerowanie listy wodowskazów z listy zlewni, którymi
jesteś zainteresowany: ::

   python imgw_podest.py 3
   python imgw_podest.py 4

Wyjście tych poleceń **musi** się znaleźć w pliku ``config.py`` w miejscu
oznaczonym jak poniżej (w przypadku korzystania z kilku zlewni należy połączyć
wszystkie listy): ::

    imgw_podest = m()

    imgw_podest.wodowskazy = [
        << tutaj! >>
    ]

Kolejnym krokiem jest zawężenie się do tylko tych wodowskazów, którymi jesteś
zainteresowany. Można to zrobić na dwa sposoby: usuwając niepotrzebne wiersze
(kiepsko) lub komentując niepotrzebne znakiem ``#`` (lepiej), np.: ::

    imgw_podest = m()

    imgw_podest.wodowskazy = [
        #'3.149180010',   # Nazwa: Krzyżanowice, rzeka: Odra
        #'3.149180020',   # Nazwa: Chałupki, rzeka: Odra
        #'3.149180030',   # Nazwa: Łaziska, rzeka: Olza
        '3.149180060',   # Nazwa: Cieszyn, rzeka: Olza
        '3.149180070',   # Nazwa: Cieszyn, rzeka: Olza-Młynówka
        '3.149180130',   # Nazwa: Istebna, rzeka: Olza
        #'3.149180300',   # Nazwa: Olza, rzeka: Odra
        #'3.150150010',   # Nazwa: Mirsk, rzeka: Kwisa
        #'3.150150020',   # Nazwa: Mirsk, rzeka: Czarny Potok

    << i tak dalej... >>
        ]

W ten sposób, pomimo przerośniętego pliku konfiguracyjnego, zyskujemy łatwość
w aktualizowaniu listy wodowskazów.

Zależności językowe
--------------------

Po sporządzeniu listy interesujących Cię wodowskazów kolejnym krokiem jest
wygenerowanie pliku słownika. Niestety, ``imgw_podest`` ma w obecnie
(2012-02-15) wadę polegającą na tym, że w pliku słownika będą wszystkie nazwy
używane w danej zlewni. Wspomniany plik słownika można wygenerować za 
pomocą: ::

    python imgw_podest gen 3

Po "przepuszczeniu" go przez np. skrypt ściągający sample w kilka chwil mamy
wszystkie potrzebne frazy gotowe do użytku.

Uwaga!
------

W zależności od wybranej zlewni moduł pobiera całkiem znaczne ilości danych
(nawet 300 kB). Weź to pod uwagę przy korzystaniu z łącz, przy których płacisz
za każdy przesłany megabajt...
