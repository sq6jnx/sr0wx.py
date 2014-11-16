Konfiguracja "rdzenia"
======================

W tym miejscu odnajdziesz informacje na temat jak skonfigurować modłuł główny
(rzeń) ``sr0wx``. W zasadzie zobaczysz fragmenty mojego osobistego pliku
``config.py`` z pewnymi dodatkowymi informacjami. To, czego tu **nie**
znajdziesz to informacje w jaki sposób skonfigurować poszczególne moduły. Te
informacje powinieneś znaleźć na innych stronach tej instrukcji.

**Ostrzeżenie**: w instrukcji (jak i w całym ``sr0wx``) możesz znaleźć rzeczy, z
których nie jestem specjalnie dumny. Będę wdzięczny za przesłanie mi poprawek
(np. w postaci patcha).

Część dotyczącą konfiguracji "rdzenia" ``sr0wx`` można podzielić na kilka,
bardzo niewielkich części:

Po pierwsze, konfiguracja subtonu (dość jasna myślę): ::

  CTCSS = 88.8
  playCTCSS = False
  CTCSSVolume = 0.1

Pierwsza linia oznacza, że stacja używa subtonu 88.8 Hz. Innymi dopuszczalnymi
wartościami są wszystkie liczby zmiennoprzecinkowe jak i kody kanałów do ``'A'``
do ``'AL'``.

Fragment ``playCTCSS = False`` oznacza, że subton CTCSS będzie odtwarzany w tle
**tylko wtedy** gdy któryś z modułów o to poprosi. Innymi dopuszczalnymi wartościami
są ``True`` (ton będzie odtwarzany zawsze) i ``None`` (nigdy).

W następnych liniach mam u siebie zdefiniowane w jaki sposób ``sr0wx.py``
uruchami PTT. Dzieje się to poprzez wysłanie sygnału RTS na pinie 7 RS232
podpiętym jako ``dev/ttyS0``. Wartość ``SerialBaudRate`` nie jest w tym momemcie
w jakikolwiek sposób używana, ale w przyszłości być może. ::

  serialPort     = '/dev/ttyS0'
  serialBaudRate = 9600
  
W związku z tym, że moja stacja mówi po polsku mam zdefiniowany język jako
``pl_google`` (jako, że korzystam z sampli ściągniętych z
``translate.google.com``; zobacz także stronę z innymi językami) ::
  
  lang = "pl_google"
  
W następnym kroku definiujemy treść komunikatu początkowego i końcowego. Jako,
że stacja ma podawać również swój znak telegraficznie ładujemy specjalny moduł
zamieniający tekst na telegrafię: ::
 
  from lib.cw import *
  
  helloMsg = ["tu_eksperymentalna_automatyczna_stacja_pogodowa",\
      "sp6yre",cw('sp6yre),]
  goodbyeMsg = ["_","tu_sp6yre",]

I już prawie koniec. Definiowanie jakie moduły mają być uruchamiane podczas
startu jest równie łatwe: ::
  
  modules = ["module_a", "module_b"]

I to już w zasadzie koniec ustawiania modułu głównego, Kolejne linie
``config.py`` to już tylko konfiguracja poszczególnych modułów. Zaczyna się to
małą sztuczką: ::
  
  class m:
      pass

... i wygląda mniej więcej tak: ::
  
  foo_module = m()
  foo_module.option_1 = 'bar'
  

Na koniec bardzo ważna informacja: współczesne wersje  ``PyGame`` i/lub 
``Numeric`` mają jakiś błąd polegający na tym, że zarówno telegrafia jest
odtwarzana dwa razy szybciej jak powinna (a ton CTCSS ma dwa razy wyższą
częstotliwość. Próbujemy ten błąd obejść poprzez: ::

  pygameBug = 1

Jak mawia klasyk, to by było na tyle (zobacz teraz jak skonfigurować
poszczególne, interesujące Cię moduły)!

