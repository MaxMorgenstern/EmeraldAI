#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton


class AnalyzeInput(object):
    __metaclass__ = Singleton


    def Process(self, PipelineArgs):

        sentenceList = {}
        parameterList = []

        for word in PipelineArgs.WordList:
            wordList = "'{0}'".format("', '".join(word.SynonymList))

            #TODO
            isAdmin = 1

            sentenceList = SentenceResolver().GetSentencesByKeyword(sentenceList, wordList, word.Language, True, isAdmin)
            sentenceList = SentenceResolver().GetSentencesByKeyword(sentenceList, "'{0}'".format(word.NormalizedWord), word.Language, False, isAdmin)

            parameterList += list(set(word.ParameterList) - set(parameterList))
        #print "Keyword:\t\t", sentenceList

        sentenceList = SentenceResolver().GetSentencesByParameter(sentenceList, parameterList, word.Language, isAdmin)
        #print "Parameter:\t\t", sentenceList, "\t", parameterList

        # TODO
        parameterList = {}
        parameterList["User"] = "Max"
        parameterList["Time"] = time.strftime("%H%M")
        parameterList["Day"] = time.strftime("%A")
        parameterList["Category"] = "Greeting"

        calculationResult = SentenceResolver().CalculateRequirement(sentenceList, parameterList)
        sentenceList = calculationResult["sentenceList"]
        #print "Calculate Requirement:\t", sentenceList

        sentenceList = SentenceResolver().AddSentencePriority(sentenceList)
        #print "Sentence Priority:\t", sentenceList

        sentenceList = SentenceResolver().CalculateCategory(sentenceList, parameterList["Category"])
        #print "Calculate Category:\t", sentenceList

        PipelineArgs.SentenceList = sentenceList

        return PipelineArgs
