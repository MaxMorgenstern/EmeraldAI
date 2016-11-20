#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject

class Word(BaseObject):
	def __init__(self, input):
		self.Word = input
		self.NormalizedWord = None

		self.IsStopWord = False

		self.Ranking = None
		self.SynonymList = None
