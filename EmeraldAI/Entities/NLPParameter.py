#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Singleton import Singleton
import datetime

# TODO

class NLPParameter(BaseObject):
    __metaclass__ = Singleton
    # This class is a singleton as we only need one instance across the whole project

    # Date of Object Creation and last Update
    Created = None
    Updated = None

    # List of all parameters used during NLP
    ParameterList = []

    # Input and Result for actions
    Input = None
    Result = None

    __init__(self):
        self.Created = datetime.now()
        self.Updated = datetime.now()


    def UpdateParameter(self, key, value):
        self.ParameterList[key] = value
        self.Updated = datetime.now()


    def Reset(self):
        self.Created = datetime.now()
        self.Updated = datetime.now()

        self.ParameterList = []
        self.Input = None
        self.Result = None

    def SetInput(self, input):
        self.Input = input
        self.ParameterList["input"] = input
        self.Updated = datetime.now()

    def SetResult(self, result):
        self.Result = result
        self.ParameterList["result"] = result
        self.Updated = datetime.now()
