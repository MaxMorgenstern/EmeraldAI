#!/usr/bin/python
# -*- coding: utf-8 -*-
import pyowm
from datetime import datetime
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import Config


class Weather(object):
    __metaclass__ = Singleton

    __owm = None
    __language = None
    __defaultCountry = None

    def __init__(self):
        self.__language = Config().Get("Weather", "Language")
        self.__defaultCountry = Config().Get("Weather", "CountryCode2Letter")
        self.__owm = pyowm.OWM(API_key=Config().Get("Weather", "OWMAPIKey"), language=self.__language)

    def GetCurrentWeather(self, location, country=None):
        if(country is None):
            country = self.__defaultCountry
        forcast = self.__owm.weather_at_place(
            "{0},{1}".format(location, country))
        return forcast.get_weather()

    def GetFutureWeather(self, location, date=None, country=None):
        if(country is None):
            country = self.__defaultCountry
        if(date is None):
            date = datetime.date.today() + datetime.timedelta(days=1)
        forcast = self.__owm.daily_forecast(
            "{0},{1}".format(location, country))
        return forcast.get_weather_at(date)

    def GetThreeHoursForecast(self, location, country=None):
        if(country is None):
            country = self.__defaultCountry
        forcast = self.__owm.three_hours_forecast(
            "{0},{1}".format(location, country))
        return forcast.get_forecast()

    def GetDailyForecast(self, location, country=None):
        if(country is None):
            country = self.__defaultCountry
        forcast = self.__owm.daily_forecast(
            "{0},{1}".format(location, country))
        return forcast.get_forecast()
