#!/usr/bin/python
# -*- coding: utf-8 -*-

class Word(BaseObject):
  def __init__(self, input):
    self.Word = input
    self.Ranking = None
    self.IsStopWord = False

    self.SynonymList = None
