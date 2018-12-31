#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.NLP.SentenceResolver import SentenceResolver
from EmeraldAI.Entities.ContextParameter import ContextParameter
from EmeraldAI.Entities.User import User
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Logger import *

class AnalyzeScope(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__RemoveBeforeRequirementCalculation = Config().GetBoolean("Pipeline.ScopeAnalyzer", "RemoveLowPrioritySentencesBeforeRequirement") #False
        self.__RemoveAfterRequirementCalculation = Config().GetBoolean("Pipeline.ScopeAnalyzer", "RemoveLowPrioritySentencesAfterRequirement") #True
        self.__RemoveStopwordOnlySentences = Config().GetBoolean("Pipeline.ScopeAnalyzer", "RemoveStopwordOnlySentences") #True

    def Process(self, PipelineArgs):
        FileLogger().Info("AnalyzeScope, Process()")
        sentenceList = {}
        wordParameterList = []

        user = User().LoadObject()
        for word in PipelineArgs.WordList:
            if(len(word.SynonymList) > 0):
                wordList = "'{0}'".format("', '".join(word.SynonymList))
                sentenceList = SentenceResolver().GetSentencesByKeyword(sentenceList, wordList, word.NormalizedWord, word.Language, True, (user.Admin or user.Trainer))
            sentenceList = SentenceResolver().GetSentencesByKeyword(sentenceList, "'{0}'".format(word.NormalizedWord), word.NormalizedWord, word.Language, False, (user.Admin or user.Trainer))

            wordParameterList += list(set(word.ParameterList) - set(wordParameterList))

        sentenceList = SentenceResolver().GetSentencesByParameter(sentenceList, wordParameterList, PipelineArgs.Language, (user.Admin or user.Trainer))

        contextParameter = ContextParameter().LoadObject(240)
        contextParameter.UpdateParameter("Wordtype", wordParameterList)
        contextParameter.SaveObject()

        if self.__RemoveStopwordOnlySentences:
            sentenceList = SentenceResolver().RemoveStopwordOnlySentences(sentenceList)

        if self.__RemoveBeforeRequirementCalculation:
            sentenceList = SentenceResolver().RemoveLowPrioritySentences(sentenceList)

        contextParameterDict = contextParameter.GetParameterDictionary()
        calculationResult = SentenceResolver().CalculateRequirement(sentenceList, contextParameterDict)
        sentenceList = calculationResult["sentenceList"]

        if self.__RemoveAfterRequirementCalculation:
            sentenceList = SentenceResolver().RemoveLowPrioritySentences(sentenceList, True)

        sentenceList = SentenceResolver().AddActionBonus(sentenceList)
        sentenceList = SentenceResolver().AddSentencePriority(sentenceList)
        sentenceList = SentenceResolver().CalculateCategory(sentenceList, contextParameterDict["Category"])

        PipelineArgs.SentenceList = sentenceList

        FileLogger().Info("AnalyzeScope, Process(), SentenceList: {0}".format(PipelineArgs.SentenceList))
        return PipelineArgs
