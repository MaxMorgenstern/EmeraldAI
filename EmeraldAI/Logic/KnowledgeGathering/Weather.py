#!/usr/bin/python
# -*- coding: utf-8 -*-
import pyowm
from datetime import datetime
from EmeraldAI.Logic.Singleton import Singleton


class Weather(object):
    __metaclass__ = Singleton

    __owm = None
    __language = None
    __defaultCountry = None

    def __init__(self):
        self.__language = 'de'
        self.__defaultCountry = 'de'
        self.__owm = pyowm.OWM(API_key='47748de03b79380c94ecc84ef729f301', language='de')


    def GetCurrentWeather(location, country=None):
        if(country==None):
            country = self.__defaultCountry
        forcast = self.__owm.weather_at_place("{0},{1}".format(location, country))
        return forcast.get_weather()

    def GetFutureWeather(location, date=None, country=None):
        if(country==None):
            country = self.__defaultCountry
        if(date==None):
            date = datetime.date.today() + datetime.timedelta(days=1)
        forcast = self.__owm.daily_forecast("{0},{1}".format(location, country))
        return tw = forcast.get_weather_at(date)

    def GetThreeHoursForecast(location, country=None):
        if(country==None):
            country = self.__defaultCountry
        forcast = self.__owm.three_hours_forecast("{0},{1}".format(location, country))
        return forcast.get_forecast()

    def GetDailyForecast(location, country=None):
        if(country==None):
            country = self.__defaultCountry
        forcast = self.__owm.daily_forecast("{0},{1}".format(location, country))
        return forcast.get_forecast()
