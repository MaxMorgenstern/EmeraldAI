#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')


from EmeraldAI.Logic.SpeechProcessing.Microsoft import *

from EmeraldAI.Logic.Audio.SoundMixer import *

m = Microsoft()

filename = m.Speak("Hallo Welt! Ich bin keine Synthetische Stimme. Sondern ein Baum")
print filename

sm = SoundMixer()
sm.Play(filename)

while sm.IsPlaying():
	time.sleep(1)

print "end"
