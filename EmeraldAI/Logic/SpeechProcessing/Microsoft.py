#!/usr/bin/python
# -*- coding: utf-8 -*-
import speech_recognition as sr
import httplib
import os
import re
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Logger import *


class Microsoft(object):
    __metaclass__ = Singleton

    __language_2letter_cc = 'de'
    __language_4letter_cc = 'de-DE'
    __audioPlayer = "afplay '{0}'"

    __voiceGender = 'Female'
    __voiceName = 'Microsoft Server Speech Text to Speech Voice (de-DE, Hedda)'
    __apiKey = None
    __accesstoken = None

    __ssmlTemplate = """<speak version='1.0' xml:lang='{0}'>
        <voice xml:lang='{0}' xml:gender='{1}' name='{2}'>
          {3}
        </voice>
      </speak>"""

    def __init__(self):
        self.__language_2letter_cc = Config().Get("TextToSpeech", "CountryCode2Letter")
        self.__language_4letter_cc = Config().Get("TextToSpeech", "CountryCode4Letter")
        self.__audioPlayer = Config().Get("TextToSpeech", "AudioPlayer") + " '{0}'"


        microphoneID = None
        microphoneName = Config().Get("SpeechToText", "Microphone")
        for i, microphone_name in enumerate(sr.Microphone().list_microphone_names()):
            if microphone_name == microphoneName:
                microphoneID = i

        self.__recognizer = sr.Recognizer()
        self.__microphone = sr.Microphone(device_index=microphoneID)

        with self.__microphone as source:
            self.__recognizer.dynamic_energy_threshold = True
            self.__recognizer.adjust_for_ambient_noise(source)

        self.__voiceGender = Config().Get("TextToSpeech", "MicrosoftVoiceGender")
        self.__voiceName = Config().Get("TextToSpeech", "MicrosoftVoiceName")
        self.__apiKey = Config().Get("TextToSpeech", "MicrosoftAPIKey")

        params = ""
        headers = {"Ocp-Apim-Subscription-Key": self.__apiKey}

        __AccessTokenHost = "api.cognitive.microsoft.com"
        path = "/sts/v1.0/issueToken"

        conn = httplib.HTTPSConnection(__AccessTokenHost)
        conn.request("POST", path, params, headers)
        response = conn.getresponse()

        data = response.read()
        conn.close()

        self.__accesstoken = data.decode("UTF-8")


    def Speak(self, audioString, playAudio=False):
        if(len(audioString) == 0):
            return
        tmpAudioFile = os.path.join(Global.EmeraldPath, "Data", "TTS", ("Microsoft_" + \
            self.__language_2letter_cc + "_" + \
            self.CleanString(audioString) + ".wav"))

        if not os.path.isfile(tmpAudioFile):
            ssml = self.__ssmlTemplate.format(
                self.__language_4letter_cc, self.__voiceGender, self.__voiceName, audioString)
            body = ssml  # .encode('utf8')

            headers = {"Content-type": "application/ssml+xml",
                       "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
                       "Authorization": "Bearer " + self.__accesstoken,
                       "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
                       "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
                       "User-Agent": "TTSForPython"}

            # Connect to server to synthesize the wave
            conn = httplib.HTTPSConnection("speech.platform.bing.com")
            conn.request("POST", "/synthesize", body, headers)
            response = conn.getresponse()

            data = response.read()
            conn.close()

            with open(tmpAudioFile, "wb") as f:
                f.write(data)

        if(playAudio):
            os.system(self.__audioPlayer.format(tmpAudioFile))
        return tmpAudioFile


    def Listen(self):
        with self.__microphone as source:
            self.__audio = self.__recognizer.listen(source)

            data = ""
            try:
                data = self.__recognizer.recognize_bing(
                    self.__audio, key=self.__apiKey, language=__language_4letter_cc, show_all=False)
            except sr.UnknownValueError as e:
                FileLogger().Warn("Microsoft Line 112: Microsoft Bing Voice Recognition could not understand audio: {0}".format(e))
            except sr.RequestError as e:
                FileLogger().Warn("Microsoft Line 114: Could not request results from Microsoft Bing Voice Recognition service: {0}".format(e))

            return data


    def CleanString(self, string):
        data = re.sub(r'\W+', '', string)
        return (data[:75] + '_TRIMMED') if len(data) > 75 else data


    def GetAvailiabeMicrophones(self):
        return sr.Microphone().list_microphone_names()

