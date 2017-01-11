#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Entities.Sentence import Sentence
from EmeraldAI.Config.Config import *
if(Config().Get("Database", "NLPDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "NLPDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

class SentenceResolver(object):
    __metaclass__ = Singleton

    __synonymFactor = 0.5
    __stopwordFactor = 0.5

    __parameterBonus = 5
    __parameterButNoKeywordFactor = 0.2
    __parameterStopwordThreshhold = 1.5

    __categoryBonus = 1

    __RequirementBonus = 1

    # TODO: config
    def __init__(self):
        self.__synonymFactor = 0.5
        self.__stopwordFactor = 0.5

        self.__parameterBonus = 5
        self.__parameterButNoKeywordFactor = 0.2
        self.__parameterStopwordThreshhold = 1.5

        self.__categoryBonus = 1

        self.__RequirementBonus = 1


    #TODO



    def GetSentencesByKeyword(self, sentenceList, word, language, isSynonym, isAdmin):
        query = """SELECT Conversation_Keyword.Stopword, Conversation_Sentence_Keyword.Priority,
                Conversation_Sentence_Keyword.SentenceID, Conversation_Keyword.Priority
                FROM Conversation_Keyword, Conversation_Sentence_Keyword, Conversation_Sentence
                WHERE Conversation_Keyword.ID = Conversation_Sentence_Keyword.KeywordID
                AND Conversation_Sentence_Keyword.SentenceID = Conversation_Sentence.ID
                AND Conversation_Sentence.Approved = {0}
                AND Conversation_Sentence.Disabled = {1}
                AND Conversation_Keyword.Normalized IN ({2}) AND Conversation_Keyword.Language = '{3}'"""
        sqlResult = db().Fetchall(query.format(isAdmin, '0', word, language))
        for r in sqlResult:
            stopwordNumber = self.__stopwordFactor if r[0] == 1 else 1
            isStopword = True if r[0] == 1 else False
            synonymNumber = self.__synonymFactor if isSynonym else 1

            if r[2] in sentenceList:
                sentenceList[r[2]].AddKeyword((r[3] + synonymNumber * stopwordNumber * r[1]), word, isStopword)
            else:
                sentenceList[r[2]] = Sentence(r[2], (r[3] + synonymNumber * stopwordNumber * r[1]), word, isStopword)

        return sentenceList

    def GetSentencesByParameter(self, sentenceList, parameterList, language, isAdmin):
        query = """SELECT Conversation_Keyword.Priority, Conversation_Sentence_Keyword.Priority,
                Conversation_Sentence_Keyword.SentenceID, Conversation_Keyword.Normalized
                FROM Conversation_Keyword, Conversation_Sentence_Keyword, Conversation_Sentence
                WHERE Conversation_Keyword.ID = Conversation_Sentence_Keyword.KeywordID
                AND Conversation_Sentence_Keyword.SentenceID = Conversation_Sentence.ID
                AND Conversation_Sentence.Approved = {0}
                AND Conversation_Sentence.Disabled = {1}
                AND Conversation_Keyword.Normalized IN ({2}) AND Conversation_Keyword.Language = '{3}'"""
        sqlResult = db().Fetchall(query.format(isAdmin, '0', "'{" + "}', '{".join(parameterList) + "}'", language))
        for r in sqlResult:

            word = "{{{0}}}".format(r[3])

            if r[2] in sentenceList:
                # if only stop-keywords present and threshhold reached
                if sentenceList[r[2]].OnlyStopwords and sentenceList[r[2]].Rating >= self.__parameterStopwordThreshhold:
                    sentenceList[r[2]].AddKeyword((r[0] + self.__parameterBonus * self.__stopwordFactor * r[1]), word)

                # if there are normal keywords present
                if not sentenceList[r[2]].OnlyStopwords:
                    sentenceList[r[2]].AddKeyword((r[0] + self.__parameterBonus * r[1]), word)
            # sentence not in list by now
            else:
                sentenceList[r[2]] = Sentence(r[2], (self.__parameterBonus * self.__parameterButNoKeywordFactor * r[1]), word)

        return sentenceList


    def AddSentencePriority(self, sentenceList):
        query = """SELECT Priority FROM Conversation_Sentence WHERE ID = '{0}'"""
        for sentenceID, value in sentenceList.iteritems():
            sqlResult = db().Fetchall(query.format(sentenceID))
            for r in sqlResult:
                if not sentenceList[sentenceID].OnlyStopwords:
                    sentenceList[sentenceID].AddPriority(r[0])
        return sentenceList


    def CalculateRequirement(self, sentenceList, parameterList, delete=True):
        query="""SELECT Conversation_Sentence_Requirement.Comparison,
            Conversation_Sentence_Requirement.Value, Conversation_Requirement.Name
            FROM Conversation_Sentence_Requirement, Conversation_Requirement
            WHERE Conversation_Sentence_Requirement.RequirementID = Conversation_Requirement.ID
            AND Conversation_Sentence_Requirement.SentenceID='{0}'
            GROUP BY Conversation_Sentence_Requirement.SentenceID, Conversation_Sentence_Requirement.RequirementID
            """

        deleteList = []
        for sentenceID, value in sentenceList.iteritems():
            sqlResult = db().Fetchall(query.format(sentenceID))
            for r in sqlResult:
                if r[0] == None:
                    if parameterList[r[2]] != r[1]:
                        deleteList.append(sentenceID)
                    else:
                        sentenceList[sentenceID].AddPriority(self.__RequirementBonus)
                    continue
                else:
                    if r[0] == "lt" and not parameterList[r[2]] < r[1]:
                        deleteList.append(sentenceID)
                    if r[0] == "le" and not parameterList[r[2]] <= r[1]:
                        deleteList.append(sentenceID)
                    if r[0] == "eq" and not parameterList[r[2]] == r[1]:
                        deleteList.append(sentenceID)
                    if r[0] == "ge" and not parameterList[r[2]] >= r[1]:
                        deleteList.append(sentenceID)
                    if r[0] == "gt" and not parameterList[r[2]] > r[1]:
                        deleteList.append(sentenceID)
                    else:
                        sentenceList[sentenceID].AddPriority(self.__RequirementBonus)
                    continue
        if delete:
            for d in list(set(deleteList)):
                del sentenceList[d]

        return {'sentenceList':sentenceList, 'deleteList':deleteList}


    def CalculateCategory(self, sentenceList, category):
        query = """SELECT Conversation_Category.Name
            FROM Conversation_Category, {0}
            WHERE Conversation_Category.ID = {0}.CategoryID
            AND {0}.SentenceID = '{1}'"""

        for sentenceID, value in sentenceList.iteritems():
            sqlResult = db().Fetchall(query.format("Conversation_Sentence_Category_Has", sentenceID))
            for r in sqlResult:
                sentenceList[sentenceID].HasCategory.append(r[0])

            sqlResult = db().Fetchall(query.format("Conversation_Sentence_Category_Set", sentenceID))
            for r in sqlResult:
                sentenceList[sentenceID].SetsCategory.append(r[0])

        if category in sentenceList[sentenceID].HasCategory:
            sentenceList[sentenceID].AddPriority(self.__categoryBonus)

        return sentenceList





