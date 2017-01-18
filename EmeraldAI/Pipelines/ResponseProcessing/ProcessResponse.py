#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
import re

#todo
import time

class ProcessResponse(object):
    __metaclass__ = Singleton

    _sentenceRatingThreshold = 2

    def Process(self, PipelineArgs):
        sentence = PipelineArgs.GetRandomSentenceWithHighestValue()

        # TODO
        if sentence == None:
            return PipelineArgs

        # TODO
        if sentence.Rating < self._sentenceRatingThreshold:
            return PipelineArgs


        # TODO - OR instead of returning - fallback to alice (set in config)

        # TODO - formal (true / default value) or informal
        PipelineArgs.ResponseRaw = sentence.GetSentenceString()
        PipelineArgs.ResponseID = sentence.ID
        PipelineArgs.ResponseFound = True

        # TODO
        parameterList = {}
        parameterList["name"] = "Unknown"
        parameterList["input"] = "Hugo"
        parameterList["result"] = "ein kleiner Troll"

        PipelineArgs.Response = PipelineArgs.ResponseRaw
        keywords = re.findall(r"\{(.*?)\}", PipelineArgs.Response)
        for keyword in keywords:
            if keyword in parameterList:
                replaceword = parameterList[keyword]
                if replaceword == "Unknown":
                    replaceword = ""
                PipelineArgs.Response = PipelineArgs.Response.replace("{{{0}}}".format(keyword), replaceword)
            else:
                PipelineArgs.Response = PipelineArgs.Response.replace("{{{0}}}".format(keyword), "")


        # TODO
        # customize
        return PipelineArgs
