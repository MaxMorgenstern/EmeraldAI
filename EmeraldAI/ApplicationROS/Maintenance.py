#!/usr/bin/python
# -*- coding: utf-8 -*-

print "TODO"

"""
Check for new version

Rebuild Person and Mood CV models

"""


"""
from EmeraldAI.Logic.ComputerVision.ModelMonitor import ModelMonitor


def EnsureModelUpdate():
    monitor = ModelMonitor()
    predictionModules = Config().GetList("ComputerVision", "Modules")

    for moduleName in predictionModules:
        if(monitor.CompareHash(moduleName, monitor.GetStoredHash(moduleName))):
            print "Model '{0}' up to date".format(moduleName)
            continue
        print "Rebuild Model '{0}'...".format(moduleName)
        monitor.Rebuild(moduleName)
"""
