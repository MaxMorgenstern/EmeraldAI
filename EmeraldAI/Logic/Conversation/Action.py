#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
import importlib

class SentenceResolver(object):
    __metaclass__ = Singleton

    def CreateClass(self, moduleName, className):
        module = importlib.import_module(moduleName)
        MyClass = getattr(module, className)
        return MyClass()

    def CallMethod(self, moduleName, className, functionName):
        instance = self.CreateClass(moduleName, className)
        method = getattr(instance, functionName)
        return method()

    def CallFunction(self, moduleName, className, functionName, arg1, arg2=None, arg3=None):
        instance = self.CreateClass(moduleName, className)
        method = getattr(instance, functionName)

        if arg3 not None:
            return method(arg1, arg2, arg3)

        if arg2 not None:
            return method(arg1, arg2)

        return method(arg1)
