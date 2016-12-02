#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from EmeraldAI.Logic.Modules import Global


def ReadFile(foldername, filename):
    script_dir = Global.EmeraldPath + \
        "Data/{0}/{1}".format(foldername, filename)
    return [line.rstrip('\n').rstrip('\r') for line in open(script_dir)]


def DetectLanguage(input):
    # 207 most common words in germen + hallo = 208
    words_DE = ReadFile("Commonwords", "de.txt")

    # 207 most common words in english + hello = 208
    words_EN = ReadFile("Commonwords", "en.txt")

    exactMatch_DE = re.compile(r'\b%s\b' % '\\b|\\b'.join(
        words_DE), flags=re.IGNORECASE | re.UNICODE)
    count_DE = len(exactMatch_DE.findall(input))

    exactMatch_EN = re.compile(r'\b%s\b' % '\\b|\\b'.join(
        words_EN), flags=re.IGNORECASE | re.UNICODE)
    count_EN = len(exactMatch_EN.findall(input))

    if(count_EN > count_DE):
        return "en"
    return "de"


def WordSegmentation(input):
    segmentationRegex = re.compile(
        "[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\wÄÖÜäöüß\-]+", flags=re.UNICODE)
    return segmentationRegex.findall(input)


def RemoveStopwords(wordlist, language):
    stopwords = ReadFile("Stopwords", "{0}.txt".format(language.upper()))
    return [x for x in wordlist if x not in stopwords]


def Normalize(input, language):
    normalizedInput = input.lower()
    if(language .lower() == "de"):
        normalizedInput = normalizedInput.replace('ä', 'ae')
        normalizedInput = normalizedInput.replace('ü', 'ue')
        normalizedInput = normalizedInput.replace('ö', 'oe')
        normalizedInput = normalizedInput.replace('ß', 'ss')
    return normalizedInput
