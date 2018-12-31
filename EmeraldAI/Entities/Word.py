#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.NLP import NLP
from EmeraldAI.Logic.NLP.Thesaurus import *
from EmeraldAI.Logic.NLP import Parameterizer


class Word(BaseObject):

    def __init__(self, input=None, language=None):
        self.UsedInSentence = False
        if input is None:
            return
    	# Word | Language of word
        self.Word = input
        if language is None:
            language = NLP.DetectLanguage(input)
        self.Language = language

        # Normalized version without special characters | is word a common word
        self.NormalizedWord = NLP.Normalize(self.Word, self.Language)

        self.IsStopword = NLP.IsStopword(self.Word, self.Language)

        self.SynonymList = []
        self.SynonymList = self.__addToWordList(self.NormalizedWord, self.SynonymList, self.Language)

        synonyms = Thesaurus().GetSynonyms(self.Word)
        for synonym in synonyms:
            if synonym[0]:
                self.SynonymList = self.__addToWordList(synonym[0], self.SynonymList, self.Language)
            elif synonym[1]:
                self.SynonymList = self.__addToWordList(synonym[1], self.SynonymList, self.Language)

        self.SynonymList.remove(self.NormalizedWord)

        # parameters matching the word
        self.ParameterList = self.__getParameter(self.Word, self.Language)

    def Equals(self, comparison):
        if comparison == self.Word:
            return True

        if NLP.Normalize(comparison, self.Language) == self.NormalizedWord:
            return True

        return False

    def __getParameter(self, word, language):
        tmpParameterList = []
        self.appendIfNotNone(tmpParameterList, Parameterizer.IsLastname(word))
        self.appendIfNotNone(tmpParameterList, Parameterizer.IsFirstname(word))
        self.appendIfNotNone(tmpParameterList, Parameterizer.IsName(word))
        self.appendIfNotNone(tmpParameterList, Parameterizer.IsBotname(word))
        self.appendIfNotNone(tmpParameterList, Parameterizer.IsWeekday(word, language))
        self.appendIfNotNone(tmpParameterList, Parameterizer.IsLanguage(word, language))
        self.appendIfNotNone(tmpParameterList, Parameterizer.IsCurseword(word, language))
        self.appendIfNotNone(tmpParameterList, Parameterizer.IsMathematical(word))
        return tmpParameterList

    def __addToWordList(self, str_to_add, list_of_strings, language):
        str_to_add = NLP.Normalize(str_to_add, language)
        if str_to_add not in list_of_strings:
            list_of_strings.append(str_to_add)
        return list_of_strings

    def __repr__(self):
         return "{0} ({1})".format(self.Word, len(self.SynonymList))

    def __str__(self):
         return "{0} ({1})".format(self.Word, len(self.SynonymList))
