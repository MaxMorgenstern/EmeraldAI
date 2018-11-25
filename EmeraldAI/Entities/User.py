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
        self.CVTag = Config().Get("DEFAULT", "UnknownUserTag")

        self.DBID = -1
        self.Name = Config().Get("DEFAULT", "UnknownUserTag")
        self.LastName = None
        self.FirstName = None

        self.Birthday = None
        self.LastSeenPrevious = None
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

    def SetUserByCVTag(self, cvTag):
        if cvTag is None or self.CVTag == cvTag:
            return

        self.CVTag = cvTag
        self.__setUser("SELECT * FROM Person WHERE CVTag = '{0}'", cvTag)

    def SetUserByName(self, name):
        if name is None or self.Name == name:
            return

        self.Name = name
        self.__setUser("SELECT * FROM Person WHERE Name = '{0}'", name)

    def UpdateSpokenTo(self):
        self.LastSpokenTo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def UpdateSeen(self):
        self.LastSeen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def Reset(self):
        self.CVTag = Config().Get("DEFAULT", "UnknownUserTag")

        self.DBID = -1
        self.Name = Config().Get("DEFAULT", "UnknownUserTag")
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

    def Create(self):
        query = "TODO"
        db().Execute(query)

    def Update(self):
        if self.DBID < 1:
            return
        query = "UPDATE Person SET Name='{0}', LastName='{1}', FirstName='{2}', Birthday='{3}', LastSeen='{4}', LastSpokenTo='{5}', Gender='{6}' WHERE ID = '{7}'"
        db().Execute(query.format(self.Name, self.LastName, self.FirstName, self.Birthday, self.LastSeen, self.LastSpokenTo, self.Gender, self.DBID))
        self.SaveObject()

    def __setUser(self, query, name):
        sqlResult = db().Fetchall(query.format(name))
        for r in sqlResult:
            self.DBID = r[0]
            self.Name = r[1]
            self.LastName = r[2]
            self.FirstName = r[3]

            self.Birthday = r[5]
            self.LastSeenPrevious = r[6]
            self.LastSeen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.LastSpokenTo = r[7]
            self.Gender = r[8]

            self.Formal = r[9].lower() == "formal"
            self.Trainer = r[10] == 1
            self.Admin = r[11] == 1
            self.Update()
            continue

        self.Updated = datetime.now().strftime("%H%M")

    def __repr__(self):
         return "Name:{0}".format(self.GetName())

    def __str__(self):
         return "Name:{0}".format(self.GetName())
