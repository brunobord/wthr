#!/usr/bin/env python

from urllib2 import urlopen
import json
from xml.etree.ElementTree import XML as parse_xml
from sys import argv


class Wthr:
    def _getIP(self):
        return urlopen('http://icanhazip.com').read()[:-1]

    def _getWOEID(self, place):
        YQL_query = 'select * from geo.places where text%3D%22'
        YQL_query = YQL_query.replace(' ', '%20') + place.replace(' ', '%20') + '%22'

        url = 'http://query.yahooapis.com/v1/public/yql?q=' +\
            YQL_query + '&format=json'

        response = json.loads(urlopen(url).read())
        woeid = response['query']['results']['place'][0]['woeid']

        return woeid

    def _getLocation(self):
        ip = self._getIP()
        loc = urlopen('http://api.hostip.info/get_html.php?ip=' + ip).read()
        location = loc[loc.find('City: ') + 6: loc.find('IP: ') - 1]

        if location == '(Unknown City?)':
            print 'Could not automatically find your location. Please enter a location instead.'
            return None

        return location

    def getWeather(self, place, unit):
        if place == 'here':
            place = self._getLocation()

        # We don't need to go further, we don't know where it is
        if not place:
            return

        WOEID = self._getWOEID(place)
        url = 'http://weather.yahooapis.com/forecastrss?w=' + WOEID + '&u=' + unit

        response = parse_xml(urlopen(url).read())
        title = response.find('channel/description').text[7:] + ' on ' + response.find('channel/item/pubDate').text + ':\n'
        raw = response.find('channel/item/description').text

        start = 'Forecast:</b><BR />'
        end = '<a href'

        weather = raw[raw.find(start) + len(start): raw.find(end) - 1].replace('<br />', '')[:-1]

        return title + weather


def main():
    if len(argv) > 1:
        place = argv[1]
        unit = argv[2] if len(argv) > 2 and argv[2] in 'cf' else 'c'
    else:
        place = None

    if place != None:
        print Wthr().getWeather(place, unit)
    else:
        print 'Please specify a location'

if __name__ == '__main__':
    main()
