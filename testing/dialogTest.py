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

import random

from EmeraldAI.Pipelines.InputProcessing.ProcessInput import ProcessInput
from EmeraldAI.Entities.PipelineArgs import PipelineArgs
from EmeraldAI.Logic.Conversation.SentenceResolver import SentenceResolver



def ResolveDialog(inputProcessed):

    sentenceList = {}
    parameterList = []
    # get all sentences related to the imput and rank
    for word in inputProcessed:
        wordList = "'" + "', '".join(word.SynonymList) + "'"

        isAdmin = 1

        sentenceList = SentenceResolver().GetSentencesByKeyword(sentenceList, wordList, word.Language, True, isAdmin)
        sentenceList = SentenceResolver().GetSentencesByKeyword(sentenceList, "'"+word.NormalizedWord+"'", word.Language, False, isAdmin)

        parameterList += list(set(word.ParameterList) - set(parameterList))
    print "Keyword:\t\t", sentenceList

    sentenceList = SentenceResolver().GetSentencesByParameter(sentenceList, parameterList, word.Language, isAdmin)
    print "Parameter:\t\t", sentenceList, "\t", parameterList

    parameterList = {}
    parameterList["User"] = "Max"
    parameterList["Time"] = time.strftime("%H%M")
    parameterList["Day"] = time.strftime("%A")
    parameterList["Category"] = "Greeting"

    calculationResult = SentenceResolver().CalculateRequirement(sentenceList, parameterList)
    sentenceList = calculationResult["sentenceList"]
    print "Calculate Requirement:\t", sentenceList


    sentenceList = SentenceResolver().AddSentencePriority(sentenceList)
    print "Sentence Priority:\t", sentenceList

    sentenceList = SentenceResolver().CalculateCategory(sentenceList, parameterList["Category"])
    print "Calculate Category:\t", sentenceList

    return GetHighestValue(sentenceList)


# TODO - also pass the whole node / sentence object
def GetHighestValue(dataList, margin=0):
    if dataList != None and len(dataList) > 0:
        highestRanking = max(node.Rating for node in dataList.values())
        if margin > 0:
            result = [node.ID for node in dataList.values() if node.Rating>=(highestRanking-margin)]
        else:
            result = [node.ID for node in dataList.values() if node.Rating==highestRanking]
        return result
    return None

def doWork(inputString):
    print inputString
    pa = PipelineArgs(inputString)

    # THIS SHOULD BE DONE BY THE PIPELINE BEFORE - NOT SPECIFIC TO RESPLVING THE COMMAND
    pa = ProcessInput().Process(pa)
    print("processInput() done --- %s seconds ---" % (time.time() - start_time))

    dialogResult = ResolveDialog(pa.WordList)
    print("--- %s seconds ---" % (time.time() - start_time))

    print dialogResult
    print ""

    if dialogResult != None and len(dialogResult) > 0:
        print random.choice(dialogResult)

    print("--- %s seconds ---" % (time.time() - start_time))




doWork("Guten Abend Peter")

doWork("Guten abend, Wer war Freddy Mercury")

doWork("Was ist drei plus sieben?")





