#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Entities.Bot import Bot
from datetime import datetime
from EmeraldAI.Entities.User import User

# TODO

class NLPParameter(BaseObject):
    __metaclass__ = Singleton
    # This class is a singleton as we only need one instance across the whole project

    # Date of Object Creation and last Update
    Created = None
    Updated = None

    # List of all parameters used during NLP
    ParameterList = {}

    # Input and Result for actions
    ActionInput = None
    ActionResult = None

    def __init__(self):
        self.Created = datetime.now()
        self.Updated = datetime.now()

        self.ParameterList["User"] = "Unknown"
        self.ParameterList["Name"] = "Unknown"
        self.ParameterList["Time"] = datetime.now().strftime("%H%M")
        self.ParameterList["Day"] = datetime.today().strftime("%A")
        self.ParameterList["Category"] = "Greeting"

        # Add Bot Parameter
        self.ParameterList.update(Bot().toDict())


    def GetParameterList(self):
        self.ParameterList["Time"] = datetime.now().strftime("%H%M")
        self.ParameterList["Day"] = datetime.today().strftime("%A")

        # TODO - update user parameter
        self.ParameterList["Name"] = User().Name
        self.ParameterList["User"] = self.ParameterList["Name"]

        return self.ParameterList


    def UpdateParameter(self, key, value):
        self.ParameterList[key] = value
        self.Updated = datetime.now()

    def Reset(self):
        self.Created = datetime.now()
        self.Updated = datetime.now()

        self.ParameterList = {}
        self.ParameterList["User"] = "Unknown"
        self.ParameterList["Name"] = "Unknown"

        self.Input = None
        self.Result = None

    def SetInput(self, inputString):
        self.ActionInput = inputString
        self.ParameterList["Input"] = inputString
        self.Updated = datetime.now()

    def SetResult(self, result):
        self.ActionResult = result
        self.ParameterList["Result"] = result
        self.Updated = datetime.now()
