#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject

class Word(BaseObject):

	def __init__(self, input, language):
		self.Word = input
		self.Language = language

		self.NormalizedWord = None
		self.IsStopword = False

		self.Ranking = 0
		self.SynonymList = []
