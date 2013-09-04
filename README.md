# weerapi: A basic KNMI weather API

This is a very basic JSON API for very basic weather data from the
[Royal Netherlands Meteorological Institute](http://www.knmi.nl/index_en.html).

The KNMI offers no simple API for simple data, so I built this one, based on scraping their website.
Currently, it only offers a single API call, for the latest weather observations at 36 monitoring stations.

## Usage

Call http://weer.solidlinks.nl/actueel/ or run your own instance. Be gentle if you want to use mine :)

The data format should mostly speak for itself. Units are:

* Temperatuur is in degrees celcius
* Humidity is a percentage
* Wind speed is in m/s
* Visibility is in meters
* Pressure is in hPa

## Notes

* The data is cached for two minutes. The KNMI refreshes this data every ten minutes.
* The geographical coordinates of the measuring stations are quite rough. If you can provide better ones,
  create an issue or a pull request.
* Please attribute KNMI as a source if you use this.