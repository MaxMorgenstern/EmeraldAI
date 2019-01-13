#!/usr/bin/python
# -*- coding: utf-8 -*-
import mysql.connector
from cachetools import cached
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import Config


class MySQL(object):
    __metaclass__ = Singleton

    __Database = None

    def __init__(self):
        config = Config()
        database = config.Get("Database", "MySQLDatabase")
        password = config.Get("Database", "MySQLPassword")
        host = config.Get("Database", "MySQLHost")
        self.__Database = self.GetDB(database, password, host)

    def GetDB(self, database, user="root", passwd=None, host="127.0.0.1"):
        return mysql.connector.connect(user=user, password=passwd, host=host, database=database)

    @cached(cache={})
    def Execute(self, sql):
        return self.ExecuteDB(self.__Database, sql)

    def ExecuteDB(self, db, sql):
        cur = db.cursor()
        cur.execute(sql)
        return cur

    @cached(cache={})
    def Fetchall(self, sql, index=None):
        return self.FetchallDB(self.__Database, sql, index)

    def FetchallCacheBreaker(self, sql, index=None):
        return self.FetchallDB(self.__Database, sql, index)

    def FetchallDB(self, db, sql, index=None):
        result = []
        for row in self.ExecuteDB(db, sql).fetchall():
            if index is not None:
                row = row[index]
            result.append(row)
        return result


    def Disconnect(self):
        self.DisconnectDB(self.__Database)

    def DisconnectDB(self, db):
        db.close()
