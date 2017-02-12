#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.NLP.SentenceResolver import SentenceResolver
from EmeraldAI.Entities.NLPParameter import NLPParameter
from EmeraldAI.Entities.User import User
from EmeraldAI.Config.Config import *

class AnalyzeScope(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__RemoveBeforeRequirementCalculation = Config().GetBoolean("Pipeline.ScopeAnalyzer", "RemoveLowPrioritySentencesBeforeRequirement") #False
        self.__RemoveAfterRequirementCalculation = Config().GetBoolean("Pipeline.ScopeAnalyzer", "RemoveLowPrioritySentencesAfterRequirement") #True
        self.__RemoveStopwordOnlySentences = Config().GetBoolean("Pipeline.ScopeAnalyzer", "RemoveStopwordOnlySentences") #True

    def Process(self, PipelineArgs):

        sentenceList = {}
        wordParameterList = []

        for word in PipelineArgs.WordList:

            user = User()
            if(len(word.SynonymList) > 0):
                wordList = "'{0}'".format("', '".join(word.SynonymList))
                sentenceList = SentenceResolver().GetSentencesByKeyword(sentenceList, wordList, word.NormalizedWord, word.Language, True, (user.Admin or user.Trainer))
            sentenceList = SentenceResolver().GetSentencesByKeyword(sentenceList, "'{0}'".format(word.NormalizedWord), word.NormalizedWord, word.Language, False, (user.Admin or user.Trainer))

            wordParameterList += list(set(word.ParameterList) - set(wordParameterList))

        sentenceList = SentenceResolver().GetSentencesByParameter(sentenceList, wordParameterList, PipelineArgs.Language, (user.Admin or user.Trainer))
        NLPParameter().UpdateParameter("Wordtype", wordParameterList)

        if self.__RemoveStopwordOnlySentences:
            sentenceList = SentenceResolver().RemoveStopwordOnlySentences(sentenceList)

        if self.__RemoveBeforeRequirementCalculation:
            sentenceList = SentenceResolver().RemoveLowPrioritySentences(sentenceList)

        parameterList = NLPParameter().GetParameterList()
        calculationResult = SentenceResolver().CalculateRequirement(sentenceList, parameterList)
        sentenceList = calculationResult["sentenceList"]

        if self.__RemoveAfterRequirementCalculation:
            sentenceList = SentenceResolver().RemoveLowPrioritySentences(sentenceList, True)

        sentenceList = SentenceResolver().AddActionBonus(sentenceList)
        sentenceList = SentenceResolver().AddSentencePriority(sentenceList)
        sentenceList = SentenceResolver().CalculateCategory(sentenceList, parameterList["Category"])

        PipelineArgs.SentenceList = sentenceList

        return PipelineArgs
