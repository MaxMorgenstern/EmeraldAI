#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from EmeraldAI.Entities.BaseObject import BaseObject


class PipelineArgs(BaseObject):

    def __init__(self, input):
        # Original Input
        self.Input = input
        self.Normalized = input

        # Input Language | List of EmeraldAI.Entities.BaseObject.Word objects | List of parameters
        self.Language = None
        self.WordList = None
        self.SentenceList = None
        self.ParameterList = None

        # Input with parameterized data
        self.ParameterizedInput = None

        # TODO Conversation History
        self.History = None

        # Response with patameters | Raw response string | Response ID | Response found
        self.Response = None
        self.ResponseRaw = None
        self.ResponseID = None
        self.ResponseFound = False
        self.ResponseAudio = None

        # TODO
        self.SessionID = 0

        # TODO - List of Errors
        self.Error = None


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
