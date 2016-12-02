#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.Modules import NLP

#from EmeraldAI.Logic.SpeechProcessing.Google import *
#from EmeraldAI.Logic.SpeechProcessing.Ivona import *
from EmeraldAI.Logic.AliceBot import *
from EmeraldAI.Logic.Thesaurus import *
from EmeraldAI.Logic.Modules.Database import SQlite3

from EmeraldAI.Entities.Word import Word

#google = Google()
#ivona = Ivona()
#alice = AliceBot("DE")

thesaurus = Thesaurus()
litedb = SQlite3.GetDB("brain")


def addToList(str_to_add, list_of_strings, language):
    str_to_add = NLP.Normalize(str_to_add, language)
    if str_to_add not in list_of_strings:
        list_of_strings.append(str_to_add)
    return list_of_strings


def processInputData(data):
    language = NLP.DetectLanguage(data)

    # hallöchen --> hall + öchen
    wordSegments = NLP.WordSegmentation(data)
    cleanWordSegments = NLP.RemoveStopwords(wordSegments, language)

    wordList = []

    for word in wordSegments:
        w = Word(word, language)

        # print word.lower() + " - " +  word.decode('utf8').title()

        w.IsStopword = word not in cleanWordSegments
        if(w.IsStopword):
            w.Priority *= 0.5
        w.NormalizedWord = NLP.Normalize(word, language)

        w.SynonymList = addToList(word, w.SynonymList, language)
        synonyms = thesaurus.GetSynonyms(w.Word)
        if(len(synonyms) == 0):
            synonyms = thesaurus.GetSynonyms(w.NormalizedWord, True)

        for synonym in synonyms:
            if synonym[0]:
                w.SynonymList = addToList(synonym[0], w.SynonymList, language)
            else:
                w.SynonymList = addToList(synonym[1], w.SynonymList, language)
        wordList.append(w)

        # print w.toJSON()
    return wordList

"""
#move
sql = "SELECT * FROM Dialog_Keyword, Dialog_Trigger WHERE Dialog_Keyword.Normalized_Keyword IN ({wordlist}) AND Dialog_Keyword.ID = Dialog_Trigger.Keyword_ID;"
finalsql = sql.format(wordlist = ','.join(['?']*len(synonymList)))
result = SQlite3.Fetchall(litedb, finalsql, synonymList)
print result
"""
# add result to global array initial priority
# if result already present decrease priority
# stopwords = decrease priority by 50%
# synonym = decrease priority by 50%
# stopword + synonym = decrease priority by 30%
# Dialog_Trigger.Priority

# get sentence with highest priority
# replace placeholder


# Input Processing
# Language Detection
# Sentence + Word Segmentation
# Word Tagging + Synonym detection
# strip stoppwords

# Input Analyzer
# Phrase Detection
# Pattern Detection
# Context Pipeline

# Response Processing
# Answer Pipeline
# Answer selection
# ELIZA fallback
# Customize Answer
# Train Conversation


# Get Input
# NLP
# Find Answer in DB
# Not Found Fallback to Eliza
# Found - Good
# Train DB


# Username
# User Data

# Timestamp
#

"""
INSERT OR IGNORE INTO Dialog_Keyword (Keyword, Normalized_Keyword, Stopword) VALUES ('', '')
INSERT OR IGNORE INTO Dialog_Keyword_Sentence (Keyword_ID, Sentence_ID) VALUES ('', '')
INSERT OR IGNORE INTO Dialog_Sentence (Sentence, Normalized_Sentence, Category, Language) VALUES ('', '', '', '')
INSERT OR IGNORE INTO Dialog_Trigger (Keyword_ID, Sentence_ID, Priority) VALUES ('', '')



SELECT * FROM Dialog_Keyword, Dialog_Trigger WHERE Normalized_Keyword = '' AND Dialog_Keyword.ID = Dialog_Trigger.Keyword_ID

"""

loop = True

while(loop):
  #inputData = google.Listen()
    inputData = raw_input("Enter Response: ")
    # print "We got: '{0}'".format(inputData)

    if(inputData.lower() == 'ende' or inputData.lower() == 'beenden'):
        loop = False
    elif(len(inputData) == 0):
        print "No Data found"
    else:
        #response = alice.GetResponse(inputData)
        response = processInputData(inputData)
        print "We respond: '{0}'".format(response)
        #audioPath = ivona.Speak(response)
        #os.system("afplay '{0}'".format(audioPath))
