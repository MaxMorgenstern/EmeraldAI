#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import aiml
from EmeraldAI.Logic.Global import Global

class AliceBot(object):
  kernel = None
  language = None

  brainPath = None
  AIMLPath = None

  _globalSessionID = "_global"

  def __init__(self, language):
    self.language = language
    self.kernel = aiml.Kernel()

    self.brainPath = Global().EmeraldPath + "Data/AIML/Brain/brain_" + language + ".brn"
    self.AIMLPath = Global().EmeraldPath + "Data/AIML/" + language.upper() + "/"

    if os.path.isfile(self.brainPath):
        self.kernel.bootstrap(self.brainPath)
    else:
        for root, dirs, filenames in os.walk(self.AIMLPath):
            for f in filenames:
                if(not f.startswith('.') and f.endswith('.aiml')):
                    self.kernel.bootstrap(learnFiles = self.AIMLPath + f)
    self.kernel.saveBrain(self.brainPath)

  def SetPredicate(self, name, value, sessionId = _globalSessionID):
    self.kernel.setPredicate(name, value, sessionId)

  def SetBotPredicate(self, name, value):
    self.kernel.setBotPredicate(name, value)

  def GetResponse(self, input, sessionId = _globalSessionID):
    if len(input) == 0:
      return ""
    return self.kernel.respond(input, sessionId)

  def SaveBrain(self, name, value):
    self.kernel.saveBrain(brainPath)
