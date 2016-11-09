#!/usr/bin/python
# -*- coding: utf-8 -*-
import speech_recognition as sr
import os
from gtts import gTTS

class Google(object):

  language_2letter_cc = 'de'
  language_4letter_cc = 'de-DE'
  audioPlayer = "afplay {0}"

  def Speak(self, audioString):
    tts = gTTS(text=audioString, lang=self.language_2letter_cc)
    tts.save("TMPAudioGoogle.mp3")
    os.system(self.audioPlayer.format("TMPAudioGoogle.mp3"))

  def Listen(self):
    r = sr.Recognizer()
    with sr.Microphone() as source:
      audio = r.listen(source)

    data = ""
    try:
      data = r.recognize_google(audio, key = None, language = self.language_4letter_cc, show_all = False)
    except sr.UnknownValueError:
      print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data

"""
TODO: tmp audio path
log instead of print
google key from config
CC from config


pip install SpeechRecognition

"""
