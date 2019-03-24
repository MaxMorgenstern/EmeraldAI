#!/usr/bin/python
# -*- coding: utf-8 -*-
import dateparser
from datetime import datetime
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

