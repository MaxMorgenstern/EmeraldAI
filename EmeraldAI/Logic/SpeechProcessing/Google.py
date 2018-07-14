#!/usr/bin/python
# -*- coding: utf-8 -*-
import speech_recognition as sr
import os
import re
from gtts import gTTS
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Logger import *


class Google(object):
    __metaclass__ = Singleton

    __language_2letter_cc = 'de'
    __language_4letter_cc = 'de-DE'
    __audioPlayer = "afplay '{0}'"
    __apiKey = None

    __asyncInit = False
    __asyncResultList = []

    def __init__(self):
        self.__language_2letter_cc = Config().Get("TextToSpeech", "CountryCode2Letter")
        self.__language_4letter_cc = Config().Get("TextToSpeech", "CountryCode4Letter")
        self.__audioPlayer = Config().Get("TextToSpeech", "AudioPlayer") + " '{0}'"

        self.__asyncInit = False

        microphoneID = None
        microphoneName = Config().Get("SpeechToText", "Microphone")
        for i, microphone_name in enumerate(sr.Microphone().list_microphone_names()):
            if microphone_name == microphoneName:
                microphoneID = i

        if microphoneID is None:
            FileLogger().Error("Google Line 38: No microphone found - Exit")
            raise Exception("Google: No microphone found - Exit")
            return

        self.__recognizer = sr.Recognizer()
        #Represents the minimum length of silence (in seconds) that will register as the
        #end of a phrase. Can be changed.
        #Smaller values result in the recognition completing more quickly, but might result
        #in slower speakers being cut off.
        self.__recognizer.pause_threshold = 0.5
        self.__recognizer.operation_timeout = 3

        self.__microphone = sr.Microphone(device_index=microphoneID)

        with self.__microphone as source:
            self.__recognizer.dynamic_energy_threshold = True
            self.__recognizer.adjust_for_ambient_noise(source)

        self.__apiKey = Config().Get("TextToSpeech", "GoogleAPIKey")
        if(len(self.__apiKey) == 0):
            self.__apiKey = None


    def Speak(self, audioString, playAudio=False):
        if(len(audioString) == 0):
            return
        tmpAudioFile = os.path.join(Global.EmeraldPath, "Data", "TTS", ("Google_" + \
            self.__language_2letter_cc + "_" + \
            self.CleanString(audioString) + ".mp3"))

        if not os.path.isfile(tmpAudioFile):
            tts = gTTS(text=audioString, lang=self.__language_2letter_cc)
            tts.save(tmpAudioFile)

        if(playAudio):
            os.system(self.__audioPlayer.format(tmpAudioFile))
        return tmpAudioFile


    def AsyncCallback(self, recognizer, audio):
        data = ""
        try:
            data = self.__recognizer.recognize_google(audio,
                key=self.__apiKey, language=self.__language_4letter_cc, show_all=False)
        except sr.UnknownValueError as e:
            FileLogger().Warn("Google Line 83: Google Speech Recognition could not understand audio: {0}".format(e))
        except sr.RequestError as e:
            FileLogger().Warn("Google Line 85: Could not request results from Google Speech Recognition service: {0}".format(e))
        except Exception as e:
            FileLogger().Warn("Google Line 87: Error on executing Google Speech Recognition service: {0}".format(e))

        if(len(data)>0):
            self.__asyncResultList.append(data)

    def ListenAsync(self):
        if not self.__asyncInit:
            self.__recognizer.listen_in_background(self.__microphone, self.AsyncCallback)
            self.__asyncInit = True

        if (len(self.__asyncResultList)>0):
            return self.__asyncResultList.pop(0)
        return ""


    def Listen(self):
        with self.__microphone as source:
            self.__audio = self.__recognizer.listen(source)

            data = ""
            try:
                data = self.__recognizer.recognize_google(
                    self.__audio, key=self.__apiKey, language=self.__language_4letter_cc, show_all=False)
            except sr.UnknownValueError as e:
                FileLogger().Warn("Google Line 75: Google Speech Recognition could not understand audio: {0}".format(e))
            except sr.RequestError as e:
                FileLogger().Warn("Google Line 77: Could not request results from Google Speech Recognition service: {0}".format(e))
            except Exception as e:
                FileLogger().Warn("Google Line 81: Error on executing Google Speech Recognition service: {0}".format(e))

            return data


    def CleanString(self, string):
        data = re.sub(r'\W+', '', string)
        return (data[:75] + '_TRIMMED') if len(data) > 75 else data


    def GetAvailiabeMicrophones(self):
        return sr.Microphone().list_microphone_names()


"""

TODO:
energy_threshold
The recognizer tries to recognize speech even when I’m not speaking.
Try increasing the recognizer_instance.energy_threshold property.
This is basically how sensitive the recognizer is to when recognition should start.
Higher values mean that it will be less sensitive, which is useful if you are in a loud room.


pip install SpeechRecognition

"""
