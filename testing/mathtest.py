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

audioPlayer = Config().Get("TextToSpeech", "AudioPlayer") + " '{0}'"

while(loop):
    data = google.Listen()
    print "We got: '{0}'".format(data)

    if(data.lower() == 'ende' or data.lower() == 'beenden'):
        loop = False
    elif(len(data) == 0):
        print "No data found"
    else:
    	print m.Calculate(data)
