# WeerAPI: A basic KNMI weather API

This is a very basic JSON API for very basic weather data from the
[Royal Netherlands Meteorological Institute](http://www.knmi.nl/index_en.html).

The KNMI offers no simple API for simple data, so I built this one, which scrapes their website.
Currently, it only offers a single API call, for the
[latest weather observations](http://www.knmi.nl/actueel/)
at 36 monitoring stations.

## Usage

Call http://weer.solidlinks.nl/actueel/ or run your own instance. Be gentle if you want to use mine :)

The data format should mostly speak for itself. Units are:

* Temperatuur is in degrees celcius
* Humidity is a percentage
* Wind speed is in m/s and Beaufort
* Visibility is in meters
* Pressure is in hPa

## Notes

* The data is cached for two minutes. The KNMI refreshes this data every ten minutes.
* The geographical coordinates of the measuring stations are very rough. If you can provide better ones,
  [create an issue](https://github.com/erikr/weerapi/issues/new) or a pull request.
* Please attribute KNMI as a source if you use this.