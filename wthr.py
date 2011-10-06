#-------------------------------------------------------------------------------
# Name:        wthr
# Purpose:
#
# Author:      Giles
#
# Created:     05/10/2011
# Copyright:   (c) Giles 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import urllib2
import json
import xml.etree.ElementTree as xml
from optparse import OptionParser

def main():
    pass

if __name__ == '__main__':
    main()

parser = OptionParser()
parser.add_option("-p", "--place", dest="place", help="Get the weather in the given location", metavar="PLACE")
parser.add_option("-u", "--unit", dest="unit", help="Specify the unit of the temperature", metavar="UNIT")

options, args = parser.parse_args()
#print options
place = options.place
unit = options.unit
unit = unit if (unit == "c" or unit == "f") else "c"

class Wthr:
    def _getIP(self):
        return urllib2.urlopen("http://icanhazip.com").read()[:-1]

    def _getWOEID(self, place):
        try:
            url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.places%20where%20text%3D%22" + place.replace(" ", "%20") + "%20CA%22&format=json"
            response = json.loads(urllib2.urlopen(url).read())
            woeid = response["query"]["results"]["place"][0]["woeid"]
            return woeid
        except:
            return None

    def getLocation(self):
            ip = self._getIP()
            loc = urllib2.urlopen("http://api.hostip.info/get_html.php?ip=" + ip).read()
            location = loc[loc.find("City: ") + 6 : loc.find("IP: ") - 1]
            if location == "(Unknown City?)":
                print "Could not determine your location. Please enter a location instead."
                return None
            return location

    def getWeather(self, place, unit):
        try:
            woeid = self._getWOEID(place)
            url = "http://weather.yahooapis.com/forecastrss?w=" + woeid + "&u=" + unit
            response = xml.XML(urllib2.urlopen(url).read())
            title = response.find("channel/description").text[7:] + " on " + response.find("channel/item/pubDate").text + ":\n"
            raw = response.find("channel/item/description").text
            start_string = "Forecast:</b><BR />"
            end_string = "<a href"
            weather = raw[raw.find(start_string) + len(start_string) : raw.find(end_string) - 1].replace("<br />", "")[:-1]
            return title + weather
        except:
            return "Could not get weather"

wthr = Wthr()
if place != None:
    if place == 'here':
        location = wthr.getLocation()
        print wthr.getWeather(location, unit)
    else:
        print wthr.getWeather(place, unit)
else:
    print "Please specify a location"