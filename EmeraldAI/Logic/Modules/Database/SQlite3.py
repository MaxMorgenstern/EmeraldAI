#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as lite
from EmeraldAI.Logic.Modules import Global

def GetDB(database):
  con = lite.connect(Global.EmeraldPath + 'Data/SqliteDB/' + database.rstrip(".sqlite") + ".sqlite")
  con.text_factory = str
  return con


def Execute(db, sql, args=None):
  cur = db.cursor()
  if args:
    cur.execute(sql, args)
  else:
    cur.execute(sql)
  db.commit()
  return cur


def Fetchall(db, sql, args=None):
  cur = db.cursor()
  if args:
    cur.execute(sql, args)
  else:
    cur.execute(sql)
  rows = cur.fetchall()
  return rows


def Disconnect(db):
  db.commit()
  db.close()
