#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.SpeechProcessing.Google import *
from EmeraldAI.Logic.SpeechProcessing.Microsoft import *
from EmeraldAI.Logic.SpeechProcessing.Wit import *
from EmeraldAI.Config.Config import *

class STT(object):
    __metaclass__ = Singleton


    def __init__(self):
        self.__sttProvider = Config().Get("SpeechToText", "Provider") # Google

    def Process(self):
        if(self.__sttProvider.lower() == "google"):
            data = Google().Listen()

        if(self.__sttProvider.lower() == "microsoft"):
            data = Microsoft().Listen()

        if(self.__sttProvider.lower() == "wit"):
            data = Wit().Listen()

        if(len(data) == 0):
            return None

        return PipelineArgs(data)
