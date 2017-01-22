#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import *


class Trainer(object):
    __metaclass__ = Singleton


    def __init__(self):
        self.__trainData = Config().GetBoolean("Trainer", "Enabled") # True


    def Process(self, PipelineArgs):
    	# TODO
    	return True
