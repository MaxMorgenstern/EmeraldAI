#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as lite
from cachetools import cached
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Logger import *

class SQlite3(object):
    __metaclass__ = Singleton

    __Database = None

    def __init__(self):
        self.__Database = self.GetDB(Config().Get("Database", "SQliteDatabase"))

    def GetDB(self, database):
        con = lite.connect(os.path.join(Global.EmeraldPath, "Data", "SqliteDB", database.rstrip(".sqlite") + ".sqlite"), check_same_thread=False)
        con.text_factory = str
        return con

    @cached(cache={})
    def Execute(self, sql, args=None):
        return self.ExecuteDB(self.__Database, sql, args)

    def ExecuteDB(self, db, sql, args=None):
        try:
            cur = db.cursor()
            if args:
                cur.execute(sql, args)
            else:
                cur.execute(sql)
            db.commit()
            return cur.lastrowid
        except lite.IntegrityError as e:
            if(not e.lower().startswith("unique")):
                FileLogger().Error("SQlite3 Line 37: IntegrityError: {0}".format(e))
            return None
        except lite.OperationalError as e:
            FileLogger().Error("SQlite3 Line 40: OperationError: {0}".format(e))
            return None

    @cached(cache={})
    def Fetchall(self, sql, args=None):
        return self.FetchallDB(self.__Database, sql, args)

    def FetchallCacheBreaker(self, sql, args=None):
        return self.FetchallDB(self.__Database, sql, args)

    def FetchallDB(self, db, sql, args=None):
        try:
            cur = db.cursor()
            if args:
                cur.execute(sql, args)
            else:
                cur.execute(sql)
            rows = cur.fetchall()
        except Exception as e:
            FileLogger().Error("SQlite3 Line 59: {0}".format(e))
            return []
        return rows


    def Disconnect(self):
        self.DisconnectDB(self.__Database)

    def DisconnectDB(self, db):
        db.commit()
        db.close()
