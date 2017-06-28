#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from EmeraldAI.Logic.Singleton import Singleton

class SoundMixer():
    __metaclass__ = Singleton

    def __init__(self):
        pygame.mixer.init()

    def Play(self, filename):
        if(self.IsPlaying()):
            self.Stop()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    def Stop(self):
        pygame.mixer.music.stop()

    def Pause(self):
        pygame.mixer.music.pause()

    def Unpause(self):
        pygame.mixer.music.unpause()

    def IsPlaying(self):
        return pygame.mixer.music.get_busy()

    def Mute(self):
        pygame.mixer.music.set_volume(0)

    def UnMute(self):
        pygame.mixer.music.set_volume(1)
