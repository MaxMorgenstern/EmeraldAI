#!/usr/bin/python
# -*- coding: utf-8 -*-
import speech_recognition as sr
import os
import re
from gtts import gTTS
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Config.Config import *

class Google(object):

  __language_2letter_cc = 'de'
  __language_4letter_cc = 'de-DE'
  __audioPlayer = "afplay '{0}'"
  __apiKey = None

  def __init__(self):
    self.__language_2letter_cc = Config().Get("TextToSpeech", "CountryCode2Letter")
    self.__language_4letter_cc = Config().Get("TextToSpeech", "CountryCode4Letter")
    self.__audioPlayer = Config().Get("TextToSpeech", "AudioPlayer") + " '{0}'"

    self.__apiKey = Config().Get("TextToSpeech", "GoogleAPIKey")
    if(len(self.__apiKey) == 0):
      self.__apiKey = None

  def Speak(self, audioString, playAudio=False):
    if(len(audioString) == 0):
      return
    tmpAudioFile = Global.EmeraldPath + "Data/TTS/Google_" + self.__language_2letter_cc + "_" + self.CleanString(audioString) + ".mp3"

    if not os.path.isfile(tmpAudioFile):
      tts = gTTS(text=audioString, lang=self.__language_2letter_cc)
      tts.save(tmpAudioFile)

    if(playAudio):
      os.system(self.__audioPlayer.format(tmpAudioFile))
    return tmpAudioFile

  def Listen(self):
    r = sr.Recognizer()
    with sr.Microphone() as source:
      audio = r.listen(source)

    data = ""
    try:
      data = r.recognize_google(audio, key = self.__apiKey, language = self.__language_4letter_cc, show_all = False)
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

log instead of print


the same for microsoft:
energy_threshold
The recognizer tries to recognize speech even when I’m not speaking.
Try increasing the recognizer_instance.energy_threshold property.
This is basically how sensitive the recognizer is to when recognition should start.
Higher values mean that it will be less sensitive, which is useful if you are in a loud room.


pip install SpeechRecognition

"""
