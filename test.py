#!/usr/bin/python
# -*- coding: utf-8 -*-

from EmeraldAI.Entities.Word import *
from EmeraldAI.Logic.Global import *
from EmeraldAI.Logic.NLP import *
from EmeraldAI.Config.Config import *

from EmeraldAI.Logic.Logger import *


x = Word("hi")

print x.toJSON()


print Global().RootPath

print Global().EmeraldPath


print NLP().DetectLanguage("Hallo, dies ist ein nötiger Test!")

print Config().Get("Server", "Username")
print Config().Get("Server", "Password")
print Config().Get("Server", "Debug")



LogTwo = Logger("ConsoleLogger")

LogTwo.Info("Hallo, Welt!")
LogTwo.Debug("Hallo, Welt!")
LogTwo.Error("Hallo, Welt!")
LogTwo.Critical("Hallo, Welt!")

