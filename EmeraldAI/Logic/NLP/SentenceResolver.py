#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Entities.Sentence import Sentence
from EmeraldAI.Config.Config import *
if(Config().Get("Database", "ConversationDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "ConversationDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

class SentenceResolver(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__synonymFactor = Config().GetFloat("SentenceResolver", "SynonymFactor") #0.5
        self.__stopwordFactor = Config().GetFloat("SentenceResolver", "StopwordFactor") #0.5
        self.__parameterFactor = Config().GetFloat("SentenceResolver", "ParameterFactor") #5
        self.__parameterFactorNoKeyword = Config().GetFloat("SentenceResolver", "ParameterFactorNoKeyword") #0.2

        self.__parameterStopwordThreshold = Config().GetFloat("SentenceResolver", "ParameterStopwordThreshold") #1.5

        self.__categoryBonus = Config().GetFloat("SentenceResolver", "CategoryBonus") #1
        self.__RequirementBonus = Config().GetFloat("SentenceResolver", "RequirementBonus") #1
        self.__ActionBonus = Config().GetFloat("SentenceResolver", "ActionBonus") #1.5


    def GetSentencesByKeyword(self, sentenceList, word, language, isSynonym, isTrainer):
        query = """SELECT DISTINCT Conversation_Sentence_Keyword.SentenceID, Conversation_Keyword.Stopword,
                Conversation_Sentence_Keyword.Priority, Conversation_Keyword.Priority, Conversation_Keyword.Normalized
                FROM Conversation_Keyword, Conversation_Sentence_Keyword, Conversation_Sentence
                WHERE Conversation_Keyword.ID = Conversation_Sentence_Keyword.KeywordID
                AND Conversation_Sentence_Keyword.SentenceID = Conversation_Sentence.ID
                AND Conversation_Sentence.Approved >= {0}
                AND Conversation_Sentence.Disabled = 0
                AND Conversation_Keyword.Normalized IN ({1}) AND Conversation_Keyword.Language = '{2}'"""
        trainer = 0 if isTrainer else 1
        sqlResult = db().Fetchall(query.format(trainer, word, language))
        for r in sqlResult:
            stopwordFactor = self.__stopwordFactor if r[1] == 1 else 1
            isStopword = True if r[1] == 1 else False
            synonymFactor = self.__synonymFactor if isSynonym else 1

            if r[0] in sentenceList:
                sentenceList[r[0]].AddKeyword((r[3] + synonymFactor * stopwordFactor * r[2]), r[4], isStopword)
            else:
                sentenceList[r[0]] = Sentence(r[0], (r[3] + synonymFactor * stopwordFactor * r[2]), r[4], isStopword)

        return sentenceList

    def GetSentencesByParameter(self, sentenceList, wordParameterList, language, isTrainer):
        query = """SELECT DISTINCT Conversation_Sentence_Keyword.SentenceID, Conversation_Keyword.Priority,
                Conversation_Sentence_Keyword.Priority, Conversation_Keyword.Normalized
                FROM Conversation_Keyword, Conversation_Sentence_Keyword, Conversation_Sentence
                WHERE Conversation_Keyword.ID = Conversation_Sentence_Keyword.KeywordID
                AND Conversation_Sentence_Keyword.SentenceID = Conversation_Sentence.ID
                AND Conversation_Sentence.Approved >= {0}
                AND Conversation_Sentence.Disabled = 0
                AND Conversation_Keyword.Normalized IN ({1}) AND Conversation_Keyword.Language = '{2}'"""
        trainer = 0 if isTrainer else 1
        sqlResult = db().Fetchall(query.format(trainer, "'{" + "}', '{".join(wordParameterList) + "}'", language))
        for r in sqlResult:
            word = "{{{0}}}".format(r[3])

            if r[0] in sentenceList:
                # if only stop-keywords present and threshold reached
                if sentenceList[r[0]].OnlyStopwords and sentenceList[r[0]].Rating >= self.__parameterStopwordThreshold:
                    sentenceList[r[0]].AddKeyword((r[1] + self.__parameterFactor * r[2] * self.__stopwordFactor), word)

                # if there are normal keywords present
                if not sentenceList[r[0]].OnlyStopwords:
                    sentenceList[r[0]].AddKeyword((r[1] + self.__parameterFactor * r[2]), word)
            # sentence not in list by now
            else:
                sentenceList[r[0]] = Sentence(r[0], (self.__parameterFactor * r[2] * self.__parameterFactorNoKeyword), word)

        return sentenceList

    def AddActionBonus(self, sentenceList):
        query = """SELECT Conversation_Action.ID
            FROM Conversation_Sentence_Action, Conversation_Action
            WHERE Conversation_Sentence_Action.ActionID = Conversation_Action.ID
            AND Conversation_Sentence_Action.SentenceID = '{0}' LIMIT 1"""

        for sentenceID, value in sentenceList.iteritems():
            sqlResult = db().Fetchall(query.format(sentenceID))
            for r in sqlResult:
                sentenceList[sentenceID].AddPriority(self.__ActionBonus)
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
                requirementName = r[2].title()
                if r[0] == None:
                    if parameterList[requirementName] != r[1]:
                        deleteList.append(sentenceID)
                    else:
                        sentenceList[sentenceID].AddPriority(self.__RequirementBonus)
                    continue
                else:
                    if r[0] == "lt" and not parameterList[requirementName] < r[1]:
                        deleteList.append(sentenceID)
                    if r[0] == "le" and not parameterList[requirementName] <= r[1]:
                        deleteList.append(sentenceID)
                    if r[0] == "eq" and not parameterList[requirementName] == r[1]:
                        deleteList.append(sentenceID)
                    if r[0] == "ge" and not parameterList[requirementName] >= r[1]:
                        deleteList.append(sentenceID)
                    if r[0] == "gt" and not parameterList[requirementName] > r[1]:
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
