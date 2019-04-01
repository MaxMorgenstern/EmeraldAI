#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date, datetime

from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import Config

class Bot(BaseObject):
    __metaclass__ = Singleton
    # This class is a singleton as we only need one instance across the whole project, the currently active user

    def __init__(self):
        self.Name = Config().Get("Bot", "Name")
        self.Gender = Config().Get("Bot", "Gender")
        self.BuildDate = Config().Get("Bot", "BuildDate")
        self.Developer = Config().Get("Bot", "Developer")
        self.Origin = Config().Get("Bot", "Origin")

        born = datetime.strptime(self.BuildDate, '%d.%m.%Y')
        today = date.today()
        self.Age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        self.Status = "OK"
        self.Battery = "100%"

    def __repr__(self):
         return "{0}".format(self.Name)

    def __str__(self):
         return "{0}".format(self.Name)
