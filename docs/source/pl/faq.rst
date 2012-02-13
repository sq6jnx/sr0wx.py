(nie)Często Zadawane Pytania
============================

Ogólne
------

``SR0WX.py``? A cóż to takiego?
  Oj... Zacznij od przeczytania pierwszego akapitu na stronie głównej.

Jakie rodzaje informacji potrafi to podawać?
  Takie, o jakie poprosisz: obecny stan pogody, prognoza pogody, zagrożenia
  hydrologiczne i meteorologiczne. Obejrzyj stronę z listą modułów. Jeśli nie
  znajdziesz tam źródła potrzebnych ci informacji rozważ napisanie własnego
  modułu.

Ile to kosztuje?
  Oprogramowanie jest udostępniane na licencji Apache 2.0, wiec nie,
  rozpowszechniane jest za darmo. Oczywiście, do tego należy dodać sprzęt, który 
  może cię kosztować jakieś
  300 PLN (komputer, nadajnik, antena...).

Skąd mogę to ściągnąć??
  Sprawdź stronę "Pobierz". Link powinien być gdzieś na stronie głównej.

Na jakich systemach operacyjnych to działa?
  Teoretycznie na każdym, dla którego istnieje w miarę współczesna (2.6 lub
  nowsza) wersja Pythona. Zaliczają się do tego wszelakie rodzaje Linuksa,
  współczesne Windowsy, pewnie także MacOS i wiele, wiele innych. Weź jednak pod
  uwagę, że oprogramowanie tworzymy (i co nieco testujemy) pod współcześnie 
  wspieraną wersją Ubuntu LTS.
  
Nie jestem specjalistą od (tu nazwa systemu operacyjnego). Pomożecie?A
  Pomożemy!, przynajmniej na tyle na ile będziemy mogli. Wyślij nam maila z
  opisem problemu.

Czy pomożecie mi w uruchomieniu stacji?
  Jasne! Możemy skompletować za ciebie większość sprzętu, zainstalować na nim
  oprogramowanie i przetestować jak się zachowuje a to za zwrot kosztów wydanych
  na sprzęt. Zachowujemy sobie prawo do doliczenia kilku procent, ale na pewno
  nie zbankrutujesz na tym. Ale najpierw -- wyślij nam maila.

Szczegółowe
-----------

Jak zmusić ``sr0wx.py`` do podawania komunikatów co X minut?
  Na systemach \*nixowych prawdopodobnie najlepszym pomysłem będzie ``cron``.
  Słyszałem, że windowsowy *Menedżer zadań* spełnia podobne funkcje.

Czy ``sr0wx.py`` może wysłać mi maila gdy coś pójdzie nie tak?
  Tak. Musisz skonfigurować poprawnie moduł ``debug``. Pewnie nie będziesz
  chciał konfigurować serwera poczty, więc pewnie wystarczy ci ``sendemail``?

Czy da się stacje skonfigurować zdalnie?
  Sugerowałbym zainstalowanie na stacji serwera OpenSSH. W przypadku komputerów
  z Windows jest narzędzie zwane Zdalny Pulpit. Dla Maców też coś takiego się
  znajdzie. 

Głupie
------

Nie bangla!!
  Zobacz http://i.imgur.com/jacoj.jpg
