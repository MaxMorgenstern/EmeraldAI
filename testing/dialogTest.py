#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import os
import itertools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

import time

def __groupSeparator(line):
    return line=='\n'

def addToList(str_to_add, list_of_strings):
    if str_to_add not in list_of_strings:
        list_of_strings.append(str_to_add)
    return list_of_strings


# Training #############
from EmeraldAI.Logic.Trainer.DialogTrainer import *

start_time = time.time()

dt = DialogTrainer()

language = "de"
colCount = 6
data=""
#data = """Q;;Guten Abend;;Greeting;
#Q;;Guten Morgen;;Greeting;
#Q;;Guten Tag;;Greeting;
#Q;;Moin Moin;;Greeting;
#Q;;Hallo;;Greeting;
#Q;;Tach;;Greeting;
#Q;;Tag auch;;Greeting;
#Q;;Hallöchen;;Greeting;
#A;;Hallo {name}.;Greeting;;
#A;;Guten Tag {name}.;Greeting;;
#A;;Guten Tag {name}. Wie kann ich Ihnen heute behilflich sein?;Greeting;Question;
#A;;Ich wünsche Ihnen einen schönen guten Tag!;Greeting;;
#A;User:Unknown;Guten Tag. Wie ist Ihr Name?;Greeting;Question|Name;
#A;Time:lt1100|User:Unknown;Guten Morgen. Wie ist Ihr Name?;Greeting;Question|Name;
#A;Time:lt1100;Ich wünsche Ihnen ebenfalls einen guten Morgen {name}.;Greeting;;
#A;Time:lt1100;Guten Morgen {name}.;Greeting;;
#A;Time:lt1100;Guten Morgen {name}. Wie geht es Ihnen heute Früh?;Greeting;Wellbeing|Question;
#A;Time:lt1100;Hallo {name}, wie geht es Ihnen heute?;Greeting;Wellbeing|Question;
#A;Time:lt1100|Day:Monday;Guten Morgen {name}. Ich hoffe Sie hatten ein schönes Wochenende?;Greeting;Wellbeing|Question;
#A;Time:lt1100|Day:Monday;Guten Morgen {name}. Ich hoffe Sie hatten ein erholsames Wochenende?;Greeting;Wellbeing|Question;
#A;Time:gt1700;Guten Abend {name}. Ich hoffe Sie hatten einen schönen Tag.;Greeting;Wellbeing|Question;
#A;Time:gt1700;Guten Abend {name}.;Greeting;;
#---
#Q;;Wer ist {name};;Command;
#A;;{name} ist {result};;;
#"""

comparisonValues = ["lt", "gt", "le", "eq", "ge"]

qlist = []
for key, group in itertools.groupby(data, __groupSeparator):

    line = ''.join(str(e) for e in group)
    line = line.strip()
    if (len(line) > 1):

        if(line == "---"):
            qlist = []
            continue

        splitLine = line.split(";")
        if(len(splitLine) == colCount):
            qa = splitLine[0]
            req = splitLine[1]
            sent = splitLine[2]
            hasC = splitLine[3]
            setC = splitLine[4]
            act = splitLine[5]

            if(qa == "Q"):
                qlist += list(set(dt.TrainKeywords(sent, language)) - set(qlist))

            if(qa == "A"):
                requirementObjectList = []
                for r in req.split("|"):
                    if(len(r) > 2):
                        temp = r.split(":")

                        rName = temp[0]
                        if (temp[1][0:2] not in comparisonValues):
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

                # TODO
                followUpActionObject = None

                dt.TrainSentence(sent, language, qlist, requirementObjectList, hasCategoryList, setCategoryList, followUpActionObject)

print("--- %s seconds ---" % (time.time() - start_time))


# Resolving #############

from EmeraldAI.Logic.Modules import NLP
from EmeraldAI.Entities.Word import Word
from EmeraldAI.Logic.Thesaurus import *
from EmeraldAI.Logic.Modules import Parameterizer


thesaurus = Thesaurus()

def addToWordList(str_to_add, list_of_strings, language):
    str_to_add = NLP.Normalize(str_to_add, language)
    if str_to_add not in list_of_strings:
        list_of_strings.append(str_to_add)
    return list_of_strings

def append(parent, child):
    if child is not None:
        parent.append(child)

