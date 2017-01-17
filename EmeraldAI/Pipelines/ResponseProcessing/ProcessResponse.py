#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton

class ProcessResponse(object):
    __metaclass__ = Singleton

    def Process(self, PipelineArgs):
        sentenceID = PipelineArgs.GetRandomSentenceWithHighestValue()
        # TODO
        # get sentence
        # replace placeholder
        # customize
        # TTS
        # return
        return PipelineArgs
