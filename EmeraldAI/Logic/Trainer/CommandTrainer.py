#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Modules import NLP
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Singleton import Singleton

if(Config().Get("Database", "NLPDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "NLPDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db

class CommandTrainer(object):
    __metaclass__ = Singleton

    def TrainPattern(self, Name, Pattern, Language, Module, Class, Function):

        wordSegments = NLP.WordSegmentation(Pattern, True)


        # TODO: Remove Command_Pattern_Module Table - this is a 1:n relation


        query = "INSERT INTO Command_Pattern ('Name', 'Pattern', 'Language', 'KeywordLength') Values ('{0}', '{1}', '{2}', '{3}')".format(Name, Pattern, Language, len(wordSegments))
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

        query = "INSERT INTO Command_Module ('Module', 'Class', 'Function') Values ('{0}', '{1}', '{2}')".format(Module, Class, Function)
        ModuleID = db().Execute(query)

        query = "INSERT INTO Command_Pattern_Module ('PatternID', 'ModuleID') Values ('{0}', '{1}')".format(PatternID, ModuleID)
        db().Execute(query)


        print "New Pattern '{0}'".format(Pattern)
        return True

