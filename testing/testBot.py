#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.SpeechProcessing.Google import *
from EmeraldAI.Logic.SpeechProcessing.Ivona import *
from EmeraldAI.Logic.NLP.AliceBot import *

google = Google()
ivona = Ivona()
alice = AliceBot("DE")

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
        response = alice.GetResponse(data)
        print "We respond: '{0}'".format(response)
        audioPath = ivona.Speak(response)
        print "Playing file: '{0}'".format(audioPath)
        print audioPlayer.format(audioPath)
        #os.system(audioPlayer.format(audioPath).replace('/', '\\'))
        os.system(audioPlayer.format(audioPath))


"""
pip install PyAudio
pip install SpeechRecognition
pip install gTTS
pip install aiml
"""
