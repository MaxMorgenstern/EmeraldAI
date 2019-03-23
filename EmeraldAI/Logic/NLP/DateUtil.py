#!/usr/bin/python
# -*- coding: utf-8 -*-
#import re
import dateparser
from datetime import datetime

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
        return dateparser.parse(input, languages=languageList)
