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
#A;Time:gt1700;Guten Abend {name}.;Greeting;;"""

comparisonValues = ["lt", "gt", "le", "eq", "ge"]

qlist = []
for key, group in itertools.groupby(data, __groupSeparator):

    line = ''.join(str(e) for e in group)
    line = line.strip()
    if (len(line) > 1):
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

            if(qa == ""):
                qlist = []

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

        w.SynonymList = addToWordList(word, w.SynonymList, language)

        synonyms = thesaurus.GetSynonyms(w.Word)

        append(w.ParameterList, Parameterizer.IsLastname(word))
        append(w.ParameterList, Parameterizer.IsFirstname(word))
        append(w.ParameterList, Parameterizer.IsName(word))
        append(w.ParameterList, Parameterizer.IsEquation(word))
        append(w.ParameterList, Parameterizer.IsBotname(word))
        append(w.ParameterList, Parameterizer.IsWeekday(word, language))
        append(w.ParameterList, Parameterizer.IsLanguage(word, language))
        append(w.ParameterList, Parameterizer.IsCurseword(word, language))

        for synonym in synonyms:
            if synonym[0]:
                w.SynonymList = addToWordList(synonym[0], w.SynonymList, language)
            else:
                w.SynonymList = addToWordList(synonym[1], w.SynonymList, language)
        wordList.append(w)
        print w.toJSON()
        print("--- %s seconds ---" % (time.time() - start_time))
    return wordList


__synonymFactor = 0.5
__stopwordFactor = 0.5
__RequirementBonus = 1

def ResolveDialog(inputProcessed):

    sentenceList = {}
    # get all sentences related to the imput and rank
    for word in inputProcessed:
        wordList = "'" + "', '".join(word.SynonymList) + "'"

        query = """SELECT Conversation_Keyword.Stopword, Conversation_Sentence_Keyword.Priority, Conversation_Sentence_Keyword.SentenceID
            FROM Conversation_Keyword, Conversation_Sentence_Keyword, Conversation_Sentence
            WHERE Conversation_Keyword.ID = Conversation_Sentence_Keyword.KeywordID
            AND Conversation_Sentence_Keyword.KeywordID = Conversation_Sentence.ID
            AND Conversation_Sentence.Approved = {0}
            AND Conversation_Sentence.Disabled = {1}
            AND Conversation_Keyword.Normalized IN ({2}) AND Conversation_Keyword.Language = '{3}'"""

        query = """SELECT Conversation_Keyword.Stopword, Conversation_Sentence_Keyword.Priority, Conversation_Sentence_Keyword.SentenceID
            FROM Conversation_Keyword, Conversation_Sentence_Keyword
            WHERE Conversation_Keyword.ID = Conversation_Sentence_Keyword.KeywordID
            AND Conversation_Keyword.Normalized IN ({0}) AND Conversation_Keyword.Language = '{1}'
            """
        # Get all Synonyms
        sqlResult = db().Fetchall(query.format(wordList, word.Language))
        for r in sqlResult:
            stopwordNumer = 1
            if(r[0] == 1):
                stopwordNumer *= __stopwordFactor

            if r[2] in sentenceList:
                sentenceList[r[2]] += (__synonymFactor * stopwordNumer * r[1])
            else:
                sentenceList[r[2]] = (__synonymFactor * stopwordNumer * r[1])


        # Get actual word
        sqlResult = db().Fetchall(query.format("'"+word.NormalizedWord+"'", word.Language))
        for r in sqlResult:
            stopwordNumer = 1
            if(r[0] == 1):
                stopwordNumer *= __stopwordFactor

            if r[2] in sentenceList:
                sentenceList[r[2]] += (stopwordNumer * r[1])
            else:
                sentenceList[r[2]] = (stopwordNumer * r[1])

        # r[1] == Priority of keyword-sentence relation

    print sentenceList

    User = "Max"
    Time = time.strftime("%H%M")
    Day = time.strftime("%A")

    print User, Time, Day
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
            if r[2] == "User" and r[1] != User:
                deleteList.append(sentenceID)
                break
            if r[2] == "User" and r[1] == User:
                sentenceList[sentenceID] += __RequirementBonus
                break

            if r[2] == "Time":
                if r[0] == "lt" and not Time < r[1]:
                    deleteList.append(sentenceID)
                if r[0] == "le" and not Time <= r[1]:
                    deleteList.append(sentenceID)
                if r[0] == "eq" and not Time == r[1]:
                    deleteList.append(sentenceID)
                if r[0] == "ge" and not Time >= r[1]:
                    deleteList.append(sentenceID)
                if r[0] == "gt" and not Time > r[1]:
                    deleteList.append(sentenceID)
                else:
                    sentenceList[sentenceID] += __RequirementBonus
                break

            if r[2] == "Day" and r[1] != Day:
                deleteList.append(sentenceID)
                break
            if r[2] == "Day" and r[1] == Day:
                sentenceList[sentenceID] += __RequirementBonus
                break

    print sentenceList
    for d in deleteList:
        del sentenceList[d]
    print sentenceList

    highestRanking = max(sentenceList.values())
    result = [key for key in sentenceList if sentenceList[key]==highestRanking]
    return result

inputString = "Guten Morgen"
print inputString

# THIS SHOULD BE DONE BY THE PIPELINE BEFORE - NOT SPECIFIC TO RESPLVING THE COMMAND
inputWordList = processInput(inputString)
print("processInput() done --- %s seconds ---" % (time.time() - start_time))

dialogResult = ResolveDialog(inputWordList)
print("--- %s seconds ---" % (time.time() - start_time))

print dialogResult
print ""

import random
print random.choice(dialogResult)


print("--- %s seconds ---" % (time.time() - start_time))

