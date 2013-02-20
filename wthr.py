#!/usr/bin/env python
"""wthr is a Python script for checking the weather from the command line.
"""
from urllib2 import urlopen
import json
from xml.etree.ElementTree import XML as parse_xml
from sys import argv


class Wthr:
    """Main Wthr class. Computes location and sends weather information to the
    user.
    """
    def _get_ip(self):
        "Fetch the user IP Address"
        return urlopen('http://icanhazip.com').read()[:-1]

    def _get_woeid(self, place):
        "Get Weather information"
        yql_query = 'select * from geo.places where text%3D%22' + place + '%22'
        yql_query = yql_query.replace(' ', '%20')

        url = 'http://query.yahooapis.com/v1/public/yql?q=%s&format=json' \
            % yql_query

        response = json.loads(urlopen(url).read())
        woeid = response['query']['results']['place'][0]['woeid']

        return woeid

    def _get_location(self):
        "Get location from IP"
        ip_addr = self._get_ip()
        loc = urlopen('http://api.hostip.info/get_html.php?ip=%s' % ip_addr).read()
        location = loc[loc.find('City: ') + 6: loc.find('IP: ') - 1]

        if location == '(Unknown City?)':
            print 'Could not automatically find your location. Please enter a location instead.'
            return None

        return location

    def get_weather(self, place, unit):
        """Get Weather information.
        Use the argument 'place' to say which city you want to know about. if
        the place argument is "here", it'll fetch your place from your IP.
        """
        if place == 'here':
            place = self._get_location()

        woeid = self._get_woeid(place)
        url = 'http://weather.yahooapis.com/forecastrss?w=%s&u=%s' % (woeid, unit)

        response = parse_xml(urlopen(url).read())
        title = response.find('channel/description').text[7:] + \
            ' on ' + response.find('channel/item/pubDate').text + ':\n'
        raw = response.find('channel/item/description').text

        start = 'Forecast:</b><BR />'
        end = '<a href'

        weather = raw[raw.find(start) + len(start): raw.find(end) - 1].replace('<br />', '')[:-1]

        return title + weather


def main():
    "Main program"
    if len(argv) > 1:
        place = argv[1]
        unit = argv[2] if len(argv) > 2 and argv[2] in 'cf' else 'c'
    else:
        place = None

    if place != None:
        print Wthr().get_weather(place, unit)
    else:
        print 'Please specify a location'

if __name__ == '__main__':
    main()
