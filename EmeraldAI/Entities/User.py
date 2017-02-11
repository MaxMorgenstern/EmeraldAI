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

    CVTag = None

    Name = "Unknown"
    LastName = None
    FirstName = None

    Birthday = None
    LastSeen = None
    LastSpokenTo = None

    Gender = "male"

    Properties = []

    Formal = True
    Trainer = False
    Admin = False

    Updated = None

    def GetCVTag(self):
        return self.CVTag

    def GetName(self):
        if self.Formal:
            if self.Gender.lower() == "female":
                nameWrapper =  Config().Get("DEFAULT", "FormalFormOfAddressFemale")
            else:
                nameWrapper = Config().Get("DEFAULT", "FormalFormOfAddressMale")
            return nameWrapper.format(self.LastName)

        if not self.Name:
            return self.FirstName
        return self.Name

    def SetUserByCVTag(self, cvTag, deepProcess=True):
        if cvTag == None or self.CVTag == cvTag:
            return

        self.CVTag = cvTag
        if not deepProcess:
            return

        self.__setUser("SELECT * FROM Person WHERE CVTag = '{0}'")

    def SetUserByName(self, name, deepProcess=True):
        if name == None or self.Name == name:
            return

        self.Name = name
        if not deepProcess:
            return

        self.__setUser("SELECT * FROM Person WHERE Name = '{0}'")

    def __setUser(self, query):
        sqlResult = db().Fetchall(query.format(name))
        for r in sqlResult:
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
