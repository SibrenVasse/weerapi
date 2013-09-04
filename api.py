from BeautifulSoup import BeautifulSoup
import memcache
import requests
import json
from flask import Flask, Response

import config

app = Flask(__name__)
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

@app.route("/actueel/")
def actueel():
    data = mc.get(config.MEMCACHE_KEY)
    if not data:
        headers = {'User-Agent': 'weerapi -- https://github.com/erikr/weerapi'}
        data = requests.get('http://m.knmi.nl/index.php?i=Actueel&s=tabel_10min_data', headers=headers).text
        mc.set(config.MEMCACHE_KEY, data, time=config.MEMCACHE_EXPIRY)

    results = {}
    soup = BeautifulSoup(data)

    for row in soup.find(id="sortable").findAll('tr'):
        fields = row.findAll('td')
        if not fields:
            continue

        fields = [field.text.replace('&nbsp;', '').strip() for field in fields]

        (name, weather_type, temperature, humidity, wind_direction, wind_speed, visibility, pressure) = fields

        if name and name in config.LOCATION_MAPPING:
            (latitude, longitude) = config.LOCATION_MAPPING[name]
        else:
            latitude = None
            longitude = None

        wind_direction_deg = config.WIND_DIRECTION_MAPPING.get(wind_direction)

        results[name] = {
            'latitude': latitude,
            'longitude': longitude,
            'wind_direction_deg': wind_direction_deg,
            'wind_direction': wind_direction,
            'weather_type': weather_type,
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'visibility': visibility,
            'pressure': pressure,
        }

    response = {
        'actueel': results,
        'source': 'KNMI',
        'timestamp': soup.find('div', {'class': 'alineakop'}).text.replace('Waarnemingen ', '')
    }
    return Response(response=json.dumps(response, indent=4),
                    status=200,
                    mimetype="application/json")


if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'eromijn@solidlinks.nl',
                               'eromijn@solidlinks.nl', 'Weer error')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5001)

