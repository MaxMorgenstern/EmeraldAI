#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
from os.path import dirname, abspath, join


class BaseConfig(object):
    __config = None

    def __init__(self, config):
        self.__config = config

    def Get(self, section, parameter):
        return self.__config.get(section, parameter)

    def GetInt(self, section, parameter):
        return self.__config.getint(section, parameter)

    def GetFloat(self, section, parameter):
        return self.__config.getfloat(section, parameter)

    def GetBoolean(self, section, parameter):
        return self.__config.getboolean(section, parameter)

    def GetList(self, section, parameter):
        return self.__config.get(section, parameter).split(",")

    def Set(self, section, parameter, value):
        if not self.__config.has_section(section):
            self.__config.add_section(section)
        return self.__config.set(section, parameter, value)

    def Write(self, fileLocation):
        with open(fileLocation, 'wb') as configfile:
            self.__config.write(configfile)
