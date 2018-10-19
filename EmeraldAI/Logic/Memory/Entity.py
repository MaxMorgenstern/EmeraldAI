#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import *
if(Config().Get("Database", "ConversationDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "ConversationDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

from EmeraldAI.Logic.Memory.Base import Base

class Entity(Base):
    __metaclass__ = Singleton

    def __init__(self):
        query = """SELECT ID FROM Memory WHERE ParentID = '1' AND Key = 'Entity'"""
        sqlResult = db().Fetchall(query)
        parentID = -1
        for r in sqlResult:
            parentID = r[0]
        Base.__init__(self, parentID)
