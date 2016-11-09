#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
from EmeraldAI.Entities.Word import *
from EmeraldAI.Logic.Global import *
from EmeraldAI.Logic.NLP import *
from EmeraldAI.Config.Config import *



x = Word("hi")

print x.toJSON()


print Global().RootPath

print Global().EmeraldPath


print NLP().DetectLanguage("Hallo, dies ist ein nötiger Test!")

print Config().Get("Server", "Username")
print Config().Get("Server", "Password")
print Config().Get("Server", "Debug")


"""

from EmeraldAI.Logic.Logger import *
LogTwo = Logger("FileLogger")

LogTwo.Info("Hallo, Welt!")
LogTwo.Debug("Hallo, Welt!")
LogTwo.Error("Hallo, Welt!")
LogTwo.Critical("Hallo, Welt!")


#from EmeraldAI.Logic.AliceBot import *


#AliceDE = AliceBot("DE")


from EmeraldAI.Logic.SpeechProcessing.Google import *
from EmeraldAI.Logic.SpeechProcessing.Microsoft import *

g = Google()
g.Speak("Frau Maus, ich singe dir ein Lied: pv zk pv pv zk pv zk kz zk pv pv pv zk pv zk zk pzk pzk pvzkpkzvpvzk kkkkkk bsch")
g.Speak("Hallo Welt!")

print "-----"

m = Microsoft()
m.Speak("Frau Maus, ich singe dir ein Lied: pv zk pv pv zk pv zk kz zk pv pv pv zk pv zk zk pzk pzk pvzkpkzvpvzk kkkkkk bsch")
m.Speak("Hallo Welt!")
