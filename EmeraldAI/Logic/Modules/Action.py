#!/usr/bin/python
# -*- coding: utf-8 -*-
import importlib
from EmeraldAI.Logic.Logger import *

def CreateClass(moduleName, className):
    module = importlib.import_module(moduleName)
    MyClass = getattr(module, className)
    return MyClass()

def CallMethod(moduleName, className, functionName):
    instance = CreateClass(moduleName, className)
    method = getattr(instance, functionName)
    return method()

def CallFunction(moduleName, className, functionName, arg1=None, arg2=None, arg3=None):
    ileLogger().Info("Action called: {0}, {1}, {2}".format(moduleName, className, functionName))
    instance = CreateClass(moduleName, className)
    method = getattr(instance, functionName)

    if arg3 != None:
        return method(arg1, arg2, arg3)

    if arg2 != None:
        return method(arg1, arg2)

    if arg1 != None:
        return method(arg1)

    return method()
