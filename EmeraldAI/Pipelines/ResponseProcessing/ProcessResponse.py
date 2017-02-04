#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Entities.NLPParameter import NLPParameter
from EmeraldAI.Logic.NLP import NLP
from EmeraldAI.Entities.User import User
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.NLP.AliceBot import *
from EmeraldAI.Logic.Modules import Action
import re

class ProcessResponse(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__sentenceRatingThreshold = Config().GetFloat("NLP", "SentenceRatingThreshold") # 2
        self.__aliceAsFallback = Config().GetBoolean("NLP", "AliceAsFallback") # True
        self.__language_2letter_cc = Config().Get("NLP", "CountryCode2Letter")
        self.__alice = AliceBot(self.__language_2letter_cc)


    def Process(self, PipelineArgs):
        sentence = PipelineArgs.GetRandomSentenceWithHighestValue()

        responseFound = True
        if sentence == None or sentence.Rating < self.__sentenceRatingThreshold:
            responseFound = False

        if responseFound:
            user = User()
            PipelineArgs.ResponseRaw = sentence.GetSentenceString(user.Formal)
            PipelineArgs.Response = PipelineArgs.ResponseRaw
            PipelineArgs.ResponseID = sentence.ID
            PipelineArgs.ResponseFound = True
            PipelineArgs.InputWithoutBasewords = NLP.TrimBasewords(PipelineArgs)

            sentenceAction = sentence.GetAction()
            if sentenceAction != None and len(sentenceAction["Module"]) > 0:
                actionResult = Action.CallFunction(sentenceAction["Module"], sentenceAction["Class"], sentenceAction["Function"], PipelineArgs)
                NLPParameter().SetInput(actionResult["Input"])
                NLPParameter().SetResult(actionResult["Result"])

            parameterList = NLPParameter().GetParameterList()

            keywords = re.findall(r"\{(.*?)\}", PipelineArgs.Response)
            for keyword in keywords:
                if keyword.title() in parameterList:
                    replaceword = parameterList[keyword.title()]
                    if replaceword == None or replaceword == "Unknown":
                        replaceword = ""
                    PipelineArgs.Response = PipelineArgs.Response.replace("{{{0}}}".format(keyword.lower()), replaceword)
                else:
                    PipelineArgs.Response = PipelineArgs.Response.replace("{{{0}}}".format(keyword.lower()), "")

        elif not responseFound and self.__aliceAsFallback:
            PipelineArgs.Response  = self.__alice.GetResponse(PipelineArgs.Input)
            PipelineArgs.ResponseFound = True
            PipelineArgs.TrainConversation = False

        return PipelineArgs
