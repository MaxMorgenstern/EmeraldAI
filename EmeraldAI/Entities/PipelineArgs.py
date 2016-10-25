#!/usr/bin/python
# -*- coding: utf-8 -*-

class PipelineData(BaseObject):
    def __init__(self, input):
      self.Input = input

      self.Language = None
      self.WordList = None
      self.WordlistClean = None
      self.SynonymList = None

      self.Context = None
      self.User = None

      self.Answer = None
      self.AnswerFound = False

      self.Pattern = None
      self.PatternFound = False

      self.Error = None
