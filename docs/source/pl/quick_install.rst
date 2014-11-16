Szybka i łatwa instalacja sr0wx
===============================

Ostrzeżenie
-----------

Ten tytuł jest nieco na wyrost. Instalacja sr0wx nie jest może strasznie
skomplikowana, ale rozdział te poświęcę na przygotowanie stacji od A do Z, tj. w
taki sposób, aby na koniec otrzymać kartę CF gotową do włożenia do małego
komputera.

Nie musisz czytać tego rozdziału od deski do deski -- niektóre rzeczy, o których
będę tutaj pisał nie muszą być niezbędne w Twoim przypadku. Może po prostu chcesz
"odpalić" stację na próbę?

I na koniec -- instalację przeprowadzam na moim domowym, nieco leciwym już
laptopie z zainstalowanym Ubuntu 11.10. Spodziewam się, że np. na Windows
instalacja "na kartę CF" może przebiegać nieco inaczej, dlatego też proszę o
wszelkie dodatkowe informacje od osób, którym udało się powtórzyć te proces na
innych, niż Linux, systemach operacyjnych.

Składniki
---------

Jak napisałem na wstępie, instalację będę przeprowadzać z myślą o małym
urządzeniu. Potrzebuję więc:

#. Małego komputera, np. HP Terminal, IGEL, etc

#. Karty CF (4 GB to w zasadzie minimum, choć da się uruchomić na 2 GB)

#. Przejściówki IDE/CF (jeśli terminal nie ma slotu CF; są tanie, ale ciężko je
dostać)

#. Interfejsu RS232/PTT (do opisania później)

a także:

#. Komputera z zainstalowanym serwerem maszyn wirtualnych (tu: VirtualBox)

#. Płyty ISO (np:
http://releases.ubuntu.com/11.10/ubuntu-11.10-server-i386.iso.torrent; odradzam
ISO z ubuntu.pl). 

Przygotowanie maszyny wirtualnej
--------------------------------

Po zainstalowaniu VirtualBox na komputerze należy utworzyć i skonfigurować
wirtualny komputerek. Operacja ta podzielona jest na etapy:

#. Nazwa, np. ``sr0wx_4GB``, system operacyjny Linux, wersja Ubuntu

#. Rozmiar pamięci podstawowej -- wystarczy 256 MB

#. Startowy dysk twardy -- stwórz nowy wirtualny dysk startowy, w kolejnym kroku
pozostaw zaznaczoną opcję VDI, dalej *Dynamically Allocated* (oznacza to, że
plik, w którym będzie zapisany nasz wirtualny dysk będzie rósł w miarę potrzeb
maksymalnie jednak do zadeklarowanego rozmiaru).

#. Kolejny krok wymaga większej uwagi. Uwierz lub nie, ale obraz o wielkości 4
GB **za Chiny Ludowe i obie Koree** nie zmieści się na karcie 4 GB gdyż kilka
lat temu spece od marketingu wpadli na genialny pomysł: 1 MB = 1000 kB
(brakującej różnicy 24 kB przecież nikt nie zauważy). Również
karty jednego producenta o tej samej nominalnej pojemności różnią się między
sobą wielkością. Dla bezpieczeństwa zrób dysk o wielkości 3.5 GB -- na pewno się
zmieści.

.. NOTE:: Dla bezpieczeństwa warto przeprowadzić mniej-więcej taką
    kalkulację:

    4 GB = 4 000 MB = 4 000 000 kB marketingowych
    4 000 000 kB marketingowe = 3 900 MB "prawidłowe" = 3.8 GB (prawidłowe)

    Nie zdziw się jednak, gdy i taki obraz nie zmieści się finalnie na karcie 
    i całą operację będziesz musiał zacząć od początku. 

#. Naciskamy Dalej, Dalej, Dalej...

Przy pierwszym uruchomieniu maszyny wirtualnej zostaniesz poproszony o podanie
obrazu dysku -- należy po prostu wskazać wcześniej ściągnięty plik ISO.

Instalacja Ubuntu Server
-----------------------

Proces instalacji został w wielu miejscach dokładnie opisany, pierwszy-lepszy
link z Google wskazał
http://www.geek.pc.pl/instalacja-ubuntu-server-edition-10-04-lts/. W większości
przypadków instalacja ogranicza się do wciskania dalej, ja jednak dodam swoje
trzy grosze:

#. Nazwa hosta -- proponuję zmienić na nazwę stacji klubowej, znak operatora
lub, najlepiej, na znak pozwolenia na stację automatyczną.

