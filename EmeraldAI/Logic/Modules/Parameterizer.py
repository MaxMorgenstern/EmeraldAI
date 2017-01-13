#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Modules import NLP
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.KnowledgeGathering.Math import Math

if(Config().Get("Database", "NLPDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "NLPDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

Empty = None

Firstname = "firstname"
Lastname = "lastname"
Name = "name"
Mathematical = "mathematical"
Equation = "equation"
Botname = "botname"

Weekday = "weekday"
Language = "language"
Curseword = "curseword"

#####

def IsFirstname(word):
    if(NLP.IsFirstname(word)):
        return Firstname
    return Empty

def IsLastname(word):
    if(NLP.IsLastname(word)):
        return Lastname
    return Empty

def IsName(word):
    if(NLP.IsFirstname(word) or NLP.IsLastname(word)):
        return Name
    return Empty

def IsMathematical(word):
    if(Math().IsMathematicalWord(word)):
        return Mathematical
    return Empty

def IsEquation(sentence):
    if(Math().IsEquation(sentence)):
        return Equation
    return Empty

def IsBotname(word):
    if (word.lower() == Config().Get("Bot", "Name").lower()):
        return Botname
    return Empty


# TODO
def IsTime(word):
    return "time"

def IsDate(word):
    return "date"

def IsLocation(word):
    return "location"



def IsWeekday(word, language):
    result = db().Fetchall("SELECT * FROM NLP_Words WHERE Type = 'weekday' AND Word='{0}' AND Language='{1}'".format(word.title(), language.lower()))
    if (len(result) > 0):
        return Weekday
    return Empty

def IsLanguage(word, language):
    result = db().Fetchall("SELECT * FROM NLP_Words WHERE Type = 'language' AND Word='{0}' AND Language='{1}'".format(word.title(), language.lower()))
    if (len(result) > 0):
        return Language
    return Empty

def IsCurseword(word, language):
    result = db().Fetchall("SELECT * FROM NLP_Words WHERE Type = 'curseword' AND Word='{0}' AND Language='{1}'".format(word.title(), language.lower()))
    if (len(result) > 0):
        return Curseword
    return Empty



