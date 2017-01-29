#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.NLP import NLP
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Singleton import Singleton

if(Config().Get("Database", "NLPDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "NLPDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

class Requirement(object):
    Name = None
    Comparison = None
    Value = None

    def __init__(self, Name, Comparison, Value):
        self.Name = Name
        self.Comparison = Comparison
        self.Value = Value

class Action(object):
    Name = None
    Module = None
    Class = None
    Function = None

    def __init__(self, Name, Module, Class, Function):
        self.Name = Name
        self.Module = Module
        self.Class = Class
        self.Function = Function


class DialogTrainer(object):
    __metaclass__ = Singleton

    def SaveKeyword(self, Word, Language):
        isStopword = 0
        if NLP.IsStopword(Word, Language):
            isStopword = 1
        query = "INSERT INTO Conversation_Keyword ('Keyword', 'Normalized', 'Language', 'Stopword') Values ('{0}', '{1}', '{2}', '{3}')".format(Word, NLP.Normalize(Word, Language), Language, isStopword)
        keywordID = db().Execute(query)
        if(keywordID == None):
            query = "SELECT ID FROM Conversation_Keyword WHERE Normalized = '{0}'".format(NLP.Normalize(Word, Language))
            keywordID = db().Fetchall(query)[0][0]
        return keywordID

    def SaveRequirement(self, Name):
        query = "INSERT INTO Conversation_Requirement ('Name') Values ('{0}')".format(Name)
        requirementID = db().Execute(query)
        if(requirementID == None):
            query = "SELECT ID FROM Conversation_Requirement WHERE Name = '{0}'".format(Name)
            requirementID = db().Fetchall(query)[0][0]
        return requirementID

    def SaveCategory(self, Name):
        query = "INSERT INTO Conversation_Category ('Name') Values ('{0}')".format(Name)
        categoryID = db().Execute(query)
        if(categoryID == None):
            query = "SELECT ID FROM Conversation_Category WHERE Name = '{0}'".format(Name)
            categoryID = db().Fetchall(query)[0][0]
        return categoryID

    def SaveAction(self, Name, Module, Class, Function):
        query = "INSERT INTO Conversation_Action ('Name', 'Module', 'Class', 'Function') Values ('{0}')".format(Name, Module, Class, Function)
        actionID = db().Execute(query)
        if(actionID == None):
            query = "SELECT ID FROM Conversation_Action WHERE Name = '{0}'".format(Name)
            actionID = db().Fetchall(query)[0][0]
        return actionID


    def TrainKeywords(self, Sentence, Language):
        keywordList = []
        wordSegments = NLP.WordSegmentation(Sentence, True)
        for word in wordSegments:
            keywordID = self.SaveKeyword(word, Language)
            if keywordID not in keywordList:
                keywordList.append(keywordID)
        return keywordList


    # TODO: ensure we don't train sentences multiple times
    def TrainSentence(self, Sentence, Language, KeywordList, RequirementObjectList, HasCategoryList, SetCategoryList, ActionName):
        # Train Keywords of response
        self.TrainKeywords(Sentence, Language)

        # save sentence
        query = "INSERT INTO Conversation_Sentence ('Sentence', 'Language', 'Source', 'Approved') Values ('{0}', '{1}', '{2}', '{3}')".format(Sentence, Language, "Trainer", "1")
        sentenceID = db().Execute(query)
        if(sentenceID == None):
            query = "SELECT ID FROM Conversation_Sentence WHERE Sentence = '{0}'".format(Sentence)
            sentenceID = db().Fetchall(query)[0][0]


        # link keyword - sentence
        for keyword in KeywordList:
            if(type(keyword) == int):
                keywordID = keyword
            else:
                keywordID = self.SaveKeyword(keyword, Language)
            query = "INSERT INTO Conversation_Sentence_Keyword ('KeywordID', 'SentenceID') Values ('{0}', '{1}')".format(keywordID, sentenceID)
            db().Execute(query)


        for requirement in RequirementObjectList:
            # create requirement if it does not exist - or get ID
            requirementID = self.SaveRequirement(requirement.Name)
            # Link requirement - sentence

            if(requirement.Comparison == None):
                query = "INSERT INTO Conversation_Sentence_Requirement ('SentenceID', 'RequirementID', 'Value') Values ('{0}', '{1}', '{2}')".format(sentenceID, requirementID, requirement.Value)
            else:
                query = "INSERT INTO Conversation_Sentence_Requirement ('SentenceID', 'RequirementID', 'Comparison', 'Value') Values ('{0}', '{1}', '{2}', '{3}')".format(sentenceID, requirementID, requirement.Comparison, requirement.Value)
            db().Execute(query)


        for category in HasCategoryList:
            if(len(category) > 1):
                # create category if it does not exist - or get ID
                categoryID = self.SaveCategory(category)
                # Link category - sentence
                query = "INSERT INTO Conversation_Sentence_Category_Has ('SentenceID', 'CategoryID') Values ('{0}', '{1}')".format(sentenceID, categoryID)
                db().Execute(query)


        for category in SetCategoryList:
            if(len(category) > 1):
                # create set category if it does not exist - or get ID
                categoryID = self.SaveCategory(category)
                # Link set category - sentence
                query = "INSERT INTO Conversation_Sentence_Category_Set ('SentenceID', 'CategoryID') Values ('{0}', '{1}')".format(sentenceID, categoryID)
                db().Execute(query)


        if(ActionName != None and len(ActionName) > 1):
            # create follow up action if it does not exist - or get ID
            #actionID = self.SaveAction(FollowUpActionObject.Name, FollowUpActionObject.Module, FollowUpActionObject.Class, FollowUpActionObject.Function)
            # Link follow up action - sentence
            query = "SELECT ID FROM Conversation_Action WHERE Name = '{0}'".format(ActionName)
            actionID = db().Fetchall(query)[0][0]
            query = "INSERT INTO Conversation_Sentence_Action ('SentenceID', 'ActionID') Values ('{0}', '{1}')".format(sentenceID, actionID)
            db().Execute(query)

        return True

