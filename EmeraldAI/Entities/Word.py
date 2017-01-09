#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject


class Word(BaseObject):

    def __init__(self, input, language):
    	# Word | Language of word
        self.Word = input
        self.Language = language

        # Normalized version without special characters | is word a common word
        self.NormalizedWord = None
        self.IsStopword = False

        # priority | list of synonyms
        self.Priority = 1
        self.SynonymList = []

        # parameters mathing the word
        self.ParameterList = []
