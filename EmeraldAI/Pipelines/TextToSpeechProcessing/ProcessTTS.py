#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.SpeechProcessing.Google import *
from EmeraldAI.Logic.SpeechProcessing.Ivona import *
from EmeraldAI.Logic.SpeechProcessing.Microsoft import *
from EmeraldAI.Config.Config import *

class ProcessSTT(object):
    __metaclass__ = Singleton


    def __init__(self):
        self.__ttsProvider = Config().GetFloat("TextToSpeech", "Provider") # Ivona

    def Process(self, PipelineArgs):
    	if(PipelineArgs.ResponseFound):

	        if(self.__ttsProvider.lower() == "google"):
	            data = Google().Speak(PipelineArgs.Response, True)

	        if(self.__ttsProvider.lower() == "microsoft"):
	            data = Microsoft().Speak(PipelineArgs.Response, True)

	        if(self.__ttsProvider.lower() == "ivona"):
	            data = Ivona().Speak(PipelineArgs.Response, True)

	        PipelineArgs.ResponseAudio = data
	        return PipelineArgs

    	return None
