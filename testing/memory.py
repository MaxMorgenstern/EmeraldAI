#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')
import time

from EmeraldAI.Logic.Memory.Brain import Brain as BrainMemory

BrainMemory().Set("CancelSTT", "False")
if (BrainMemory().GetBoolean("CancelSTT")):
	print "True"


BrainMemory().Set("CancelSTT", "True")
if (BrainMemory().GetBoolean("CancelSTT")):
	print "True"


BrainMemory().Set("TEST_Time", time.time())
if (BrainMemory().GetFloat("TEST_Time") <= time.time()):
	print BrainMemory().GetFloat("TEST_Time"), time.time()

