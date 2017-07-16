#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.ComputerVision.ModelMonitor import ModelMonitor
from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Logic.Logger import *


def EnsureModelUpdate():
    moduleList = Config().GetList("ComputerVision", "Modules")

    for moduleName in moduleList:
        if(ModelMonitor().CompareHash(moduleName, ModelMonitor().GetStoredHash(moduleName))):
            continue
        FileLogger().Info("CV Model Rebuilder: Rebuild {0} Model".format(moduleName))
        ModelMonitor().Rebuild(moduleName)


##### MAIN #####

if __name__ == "__main__":
    if(Pid.HasPid("CVModelRebuilder")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("CVModelRebuilder")
    try:
    	EnsureModelUpdate()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("CVModelRebuilder")
