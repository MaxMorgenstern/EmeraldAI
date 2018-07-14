#!/usr/bin/python
# -*- coding: utf-8 -*-
import speech_recognition as sr
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Logger import *


class Wit(object):
    __metaclass__ = Singleton

    __apiKey = None

    def __init__(self):
        microphoneID = None
        microphoneName = Config().Get("SpeechToText", "Microphone")
        for i, microphone_name in enumerate(sr.Microphone().list_microphone_names()):
            if microphone_name == microphoneName:
                microphoneID = i

        if microphoneID is None:
            FileLogger().Error("Wit Line 22: No microphone found - Exit")
            raise Exception("Wit: No microphone found - Exit")
            return

        self.__recognizer = sr.Recognizer()
        self.__microphone = sr.Microphone(device_index=microphoneID)

        with self.__microphone as source:
            self.__recognizer.dynamic_energy_threshold = True
            self.__recognizer.adjust_for_ambient_noise(source)

        self.__apiKey = Config().Get("TextToSpeech", "WitAPIKey")
        if(len(self.__apiKey) == 0):
            self.__apiKey = None


    def Listen(self):
        with self.__microphone as source:
            self.__audio = self.__recognizer.listen(source)

            data = ""
            try:
                data = self.__recognizer.recognize_wit(
                    self.__audio, key=self.__apiKey, language=self.__language_4letter_cc, show_all=False)
            except sr.UnknownValueError as e:
                FileLogger().Warn("Wit.ai Line 47: Could not understand audio: {0}".format(e))
            except sr.RequestError as e:
                FileLogger().Warn("Wit.ai Line 49: Could not request results from Wit.ai service: {0}".format(e))

            return data

    def GetAvailiabeMicrophones(self):
        return sr.Microphone().list_microphone_names()
