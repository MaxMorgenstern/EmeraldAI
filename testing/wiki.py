#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.KnowledgeGathering.Wikipedia import *

w = Wikipedia()

summary = w.GetSummary("angela merkel", True)
print summary

print "-----"

summary = w.GetSummary("Angela Merkel", True)
print summary

print "-----"

summary = w.GetSummary("singen")
print summary

print "-----"

summary = w.GetSummary("singen", True)
print summary

print "-----"

summary = w.GetSummary("Maximilian Porzelt", True)
print summary
