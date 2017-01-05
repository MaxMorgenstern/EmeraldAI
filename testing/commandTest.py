#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

import time

# Training #############
from EmeraldAI.Logic.Trainer.CommandTrainer import *

start_time = time.time()

ct = CommandTrainer()
ct.TrainPattern("Name", "Wieviel ist {equation}", "de", "ModuleX", "ClassX", "FunctionX")
ct.TrainPattern("Name", "Wer ist {name}", "de", "ModuleY", "ClassY", "FunctionY")
ct.TrainPattern("Name", "Wie macht man Butter", "de", "ModuleZ", "ClassZ", "FunctionZ")
ct.TrainPattern("Name", "Wieviel Cent ist ein Euro wert", "de", "ModuleA", "ClassA", "FunctionA")


print("--- %s seconds ---" % (time.time() - start_time))




# Resolving #############
from collections import Counter

from EmeraldAI.Logic.Modules import NLP
from EmeraldAI.Entities.Word import Word
from EmeraldAI.Logic.Thesaurus import *
from EmeraldAI.Logic.Modules import Parameterizer

if(Config().Get("Database", "NLPDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "NLPDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

start_time = time.time()

thesaurus = Thesaurus()

def addToList(str_to_add, list_of_strings, language):
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

        w.SynonymList = addToList(word, w.SynonymList, language)

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
                w.SynonymList = addToList(synonym[0], w.SynonymList, language)
            else:
                w.SynonymList = addToList(synonym[1], w.SynonymList, language)
        wordList.append(w)
        print("--- %s seconds ---" % (time.time() - start_time))
    return wordList



def ResolveCommand(inputProcessed):
    patternList = []
    parameterList = []
    for word in inputProcessed:
        wordList = "'" + "', '".join(word.SynonymList) + "'"

        parameterList += list(set(word.ParameterList) - set(parameterList))

        query = """SELECT distinct(Command_Pattern_Keyword.PatternID)
            FROM Command_Keyword, Command_Pattern_Keyword
            WHERE Normalized in ({0})
            AND Command_Keyword.ID = Command_Pattern_Keyword.KeywordID
            """.format(wordList)
        sqlResult = db().Fetchall(query)
        for r in sqlResult:
            patternList.append(r[0])

    query = """SELECT distinct(Command_Pattern_Keyword.PatternID)
        FROM Command_Keyword, Command_Pattern_Keyword
        WHERE Normalized in ({0})
        AND Command_Keyword.ID = Command_Pattern_Keyword.KeywordID
        """.format("'{" + "}', '{".join(parameterList) + "}'")
    sqlResult = db().Fetchall(query)
    for r in sqlResult:
        patternList.append(r[0])

    patternDict = dict(Counter(patternList))
    print patternDict
    moduleToCall = None
    for key, value in patternDict.iteritems():
        query = """SELECT Command_Module.Module, Command_Module.Class, Command_Module.Function
            FROM Command_Pattern, Command_Pattern_Module, Command_Module
            WHERE Command_Pattern.ID = {0}
            ANd Command_Pattern.KeywordLength = {1}
            AND Command_Pattern.ID = Command_Pattern_Module.PatternID
            AND Command_Pattern_Module.ModuleID = Command_Module.ID
            """.format(key, value)
        sqlResult = db().Fetchall(query)
        for re in sqlResult:
            moduleToCall = re
            break

    return moduleToCall




inputString = "Günther, Wieviel ergibt 56 plus 87"
print inputString

inputWordList = processInput(inputString)
print("--- %s seconds ---" % (time.time() - start_time))

commandResult = ResolveCommand(inputWordList)
print("--- %s seconds ---" % (time.time() - start_time))

print commandResult
print ""





inputString = "Wer ist Albert Einstein"
print inputString

inputWordList = processInput(inputString)
print("--- %s seconds ---" % (time.time() - start_time))

commandResult = ResolveCommand(inputWordList)
print("--- %s seconds ---" % (time.time() - start_time))

print commandResult

