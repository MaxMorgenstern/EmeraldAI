#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Entities.Bot import Bot
from datetime import datetime
from EmeraldAI.Entities.User import User

class NLPParameter(BaseObject):
    __metaclass__ = Singleton
    # This class is a singleton as we only need one instance across the whole project

    # Date of Object Creation and last Update
    Created = None
    Updated = None

    # List of all parameters used during NLP
    ParameterDictionary = {}

    # Input and Result for actions
    ActionInput = None
    ActionResult = None

    def __init__(self):
        self.Created = datetime.now()
        self.Updated = datetime.now()

        self.ParameterDictionary["Time"] = datetime.now().strftime("%H%M")
        self.ParameterDictionary["Day"] = datetime.today().strftime("%A")
        self.ParameterDictionary["Category"] = "Greeting"

        # Add Bot Parameter
        self.ParameterDictionary.update(Bot().toDict("Bot"))
        # Add User Parameter
        self.ParameterDictionary.update(User().toDict("User"))
        self.ParameterDictionary["Name"] = "Unknown"
        self.ParameterDictionary["User"] = "Unknown"
        self.ParameterDictionary["Usertype"] = "User"


    def GetParameterDictionary(self):
        self.ParameterDictionary["Time"] = datetime.now().strftime("%H%M")
        self.ParameterDictionary["Day"] = datetime.today().strftime("%A")

        # Update Bot Parameter
        self.ParameterDictionary.update(Bot().toDict("Bot"))
        # Update User Parameter
        self.ParameterDictionary.update(User().toDict("User"))
        self.ParameterDictionary["Name"] = User().GetName()
        self.ParameterDictionary["User"] = self.ParameterDictionary["Name"]
        userType = "User"
        if(User().Trainer):
            userType = "Trainer"
        if(User().Admin):
            userType = "Admin"
        self.ParameterDictionary["Usertype"] = userType
        return self.ParameterDictionary


    def UpdateParameter(self, key, value):
        self.ParameterDictionary[key] = value
        self.Updated = datetime.now()


    def Reset(self):
        self.Created = datetime.now()
        self.Updated = datetime.now()

        self.ParameterDictionary = {}

        # Add Bot Parameter
        self.ParameterDictionary.update(Bot().toDict("Bot"))
        # Add User Parameter
        self.ParameterDictionary.update(User().toDict("User"))
        self.ParameterDictionary["Name"] = "Unknown"
        self.ParameterDictionary["User"] = "Unknown"

        self.Input = None
        self.Result = None

        self.ActionInput = None
        self.ActionResult = None


    def SetInput(self, inputString):
        self.ActionInput = inputString
        self.ParameterDictionary["Input"] = inputString
        self.Updated = datetime.now()

    def SetResult(self, result):
        self.ActionResult = result
        self.ParameterDictionary["Result"] = result
        self.Updated = datetime.now()

    def UnsetInputAndResult(self):
        self.ActionInput = None
        if "Input" in self.ParameterDictionary:
            del self.ParameterDictionary["Input"]
        self.ActionResult = None
        if "Result" in self.ParameterDictionary:
            self.ParameterDictionary.pop("Result")
        self.Updated = datetime.now()
