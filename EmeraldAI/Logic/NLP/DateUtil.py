#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from dateutil import parser

from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Config.Config import Config
from EmeraldAI.Logic.Singleton import Singleton
if(Config().Get("Database", "NLPDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "NLPDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db


class DateUtil(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.t = ""

    def parseTime(self, input):
        # ^([0-9]|0[0-9]|1[0-9]|2[0-3]):?([0-5][0-9])*(\s?)Uhr$
        return None

    def parse(self, input):
        return parser.parse(input, parserinfo=GermanParserInfo())

class GermanParserInfo(parser.parserinfo):
    WEEKDAYS = [("Mo.", "Montag"),
                ("Di.", "Dienstag"),
                ("Mi.", "Mittwoch"),
                ("Do.", "Donnerstag"),
                ("Fr.", "Freitag"),
                ("Sa.", "Samstag"),
                ("So.", "Sonntag")]