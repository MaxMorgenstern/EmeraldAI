#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Entities.Sentence import Sentence
from EmeraldAI.Config.Config import Config
from EmeraldAI.Logic.Logger import FileLogger
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
        self.__InteractionBonus = Config().GetFloat("SentenceResolver", "InteractionBonus") #1.75

        self.__MinSentenceCountForRemoval = Config().GetFloat("SentenceResolver", "MinSentenceCountForRemoval") #5
        self.__RemoveSentenceBelowThreshold = Config().GetFloat("SentenceResolver", "RemoveSentenceBelowThreshold") #1.5

        self.__MinNonStopwordSentences = Config().GetFloat("SentenceResolver", "MinNonStopwordSentences") #1

        self.__NoneTag = "None"

    def GetSentenceByCategory(self, category, language, isTrainer):
        sentenceDictionary = {}
        query = """SELECT cs.ID
            FROM Conversation_Category as cc , Conversation_Sentence_Category_Has as csch,  Conversation_Sentence as cs
            WHERE cc.Name = '{0}'
            AND cc.ID = csch.CategoryID
            AND csch.SentenceID = cs.ID
            AND cs.Approved >= {1}
            AND cs.Language = '{2}'
            AND cs.Disabled = 0
            """
        trainer = 0 if isTrainer else 1
        sqlResult = db().Fetchall(query.format(category, trainer, language))
        for r in sqlResult:
            sentenceDictionary[r[0]] = Sentence(r[0],  0, category, False)
        return sentenceDictionary


    def GetSentencesByKeyword(self, sentenceList, word, baseWord, language, isSynonym, isTrainer):
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
            synonymTag = "(* {0})".format(baseWord) if isSynonym else ""

            if r[0] in sentenceList:
                sentenceList[r[0]].AddKeyword((r[3] + synonymFactor * stopwordFactor * r[2]), r[4], isStopword)
            else:
                sentenceList[r[0]] = Sentence(r[0], (r[3] + synonymFactor * stopwordFactor * r[2]), r[4], isStopword)

            sentenceList[r[0]].AddBaseword("{0}{1}".format(r[4], synonymTag))

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
    
    def GetSentenceByInteraction(self, sentenceList, interaction, language, isTrainer):
        query = """SELECT Conversation_Sentence.ID, Conversation_Sentence.Priority
            FROM Conversation_Interaction, Conversation_Interaction_Sentence, Conversation_Sentence
            WHERE Conversation_Interaction.Name = '{0}'
            AND Conversation_Interaction.ID = Conversation_Interaction_Sentence.InteractionID
            AND Conversation_Sentence.ID = Conversation_Interaction_Sentence.SentenceID
            AND Conversation_Sentence.Approved >= {1}
            AND Conversation_Sentence.Disabled = 0
            AND Conversation_Sentence.Language = '{2}'"""
        trainer = 0 if isTrainer else 1

        sqlResult = db().Fetchall(query.format(interaction, trainer, language))
        for r in sqlResult:
            sentenceList[r[0]] = Sentence(r[0],  r[1], interaction, False)
            sentenceList[r[0]].InteractionName = interaction
            sentenceList[r[0]].AddPriority(self.__InteractionBonus)

        return sentenceList

    def AddInteractionBonus(self, sentenceList):
        for sentenceID in sentenceList.iterkeys():
            if sentenceList[sentenceID].InteractionName is not None:
                sentenceList[sentenceID].AddPriority(self.__InteractionBonus)
        return sentenceList

    def AddActionBonus(self, sentenceList):
        query = """SELECT Conversation_Action.ID
            FROM Conversation_Sentence_Action, Conversation_Action
            WHERE Conversation_Sentence_Action.ActionID = Conversation_Action.ID
            AND Conversation_Sentence_Action.SentenceID = '{0}' LIMIT 1"""

        for sentenceID in sentenceList.iterkeys():
            sqlResult = db().Fetchall(query.format(sentenceID))
            for _ in sqlResult:
                sentenceList[sentenceID].AddPriority(self.__ActionBonus)
        return sentenceList


    def AddSentencePriority(self, sentenceList):
        query = """SELECT Priority FROM Conversation_Sentence WHERE ID = '{0}'"""
        for sentenceID in sentenceList.iterkeys():
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
            GROUP BY Conversation_Sentence_Requirement.SentenceID,
                Conversation_Sentence_Requirement.RequirementID,
                Conversation_Sentence_Requirement.Comparison
            """
        deleteList = []
        for sentenceID in sentenceList.iterkeys():
            sqlResult = db().Fetchall(query.format(sentenceID))
            for r in sqlResult:
                requirementName = r[2].title()
                
                if requirementName not in parameterList and r[1].lower() != self.__NoneTag.lower():
                    FileLogger().Error("SentenceResolver Line 171: Requirement missing in parameter list: {0}".format(requirementName))
                    deleteList.append(sentenceID)
                    continue

                if r[0] is None:
                    if type(parameterList[requirementName]) == list and r[1].lower() not in parameterList[requirementName]:
                        deleteList.append(sentenceID)
                    elif type(parameterList[requirementName]) == str and parameterList[requirementName].lower() != r[1].lower():
                        deleteList.append(sentenceID)
                    else:
                        sentenceList[sentenceID].AddPriority(self.__RequirementBonus)
                    continue
                else:
                    if r[1].lower() == self.__NoneTag.lower():
                        if (r[0] == "eq" and (requirementName in parameterList and parameterList[requirementName] is not None)):
                            deleteList.append(sentenceID)
                            continue
                        if (r[0] == "ne" and not (requirementName in parameterList and parameterList[requirementName] is not None)):
                            deleteList.append(sentenceID)
                            continue
                        sentenceList[sentenceID].AddPriority(self.__RequirementBonus)
                        continue
                    if r[0] == "lt" and not parameterList[requirementName] < r[1]:
                        deleteList.append(sentenceID)
                        continue
                    if r[0] == "le" and not parameterList[requirementName] <= r[1]:
                        deleteList.append(sentenceID)
                        continue
                    if r[0] == "eq" and not parameterList[requirementName] == r[1]:
                        deleteList.append(sentenceID)
                        continue
                    if r[0] == "ne" and not parameterList[requirementName] != r[1]:
                        deleteList.append(sentenceID)
                        continue
                    if r[0] == "ge" and not parameterList[requirementName] >= r[1]:
                        deleteList.append(sentenceID)
                        continue
                    if r[0] == "gt" and not parameterList[requirementName] > r[1]:
                        deleteList.append(sentenceID)
                        continue

                    sentenceList[sentenceID].AddPriority(self.__RequirementBonus)
                    
        if delete:
            for d in list(set(deleteList)):
                del sentenceList[d]

        return {'sentenceList':sentenceList, 'deleteList':deleteList}


    def CalculateCategory(self, sentenceList, category):
        query = """SELECT Conversation_Category.Name
            FROM Conversation_Category, {0}
            WHERE Conversation_Category.ID = {0}.CategoryID
            AND {0}.SentenceID = '{1}'"""

        for sentenceID in sentenceList.iterkeys():
            sqlResult = db().Fetchall(query.format("Conversation_Sentence_Category_Has", sentenceID))
            for r in sqlResult:
                sentenceList[sentenceID].HasCategory.append(r[0])

            sqlResult = db().Fetchall(query.format("Conversation_Sentence_Category_Set", sentenceID))
            for r in sqlResult:
                sentenceList[sentenceID].SetsCategory.append(r[0])

            if category in sentenceList[sentenceID].HasCategory:
                sentenceList[sentenceID].AddPriority(self.__categoryBonus)

        return sentenceList


    def RemoveLowPrioritySentences(self, sentenceList, useDynamicThreshold=False):
        priorityThreshold = self.__RemoveSentenceBelowThreshold
        if(len(sentenceList) >= self.__MinSentenceCountForRemoval):
            highestRanking = max(node.Rating for node in sentenceList.values())

            if useDynamicThreshold:
                lowestRanking = min(node.Rating for node in sentenceList.values())
                dynamicThreshold = (lowestRanking * 3 + highestRanking + priorityThreshold) / 5
                usedThreshold = priorityThreshold if priorityThreshold > dynamicThreshold else dynamicThreshold
            else:
                usedThreshold = priorityThreshold

            if highestRanking > usedThreshold:
                deleteResult = [node for node in sentenceList.values() if node.Rating <= usedThreshold]
                for d in list(set(deleteResult)):
                    del sentenceList[d.ID]
        return sentenceList


    def RemoveStopwordOnlySentences(self, sentenceList):
        minNonStopwordSentences = self.__MinNonStopwordSentences
        minNonStopwordSentences = minNonStopwordSentences if minNonStopwordSentences > 0 else 1

        stopwordSentences = [node for node in sentenceList.values() if node.OnlyStopwords]
        if(len(sentenceList) - minNonStopwordSentences >= stopwordSentences):
            for d in list(set(stopwordSentences)):
                del sentenceList[d.ID]
        return sentenceList