"""
Speak:
https://www.microsoft.com/cognitive-services/en-us/Speech-api/documentation/API-Reference-REST/BingVoiceOutput

Locale  Gender  Service name mapping
ar-EG*  Female  "Microsoft Server Speech Text to Speech Voice (ar-EG, Hoda)"
de-DE   Female  "Microsoft Server Speech Text to Speech Voice (de-DE, Hedda)"
de-DE   Male    "Microsoft Server Speech Text to Speech Voice (de-DE, Stefan, Apollo)"
en-AU   Female  "Microsoft Server Speech Text to Speech Voice (en-AU, Catherine)"
en-CA   Female  "Microsoft Server Speech Text to Speech Voice (en-CA, Linda)"
en-GB   Female  "Microsoft Server Speech Text to Speech Voice (en-GB, Susan, Apollo)"
en-GB   Male    "Microsoft Server Speech Text to Speech Voice (en-GB, George, Apollo)"
en-IN   Male    "Microsoft Server Speech Text to Speech Voice (en-IN, Ravi, Apollo)"
en-US   Female  "Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)"
en-US   Male    "Microsoft Server Speech Text to Speech Voice (en-US, BenjaminRUS)"
es-ES   Female  "Microsoft Server Speech Text to Speech Voice (es-ES, Laura, Apollo)"
es-ES   Male    "Microsoft Server Speech Text to Speech Voice (es-ES, Pablo, Apollo)"
es-MX   Male    "Microsoft Server Speech Text to Speech Voice (es-MX, Raul, Apollo)"
fr-CA   Female  "Microsoft Server Speech Text to Speech Voice (fr-CA, Caroline)"
fr-FR   Female  "Microsoft Server Speech Text to Speech Voice (fr-FR, Julie, Apollo)"
fr-FR   Male    "Microsoft Server Speech Text to Speech Voice (fr-FR, Paul, Apollo)"
it-IT   Male    "Microsoft Server Speech Text to Speech Voice (it-IT, Cosimo, Apollo)"
ja-JP   Female  "Microsoft Server Speech Text to Speech Voice (ja-JP, Ayumi, Apollo)"
ja-JP   Male    "Microsoft Server Speech Text to Speech Voice (ja-JP, Ichiro, Apollo)"
pt-BR   Male    "Microsoft Server Speech Text to Speech Voice (pt-BR, Daniel, Apollo)"
ru-RU   Female  "Microsoft Server Speech Text to Speech Voice (ru-RU, Irina, Apollo)"
ru-RU   Male    "Microsoft Server Speech Text to Speech Voice (ru-RU, Pavel, Apollo)"
zh-CN   Female  "Microsoft Server Speech Text to Speech Voice (zh-CN, HuihuiRUS)"
zh-CN   Female  "Microsoft Server Speech Text to Speech Voice (zh-CN, Yaoyao, Apollo)"
zh-CN   Male    "Microsoft Server Speech Text to Speech Voice (zh-CN, Kangkang, Apollo)"
zh-HK   Female  "Microsoft Server Speech Text to Speech Voice (zh-HK, Tracy, Apollo)"
zh-HK   Male    "Microsoft Server Speech Text to Speech Voice (zh-HK, Danny, Apollo)"
zh-TW   Female  "Microsoft Server Speech Text to Speech Voice (zh-TW, Yating, Apollo)"
zh-TW   Male    "Microsoft Server Speech Text to Speech Voice (zh-TW, Zhiwei, Apollo)"
"""
