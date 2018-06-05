#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
from os.path import dirname, abspath, join


class BaseConfig(object):
    __config = None

    def __init__(self, configName):
        config = ConfigParser.ConfigParser()
        config.read(join(dirname(abspath(__file__)), configName))
        self.__config = config

        configFallback = ConfigParser.ConfigParser()
        configFallback.read(join(dirname(abspath(__file__)), "{0}.example".format(configName)))
        self.__configFallback = configFallback


    def Get(self, section, parameter, fallback=True):
        if self.__config.has_option(section, parameter):
            return self.__config.get(section, parameter)
        if fallback:
            return self.__configFallback.get(section, parameter)
        raise Exception("Emerald Config: No option '{0}' in section: '{1}'".format(parameter, section))

    def GetInt(self, section, parameter, fallback=True):
        if self.__config.has_option(section, parameter):
            return self.__config.getint(section, parameter)
        if fallback:
            return self.__configFallback.getint(section, parameter)
        raise Exception("Emerald Config: No option '{0}' in section: '{1}'".format(parameter, section))

    def GetFloat(self, section, parameter, fallback=True):
        if self.__config.has_option(section, parameter):
            return self.__config.getfloat(section, parameter)
        if fallback:
            return self.__configFallback.getfloat(section, parameter)
        raise Exception("Emerald Config: No option '{0}' in section: '{1}'".format(parameter, section))

    def GetBoolean(self, section, parameter, fallback=True):
        if self.__config.has_option(section, parameter):
            return self.__config.getboolean(section, parameter)
        if fallback:
            return self.__configFallback.getboolean(section, parameter)
        raise Exception("Emerald Config: No option '{0}' in section: '{1}'".format(parameter, section))

    def GetList(self, section, parameter, fallback=True):
        if self.__config.has_option(section, parameter):
            return self.__config.get(section, parameter).split(",")
        if fallback:
            return self.__configFallback.get(section, parameter).split(",")
        raise Exception("Emerald Config: No option '{0}' in section: '{1}'".format(parameter, section))


    def Set(self, section, parameter, value):
        if not self.__config.has_section(section):
            self.__config.add_section(section)
        return self.__config.set(section, parameter, value)

    def Write(self, fileLocation):
        with open(fileLocation, 'wb') as configfile:
            self.__config.write(configfile)
