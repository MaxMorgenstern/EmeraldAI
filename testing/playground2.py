#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Config.Config import *

male =  Config().Get("DEFAULT", "FormalFormOfAddressMale")
female = Config().Get("DEFAULT", "FormalFormOfAddressFemale")

print male.format("Porzelt")
print female.format("Porzelt")



from EmeraldAI.Logic.Logger import *

LogTwo = Logger("FileLogger")

LogTwo.Info("Hallo, Welt!")
LogTwo.Debug("Hallo, Welt!")
LogTwo.Error("Hallo, Welt!")
LogTwo.Critical("Hallo, Welt!")




FileLog = FileLogger()

FileLog.Info("Hallo, du tolle Welt!")
FileLog.Debug("Hallo, du tolle Welt!")
FileLog.Error("Hallo, du tolle Welt!")
FileLog.Critical("Hallo, du tolle Welt!")


ConsoleLogger = ConsoleLogger()

ConsoleLogger.Info("Hallo, -console- du tolle Welt!")
ConsoleLogger.Debug("Hallo, -console- du tolle Welt!")
ConsoleLogger.Error("Hallo, -console- du tolle Welt!")
ConsoleLogger.Critical("Hallo, -console- du tolle Welt!")


BaseLogger = BaseLogger()

BaseLogger.Info("Hallo, -base- du tolle Welt!")
BaseLogger.Debug("Hallo, -base- du tolle Welt!")
BaseLogger.Error("Hallo, -base- du tolle Welt!")
BaseLogger.Critical("Hallo, -base- du tolle Welt!")
