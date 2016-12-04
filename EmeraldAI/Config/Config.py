#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
import os
from EmeraldAI.Logic.Singleton import Singleton


class Config():
    __metaclass__ = Singleton
    __config = None

    def __init__(self):
        self.__config = ConfigParser.ConfigParser()
        self.__config.read(os.path.dirname(
            os.path.abspath(__file__)) + "/base.config")

    def Get(self, section, parameter):
        return self.__config.get(section, parameter)

    def GetInt(self, section, parameter):
        return self.__config.getint(section, parameter)

    def GetFloat(self, section, parameter):
        return self.__config.getfloat(section, parameter)

    def GetBoolean(self, section, parameter):
        return self.__config.getboolean(section, parameter)
