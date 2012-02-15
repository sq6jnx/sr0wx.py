``povodi_cz`` -- Ostrzeżenia hydrologiczne dla Czech
=====================================================

``povodi_cz`` podaje ostrzeżenia hydrologiczne dla obszaru całego kraju na 
postawie informacji CHMI (Czeskiego Instytutu Hydrometeorologicznego).

Moduł należy do grupy modułów podających informacje o zagrożeniach
hydrologicznych.

Przeznaczenie
-------------

CHMI jest jedyną znaną nam organizacją monitorującą wodowskazy w Czechach.
Biorąc pod uwagę dość rzadką sieć wodowskazów IMGW na terenach przygranicznych i
ograniczony dostęp do informacji o stanach wód zdecydowaliśmy się na stworzenie
modułu podającego ostrzeżenia hydrologiczne dla obszaru całych Czech.

``povodi_cz`` będzie prosić moduł główny o uruchomienie tonu CTCSS w
przypadku wystąpienia stanów alarmowych na którymkolwiek z wodowskazów z
listy (patrz konfiguracja).

Zależności
----------

Pythonowy pakiet BeautifulSoup, http://www.crummy.com/software/BeautifulSoup/, w
wersji 3.2.0 (dostępny w paczkach) ::

    $ python
    Python 2.7.2+ (default, Oct  4 2011, 20:03:08) 
    [GCC 4.6.1] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import BeautifulSoup
    >>> BeautifulSoup.__version__
    '3.2.0'


Konfiguracja
------------

Do poprawnej konfiguracji ``povodi_cz`` przyda się dostęp do 
http://www.pod.cz/portal/sap/pl/index.htm i dalszych stron, gdyż niektóre rzeki
mogą być trudne do zlokalizowania na mapie.

Po pierwsze, wynik polecenia ``python povodi_cz.py conf`` powinien znaleźć się w
``config.py`` i wyglądać mniej więcej tak: ::

    povodi_cz = m()

    povodi_cz.stations = [
        ['pmo1','046'],	# Branná, station Jindřichov
        ['pmo1','035'],	# Desná, station Šumperk
        ['pmo1','001'],	# Morava, station Raškov

        << i tak dalej >>
    ]

Jak znaleźć stację oznaczoną przeze mnie jako ``['pmo1','046']``? Znajduje się
ona na stronie www.**pmo**.cz/portal/sap/pl/mapa_**1**.htm (zwróć uwagę na
pogrubione fragmenty adresu).

Na tym etapie proponuję oznaczyć hashem (``#``) te wodowskazy, których stan nie
jest istotny dla bezpieczeństwa Twojej okolicy, tj. np.: ::    

    povodi_cz.stations = [
        #['pla1','7'],	# Bystřice, station Rohoznice
        #['pla1','2'],	# Bělá, station Častolovice
        ['pla1','3'],	# Bělá, station Jedlová v Orlických horách
        #['pla1','10'],	# Cidlina, station Sány

        << i tak dalej >>
    ]

Drugim krokiem jest uruchomienie 
$ python povodi_cz.py dict

$ python povodi_cz.py json




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

Nazwy wodowskazów znajdujących się na terenie Czech są oczywiście w języku
czeskim, który ma nieco inną melodię od języka polskiego i w związku z tym nazwy
geograficzne rzek i miejscowości muszą być czytane w nieco inny sposób. 

Grzegorz SP6TPW, pomysłodawca modułu, przetłumaczył nazwy niektórych
przygranicznych wodowskazów i rzek, jego praca dostępna jest w pliku 
``pl_google/povodi_cz_dict_pl.py``.

Lista pozostałych sampli tego modułu znajduje się w pliku 
``pl_google/dictionary.py``.

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

Podziękowania
-------------
