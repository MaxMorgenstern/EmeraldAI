#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Modules import NLP
from EmeraldAI.Entities.Word import Word
from EmeraldAI.Logic.Thesaurus import *
from EmeraldAI.Logic.Modules import Parameterizer
from EmeraldAI.Logic.Singleton import Singleton


class ProcessInput(object):
    __metaclass__ = Singleton

    def __addToWordList(self, str_to_add, list_of_strings, language):
        str_to_add = NLP.Normalize(str_to_add, language)
        if str_to_add not in list_of_strings:
            list_of_strings.append(str_to_add)
        return list_of_strings

    def __appendIfNotNone(self, parent, child):
        if child is not None:
            parent.append(child)


    def Process(self, PipelineArgs):

        PipelineArgs.Language = NLP.DetectLanguage(PipelineArgs.Input)

        wordSegments = NLP.WordSegmentation(PipelineArgs.Input)
        cleanWordSegments = NLP.RemoveStopwords(wordSegments, PipelineArgs.Language)

        wordList = []
        parameterList = []

        for word in wordSegments:
            w = Word(word, PipelineArgs.Language)

            w.IsStopword = word not in cleanWordSegments
            w.NormalizedWord = NLP.Normalize(word, PipelineArgs.Language)

            self.__appendIfNotNone(w.ParameterList, Parameterizer.IsLastname(word))
            self.__appendIfNotNone(w.ParameterList, Parameterizer.IsFirstname(word))
            self.__appendIfNotNone(w.ParameterList, Parameterizer.IsName(word))
            self.__appendIfNotNone(w.ParameterList, Parameterizer.IsBotname(word))
            self.__appendIfNotNone(w.ParameterList, Parameterizer.IsWeekday(word, PipelineArgs.Language))
            self.__appendIfNotNone(w.ParameterList, Parameterizer.IsLanguage(word, PipelineArgs.Language))
            self.__appendIfNotNone(w.ParameterList, Parameterizer.IsCurseword(word, PipelineArgs.Language))

            # TODO - more than one word has to be equation
            self.__appendIfNotNone(w.ParameterList, Parameterizer.IsEquation(word))
            parameterList += list(set(w.ParameterList) - set(parameterList))

            w.SynonymList = self.__addToWordList(w.NormalizedWord, w.SynonymList, PipelineArgs.Language)
            synonyms = Thesaurus().GetSynonyms(w.Word)
            for synonym in synonyms:
                if synonym[0]:
                    w.SynonymList = self.__addToWordList(synonym[0], w.SynonymList, PipelineArgs.Language)
                else:
                    w.SynonymList = self.__addToWordList(synonym[1], w.SynonymList, PipelineArgs.Language)
            w.SynonymList.remove(w.NormalizedWord)

            wordList.append(w)

        PipelineArgs.WordList = wordList
        PipelineArgs.ParameterList = parameterList

        return PipelineArgs
