``imgw_podest`` -- Ostrzeżenia hydrologiczne dla Polski
=======================================================

``imgw_podest`` podaje ostrzeżenia hydrologiczne dla obszaru całego kraju na postawie informacji IMGW.

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

Po wejściu na stronę http://www.pogodynka.pl/polska/podest/ (i dalszych) zobaczysz mapę
zlewni w Polsce. Zlokalizuj miejsce zainstalowania stacji na tej mapie i
określ, wodowskazami z których zlewni będziesz zainteresowany. Po uruchomieniu 
``python imgw_podest.py`` zobaczysz listę zlewni wykorzystywaną przez
``imgw_podest``.

Kolejnym krokiem jest wygenerowanie listy wodowskazów z listy zlewni, którymi
jesteś zainteresowany: ::

   python imgw_podest.py 3
   python imgw_podest.py 4

Wyjście tych poleceń musi się znaleźć w pliku ``config.py`` w miejscu
oznaczonym jak poniżej (w przypadku korzystania z kilku zlewni należy połączyć
wszystkie listy): ::

    imgw_podest = m()

    imgw_podest.wodowskazy = [
        << tutaj! >>
    ]

Kolejnym krokiem jest zawężenie się do tylko tych wodowskazów, którymi jesteś
zainteresowany. Można to zrobić na dwa sposoby: usuwając niepotrzebne wiersze
(kiepsko) lub zakomentowując niepotrzebne znakiem ``#`` (lepiej), np.: ::

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



Z jakich bibliotek moduł korzysta? Całkiem standardowych, jak ``os`` i ``sys``?
Jakichś jeszcze? Jeśli korzysta z ``bardzo_nietypowego_modulu`` napisz skąd go
pobrać i w jakiej wersji był przez Ciebie testowany.

Jeśli nie korzystasz z żadnych cudów napisz po porstu *nic niestandardowego*.


Czy moduł jest w jakiś sposób konfigurowalny? Podaj przykłady, chociażby jak
poniżej: ::

  foo_module = m()
  foo_module.zipcode = '01-234'
  foo_module.hang_computer_on_init = True # True or False. None means "roll a dice"
  foo_module.message = """
  your_computer_will_be_assimilatted_in {RANDOM_NO_OF_SECONDS}
  _ resistance_is_futile"""

gdzie ``{RANDOM_NO_OF_SECONDS}`` jest zamieniane na liczbę sekund plus słowo
*sekund* we właściwym przypadku.

Zależności językowe
--------------------

Z jakich sampli dźwiękowych (słów, fraz) moduł korzysta? Czy i w jaki sposób
można taką listę wygenerować? Podaj przykłady użycia.

