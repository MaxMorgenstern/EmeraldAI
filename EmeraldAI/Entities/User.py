#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Singleton import Singleton
from datetime import datetime

# TODO

class User(BaseObject):
    __metaclass__ = Singleton
    # This class is a singleton as we only need one instance across the whole project, the currently active user

    CVTag = None

    Name = "Unknown"
    LastName = None
    FirstName = None

    Gender = "Male"
    Birthday = None

    LastSeen = None
    LastSpokenTo = None

    Properties = []

    Formal = True
    Trainer = False
    Admin = False

    Updated = None

    def GetCVTag(self):
        return self.CVTag

    def SetUserByCVTag(self, cvTag, deepProcess=True):
        if cvTag == None:
            return

        self.CVTag = cvTag
        if not deepProcess:
            return

        # TODO - get details from DB
        self.Name = cvTag

        self.Updated = datetime.now().strftime("%H%M")
        #######

    def GetName(self):
        return self.Name

    def SetUserByName(self, name, deepProcess=True):
        if name == None:
            return

        self.Name = name

        if not deepProcess:
            return

        # TODO - get details from DB
        self.Name = cvTag

        self.Updated = datetime.now().strftime("%H%M")
        #######
