#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.NLP import NLP
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Singleton import Singleton

if(Config().Get("Database", "ConversationDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "ConversationDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

# TODO - include at dialog trainer

class CommandTrainer(object):
    __metaclass__ = Singleton

    def TrainPattern(self, Name, Pattern, Language, Module, Class, Function):
        wordSegments = NLP.WordSegmentation(Pattern, True)

        query = "SELECT ID FROM Command_Module WHERE Module = '{0}' AND Class = '{1}' AND Function = '{2}'".format(Module, Class, Function)
        result = db().Fetchall(query)
        if (len(result) > 0):
            ModuleID = result[0][0]
        else:
            query = "INSERT INTO Command_Module ('Module', 'Class', 'Function') Values ('{0}', '{1}', '{2}')".format(Module, Class, Function)
            ModuleID = db().Execute(query)

        query = "INSERT INTO Command_Pattern ('Name', 'Pattern', 'Language', 'KeywordLength', 'ModuleID') Values ('{0}', '{1}', '{2}', '{3}', '{4}')".format(Name, Pattern, Language, len(wordSegments), ModuleID)
        PatternID = db().Execute(query)
        if(PatternID == None):
            #query = "SELECT ID FROM Command_Pattern WHERE Pattern = '{0}'".format(Pattern)
            #PatternID = db().Fetchall(query)[0][0]
            print "Pattern already exists! '{0}'".format(Pattern)
            return False

        for word in wordSegments:
            query = "INSERT INTO Command_Keyword ('Keyword', 'Normalized', 'Language') Values ('{0}', '{1}', '{2}')".format(word, NLP.Normalize(word, Language), Language)
            KeywordID = db().Execute(query)
            if(KeywordID == None):
                query = "SELECT ID FROM Command_Keyword WHERE Keyword = '{0}'".format(word)
                KeywordID = db().Fetchall(query)[0][0]

            query = "INSERT INTO Command_Pattern_Keyword ('PatternID', 'KeywordID') Values ('{0}', '{1}')".format(PatternID, KeywordID)
            db().Execute(query)

        print "New pattern created: '{0}'".format(Pattern)
        return True

# OBSOLETE!
