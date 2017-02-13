#!/usr/bin/python
# -*- coding: utf-8 -*-
import itertools

from EmeraldAI.Logic.NLP import NLP
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Singleton import Singleton

if(Config().Get("Database", "ConversationDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "ConversationDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

class Requirement(object):
    Name = None
    Comparison = None
    Value = None

    def __init__(self, Name, Comparison, Value):
        self.Name = Name
        self.Comparison = Comparison
        self.Value = Value

class DialogTrainer(object):
    __metaclass__ = Singleton

    __comparisonValues = ["lt", "gt", "le", "eq", "ge"]

    def __init__(self):
        self.__csvColCount = Config().GetInt("Trainer", "CsvColumnCount")
        self.__csvActionColCount = Config().GetInt("Trainer", "CsvActionColumnCount")

    def __groupSeparator(self, line):
        return line=='\n'

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

    def SaveKeywordsFromSentence(self, Sentence, Language):
        keywordList = []
        wordSegments = NLP.WordSegmentation(Sentence, True)
        for word in wordSegments:
            keywordID = self.SaveKeyword(word, Language)
            if keywordID not in keywordList:
                keywordList.append(keywordID)
        return keywordList

    def SaveSentence(self, Sentence, Language, UserName, Approved = 0):
        query = "INSERT INTO Conversation_Sentence ('Sentence', 'Language', 'Source', 'Approved') Values ('{0}', '{1}', '{2}', '{3}')".format(Sentence, Language, UserName, 0)
        sentenceID = db().Execute(query)
        if(sentenceID == None):
            query = "SELECT ID FROM Conversation_Sentence WHERE Sentence = '{0}'".format(Sentence)
            sentenceID = db().Fetchall(query)[0][0]
        return sentenceID

    def LinkKeywordAndSentence(self, KeywordList, Language, SentenceID):
        for keyword in KeywordList:
            if(type(keyword) == int):
                keywordID = keyword
            else:
                keywordID = self.SaveKeyword(keyword, Language)
            query = "INSERT INTO Conversation_Sentence_Keyword ('KeywordID', 'SentenceID') Values ('{0}', '{1}')".format(keywordID, SentenceID)
            db().Execute(query)


    def TrainSentence(self, OutputSentence, ResponseSentence, Language, UserName):
        # Train Keywords of both sentences
        outputKeywords = self.SaveKeywordsFromSentence(OutputSentence, Language)
        responseKeywords = self.SaveKeywordsFromSentence(ResponseSentence, Language)

        # save sentence
        sentenceID = self.SaveSentence(ResponseSentence, Language, UserName)

        # link keywords to sentence
        self.LinkKeywordAndSentence(outputKeywords, Language, sentenceID)


    def TrainFullSentence(self, Sentence, Language, KeywordList, RequirementObjectList, HasCategoryList, SetCategoryList, ActionName):
        # Train Keywords of sentence
        self.SaveKeywordsFromSentence(Sentence, Language)

        # save sentence
        sentenceID = self.SaveSentence(Sentence, Language, "Trainer", "1")

        # link keywords to sentence
        self.LinkKeywordAndSentence(KeywordList, Language, sentenceID)

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
            # Link follow up action - sentence
            query = "SELECT ID FROM Conversation_Action WHERE Name = '{0}'".format(ActionName)
            actionIDRow = db().Fetchall(query)
            if len(actionIDRow) > 0:
                query = "INSERT INTO Conversation_Sentence_Action ('SentenceID', 'ActionID') Values ('{0}', '{1}')".format(sentenceID, actionIDRow[0][0])
                db().Execute(query)

        return True


    def TrainActionCSV(self, data, language):
        for key, group in itertools.groupby(data, self.__groupSeparator):
            line = ''.join(str(e) for e in group)
            line = line.strip()
            if (len(line) > 1):
                splitLine = line.split(";")
                if(len(splitLine) == self.__csvActionColCount):
                    name = splitLine[0]
                    moduleName = splitLine[1]
                    className = splitLine[2]
                    functionName = splitLine[3]

                    self.SaveAction(name, moduleName, className, functionName)


    def TrainCSV(self, data, language):
        qlist = []
        for key, group in itertools.groupby(data, self.__groupSeparator):
            line = ''.join(str(e) for e in group)
            line = line.strip()
            if (len(line) > 1):

                # on empty line reset
                if(line == ";;;;;"):
                    qlist = []
                    continue

                splitLine = line.split(";")
                if(len(splitLine) == self.__csvColCount):
                    qa = splitLine[0]
                    req = splitLine[1]
                    sent = splitLine[2]
                    hasC = splitLine[3]
                    setC = splitLine[4]
                    act = splitLine[5]

                    # Question
                    if(qa == "Q"):
                        qlist += list(set(self.SaveKeywordsFromSentence(sent, language)) - set(qlist))

                    # Response
                    if(qa == "A"):
                        requirementObjectList = []
                        for r in req.split("|"):
                            if(len(r) > 2):
                                temp = r.split(":")

                                rName = temp[0]
                                if (temp[1][0:2] not in self.__comparisonValues):
                                    rComparison = None
                                    rValue = temp[1]
                                else:
                                    rComparison = temp[1][0:2]
                                    rValue = temp[1][2:]
                                requirementObjectList.append(Requirement(rName, rComparison, rValue))

                        hasCategoryList = []
                        for h in hasC.split("|"):
                            hasCategoryList.append(h)

                        setCategoryList = []
                        for s in setC.split("|"):
                            setCategoryList.append(s)

                        self.TrainFullSentence(sent, language, qlist, requirementObjectList, hasCategoryList, setCategoryList, act)

