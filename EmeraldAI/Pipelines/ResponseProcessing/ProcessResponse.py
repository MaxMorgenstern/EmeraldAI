#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Entities.NLPParameter import NLPParameter
from EmeraldAI.Entities.User import User
import re

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

        user = User()
        PipelineArgs.ResponseRaw = sentence.GetSentenceString(user.Formal)
        PipelineArgs.ResponseID = sentence.ID
        PipelineArgs.ResponseFound = True

        parameter = NLPParameter()

        PipelineArgs.Response = PipelineArgs.ResponseRaw
        keywords = re.findall(r"\{(.*?)\}", PipelineArgs.Response)
        for keyword in keywords:
            if keyword.title() in parameter.ParameterList:
                replaceword = parameter.ParameterList[keyword.title()]
                if replaceword == None or replaceword == "Unknown":
                    replaceword = ""
                PipelineArgs.Response = PipelineArgs.Response.replace("{{{0}}}".format(keyword.lower()), replaceword)
            else:
                PipelineArgs.Response = PipelineArgs.Response.replace("{{{0}}}".format(keyword.lower()), "")


        # TODO
        # customize
        return PipelineArgs
