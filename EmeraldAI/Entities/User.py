#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Singleton import Singleton
from datetime import datetime

from EmeraldAI.Config.Config import *
if(Config().Get("Database", "UserDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "UserDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

class User(BaseObject):
    __metaclass__ = Singleton
    # This class is a singleton as we only need one instance across the whole project, the currently active user

    def __init__(self):
        self.CVTag = "Unknown"

        self.Name = "Unknown"
        self.LastName = None
        self.FirstName = None

        self.Birthday = None
        self.LastSeen = None
        self.LastSpokenTo = None

        self.Gender = "male"

        self.Properties = []

        self.Formal = True
        self.Trainer = False
        self.Admin = False

        self.Updated = None

    def GetCVTag(self):
        return self.CVTag

    def GetName(self):
        if self.Formal and self.LastName:
            if self.Gender.lower() == "female":
                nameWrapper =  Config().Get("DEFAULT", "FormalFormOfAddressFemale")
            else:
                nameWrapper = Config().Get("DEFAULT", "FormalFormOfAddressMale")
            return nameWrapper.format(self.LastName)

        elif not self.Name and self.FirstName:
            return self.FirstName
        elif self.Name:
            return self.Name
        return None

    def SetUserByCVTag(self, cvTag, deepProcess=True):
        if cvTag == None or self.CVTag == cvTag:
            return

        self.CVTag = cvTag
        if not deepProcess:
            return

        self.__setUser("SELECT * FROM Person WHERE CVTag = '{0}'", cvTag)

    def SetUserByName(self, name, deepProcess=True):
        if name == None or self.Name == name:
            return

        self.Name = name
        if not deepProcess:
            return

        self.__setUser("SELECT * FROM Person WHERE Name = '{0}'", name)

    def __setUser(self, query, name):
        sqlResult = db().Fetchall(query.format(name))
        for r in sqlResult:
            self.Name = r[1]
            self.LastName = r[2]
            self.FirstName = r[3]

            self.Birthday = r[5]
            self.LastSeen = r[6]
            self.LastSpokenTo = r[7]
            self.Gender = r[8]

            self.Formal = r[9].lower() == "formal"
            self.Trainer = r[10] == 1
            self.Admin = r[11] == 1
            continue

        self.Updated = datetime.now().strftime("%H%M")

    def __repr__(self):
         return "Name:{0}".format(self.GetName())

    def __str__(self):
         return "Name:{0}".format(self.GetName())
