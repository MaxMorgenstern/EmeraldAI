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

    BasewordList = []

    HasCategory = []
    SetsCategory = []

    ActionID = None

    def __init__(self, ID, Rating, Keyword, IsStopword=True):
        self.ID = ID
        self.Rating = Rating
        self.KeywordList = [Keyword]
        self.OnlyStopwords = IsStopword

        self.BasewordList = []

        self.HasCategory = []
        self.SetsCategory = []

    def AddBaseword(self, Baseword):
        self.BasewordList.append(Baseword)

    def AddKeyword(self, Rating, Keyword, IsStopword=True):
        self.Rating += Rating
        self.KeywordList.append(Keyword)
        if self.OnlyStopwords:
            self.OnlyStopwords = IsStopword

    def AddPriority(self, Rating):
        self.Rating += Rating

    def GetAnimation(self):
        query = "SELECT Animation FROM Conversation_Sentence WHERE ID = '{0}'"
        sqlResult = db().Fetchall(query.format(self.ID))
        for r in sqlResult:
            return r[0]
        return None

    def GetSentenceString(self, formal=True):
        query = "SELECT Sentence, Formal, Informal FROM Conversation_Sentence WHERE ID = '{0}'"
        sqlResult = db().Fetchall(query.format(self.ID))
        for r in sqlResult:
            data = self.__formalOrOther(r, formal)
            if data is not None:
                return data
        return None

    def GetAction(self):
        query = """SELECT Conversation_Action.Name, Conversation_Action.Module,
            Conversation_Action.Class, Conversation_Action.Function, Conversation_Action.ID
            FROM Conversation_Sentence_Action, Conversation_Action
            WHERE Conversation_Sentence_Action.ActionID = Conversation_Action.ID
            AND Conversation_Sentence_Action.SentenceID = '{0}'"""
        sqlResult = db().Fetchall(query.format(self.ID))
        for r in sqlResult:
            self.ActionID =int(r[4])
            return {'Name':r[0], 'Module':r[1], 'Class':r[2], 'Function':r[3]}
        return None

    def GetActionErrorResponse(self, language, formal=True):
        query = """SELECT Sentence, Formal, Informal FROM Conversation_Action_Error WHERE ActionID = '{0}' and Language = '{1}'"""
        sqlResult = db().Fetchall(query.format(self.ActionID, language))
        for r in sqlResult:
            data = self.__formalOrOther(r, formal)
            if data is not None:
                return data
        return None


    def __formalOrOther(self, data, formal):
        if formal:
            if data[1]:
                return data[1]
            else:
                return data[0]
        else:
            if data[2]:
                return data[2]
            else:
                return data[0]
        return None


    def __repr__(self):
         return "Rating:{0}".format(self.Rating)

    def __str__(self):
         return "Rating:{0}".format(self.Rating)
