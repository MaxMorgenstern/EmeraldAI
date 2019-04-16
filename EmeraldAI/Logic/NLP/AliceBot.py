#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import aiml
from EmeraldAI.Logic.Modules import Global


class AliceBot(object):
    kernel = None
    language = None

    __brainPath = None
    __AIMLPath = None

    __globalSessionID = "_global"

    def __init__(self, language):
        self.language = language
        self.kernel = aiml.Kernel()

        self.__brainPath = os.path.join(Global.EmeraldPath, "Data", "AIML", "Brain", ("brain_" + language + ".brn"))
        self.__AIMLPath = os.path.join(Global.EmeraldPath, "Data", "AIML", language.upper())

        if os.path.isfile(self.__brainPath):
            self.kernel.bootstrap(self.__brainPath)
        else:
            for _, _, filenames in os.walk(self.__AIMLPath):
                for f in filenames:
                    if(not f.startswith('.') and f.endswith('.aiml')):
                        self.kernel.bootstrap(learnFiles=os.path.join(self.__AIMLPath, f))
        self.kernel.saveBrain(self.__brainPath)

    def SetPredicate(self, name, value, sessionId=__globalSessionID):
        self.kernel.setPredicate(name, value, sessionId)

    def SetBotPredicate(self, name, value):
        self.kernel.setBotPredicate(name, value)

    def GetResponse(self, input, sessionId=__globalSessionID):
        if len(input) == 0:
            return ""
        return self.kernel.respond(input, sessionId)

    def SaveBrain(self, name, value):
        self.kernel.saveBrain(self.__brainPath)

    def GetSessionData(self, name):
        self.kernel.getSessionData(name)
