#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Config.Config import *
if(Config().Get("Database", "ConversationDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "ConversationDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

class Sentence(BaseObject):
    ID = None
    Rating = 0
    KeywordList = []
    OnlyStopwords = True

    HasCategory = []
    SetsCategory = []

    def __init__(self, ID, Rating, Keyword, IsStopword=True):
        self.ID = ID
        self.Rating = Rating
        self.KeywordList = [Keyword]
        self.OnlyStopwords = IsStopword

        self.HasCategory = []
        self.SetsCategory = []

    # TODO - some better output
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

    def GetSentenceString(self, formal=True):
        query = "SELECT Sentence, Formal, Informal FROM Conversation_Sentence WHERE ID = '{0}'"
        sqlResult = db().Fetchall(query.format(self.ID))
        for r in sqlResult:
            if formal:
                if r[1]:
                    return r[1]
                else:
                    return r[0]
            else:
                if r[2]:
                    return r[2]
                else:
                    return r[0]
        return None

    def GetAction(self):
        query = """SELECT Conversation_Action.*
            FROM Conversation_Sentence_Action, Conversation_Action
            WHERE Conversation_Sentence_Action.ActionID = Conversation_Action.ID
            AND Conversation_Sentence_Action.SentenceID = '{0}'"""
        sqlResult = db().Fetchall(query.format(self.ID))
        for r in sqlResult:
            return {'Name':r[0], 'Module':r[1], 'Class':r[2], 'Function':r[3]}
        return None
