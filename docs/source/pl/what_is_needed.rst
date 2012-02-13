Co jest potrzebne do uruchomienia sr0wx?
========================================

W zasadzie -- niewiele. To, czego potrzeba to:

komputer
  do uruchomienia programu. Może być to dowolna maszyna, na której można
  uruchamiać programy napisane w Pythonie. Największe doświadczenia mamy z
  urządzeniami typu terminal z procesorem ok. 800 MHz, 512 MB RAM i kartą
  pamięci CompactFlash 4GB jako dysk twardy (acz takie same rezultaty osiągamy
  na 400MHz CPU i 256 MB RAM!). Takie terminale mają tą zaletę, że nie zawierają
  żadnych elementów mechanicznych, działają na 12V i są w stanie włączyć się
  same po spadku zasilania.

nadajnik
  do nadawania sygnału audio. Póki co odbiornik nie jest (i najprawdopodobniej
  nigdy nie będzie) potrzebny. Wierzymy, że moc 5--10W jest w zupełności
  wystarczająca dla większości lokalizacji.

połączenie internetowe
  do zapiewnienia dostępu do danych. ``sr0wx.py`` może pobierać dane z wielu
  różnych źródeł (zobacz stronę moduły). Najlepsze efekty otrzymasz podłączając
  się za pomocą przewodu, ale każdy sposób (WiFi, GSM, ...) jest dobry. Przy
  okazji, modem USB może być potrzebny do obsługi modułu ``SMS_QTC``.
  
dobra lokalizacja:
  to znaczy, że: Antena stacji powinna być na tyle wysoko, aby stacja była
  odbierana z odległości 20--50 km; Zasilanie powinno być pewne; Połączenie z
  Internetem zawszedostępne.
  
częstotliwość
  obecnie w Polsce częstotliwość 144.950 jest w pewnym sensie zarezerwowana dla
  ``sr0wx.py`` i podobnych projektów (acz nic nie wiemy o konkurencyjnych
  projektach). Nie powinno być problemów z uruchomieniem projektu w I regionie
  IARU czy nawet na całym Świecie.


