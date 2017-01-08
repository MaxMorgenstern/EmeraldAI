#!/usr/bin/python
# -*- coding: utf-8 -*-

from EmeraldAI.Logic.Modules import NLP
from EmeraldAI.Entities.Word import Word
from EmeraldAI.Logic.Thesaurus import *
from EmeraldAI.Logic.Modules import Parameterizer

#################
#
# TODO
#
#################

def __addToList(str_to_add, list_of_strings, language):
    str_to_add = NLP.Normalize(str_to_add, language)
    if str_to_add not in list_of_strings:
        list_of_strings.append(str_to_add)
    return list_of_strings

def __append(parent, child):
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

        w.NormalizedWord = NLP.Normalize(word, language)

        # TODO: really?
        w.SynonymList = __addToList(word, w.SynonymList, language)

        synonyms = thesaurus.GetSynonyms(w.Word)

        __append(w.ParameterList, Parameterizer.IsLastname(word))
        __append(w.ParameterList, Parameterizer.IsFirstname(word))
        __append(w.ParameterList, Parameterizer.IsName(word))
        __append(w.ParameterList, Parameterizer.IsEquation(word))
        __append(w.ParameterList, Parameterizer.IsBotname(word))
        __append(w.ParameterList, Parameterizer.IsWeekday(word, language))
        __append(w.ParameterList, Parameterizer.IsLanguage(word, language))
        __append(w.ParameterList, Parameterizer.IsCurseword(word, language))

        for synonym in synonyms:
            if synonym[0]:
                w.SynonymList = __addToList(synonym[0], w.SynonymList, language)
            else:
                w.SynonymList = __addToList(synonym[1], w.SynonymList, language)
        wordList.append(w)
    return wordList