def processInput(data):
    language = NLP.DetectLanguage(data)
    wordSegments = NLP.WordSegmentation(data)
    cleanWordSegments = NLP.RemoveStopwords(wordSegments, language)

    wordList = []

    for word in wordSegments:
        w = Word(word, language)

        w.IsStopword = word not in cleanWordSegments
        if(w.IsStopword):
            w.Priority *= 0.5
        w.NormalizedWord = NLP.Normalize(word, language)

        append(w.ParameterList, Parameterizer.IsLastname(word))
        append(w.ParameterList, Parameterizer.IsFirstname(word))
        append(w.ParameterList, Parameterizer.IsName(word))
        append(w.ParameterList, Parameterizer.IsEquation(word)) # TODO - this needs to check more than one word
        append(w.ParameterList, Parameterizer.IsBotname(word))
        append(w.ParameterList, Parameterizer.IsWeekday(word, language))
        append(w.ParameterList, Parameterizer.IsLanguage(word, language))
        append(w.ParameterList, Parameterizer.IsCurseword(word, language))

        #if not w.IsStopword:
        w.SynonymList = addToWordList(word, w.SynonymList, language)
        synonyms = thesaurus.GetSynonyms(w.Word)
        for synonym in synonyms:
            if synonym[0]:
                w.SynonymList = addToWordList(synonym[0], w.SynonymList, language)
            else:
                w.SynonymList = addToWordList(synonym[1], w.SynonymList, language)
        w.SynonymList.remove(w.NormalizedWord)
        wordList.append(w)
        #print w.toJSON()
        print w.NormalizedWord
        print("--- %s seconds ---" % (time.time() - start_time))
    return wordList


class Sentence(object):
    ID = None
    Rating = 0
    KeywordList = []
    OnlyStopwords = True

    def __init__(self, ID, Rating, Keyword, IsStopword):
        self.ID = ID
        self.Rating = Rating
        self.KeywordList = [Keyword]
        self.OnlyStopwords = IsStopword

    def __repr__(self):
         return "R:{0} L:{1} S:{2}\n".format(self.Rating, len(self.KeywordList), self.OnlyStopwords)

    def __str__(self):
         return "R:{0} L:{1} S:{2}\n".format(self.Rating, len(self.KeywordList), self.OnlyStopwords)

    def AddKeyword(self, Rating, Keyword, IsStopword):
        self.Rating += Rating
        self.KeywordList.append(Keyword)
        if not self.OnlyStopwords:
            self.OnlyStopwords = IsStopword

    def AddPriority(self, Rating):
        self.Rating += Rating


__synonymFactor = 0.5
__stopwordFactor = 0.5

__parameterBonus = 5
__parameterButNoKeywordFactor = 0.2
__parameterOnlyStopwordThreshhold = 1.5

__RequirementBonus = 1

def GetSentencesByKeyword(sentenceList, word, language, isSynonym, isAdmin):
    query = """SELECT Conversation_Keyword.Stopword, Conversation_Sentence_Keyword.Priority,
            Conversation_Sentence_Keyword.SentenceID
            FROM Conversation_Keyword, Conversation_Sentence_Keyword, Conversation_Sentence
            WHERE Conversation_Keyword.ID = Conversation_Sentence_Keyword.KeywordID
            AND Conversation_Sentence_Keyword.SentenceID = Conversation_Sentence.ID
            AND Conversation_Sentence.Approved = {0}
            AND Conversation_Sentence.Disabled = {1}
            AND Conversation_Keyword.Normalized IN ({2}) AND Conversation_Keyword.Language = '{3}'"""
    sqlResult = db().Fetchall(query.format(isAdmin, '0', word, language))
    for r in sqlResult:
        stopwordNumber = 1
        isStopword = False
        if(r[0] == 1):
            stopwordNumber *= __stopwordFactor
            isStopword = True
        synonymNumber = 1
        if(isSynonym):
            synonymNumber *= __synonymFactor

        if r[2] in sentenceList:
            sentenceList[r[2]].AddKeyword((synonymNumber * stopwordNumber * r[1]), word, isStopword)
        else:
            sentenceList[r[2]] = Sentence(r[2], (synonymNumber * stopwordNumber * r[1]), word, isStopword)
    #print word, sentenceList
    return sentenceList

def GetSentencesByParameter(sentenceList, parameterList, language, isAdmin):
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

        stopword = "{{{0}}}".format(r[3])

        if r[2] in sentenceList:
            # if only stop-keywords present and threshhold reached
            if sentenceList[r[2]].OnlyStopwords and sentenceList[r[2]].Rating >= __parameterOnlyStopwordThreshhold:
                sentenceList[r[2]].AddKeyword((r[0] + __parameterBonus * __stopwordFactor * r[1]), stopword, True)

            # if there are normal keywords present
            if not sentenceList[r[2]].OnlyStopwords:
                sentenceList[r[2]].AddKeyword((r[0] + __parameterBonus * r[1]), stopword, True)
        # sentence not in list by now
        else:
            sentenceList[r[2]] = Sentence(r[2], (__parameterBonus * __parameterButNoKeywordFactor * r[1]), stopword, True)

    return sentenceList

