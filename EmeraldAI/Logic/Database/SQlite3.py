#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as lite
from cachetools import cached
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Config.Config import *

class SQlite3(object):
    __metaclass__ = Singleton

    __Database = None

    def __init__(self):
        self.__Database = self.GetDB(Config().Get("Database", "SQliteDatabase"))

    def GetDB(self, database):
        con = lite.connect(Global.EmeraldPath + "Data" + os.sep + "SqliteDB" + os.sep +
                           database.rstrip(".sqlite") + ".sqlite")
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
        except lite.IntegrityError:
            return None

    @cached(cache={})
    def Fetchall(self, sql, args=None):
        return self.FetchallDB(self.__Database, sql, args)

    def FetchallDB(self, db, sql, args=None):
        cur = db.cursor()
        if args:
            cur.execute(sql, args)
        else:
            cur.execute(sql)
        rows = cur.fetchall()
        return rows


    def Disconnect(self):
        self.DisconnectDB(self.__Database)

    def DisconnectDB(self, db):
        db.commit()
        db.close()
