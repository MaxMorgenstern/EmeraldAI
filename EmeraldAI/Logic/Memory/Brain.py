from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import *
if(Config().Get("Database", "ConversationDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "ConversationDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

class SentenceResolver(object):
    __metaclass__ = Singleton

    def __init__(self):
        query = """SELECT ID FROM Memory WHERE ParentID = '1' AND Key = 'Brain'"""
        sqlResult = db().Fetchall(query.format(self.ParentID, key))
        for r in sqlResult:
            self.ParentID = r[0]

    def Get(self, key):
        query = """SELECT Value FROM Memory WHERE ParentID = '{0}' AND Key = '{1}'"""
        sqlResult = db().Fetchall(query.format(self.ParentID, key))
        for r in sqlResult:
            return r[0]
        return None

    def Set(self, key, value, parentID = None):
        if(parentID == None):
            parentID = self.ParentID

        query = """SELECT ID FROM Memory WHERE ParentID = '{0}' AND Key = '{1}'"""
        sqlResult = db().Fetchall(query.format(parentID, key))

        storedId = -1
        for r in sqlResult:
            storedId = r[0]

        if(storedId > 1):
            query = "UPDATE Memory SET Key = '{1}', Value = '{2}', ParentID = '{3}' WHERE ID = {0}".format(storedId, key, value, parentID)
        else:
            query = "INSERT INTO Memory (Key, Value, ParentID) VALUES ('{0}', '{1}', '{2}')".format(key, value, parentID)

        return db().Execute(query)
