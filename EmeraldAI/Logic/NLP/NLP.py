#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Config.Config import *
if(Config().Get("Database", "NLPDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "NLPDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db


# This is just to distinguish between german and english
def DetectLanguage(input):
    # 207 most common words in germen + hallo = 208
    words_DE = Global.ReadDataFile("Commonwords", "de.txt")

    # 207 most common words in english + hello = 208
    words_EN = Global.ReadDataFile("Commonwords", "en.txt")

    exactMatch_DE = re.compile(r'\b%s\b' % '\\b|\\b'.join(
        words_DE), flags=re.IGNORECASE | re.UNICODE)
    count_DE = len(exactMatch_DE.findall(input))

    exactMatch_EN = re.compile(r'\b%s\b' % '\\b|\\b'.join(
        words_EN), flags=re.IGNORECASE | re.UNICODE)
    count_EN = len(exactMatch_EN.findall(input))

    if(count_EN > count_DE):
        return "en"
    return "de"


def WordSegmentation(input, extended=False):
    if input.startswith("TRIGGER_"):
        return [input]

    if not extended:
        segmentationRegex = re.compile(
            "[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\wÄÖÜäöüß\-]+", flags=re.UNICODE)
    else:
        segmentationRegex = re.compile(
            "[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\wÄÖÜäöüß\-\{\}]+", flags=re.UNICODE)

    return segmentationRegex.findall(input)

def GetStopwords(language):
    return Global.ReadDataFile("Stopwords", "{0}.txt".format(language.lower()))

def RemoveStopwords(wordlist, language):
    stopwords = GetStopwords(language)
    return [x for x in wordlist if x not in stopwords]

def IsStopword(word, language):
    stopwords = GetStopwords(language)
    return word in stopwords

def Normalize(input, language):
    normalizedInput = input.lower()
    if(language.lower() == "all" or language.lower() == "de"):
        normalizedInput = normalizedInput.replace('ä', 'ae')
        normalizedInput = normalizedInput.replace('ü', 'ue')
        normalizedInput = normalizedInput.replace('ö', 'oe')
        normalizedInput = normalizedInput.replace('ß', 'ss')
    return normalizedInput


def IsFirstname(input):
    normalizedInput = Normalize(input, "all")
    result = db().Fetchall("SELECT * FROM NLP_Firstname WHERE Firstname = '{0}'".format(normalizedInput.title()))
    return len(result) > 0

def IsLastname(input):
    normalizedInput = Normalize(input, "all")
    result = db().Fetchall("SELECT * FROM NLP_Lastname WHERE Lastname = '{0}'".format(normalizedInput.title()))
    return len(result) > 0

def TrimBasewords(PipelineArgs):
    inputString = PipelineArgs.Normalized
    sentence = PipelineArgs.SentenceList[PipelineArgs.ResponseID]
    for word in sentence.BasewordList:
        inputString = inputString.replace(word, "")
    return inputString.strip()

def TrimStopwords(input, language):
    stopwords = GetStopwords(language)
    inputwords = input.split()

    resultwords  = [word for word in inputwords if word.lower() not in stopwords]
    result = ' '.join(resultwords)
    return result
