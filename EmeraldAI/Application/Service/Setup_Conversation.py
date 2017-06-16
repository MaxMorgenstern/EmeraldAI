#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs

from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Logic.Modules import Excel
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Trainer.DialogTrainer import *

def read(filename):
    return codecs.open(filename, encoding='utf-8').read()

language = Config().Get("DEFAULT", "Language")
print "Start conversation setup for language {0}...".format(language.upper())

# Convert Excel File To CSV
xslPath = os.path.join(Global.EmeraldPath, "Data", "TrainingData", "{0}_Training.xlsx".format(language.upper()))
csvPath = os.path.join(Global.EmeraldPath, "Data", "TrainingData", "Training.csv")
Excel.ToCsv(xslPath, csvPath)

data = read(csvPath)

print "Train Basic sentences..."

trainer = DialogTrainer()
trainer.TrainCSV(data, language)

print "Conversation setup completed"
