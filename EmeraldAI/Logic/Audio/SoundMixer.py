#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from EmeraldAI.Logic.Singleton import Singleton
try:
    import mutagen.mp3
    isMutagenPresent = True
except ImportError:
    isMutagenPresent = False

class SoundMixer():
    __metaclass__ = Singleton

    def __init__(self):
        pygame.mixer.init()

    def Play(self, filename):
        if (filename is None):
            return
        if(self.IsPlaying()):
            self.Stop()

        if isMutagenPresent:
            pygame.mixer.quit()
            mp3 = mutagen.mp3.MP3(filename)
            pygame.mixer.init(frequency=mp3.info.sample_rate)

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
