#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.NLP.SentenceResolver import SentenceResolver
from EmeraldAI.Entities.NLPParameter import NLPParameter
from EmeraldAI.Entities.User import User

class AnalyzeScope(object):
    __metaclass__ = Singleton


    def Process(self, PipelineArgs):

        sentenceList = {}
        wordParameterList = []

        for word in PipelineArgs.WordList:

            user = User()
            if(len(word.SynonymList) > 0):
                wordList = "'{0}'".format("', '".join(word.SynonymList))
                sentenceList = SentenceResolver().GetSentencesByKeyword(sentenceList, wordList, word.Language, True, (user.Admin or user.Trainer))
            sentenceList = SentenceResolver().GetSentencesByKeyword(sentenceList, "'{0}'".format(word.NormalizedWord), word.Language, False, (user.Admin or user.Trainer))

            wordParameterList += list(set(word.ParameterList) - set(wordParameterList))

        sentenceList = SentenceResolver().GetSentencesByParameter(sentenceList, wordParameterList, PipelineArgs.Language, (user.Admin or user.Trainer))

        parameterList = NLPParameter().GetParameterList()

        calculationResult = SentenceResolver().CalculateRequirement(sentenceList, parameterList)
        sentenceList = calculationResult["sentenceList"]

        sentenceList = SentenceResolver().AddSentencePriority(sentenceList)
        sentenceList = SentenceResolver().CalculateCategory(sentenceList, parameterList["Category"])

        PipelineArgs.SentenceList = sentenceList

        return PipelineArgs
