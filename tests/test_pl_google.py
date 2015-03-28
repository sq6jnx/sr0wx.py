# -*- coding: utf-8 -*-

import unittest
import pl_google.pl_google as pl_google
import datetime

class TestKwotaSlownieFunctions(unittest.TestCase):
    """Klasa do testów jednostkowych"""

    def setUp(self):
        self.lang = pl_google.PLGoogle()
        pass

    def test_read_number(self):
        self.assertEqual(self.lang.read_number(5), "piec")
        self.assertEqual(self.lang.read_number(42), "czterdziesci dwa")
        self.assertEqual(self.lang.read_number(666), "szescset szescdziesiat szesc")
        self.assertEqual(self.lang.read_number(1024), "tysiac dwadziescia cztery")

    def test_read_pressure(self):
        self.assertEqual(self.lang.read_pressure(1), "jeden hektopaskal")
        self.assertEqual(self.lang.read_pressure(999), "dziewiecset dziewiecdziesiat dziewiec hektopaskali")
        self.assertEqual(self.lang.read_pressure(1002), "tysiac dwa hektopaskale")

    def test_read_percent(self):
        self.assertEqual(self.lang.read_percent(1), "jeden procent")
        self.assertEqual(self.lang.read_percent(2), "dwa procent")
        self.assertEqual(self.lang.read_percent(5), "piec procent")

    def test_read_temperature(self):
        self.assertEqual(self.lang.read_temperature(-20), "minus dwadziescia stopni_celsjusza")
        self.assertEqual(self.lang.read_temperature(-2), "minus dwa stopnie_celsjusza")
        self.assertEqual(self.lang.read_temperature(-1), "minus jeden stopien_celsjusza")
        self.assertEqual(self.lang.read_temperature(0), "zero stopni_celsjusza")
        self.assertEqual(self.lang.read_temperature(1), "jeden stopien_celsjusza")
        self.assertEqual(self.lang.read_temperature(2), "dwa stopnie_celsjusza")
        self.assertEqual(self.lang.read_temperature(20), "dwadziescia stopni_celsjusza")

    def test_read_speed(self):
        self.assertEqual(self.lang.read_speed(1, unit='mps'), "jeden metr_na_sekunde")
        self.assertEqual(self.lang.read_speed(2, unit='mps'), "dwa metry_na_sekunde")
        self.assertEqual(self.lang.read_speed(5, unit='mps'), "piec metrow_na_sekunde")
        self.assertEqual(self.lang.read_speed(1, unit='kmph'), "jeden kilometr_na_godzine")
        self.assertEqual(self.lang.read_speed(2, unit='kmph'), "dwa kilometry_na_godzine")
        self.assertEqual(self.lang.read_speed(5, unit='kmph'), "piec kilometrow_na_godzine")

    def test_read_degrees(self):
        self.assertEqual(self.lang.read_degrees(0), "zero stopni")
        self.assertEqual(self.lang.read_degrees(1), "jeden stopien")
        self.assertEqual(self.lang.read_degrees(2), "dwa stopnie")
        self.assertEqual(self.lang.read_degrees(5), "piec stopni")

    def test_read_direction(self):
        testcases = {
            'N':   ('polnocny',                       'polnocny',),
            'NNE': ('polnocno-polnocno-wschodni',     'polnocno-wschodni',),
            'NE':  ('polnocno-wschodni',              'polnocno-wschodni',),
            'ENE': ('wschodnio-polnocno-wschodni',   'polnocno-wschodni',),
            'E':   ('wschodni',                       'wschodni',),
            'ESE': ('wschodnio-poludniowo-wschodni',  'poludniowo-wschodni',),
            'SE':  ('poludniowo-wschodni',             'poludniowo-wschodni',),
            'SSE': ('poludniowo-poludniowo-wschodni', 'poludniowo-wschodni',),
            'S':   ('poludniowy',                     'poludniowy',),
            'SSW': ('poludniowo-poludniowo-zachodni', 'poludniowo-zachodni',),
            'SW':  ('poludniowo-zachodni',            'poludniowo-zachodni',),
            'WSW': ('zachodnio-poludniowo-zachodni',  'poludniowo-zachodni',),
            'W':   ('zachodni',                       'zachodni',),
            'WNW': ('zachodnio-polnocno-zachodni',    'polnocno-zachodni',),
            'NW':  ('polnocno-zachodni',              'polnocno-zachodni',),
            'NNW': ('polnocno-polnocno-zachodni',     'polnocno-zachodni',),
        }
        for testcase in testcases.items():
            test, result = testcase
            self.assertEqual(self.lang.read_direction(test), result[0])
            self.assertEqual(self.lang.read_direction(test, short=True), result[1])

    def test_read_datetime(self):
        in_fmt = '%Y-%m-%d %H:%M'
        out_fmt = '%d %B %H %M'

        self.assertEqual(self.lang.read_datetime(datetime.datetime.strptime('1983-06-04 14:26', in_fmt), out_fmt='%d %B %H %M'),
                         'czwartego czerwca czternasta dwadziescia szesc')
        self.assertEqual(self.lang.read_datetime('2014-11-29 18:27', in_fmt=in_fmt, out_fmt='%d %B %H %M'),
                         'dwudziestego dziewiatego listopada osiemnasta dwadziescia siedem')
        self.assertEqual(self.lang.read_datetime('2014-05-03 0:00', in_fmt=in_fmt, out_fmt='%d %B godzina %H %M'),
                         'trzeciego maja godzina zero zero-zero')
        self.assertEqual(self.lang.read_datetime('2014-05-03 20:00', in_fmt=in_fmt,
                         out_fmt=out_fmt),
                         'trzeciego maja dwudziesta zero-zero')
        self.assertEqual(self.lang.read_datetime('2014-05-03 21:05', in_fmt=in_fmt, out_fmt=out_fmt),
                         'trzeciego maja dwudziesta pierwsza piec')
        self.assertEqual(self.lang.read_datetime('2014-05-03 08:25 AM',
                                                 in_fmt='%Y-%m-%d %I:%M %p',
                                                 out_fmt=out_fmt),
                         'trzeciego maja osma dwadziescia piec')
        self.assertEqual(self.lang.read_datetime('2014-05-03 08:25 PM',
                                                 in_fmt='%Y-%m-%d %I:%M %p',
                                                 out_fmt=out_fmt),
                         'trzeciego maja dwudziesta dwadziescia piec')
        self.assertRaises(ValueError, self.lang.read_datetime,
                          *('2014-05-03 0:00', '%d %B %%', in_fmt)),
        self.assertRaises(TypeError, self.lang.read_datetime,
                          *('2014-05-03 0:00', '%d', None)),

    def test_read_callsign(self):
        self.assertEqual("stefan quebec szesc jozef natalia xawery "
                          "lamane pawel", self.lang.read_callsign('sq6jnx/p'))
        self.assertRaises(ValueError, self.lang.read_callsign, *('sq?jnx',))
if __name__ == '__main__':
    unittest.main()
