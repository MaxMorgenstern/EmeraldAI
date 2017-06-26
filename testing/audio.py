#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import time

pygame.mixer.init()
a = pygame.mixer.music.load('/Users/maximilianporzelt/Google Drive/EmeraldAI/testing/test.mp3')
pygame.mixer.music.play()


print a.get_length()

while pygame.mixer.music.get_busy():
	time.sleep(1)

#pygame.mixer.music.stop()

#pygame.mixer.music.pause()
#pygame.mixer.music.unpause()



