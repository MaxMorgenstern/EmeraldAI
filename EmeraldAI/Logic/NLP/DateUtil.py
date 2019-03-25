#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date
from datetime import datetime
from datetime import timedelta
import dateparser
from dateparser.search import search_dates

from EmeraldAI.Logic.Singleton import Singleton


class DateUtil(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.t = ""

    def parse(self, input, languageList = ['de']):
        parseResult = dateparser.parse(input, languages=languageList, 
            settings={'PREFER_DATES_FROM': 'future', 'PREFER_DAY_OF_MONTH': 'first'})
        
        if parseResult is not None:
            return parseResult

        now = datetime.now()
        searchResult = search_dates(input)

        if searchResult is None:
            return None

        returnDate = now
        for result in searchResult:
            resultDelta = result[1] - now
            returnDate += resultDelta
        return returnDate

    def isDate(self, input):
        return True

    def isTime(self, input):
        return True


    def SameDay(self, dt):
        now =  datetime.now()
        return now.date() == dt.date()

    def InRange(self, dt, range=1):
        x = dt.time()
        now =  datetime.now()
        start = (now - timedelta(minutes=range)).time()
        end = (now + timedelta(minutes=range)).time()
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end
