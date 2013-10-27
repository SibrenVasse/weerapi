from BeautifulSoup import BeautifulSoup
from ordereddict import OrderedDict
from decimal import Decimal


class KNMIData(object):

    def actueel(self, html_data):
        results = {}
        soup = BeautifulSoup(html_data)

        for row in soup.find('table').findAll('tr'):
            fields = row.findAll('td')
            if not fields:
                continue

            fields = self.clean_fields(fields)
            wind_chill = None
            if len(fields) == 8:
            	(name, weather_type, temperature, humidity, wind_direction, wind_speed_ms, visibility, pressure) = fields
            else:
            	(name, weather_type, temperature, wind_chill, humidity, wind_direction, wind_speed_ms, visibility, pressure) = fields

            if name and name in LOCATION_MAPPING:
                (latitude, longitude) = LOCATION_MAPPING[name]
            else:
                latitude = None
                longitude = None

            wind_direction_deg = WIND_DIRECTION_MAPPING.get(wind_direction)

            wind_speed_bft = None
            if wind_speed_ms:
                for scale_speed_bft in BEAUFORT_SCALE.keys():
                    if Decimal(wind_speed_ms) >= BEAUFORT_SCALE[scale_speed_bft]:
                        wind_speed_bft = scale_speed_bft

            results[name] = {
                'latitude': latitude,
                'longitude': longitude,
                'wind_direction_deg': wind_direction_deg,
                'wind_direction': wind_direction,
                'weather_type': weather_type,
                'temperature': temperature,
                'wind_chill': wind_chill,
                'humidity': humidity,
                'wind_speed_ms': wind_speed_ms,
                'wind_speed_bft': wind_speed_bft,
                'visibility': visibility,
                'pressure': pressure,
            }

        timestamp = soup.find('div', {'class': 'alineakop'}).text.replace('Waarnemingen ', '')
        return {
            'actueel': results,
            'source': 'KNMI',
            'timestamp': timestamp
        }

    def clean_fields(self, fields):
        result = []
        for field in fields:
            field = field.text.replace('&nbsp;', '').strip()
            if not field:
                field = None
            result.append(field)
        return result


WIND_DIRECTION_MAPPING = {
    'N': '0',
    'NNO': '22.5',
    'NO': '45',
    'ONO': '67.5',

    'O': '90',
    'OZO': '112.5',
    'ZO': '135',
    'ZZO': '157.5',
    'Z': '180',

    'ZZW': '202.5',
    'ZW': '225',
    'WZW': '247.5',
    'W': '270',

    'WNW': '292.5',
    'NW': '315',
    'NNW': '337.5',
}

LOCATION_MAPPING = {
    'Lauwersoog': ("53.40537", "6.21205"),
    'Nieuw Beerta': ("53.18104", "7.11859"),
    'Terschelling': ("53.37022", "5.22949"),
    'Vlieland': ("53.23235", "4.87793"),
    'Leeuwarden': ("53.18629", "5.78430"),
    'Stavoren': ("52.88295", "5.36071"),
    'Houtribdijk': ("52.62670", "5.42216"),
    'Eelde': ("53.13311", "6.56427"),
    'Hoogeveen': ("52.72862", "6.49010"),
    'Heino': ("52.43388", "6.23289"),
    'Twenthe': ("52.27425", "6.87689"),
    'Deelen': ("52.05796", "5.88313"),
    'Hupsel': ("52.10002", "6.66120"),
    'Herwijnen': ("51.82670", "5.12961"),
    'Marknesse': ("52.71156", "5.86456"),
    'Lelystad': ("52.51854", "5.47142"),
    'De Bilt': ("52.10927", "5.18097"),
    'Cabauw': ("51.96534", "4.89794"),
    'Den Helder': ("52.95628", "4.76080"),
    'Berkhout': ("52.64044", "4.99852"),
    'IJmuiden': ("52.45852", "4.61368"),
    'Wijk aan Zee': ("52.49169", "4.59333"),
    'Schiphol': ("52.30769", "4.76742"),
    'Valkenburg': ("50.86523", "5.83205"),
    'Rotterdam': ("51.92422", "4.48178"),
    'Hoek van Holland': ("51.98063", "4.13418"),
    'Wilhelminadorp': ("51.52921", "3.89688"),
    'Vlissingen': ("51.45367", "3.57091"),
    'Westdorpe': ("51.23353", "3.83032"),
    'Woensdrecht': ("51.42925", "4.30471"),
    'Gilze Rijen': ("51.55985", "4.90925"),
    'Volkel': ("51.64285", "5.65460"),
    'Eindhoven': ("51.44164", "5.46972"),
    'Ell': ("49.76296", "5.85579"),
    'Arcen': ("51.47636", "6.18095"),
    'Maastricht AP': ("50.91402", "5.77614"),
}

# Values are the lower boundary in m/s of the beaufort scale
BEAUFORT_SCALE = OrderedDict({
    0: Decimal('0'),
    1: Decimal('0.3'),
    2: Decimal('1.6'),
    3: Decimal('3.4'),
    4: Decimal('5.5'),
    5: Decimal('8'),
    6: Decimal('10.8'),
    7: Decimal('13.9'),
    8: Decimal('17.2'),
    9: Decimal('20.8'),
    10: Decimal('24.5'),
    11: Decimal('28.5'),
    12: Decimal('32.6'),
})
