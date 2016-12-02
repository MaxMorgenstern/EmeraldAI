#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/csparpa/pyowm/wiki/Usage-examples
# https://github.com/csparpa/pyowm

from datetime import datetime
import pyowm

owm = pyowm.OWM(API_key='47748de03b79380c94ecc84ef729f301',
                language='de')  # You MUST provide a valid API key

# You have a pro subscription? Use:
# owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')

# Will it be sunny tomorrow at this time in Milan (Italy) ?
#forecast = owm.daily_forecast("Hanau,de")
#tomorrow = pyowm.timeutils.tomorrow()
# print forecast.will_be_sunny_at(tomorrow)
# print forecast

# Search for current weather in London (UK)
observation = owm.weather_at_place('Bad Vilbel,de')
w = observation.get_weather()
print(w)

# Weather details
print w.get_wind()                  # {'speed': 4.6, 'deg': 330}
print w.get_humidity()              # 87
# {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
print w.get_temperature('celsius')
print w.get_detailed_status()
print w.get_status()
print w.get_snow()
print w.get_rain()
print w.get_weather_icon_name()
print w.get_sunrise_time('iso')  # GMT
print w.get_sunset_time('iso')  # GMT

print "-----"
print "-----"

fc = owm.three_hours_forecast('Bad Vilbel,de')
f = fc.get_forecast()
for weather in f:
    print(weather.get_reference_time('iso'), weather.get_detailed_status(),
          weather.get_temperature('celsius'), weather.get_wind())

print "-----"
print "-----"

fc = owm.daily_forecast('Bad Vilbel,de', limit=6)
f = fc.get_forecast()
for weather in f:
    print(weather.get_reference_time('iso'), weather.get_detailed_status(),
          weather.get_temperature('celsius'), weather.get_wind())

print "-----"

date_tomorrow = datetime(2016, 11, 30, 12, 0)
tw = fc.get_weather_at(date_tomorrow)
print tw.get_temperature('celsius')

"""
date_tomorrow = datetime(2016, 11, 30, 13, 37)
at = fc.get_weather_at(date_tomorrow)
print (at.get_reference_time('iso'),at.get_detailed_status(),at.get_temperature('celsius'))
"""

# Search current weather observations in the surroundings of
# lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
#observation_list = owm.weather_around_coords(-22.57, -43.12)
