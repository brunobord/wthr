#-------------------------------------------------------------------------------
# Name:        wthr
# Purpose:
#
# Author:      Giles
#
# Created:     05/10/2011
# Copyright:   (c) Giles Lavelle 2011
# Licence:     GPL v2
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from urllib2 import urlopen
import json
import xml.etree.ElementTree as xml
import sys

def main():
    pass

if __name__ == '__main__':
    main()

if len(sys.argv) > 1:
    place = sys.argv[1]
    if len(sys.argv) > 2:
        unit = sys.argv[2] if (sys.argv[2] == "c" or sys.argv[2] == "f") else "c"
    else: unit = "c"
else: place = None

class Wthr:
    def _getIP(self):
        return urlopen("http://icanhazip.com").read()[:-1]

    def _getWOEID(self, place):
        YQL_query = "select * from geo.places where text%3D%22"
        YQL_query = YQL_query.replace(" ", "%20") + place.replace(" ", "%20") + "%22"
        url = "http://query.yahooapis.com/v1/public/yql?q="
        url += YQL_query + "&format=json"
        response = json.loads(urlopen(url).read())
        woeid = response["query"]["results"]["place"][0]["woeid"]
        return woeid

    def _getLocation(self):
            ip = self._getIP()
            loc = urlopen("http://api.hostip.info/get_html.php?ip=" + ip).read()
            location = loc[loc.find("City: ") + 6 : loc.find("IP: ") - 1]
            if location == "(Unknown City?)":
                print "Could not automatically find your location. Please enter a location instead."
                return None
            return location

    def getWeather(self, place, unit):
            if place == "here": place = self._getLocation()
            WOEID = self._getWOEID(place)
            url = "http://weather.yahooapis.com/forecastrss?w=" + WOEID + "&u=" + unit
            response = xml.XML(urlopen(url).read())
            title = response.find("channel/description").text[7:] + " on " + response.find("channel/item/pubDate").text + ":\n"
            raw = response.find("channel/item/description").text
            start = "Forecast:</b><BR />"
            end = "<a href"
            weather = raw[raw.find(start) + len(start) : raw.find(end) - 1].replace("<br />", "")[:-1]
            return title + weather

wthr = Wthr()
if place != None: print wthr.getWeather(place, unit)
else: print "Please specify a location"