#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import operator
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.NLP import NLP
from EmeraldAI.Entities.Word import Word
from EmeraldAI.Logic.NLP import Parameterizer


class PipelineArgs(BaseObject):

    def __init__(self, input=None):
        # Original Input
        self.Input = input
        self.Normalized = input
        self.BasewordTrimmedInput = None
        self.FullyTrimmedInput = None

        # Input Language | List of EmeraldAI.Entities.BaseObject.Word objects | List of parameters
        self.Language = None
        self.WordList = []
        self.SentenceList = None
        self.ParameterList = None

        # Input with parameterized data
        self.ParameterizedInput = None

        # Response with patameters | Raw response string | Response ID | Response found
        self.Response = None
        self.ResponseRaw = None
        self.ResponseID = None
        self.ResponseFound = False

        self.Animation = None

        self.TrainConversation = True

        self.Error = []

    def AddSentence(self, sentence):
        self.Input = sentence
        self.Language = NLP.DetectLanguage(sentence)

        self.Normalized = NLP.Normalize(sentence, self.Language)

        wordSegments = NLP.WordSegmentation(sentence)       
        for word in wordSegments:

            if self.HasWord(word, True):
                continue
            w = Word(word)
            w.UsedInSentence = True
            self.AddWord(w)

        self.WordList = [x for x in self.WordList if x.UsedInSentence]

    def GetLanguage(self):
        languageDict = {}
        for word in self.WordList:
            if languageDict.has_key(word.Language):
                languageDict[word.Language] += 1
            else:
                languageDict[word.Language] = 1
        return max(languageDict.iteritems(), key=operator.itemgetter(1))[0]

    def HasWord(self, comparison, approve=False):
        for word in self.WordList:
            if word.Equals(comparison):
                if approve:
                    word.UsedInSentence = True
                return True
        return False

    def AddWord(self, word):
        self.WordList.append(word)
                

    def GetSentencesWithHighestValue(self, margin=0):
        if self.SentenceList != None and self.SentenceList:
            highestRanking = max(node.Rating for node in self.SentenceList.values())
            if margin > 0:
                result = [node for node in self.SentenceList.values() if node.Rating>=(highestRanking-margin)]
            else:
                result = [node for node in self.SentenceList.values() if node.Rating==highestRanking]
            return result
        return None

    def GetRandomSentenceWithHighestValue(self, margin=0):
        result = self.GetSentencesWithHighestValue(margin)
        if(result != None):
            return random.choice(result)
        return None

    def GetInputSentenceParameter(self):
        tmpParameterList = []
        self.appendIfNotNone(tmpParameterList, Parameterizer.IsDate(self.Input))
        self.appendIfNotNone(tmpParameterList, Parameterizer.IsTime(self.Input))
        return tmpParameterList
