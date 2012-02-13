``foo`` -- Opis nieistniejącego modułu
======================================

To jest opis nieistniejącego modułu. Może to być też szablon dla dokumentacji
nowego modułu.

Przeznaczenie
-------------

Napisz trzy lub pięć słów opisujących do czego moduł ten służy. Liczba słów może
być zarówno parzysta lub nieparzysta. Chodzi o to, aby nieco rozrzedzić, ale też
nie lać za dużo wody.

Jeśli moduł korzysta z generowania tonu CTCSS napisz kiedy to robi a kiedy nie.

Zależności
----------

Z jakich bibliotek moduł korzysta? Całkiem standardowych, jak ``os`` i ``sys``?
Jakichś jeszcze? Jeśli korzysta z ``bardzo_nietypowego_modulu`` napisz skąd go
pobrać i w jakiej wersji był przez Ciebie testowany.

Jeśli nie korzystasz z żadnych cudów napisz po porstu *nic niestandardowego*.

Konfiguracja
------------

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

Podziękowania
-------------

dla erb za pomysł i dla maćka za benedyktyńską pracę w sporządzaniu listy stacj
