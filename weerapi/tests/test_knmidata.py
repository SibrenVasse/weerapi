import os
import unittest
from weerapi.knmidata import KNMIData


class KNMIDataTest(unittest.TestCase):
    def setUp(self):
        self.knmidata = KNMIData()

    def test_actueel(self):
        my_path = os.path.dirname(os.path.abspath(__file__))
        input_data = open(my_path + '/actueel.html').read()

        result = self.knmidata.actueel(input_data)
        self.assertEqual(len(result['actueel']), 36)
        self.assertEqual(result['timestamp'], '5 september 2013 10:30')
        self.assertEqual(result['source'], 'KNMI')

        self.assertEqual(result['actueel']['Schiphol']['latitude'], '52.30769')
        self.assertEqual(result['actueel']['Schiphol']['weather_type'], 'onbewolkt')
        self.assertEqual(result['actueel']['Schiphol']['temperature'], '21.8')
        self.assertEqual(result['actueel']['Schiphol']['humidity'], '75')
        self.assertEqual(result['actueel']['Schiphol']['wind_direction'], 'ZO')
        self.assertEqual(result['actueel']['Schiphol']['wind_direction_deg'], '135')
        self.assertEqual(result['actueel']['Schiphol']['wind_speed_ms'], '4')
        self.assertEqual(result['actueel']['Schiphol']['wind_speed_bft'], 3)
        self.assertEqual(result['actueel']['Schiphol']['visibility'], '12900')
        self.assertEqual(result['actueel']['Schiphol']['pressure'], '1014.0')

        self.assertEqual(result['actueel']['Lauwersoog']['visibility'], None)
        self.assertEqual(result['actueel']['Wijk aan Zee']['wind_direction'], None)
        self.assertEqual(result['actueel']['Wijk aan Zee']['wind_direction_deg'], None)

if __name__ == '__main__':
    unittest.main()
