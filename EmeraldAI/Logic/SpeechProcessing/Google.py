#!/usr/bin/python
# -*- coding: utf-8 -*-
import speech_recognition as sr
import os
import re
from gtts import gTTS
from EmeraldAI.Logic.Global import Global
from EmeraldAI.Config.Config import *

class Google(object):

  language_2letter_cc = 'de'
  language_4letter_cc = 'de-DE'
  audioPlayer = "afplay '{0}'"
  apiKey = None

  def __init__(self):
    self.language_2letter_cc = Config().Get("TextToSpeech", "CountryCode2Letter")
    self.language_4letter_cc = Config().Get("TextToSpeech", "CountryCode4Letter")
    self.audioPlayer = Config().Get("TextToSpeech", "AudioPlayer") + " '{0}'"

    self.apiKey = Config().Get("TextToSpeech", "GoogleAPIKey")
    if(len(self.apiKey) == 0):
      self.apiKey = None

  def Speak(self, audioString):
    tmpAudioFile = Global().EmeraldPath + "Data/TTS/Google_" + self.language_2letter_cc + "_" + self.CleanString(audioString) + ".mp3"

    if not os.path.isfile(tmpAudioFile):
      tts = gTTS(text=audioString, lang=self.language_2letter_cc)
      tts.save(tmpAudioFile)

    os.system(self.audioPlayer.format(tmpAudioFile))

  def Listen(self):
    r = sr.Recognizer()
    with sr.Microphone() as source:
      audio = r.listen(source)

    data = ""
    try:
      data = r.recognize_google(audio, key = self.apiKey, language = self.language_4letter_cc, show_all = False)
    except sr.UnknownValueError:
      print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data


  def CleanString(self, string):
    data = re.sub(r'\W+', '', string)
    return (data[:75] + '_TRIMMED') if len(data) > 75 else data


"""

TODO:
self.apiKey - not in use

log instead of print


pip install SpeechRecognition

"""
