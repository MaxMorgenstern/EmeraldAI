#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from EmeraldAI.Logic.Global import Global

class AliceBot(object):
  kernel = None
  brainPath = None
  AIMLPath = None
  brainFile = None
  language = None

  def __init__(self, language):
  	self.language = language
    self.kernel = aiml.Kernel()
    self.brainPath = Global().EmeraldPath + "Data/AIML/Brain/brain_" + language + ".brn"
    self.AIMLPath = Global().EmeraldPath + "Data/AIML/" + language.upper() + "/"

    if os.path.isfile(self.brainPath):
        self.kernel.bootstrap(self.brainFile = self.brainPath)
    else:
        for root, dirs, filenames in os.walk(self.AIMLPath):
            for f in filenames:
                if(not f.startswith('.') and f.endswith('.aiml')):
                    self.kernel.bootstrap(learnFiles = self.AIMLPath + f)
    self.kernel.saveBrain(self.brainPath)
