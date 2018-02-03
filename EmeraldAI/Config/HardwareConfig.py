#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
from os.path import dirname, abspath, join
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.BaseConfig import BaseConfig


class HardwareConfig(BaseConfig):
    __metaclass__ = Singleton

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(join(dirname(abspath(__file__)), "hardware.config"))
        super(HardwareConfig, self).__init__(config)
