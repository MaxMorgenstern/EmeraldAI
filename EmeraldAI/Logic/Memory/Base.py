#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Config.Config import *
if(Config().Get("Database", "ConversationDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "ConversationDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

class Base(object):

    def __init__(self, parentID):
        self.ParentID = parentID


    def Has(self, key, parentID = None):
        if(parentID is None):
            parentID = self.ParentID

        query = """SELECT Value FROM Memory WHERE ParentID = '{0}' AND lower(Key) = '{1}'"""
        sqlResult = db().FetchallCacheBreaker(query.format(parentID, key.lower()))
        for r in sqlResult:
            return True
        return False


    def Get(self, key, parentID = None):
        if(parentID is None):
            parentID = self.ParentID

        query = """SELECT Value FROM Memory WHERE ParentID = '{0}' AND lower(Key) = '{1}'"""
        sqlResult = db().FetchallCacheBreaker(query.format(parentID, key.lower()))
        for r in sqlResult:
            return r[0]

        return None

    def GetString(self, key, parentID = None):
        return str(self.Get(key, parentID))

    def GetInt(self, key, parentID = None):
        return int(float(self.Get(key, parentID)))

    def GetFloat(self, key, parentID = None):
        return float(self.Get(key, parentID))

    def GetBoolean(self, key, parentID = None):
        val = self.Get(key, parentID)
        return val.lower() in ['true', '1']


    def Set(self, key, value, parentID = None):
        if(parentID is None):
            parentID = self.ParentID

        query = """SELECT ID FROM Memory WHERE ParentID = '{0}' AND lower(Key) = '{1}'"""
        sqlResult = db().FetchallCacheBreaker(query.format(parentID, key.lower()))

        storedId = -1
        for r in sqlResult:
            storedId = r[0]

        if(storedId > 1):
            query = "UPDATE Memory SET Key = '{1}', Value = '{2}', ParentID = '{3}' WHERE ID = {0}".format(storedId, key, value, parentID)
        else:
            query = "INSERT INTO Memory (Key, Value, ParentID) VALUES ('{0}', '{1}', '{2}')".format(key, value, parentID)

        return db().Execute(query)
