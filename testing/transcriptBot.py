#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.SpeechProcessing.Google import *

google = Google()

loop = True

f = open('transcript.txt','w')

def printfile(file, quantifyer, text):
    file.write("{0} {1}\n".format(quantifyer, text))

print "Transcript Bot has been started"

while(loop):
    data = google.Listen()
    if(len(data) > 0):
        print "We got: '{0}'".format(data)
        printfile(f, datetime.datetime.now(), data)
        if(data.lower() == 'ende' or data.lower() == 'beenden'):
            loop = False

f.close()