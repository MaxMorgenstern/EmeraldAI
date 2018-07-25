#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import *

# TODO - add more parameters

class Bot(BaseObject):
    __metaclass__ = Singleton
    # This class is a singleton as we only need one instance across the whole project, the currently active user

    def __init__(self):
        self.Name = Config().Get("Bot", "Name")
        self.Status = "OK"
        self.Battery = "100%"

    def __repr__(self):
         return "{0}".format(self.Name)

    def __str__(self):
         return "{0}".format(self.Name)
