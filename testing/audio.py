#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
import pygame
import time

pygame.mixer.init()
a = pygame.mixer.music.load('/Users/maximilianporzelt/Google Drive/EmeraldAI/testing/test.mp3')
pygame.mixer.music.play()


print a.get_length()

while pygame.mixer.music.get_busy():
	time.sleep(1)
"""

#pygame.mixer.music.stop()

#pygame.mixer.music.pause()
#pygame.mixer.music.unpause()


import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')


from EmeraldAI.Logic.Audio.SoundMixer import *


filename = '/Users/maximilianporzelt/Google Drive/EmeraldAI/testing/test.mp3'

sm = SoundMixer()
sm.Play(filename)

while sm.IsPlaying():
	time.sleep(1)

print "end"