def AddSentencePriority(sentenceList):
    query = """SELECT Priority FROM Conversation_Sentence WHERE ID = '{0}'"""
    for sentenceID, value in sentenceList.iteritems():
        sqlResult = db().Fetchall(query.format(sentenceID))
        for r in sqlResult:
            if not sentenceList[sentenceID].OnlyStopwords:
                sentenceList[sentenceID].AddPriority(r[0])
    return sentenceList


def CalculateRequirement(sentenceList, parameterList, delete=True):
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
                    sentenceList[sentenceID].AddPriority(__RequirementBonus)
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
                    sentenceList[sentenceID].AddPriority(__RequirementBonus)
                continue
    if delete:
        for d in deleteList:
            del sentenceList[d]

    return {'sentenceList':sentenceList, 'deleteList':deleteList}

def CalculateCategory():
    return None


def ResolveDialog(inputProcessed):

    sentenceList = {}
    parameterList = []
    # get all sentences related to the imput and rank
    for word in inputProcessed:
        wordList = "'" + "', '".join(word.SynonymList) + "'"

        isAdmin = 1

        sentenceList = GetSentencesByKeyword(sentenceList, wordList, word.Language, True, isAdmin)
        sentenceList = GetSentencesByKeyword(sentenceList, "'"+word.NormalizedWord+"'", word.Language, False, isAdmin)

        parameterList += list(set(word.ParameterList) - set(parameterList))

    print "Keyword:\t\t", sentenceList

    sentenceList = GetSentencesByParameter(sentenceList, parameterList, word.Language, isAdmin)

    print "Parameter:\t\t", sentenceList, "\t", parameterList

    sentenceList = AddSentencePriority(sentenceList)

    print "Sentence Priority:\t", sentenceList

    # TODO category + Priority

    parameterList = {}
    parameterList["User"] = "Max"
    parameterList["Time"] = "1000"#time.strftime("%H%M")
    parameterList["Day"] = "Monday"#time.strftime("%A")

    calculationResult = CalculateRequirement(sentenceList, parameterList)
    sentenceList = calculationResult["sentenceList"]

    print "Calculate Requirement:\t",sentenceList
    return GetHighestValue(sentenceList)


def GetHighestValue(dataList, margin=0):
    if dataList != None and len(dataList) > 0:
        highestRanking = max(node.Rating for node in dataList.values())
        if margin > 0:
            result = [node.ID for node in dataList.values() if node.Rating>=(highestRanking-margin)]
        else:
            result = [node.ID for node in dataList.values() if node.Rating==highestRanking]
        return result
    return None


import random


inputString = "Guten Abend Peter"
print inputString

# THIS SHOULD BE DONE BY THE PIPELINE BEFORE - NOT SPECIFIC TO RESPLVING THE COMMAND
inputWordList = processInput(inputString)
print("processInput() done --- %s seconds ---" % (time.time() - start_time))

dialogResult = ResolveDialog(inputWordList)
print("--- %s seconds ---" % (time.time() - start_time))

print dialogResult
print ""

if dialogResult != None and len(dialogResult) > 0:
    print random.choice(dialogResult)

print("--- %s seconds ---" % (time.time() - start_time))




inputString = "Guten abend, Wer war Freddy Mercury"
print inputString

# THIS SHOULD BE DONE BY THE PIPELINE BEFORE - NOT SPECIFIC TO RESPLVING THE COMMAND
inputWordList = processInput(inputString)
print("processInput() done --- %s seconds ---" % (time.time() - start_time))

dialogResult = ResolveDialog(inputWordList)
print("--- %s seconds ---" % (time.time() - start_time))

print dialogResult
print ""

if dialogResult != None and len(dialogResult) > 0:
    print random.choice(dialogResult)

print("--- %s seconds ---" % (time.time() - start_time))





inputString = "Was ist drei plus sieben?"
print inputString

# THIS SHOULD BE DONE BY THE PIPELINE BEFORE - NOT SPECIFIC TO RESPLVING THE COMMAND
inputWordList = processInput(inputString)
print("processInput() done --- %s seconds ---" % (time.time() - start_time))

dialogResult = ResolveDialog(inputWordList)
print("--- %s seconds ---" % (time.time() - start_time))

print dialogResult
print ""

if dialogResult != None and len(dialogResult) > 0:
    print random.choice(dialogResult)

print("--- %s seconds ---" % (time.time() - start_time))




# TODO: Keyword priority to rank parameter


