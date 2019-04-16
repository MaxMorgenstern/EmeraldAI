#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Entities.ContextParameter import ContextParameter
from EmeraldAI.Logic.NLP import NLP
from EmeraldAI.Entities.User import User
from EmeraldAI.Config.Config import Config
from EmeraldAI.Logic.NLP.AliceBot import AliceBot
from EmeraldAI.Logic.Modules import Action
from EmeraldAI.Logic.Logger import FileLogger
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
        FileLogger().Info("ProcessResponse, Process(), Sentence: {0}".format(sentence))

        responseFound = True
        if sentence is None or sentence.Rating < self.__sentenceRatingThreshold:
            responseFound = False

        if responseFound:
            user = User().LoadObject()
            PipelineArgs.ResponseRaw = sentence.GetSentenceString(user.Formal)
            PipelineArgs.Response = PipelineArgs.ResponseRaw
            PipelineArgs.ResponseID = sentence.ID
            PipelineArgs.Animation = sentence.GetAnimation()
            PipelineArgs.ResponseFound = True
            PipelineArgs.BasewordTrimmedInput = NLP.TrimBasewords(PipelineArgs)
            PipelineArgs.FullyTrimmedInput = NLP.TrimStopwords(PipelineArgs.BasewordTrimmedInput, PipelineArgs.Language)

            contextParameter = ContextParameter().LoadObject(240)

            if sentence.HasInteraction():
                contextParameter.InteractionName = sentence.InteractionName

            sentenceAction = sentence.GetAction()
            if sentenceAction != None and len(sentenceAction["Module"]) > 0:
                FileLogger().Info("ProcessResponse, Process(), Call Action: {0}, {1}, {2}".format(sentenceAction["Module"], sentenceAction["Class"], sentenceAction["Function"]))
                actionResult = Action.CallFunction(sentenceAction["Module"], sentenceAction["Class"], sentenceAction["Function"], PipelineArgs)

                if actionResult["ResultType"].title() is "Error":
                    PipelineArgs.Response = sentence.GetActionErrorResponse(PipelineArgs.Language, user.Formal)
                    PipelineArgs.ResponseRaw = None
                    PipelineArgs.Error.append("ProcessResponse - Action Error")
                else:
                    contextParameter.SetInput(actionResult["Input"])
                    contextParameter.SetResult(actionResult["Result"])
                    contextParameter.SaveObject()

                contextParameter.ResetInteraction()

            contextParameterDict = contextParameter.GetParameterDictionary()

            keywords = re.findall(r"\{(.*?)\}", PipelineArgs.Response)
            for keyword in keywords:
                if keyword.title() in contextParameterDict:
                    replaceword = contextParameterDict[keyword.title()]
                    if replaceword is None or replaceword == "Unknown":
                        replaceword = ""
                    else:
                        replaceword = "'{0}'".format(replaceword)
                    PipelineArgs.Response = PipelineArgs.Response.replace("{{{0}}}".format(keyword.lower()), str(replaceword))
                else:
                    PipelineArgs.Response = PipelineArgs.Response.replace("{{{0}}}".format(keyword.lower()), "")
                    FileLogger().Error("ProcessResponse Line 63: Parameter missing: '{0}'".format(keyword))

            contextParameter.UnsetInputAndResult()
            contextParameter.SaveObject()

        elif not responseFound and self.__aliceAsFallback:
            PipelineArgs.Response  = self.__alice.GetResponse(PipelineArgs.Input)
            PipelineArgs.ResponseFound = True
            PipelineArgs.TrainConversation = False

        FileLogger().Info("ProcessResponse, Process(), Response: {0}".format(PipelineArgs.Response))
        return PipelineArgs
