#!/usr/bin/python
# -*- coding: utf-8 -*-
import mysql.connector

def GetDB(database, user="root", passwd=None, host="127.0.0.1"):
  return mysql.connector.connect(user=user, password=passwd, host=host,database=database)


def Execute(db, sql):
  cur = db.cursor()
  cur.execute(sql)
  return cur


def Fetchall(db, sql, index=None):
  result = []
  for row in execute(db, sql).fetchall():
    if index is not None:
      row = row[index]
    result.append(row)
  return result
