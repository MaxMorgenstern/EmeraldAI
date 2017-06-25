#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.SpeechProcessing.Google import *

for i, microphone_name in enumerate(sr.Microphone().list_microphone_names()):
    print microphone_name


google = Google()

loop = True

#f = open('transcript_{0}.txt'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')),'w')

#def printfile(file, quantifyer, text):
#    file.write("{0} {1}\n".format(quantifyer, text))

print "Transcript Bot has been started"

while(loop):
    data = google.ListenAsync()
    if(len(data) > 0):
        print "We got: '{0}'".format(data)
        #printfile(f, datetime.datetime.now(), data)
        if(data.lower() == 'ende' or data.lower() == 'beenden'):
            loop = False


#f.close()
