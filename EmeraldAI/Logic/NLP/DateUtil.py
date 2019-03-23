#!/usr/bin/python
# -*- coding: utf-8 -*-
#import re
import dateparser
from datetime import datetime
from dateparser.search import search_dates


#from EmeraldAI.Logic.Modules import Global
#from EmeraldAI.Config.Config import Config
from EmeraldAI.Logic.Singleton import Singleton
"""
if(Config().Get("Database", "NLPDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "NLPDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db
"""

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

