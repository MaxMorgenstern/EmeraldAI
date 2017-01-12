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

#print m.Calculate("10 + 25")
#print m.Calculate("1.000 + 25")
#print m.Calculate("100 000 + 25")
#print m.Calculate("10,5 / 25")


print m.IsEquation("Wieviel ist drei plus sieben")	# T
print m.IsEquation("Wieviel ist 3 plus 7")	# T
print m.IsEquation("Wieviel ist drei und sieben")
print m.IsEquation("Wer sind die Rolling Stones")
print m.IsEquation("Was ist 30")
print m.IsEquation("Was ist 3 + 10")	# T
print m.IsEquation("Ich male gerne")
print m.IsEquation("Jetzt pluster dich nicht so auf")
print m.IsEquation("64 geteilt durch 8") # T

print "-----"
exit(1)

while(loop):
    data = google.Listen()
    print "We got: '{0}'".format(data)

    if(data.lower() == 'ende' or data.lower() == 'beenden'):
        loop = False
    elif(len(data) == 0):
        print "No data found"
    else:
    	print m.Calculate(data)

