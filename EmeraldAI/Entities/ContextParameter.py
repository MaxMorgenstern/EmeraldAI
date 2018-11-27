#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Entities.Bot import Bot
from datetime import datetime
from EmeraldAI.Entities.User import User

# TODO - rename to something like context parameter

class ContextParameter(BaseObject):
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

        self.__UpdateTime()
        self.ParameterDictionary["Category"] = "Greeting"

        # Add Bot Parameter
        self.ParameterDictionary.update(Bot().toDict("Bot"))
        # Add User Parameter
        self.__UpdateUser()

        self.History = [] # list of historical pipeline args

    def __UpdateUser(self):
        user = User().LoadObject()
        self.ParameterDictionary.update(user.toDict("User"))
        self.ParameterDictionary["Name"] = user.GetName()
        self.ParameterDictionary["User"] = self.ParameterDictionary["Name"]
        userType = "User"
        if(user.Trainer):
            userType = "Trainer"
        if(user.Admin):
            userType = "Admin"
        self.ParameterDictionary["Usertype"] = userType

    def __UpdateTime(self):
        self.ParameterDictionary["Time"] = datetime.now().strftime("%H%M")
        self.ParameterDictionary["Day"] = datetime.today().strftime("%A")


    def GetParameterDictionary(self):
        self.__UpdateTime()

        # Update Bot Parameter
        self.ParameterDictionary.update(Bot().toDict("Bot"))
        # Update User Parameter
        self.__UpdateUser()

        return self.ParameterDictionary

    def UpdateParameter(self, key, value):
        self.ParameterDictionary[key] = value
        self.Updated = datetime.now()


    def Reset(self):
        self.Created = datetime.now()
        self.Updated = datetime.now()

        self.__UpdateTime()

        self.ParameterDictionary = {}

        # Add Bot Parameter
        self.ParameterDictionary.update(Bot().toDict("Bot"))
        # Add User Parameter
        self.__UpdateUser()

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

    def AppendHistory(self, data):
        self.History.append(data)
