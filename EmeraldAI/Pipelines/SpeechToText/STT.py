#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.SpeechProcessing.Google import *
from EmeraldAI.Logic.SpeechProcessing.Microsoft import *
from EmeraldAI.Logic.SpeechProcessing.Wit import *
from EmeraldAI.Config.Config import *
from EmeraldAI.Entities.PipelineArgs import PipelineArgs
from EmeraldAI.Logic.Logger import *

class STT(object):
    __metaclass__ = Singleton


    def __init__(self):
        self.__sttProvider = Config().Get("SpeechToText", "Provider") # Google

    def Process(self, returnPipelineArgs = True):
        FileLogger().Info("STT, Process(), Provider: {0}".format(self.__sttProvider))

        if(self.__sttProvider.lower() == "google"):
            data = Google().Listen()

        if(self.__sttProvider.lower() == "microsoft"):
            data = Microsoft().Listen()

        if(self.__sttProvider.lower() == "wit"):
            data = Wit().Listen()

        if(len(data) == 0):
            return None

        FileLogger().Info("STT, Process(), Input Data: {0}".format(data))
        if(returnPipelineArgs):
            return PipelineArgs(data)
        return data
