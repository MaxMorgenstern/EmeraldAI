#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Modules import NLP
from EmeraldAI.Config.Config import *

if(Config().Get("Database", "NLPDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "NLPDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db


# Trainer for dialogs


