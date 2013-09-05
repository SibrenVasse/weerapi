import memcache
import requests
import json
from flask import Flask, Response, redirect

from weerapi.knmidata import KNMIData
from weerapi.config import MEMCACHE_KEY, MEMCACHE_SERVERS, MEMCACHE_EXPIRY, URL

app = Flask(__name__)
mc = memcache.Client(MEMCACHE_SERVERS, debug=0)


@app.route('/')
def home():
    return redirect("http://erikr.github.io/weerapi/")


@app.route("/actueel/")
def actueel():
    response = mc.get(MEMCACHE_KEY)
    if not response:
        headers = {'User-Agent': 'weerapi -- https://github.com/erikr/weerapi'}
        data = requests.get(URL, headers=headers).text
        response = KNMIData().actueel(data)
        mc.set(MEMCACHE_KEY, response, time=MEMCACHE_EXPIRY)

    return Response(response=json.dumps(response, indent=4),
                    status=200,
                    mimetype="application/json")


if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'wegh1@solidlinks.nl',
                               'wegh1@solidlinks.nl', 'Weer error')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5001)
