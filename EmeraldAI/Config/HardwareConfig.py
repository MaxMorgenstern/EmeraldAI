#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.BaseConfig import BaseConfig


class HardwareConfig(BaseConfig):
    __metaclass__ = Singleton

    def __init__(self):
        super(HardwareConfig, self).__init__("hardware.config")
