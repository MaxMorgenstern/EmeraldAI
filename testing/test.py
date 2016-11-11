#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.SpeechProcessing.Google import *
from EmeraldAI.Logic.SpeechProcessing.Ivona import *
from EmeraldAI.Logic.AliceBot import *

google = Google()
ivona = Ivona()
alice = AliceBot("DE")

loop = True

while(loop):
  data = google.Listen()
  print "We got: '{0}'".format(data)

  if(data.lower() == 'ende' or data.lower() == 'beenden'):
  	loop = False
  elif(len(data) == 0):
    print "No data found"
  else:
    response = alice.GetResponse(data)
    print "We respond: '{0}'".format(response)
    ivona.Speak(response)



"""
pip install SpeechRecognition
pip install gTTS
pip install aiml
"""
