#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
import os

class Config():
  _config = None

  def __init__(self):
    self._config = ConfigParser.ConfigParser()
    self._config.read(os.path.dirname(os.path.abspath(__file__))+"/base.config")

  def Get(self, section, parameter):
    return self._config.get(section, parameter)

  def GetInt(self, section, parameter):
    return self._config.getint(section, parameter)

  def GetFloat(self, section, parameter):
    return self._config.getfloat(section, parameter)

  def GetBoolean(self, section, parameter):
    return self._config.getboolean(section, parameter)
