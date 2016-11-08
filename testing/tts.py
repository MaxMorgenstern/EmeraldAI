#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
recognizer_instance.recognize_google(audio_data, key = None, language = "en-US", show_all = False)

Performs speech recognition on audio_data (an AudioData instance), using the Google Speech Recognition API.

The Google Speech Recognition API key is specified by key. If not specified, it uses a generic key that works out of the box. This should generally be used for personal or testing purposes only, as it may be revoked by Google at any time.

To obtain your own API key, simply follow the steps on the API Keys page at the Chromium Developers site. In the Google Developers Console, Google Speech Recognition is listed as "Speech API". Note that the API quota for your own keys is 50 requests per day, and there is currently no way to raise this limit.

The recognition language is determined by language, an IETF language tag like "en-US" or "en-GB", defaulting to US English. A list of supported language codes can be found here. Basically, language codes can be just the language (en), or a language with a dialect (en-US).

Returns the most likely transcription if show_all is false (the default). Otherwise, returns the raw API response as a JSON dictionary.

Raises a speech_recognition.UnknownValueError exception if the speech is unintelligible. Raises a speech_recognition.RequestError exception if the speech recognition operation failed, if the key isn't valid, or if there is no internet connection.
"""

# pip install gTTS

import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS

language_2letter_cc = 'de'
language_4letter_cc = 'de-DE'

def speak(audioString):
    print("Speak: " + audioString)
    tts = gTTS(text=audioString, lang=language_2letter_cc)
    tts.save("audio.mp3")
    os.system("afplay audio.mp3")

def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio, key = None, language = language_4letter_cc, show_all = False)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data

def jarvis(data):
    if len(data) == 0:
        return ""
    speak("Ich habe folgendes verstanden: " + data)
    """
    if "how are you" in data:
        speak("I am fine")

    if "what time is it" in data:
        speak(ctime())

    if "where is" in data:
        data = data.split(" ")
        location = data[2]
        speak("Hold on Max, I will show you where " + location + " is.")
        os.system("chromium-browser https://www.google.nl/maps/place/" + location + "/&amp;")
    """
# initialization
time.sleep(2)
speak("Hi Max, was kann ich für dich tun?")
while 1:
    data = recordAudio()
    jarvis(data)