#. Przy okazji partycjonowania dysku proponuję wykorzystać całą dostępną
przestrzeń na partcję główną (``/``) **minus** jakieś 256 MB. Koniecznie należy
ustawić flagę rozruchową. Te 256 zaoszczędzonych megabajtów przeznaczamy na
partycję wymiany (nazwaną *przestrzenią wymiany*).

#. Pełna nazwa użytkownika -- wpisz np. znak opiekuna stacji (Twój znak?), 
lub z braku lepszego pomysłu -- ``sr0wx``.

#. Hasło **musisz** bezwzględnie wprowadzić. Powinno mieć ono minimum 8 znaków w
tym wszystkie z następujących: małe i duże litery, cyfry, znaki specjalne (np.
``!@#$%``, itd.). **UNIKAJ** polskich znaków -- może się skończyć zablokowaniem
konta.

#. Na etapie wyboru oprogramowania proponuję wybrać ``OpenSSH Server`` tak, aby
można było później cokolwiek zrobić zdalnie na komputerku, tj. bez podłączania
klawiatury i monitora.

Po restarcie można się zalogować używając podanych we wcześniejszych krokach
danych (login i hasło). Jako pierwsze należy zmienić hasło użytkownika root
(administratora) poprzez: ::

    sudo passwd root

gdzie jako pierwsze należy ponownie podać swoje hasło a następnie nowe hasło
roota.

Pozostaje jeszcze zezwolić naszemu użytkownikowi (zakładamy, że jest to
``sp6yre`` korzystać z karty dźwiękowej): :: 

    sudo adduser sp6yre audio
    sudo chmod 0666 /dev/snd/*

... a następnie za pomocą programu ``alsamixer`` wszystkie "suwaki" pociągnąć do
maksimum na górę oraz włączyć kanał klawiszem ``M`` ("zapali" się "zielona
lampka").

Warto również w /boot/grub/grub.cfg zamienić set recordfail=1 na 0
(skonsultować!)


Instalacja dodatkowych pakietów
-------------------------------

Instalację nowych pakietów zaczynamy od zaktualizowania całego systemu poprzez
następującą serię poleceń (ostatnie spowoduje restart komputera): ::

    sudo apt-get update
    sudo apt-get dist-upgrade
    sudo apt-get upgrade
    reboot

W kolejnym kroku instalujemy pakiety potrzebne do zainstalowania sr0wx i
bibliotek przez niego wymaganych (lub wymaganych przez moduły sr0wx), a także 
oprogramowanie niezbędne do ściągnięcia polskich fraz: ::
    
    sudo apt-get install git python-pygame python-tz sox lame 
    sudo apt-get install alsa-utils alsa-tools python-serial

Gdy już mamy wszystko można zwolnić nieco miejsca za pomocą: ::

    sudo apt-get clean
    sudo apt-get autoremove

Jeżeli podczas instalacji Ubuntu nie wybrałeś OpenSSH proponuję również dopisać
``openssh-server``.

Instalacja sr0wx z repozytorium
-------------------------------

Repozytorium sr0wx jest przechowywane w serwisie github.com. Repozytorium to
zawiera wszelkie zmiany dokonywane w projekcie (w zasadzie) od samego jego
początku. Nie jest konieczne zaciąganie całego projektu (można pobrać jedynie
tzw. snapshot z ostatnią *wersją*), ale ze względów na łatwiejszą późniejszą
aktualizację skorzystamy z repozytorium git. Wystarczy do tego jedno 
polecenie: ::
    
    git clone git://github.com/sq6jnx/sr0wx.py.git

(w chwili gdy piszę te słowa trzeba ściągnąć historyczne już sample
nagrywane z lektorem; sr0wx już z nich nie korzysta i w zasadzie żadne moduły
poza metar i taf nie będą poprawnie działać... może kiedyś to posprzątam...)

Wchodzimy do katalogu: ::

    cd sr0wx.py


Kolejnym etapem jest dociągnięcie sampli potrzebnych do uruchamianych modułów.
Najpierw jednak należy dokonać kilku zmian:

.. note ::

    Tą część trzeba doszlifować, jest to wprost skopiowane z mojego starego
    maila... 

    3a. zobacz jak jest zbudowany plik pl_google/dictionary.py i dodaj tam
    swój znak. Niektóre z wpisów (bądź nawet całe sekcje!) nie będą Ci 
    potrzebne.

    Przekopiuj

    cp utils/google_tts_downloader.py  pl_google/

    3b. uruchom:

    cd pl_google
    python google_tts_downloader.py dictionary.py

.. note ::

    Należy też znaleźć prosty mechanizm na wyłapywanie potencjalnie za małych
    plików dźwiękowych, tj. takich, które z jakichś powodów nie wygenerowały 
    się poprawnie.

Prawdopodobnie nie będziesz zainteresowany uruchamianiem wszystkich modułów,
proponuję w config.py zostawić te, którymi jesteś zainteresowany. Informacje co
który z nich robi i jak się go konfiguruje znajdziesz w opisie modułu (o ile
zdążył powstać :( ).

Gdy już się ściągnie możemy na próbę odpalić: ::

    python sr0wx.py

.. note :: Może się okazać, że pomimo szczerych chęci dźwięk nie będzie działać.
    U mnie pomogła zmiana ustawień maszyny wirtualnej, tj. w zakładce *Dźwięk*
    zmieniłem sterownik dźwięku gospodarza na *Sterownik dźwięku ALSA*. Problem
    więc leżał nie tam gdzie go szukałem.

Ustawienie regularnego podawania komunikatu
-------------------------------------------

Jeśli planujesz uruchomienie stacji na stałe skonsultuj z grupą dyskusyjną
sr0wx@googlegroups.com z jakim przesunięciem czasowym Twoja stacja może pracować
tak, aby nie nakładała się ona z inną, niedaleko Ciebie.

Do samego uruchamiania stacji najłatwiej jest wykorzystać ``cron`` (Google). 
Pamiętaj jednak, aby zsynchronizować zegar komputera np. poleceniem: ::

    sudo ntpdate ntp.ubuntu.com

Nagrywanie surowego obrazu na kartę
-----------------------------------

.. note :: W jaki sposób zrobić, aby nie trzeba było ręcznie zmieiać eth0 na 
    eth1 w /etc/network/interfaces?

Procedurę należy rozpocząć od wyłączenia maszyny wirtualnej, np. poleceniem
``sudo poweroff``. Następnie należy wyeksportować dysk podanym poleceniem
(UWAGA! wyeksportowany plik będzie miał miał objętość wirtualnego dysku; może
być znacznie większy od pliku ``.vdi``!): ::
    
    cd ~/VirtualBox\ VMs/sr0wx_4GB/
    VBoxManage internalcommands converttoraw sr0wx_4GB.vdi sr0wx_4GB.raw

Następnie poleceniem: ::

    sudo dd if=sr0wx_4GB.raw of=/dev/sdb

... przy założeniu, że pod ``/dev/sdb`` system zamontował świeżo podpiętą kartę
CF. Jeśli pod ``/dev/sdb`` znajduje się coś innego najprawdopodobniej zniknie.

Dostęp zdalny do komputera
--------------------------

Zdalny dostęp do komputera będzie Ci niezbędny w przypadku, gdy będziesz chciał
np. zaktualizować oprogramowanie czy zmienić coś w konfiguracji lub też gdy z
niewiadomych powodów stacja przestanie funkcjonować prawidłowo. W tym celu
właśnie instalowaliśmy OpenSSH (pakiet ``openssh-server``).

Dostęp do komputera możliwy jest teraz poprzez wpisanie polecenia ``ssh
<login>@<IP komputera>``. Dostęp jest oczywiście również możliwy z komputera
pracującego pod kontrolą systemu z rodziny Windows, w tym celu polecam program
putty (http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html).

Oczywiście, jest również możliwy zdalny dostęp do komputera spoza sieci
lokalnej, informacje o tym jak przekierować porty znajdziesz w instrukcji 
obsługi swojego rutera. Warto jednak pamiętać o następujących faktach:

.. warning :: SSH działa domyślnie na porcie 22 i w zakresie sieci lokalnej nie 
    ma potrzeby tego zmieniać. Nie polecam jednak wystawiania na zewnątrz tego 
    portu, dużo bezpieczniej będzie przekierować jakiś losowo wybrany wysoki 
    numer portu z zewnątrz (np. powyżej 20 000) na lokalny port 22

    Warto również ograniczyć dostęp do usługi SSH do wyznaczonych zewnętrznych
    adresów IP. Dobrym pomysłem jest też posługiwanie się kluczami, temat ten
    znacznie wykracza jednak poza tą instrukcję, proponuje samodzielne
    poszukiwanie rozwiązań pod hasłami kluczowymi ``openssh rsa``.

Notatki różne
-------------

Głośność można wyregulować za pomocą polecenia ``alsamixer``.

.. vim: set spelllang=pl spell ft=rst textwidth=80 smartindent tabstop=4:
.. vim: set shiftwidth=4:
