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

        # Current Category | Current User
        self.Category = None
        self.UserName = None

        # Response | Response found
        self.Dialog = None
        self.DialogFound = False

        # List of Errors
        self.Error = None


    def GetSentencesWithHighestValue(self, margin=0):
        if self.SentenceList != None and len(self.SentenceList) > 0:
            highestRanking = max(node.Rating for node in self.SentenceList.values())
            if margin > 0:
                result = [node.ID for node in self.SentenceList.values() if node.Rating>=(highestRanking-margin)]
            else:
                result = [node.ID for node in self.SentenceList.values() if node.Rating==highestRanking]
            return result
        return None

    def GetRandomSentenceWithHighestValue(self, margin=0):
        return random.choice(self.GetSentencesWithHighestValue(margin))
