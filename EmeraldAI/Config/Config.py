#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.BaseConfig import BaseConfig


class Config(BaseConfig):
    __metaclass__ = Singleton

    def __init__(self):
        super(Config, self).__init__("base.config")
