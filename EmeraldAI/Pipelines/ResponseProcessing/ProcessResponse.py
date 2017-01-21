#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Entities.NLPParameter import NLPParameter
from EmeraldAI.Entities.User import User
import re

class ProcessResponse(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__sentenceRatingThreshold = Config().GetFloat("NLP", "SentenceRatingThreshold") # 2

    def Process(self, PipelineArgs):
        sentence = PipelineArgs.GetRandomSentenceWithHighestValue()

        # TODO - no sentence found
        if sentence == None:
            return PipelineArgs

        # TODO - no sentence above the minimum threshold
        if sentence.Rating < self.__sentenceRatingThreshold:
            return PipelineArgs

        # TODO - OR instead of returning - fallback to alice (set in config)

        user = User()
        PipelineArgs.ResponseRaw = sentence.GetSentenceString(user.Formal)
        PipelineArgs.Response = PipelineArgs.ResponseRaw
        PipelineArgs.ResponseID = sentence.ID
        PipelineArgs.ResponseFound = True

        parameter = NLPParameter()

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
