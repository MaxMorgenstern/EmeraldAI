#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject


class Sentence(BaseObject):
    ID = None
    Rating = 0
    KeywordList = []
    OnlyStopwords = True

    HasCategory = []
    SetsCategory = []

    Action = None

    def __init__(self, ID, Rating, Keyword, IsStopword=True):
        self.ID = ID
        self.Rating = Rating
        self.KeywordList = [Keyword]
        self.OnlyStopwords = IsStopword

        self.HasCategory = []
        self.SetsCategory = []
        self.Action = None

    def __repr__(self):
         return "R:{0} L:{1} S:{2}\n".format(self.Rating, len(self.KeywordList), self.OnlyStopwords)

    def __str__(self):
         return "R:{0} L:{1} S:{2}\n".format(self.Rating, len(self.KeywordList), self.OnlyStopwords)

    def AddKeyword(self, Rating, Keyword, IsStopword=True):
        self.Rating += Rating
        self.KeywordList.append(Keyword)
        if self.OnlyStopwords:
            self.OnlyStopwords = IsStopword

    def AddPriority(self, Rating):
        self.Rating += Rating
