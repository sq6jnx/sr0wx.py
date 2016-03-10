# -*- coding: utf-8 -*-

import unittest
import pl_microsoft.pl_microsoft as pl_microsoft
import datetime


class TestPLMicrosoft(unittest.TestCase):
    def setUp(self):
        self.lang = pl_microsoft.PLMicrosoft()

    def test_read_number(self):
        test_cases = {
            5: "piec",
            42: "czterdziesci dwa",
            666: "szescset szescdziesiat szesc",
            1024: "tysiac dwadziescia cztery",
        }

        for value, expected in test_cases.items():
            self.assertEqual(expected, self.lang.read_number(value))

    def test_read_pressure(self):
        test_cases = {
            1: "jeden hektopaskal",
            999: "dziewiecset dziewiecdziesiat dziewiec hektopaskali",
            1002: "tysiac dwa hektopaskale",
        }

        for value, expected in test_cases.items():
            self.assertEqual(expected, self.lang.read_pressure(value))

    def test_read_percent(self):
        test_cases = {
            1: "jeden procent",
            2: "dwa procent",
            5: "piec procent",
        }

        for value, expected in test_cases.items():
            self.assertEqual(expected, self.lang.read_percent(value))

    def test_read_temperature(self):
        test_cases = {
            -20: "minus dwadziescia stopni_celsjusza",
            -2: "minus dwa stopnie_celsjusza",
            -1: "minus jeden stopien_celsjusza",
            0: "zero stopni_celsjusza",
            1: "jeden stopien_celsjusza",
            2: "dwa stopnie_celsjusza",
            20: "dwadziescia stopni_celsjusza",
        }

        for value, expected in test_cases.items():
            self.assertEqual(expected, self.lang.read_temperature(value))

    def test_read_speed(self):
        multiple_test_cases = {
            'mps': {
                1:  "jeden metr_na_sekunde",
                2:  "dwa metry_na_sekunde",
                5:  "piec metrow_na_sekunde",
            },
            'kmph': {
                1: "jeden kilometr_na_godzine",
                2: "dwa kilometry_na_godzine",
                5: "piec kilometrow_na_godzine",
            }
        }

        for unit, test_cases in multiple_test_cases.items():
            for value, expected in test_cases.items():
                self.assertEqual(expected,
                                 self.lang.read_speed(value, unit=unit))


    def test_read_degrees(self):
        test_cases = {
            0: "zero stopni",
            1: "jeden stopien",
            2: "dwa stopnie",
            5: "piec stopni",
        }

        for value, expected in test_cases.items():
            self.assertEqual(expected, self.lang.read_degrees(value))

    def test_read_direction(self):
        test_cases = {
            'N':   ('polnocny',
                    'polnocny',),
            'NNE': ('polnocno-polnocno-wschodni',
                    'polnocno-wschodni',),
            'NE':  ('polnocno-wschodni',
                    'polnocno-wschodni',),
            'ENE': ('wschodnio-polnocno-wschodni',
                    'polnocno-wschodni',),
            'E':   ('wschodni',
                    'wschodni',),
            'ESE': ('wschodnio-poludniowo-wschodni',
                    'poludniowo-wschodni',),
            'SE':  ('poludniowo-wschodni',
                    'poludniowo-wschodni',),
            'SSE': ('poludniowo-poludniowo-wschodni',
                    'poludniowo-wschodni',),
            'S':   ('poludniowy',
                    'poludniowy',),
            'SSW': ('poludniowo-poludniowo-zachodni',
                    'poludniowo-zachodni',),
            'SW':  ('poludniowo-zachodni',
                    'poludniowo-zachodni',),
            'WSW': ('zachodnio-poludniowo-zachodni',
                    'poludniowo-zachodni',),
            'W':   ('zachodni',
                    'zachodni',),
            'WNW': ('zachodnio-polnocno-zachodni',
                    'polnocno-zachodni',),
            'NW':  ('polnocno-zachodni',
                    'polnocno-zachodni',),
            'NNW': ('polnocno-polnocno-zachodni',
                    'polnocno-zachodni',),
        }
        for value, expected in test_cases.items():
            self.assertEqual(expected[0], self.lang.read_direction(value))
            self.assertEqual(expected[1],
                             self.lang.read_direction(value, short=True))

    def test_read_datetime(self):
        in_fmt = '%Y-%m-%d %H:%M'
        out_fmt = '%d %B %H %M'

        test_cases = {
            'czwartego czerwca czternasta dwadziescia szesc': {
                'dt': '1983-06-04 14:26',
                'in_fmt': in_fmt,
                'out_fmt': '%d %B %H %M',
            },
            'dwudziestego dziewiatego listopada osiemnasta dwadziescia siedem': {
                'dt': '2014-11-29 18:27',
                'in_fmt': in_fmt,
                'out_fmt': '%d %B %H %M',
            },
            'trzeciego maja godzina zero zero-zero': {
                'dt': '2014-05-03 0:00',
                'in_fmt': in_fmt,
                'out_fmt': '%d %B godzina %H %M',
            },
            'trzeciego maja dwudziesta zero-zero': {
                'dt': '2014-05-03 20:00',
                'in_fmt': in_fmt,
                'out_fmt': out_fmt,
            },

            'trzeciego maja dwudziesta pierwsza piec': {
                'dt': '2014-05-03 21:05',
                'in_fmt': in_fmt,
                'out_fmt': out_fmt,
            },
            'trzeciego maja osma dwadziescia piec': {
                'dt': '2014-05-03 08:25 AM',
                'in_fmt': '%Y-%m-%d %I:%M %p',
                'out_fmt': out_fmt,
            },
            'trzeciego maja dwudziesta dwadziescia piec': {
                'dt': '2014-05-03 08:25 PM',
                'in_fmt': '%Y-%m-%d %I:%M %p',
                'out_fmt': out_fmt,
            },
        }

        for expected, args in test_cases.items():
            dt = datetime.datetime.strptime(args['dt'], args['in_fmt'])
            self.assertEqual(expected,
                             self.lang.read_datetime(dt, out_fmt=args['out_fmt']))

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
