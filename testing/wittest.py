#!/usr/bin/python
# -*- coding: utf-8 -*-
# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Wit.ai
# Wit.ai keys are 32-character uppercase alphanumeric strings
WIT_AI_KEY = "SIXPIB6BXKQHL7XAYHJLHQPBHO4TXVRR"
try:
    print("Wit.ai thinks you said " + r.recognize_wit(audio, key=WIT_AI_KEY))
except sr.UnknownValueError:
    print("Wit.ai could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Wit.ai service; {0}".format(e))
