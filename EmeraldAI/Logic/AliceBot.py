#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import aiml
from EmeraldAI.Logic.Global import Global

class AliceBot(object):
  kernel = None
  language = None

  def __init__(self, language):
    self.language = language
    self.kernel = aiml.Kernel()

    brainPath = Global().EmeraldPath + "Data/AIML/Brain/brain_" + language + ".brn"
    AIMLPath = Global().EmeraldPath + "Data/AIML/" + language.upper() + "/"

    if os.path.isfile(brainPath):
        self.kernel.bootstrap(brainPath)
    else:
        for root, dirs, filenames in os.walk(AIMLPath):
            for f in filenames:
                if(not f.startswith('.') and f.endswith('.aiml')):
                    self.kernel.bootstrap(learnFiles = AIMLPath + f)
    self.kernel.saveBrain(brainPath)
