#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.SpeechProcessing.Google import *
from EmeraldAI.Logic.KnowledgeGathering.Math import *

google = Google()
m = Math()

loop = True

print m.Calculate("10 + 25")
print m.Calculate("1.000 + 25")
print m.Calculate("100 000 + 25")
print m.Calculate("10,5 / 25")


while(loop):
    data = google.Listen()
    print "We got: '{0}'".format(data)

    if(data.lower() == 'ende' or data.lower() == 'beenden'):
        loop = False
    elif(len(data) == 0):
        print "No data found"
    else:
    	print m.Calculate(data)

