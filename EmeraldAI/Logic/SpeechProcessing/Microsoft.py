#!/usr/bin/python
# -*- coding: utf-8 -*-
import speech_recognition as sr
import httplib
from urlparse import urlparse
import json
import os

class Microsoft(object):

  language_2letter_cc = 'de'
  language_4letter_cc = 'de-DE'
  audioPlayer = "afplay {0}"

  voiceGender = 'Female'
  voiceName = 'Microsoft Server Speech Text to Speech Voice (de-DE, Hedda)'
  apiKey = "62a761e7e88f4274b912796a7c4c97c7"
  accesstoken = None

  ssmlTemplate = """<speak version='1.0' xml:lang='{0}'>
        <voice xml:lang='{0}' xml:gender='{1}' name='{2}'>
          {3}
        </voice>
      </speak>"""

  audioPlayer = "afplay"

  def __init__(self):
    params = ""
    headers = {"Ocp-Apim-Subscription-Key": self.apiKey}

    AccessTokenHost = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"

    conn = httplib.HTTPSConnection(AccessTokenHost)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = response.read()
    conn.close()

    self.accesstoken = data.decode("UTF-8")


  def Speak(audioString):
    ssml = self.ssmlTemplate.format(self.language_4letter_cc, self.voiceGender, self.voiceName, audioString)
    body = ssml #.encode('utf8')

    headers = {"Content-type": "application/ssml+xml",
      "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
      "Authorization": "Bearer " + self.accesstoken,
      "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
      "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
      "User-Agent": "TTSForPython"}

    #Connect to server to synthesize the wave
    conn = httplib.HTTPSConnection("speech.platform.bing.com")
    conn.request("POST", "/synthesize", body, headers)
    response = conn.getresponse()
#      print(response.status, response.reason)

    data = response.read()
    conn.close()
#       len(data)

    with open("TMPAudioMicrosoft.wav", "wb") as f:
      f.write(data)

    os.system(self.audioPlayer.format("TMPAudioMicrosoft.wav"))


  def Listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
      audio = r.listen(source)

    data = ""
    try:
      data = r.recognize_bing(audio, key = self.apiKey, language = language_4letter_cc, show_all = False)
    except sr.UnknownValueError:
        print("Microsoft Bing Voice Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
    return data



"""

pip install SpeechRecognition

Speak:

https://www.microsoft.com/cognitive-services/en-us/Speech-api/documentation/API-Reference-REST/BingVoiceOutput


Locale	Gender	Service name mapping
ar-EG*	Female	"Microsoft Server Speech Text to Speech Voice (ar-EG, Hoda)"
de-DE	Female	"Microsoft Server Speech Text to Speech Voice (de-DE, Hedda)"
de-DE	Male	"Microsoft Server Speech Text to Speech Voice (de-DE, Stefan, Apollo)"
en-AU	Female	"Microsoft Server Speech Text to Speech Voice (en-AU, Catherine)"
en-CA	Female	"Microsoft Server Speech Text to Speech Voice (en-CA, Linda)"
en-GB	Female	"Microsoft Server Speech Text to Speech Voice (en-GB, Susan, Apollo)"
en-GB	Male	"Microsoft Server Speech Text to Speech Voice (en-GB, George, Apollo)"
en-IN	Male	"Microsoft Server Speech Text to Speech Voice (en-IN, Ravi, Apollo)"
en-US	Female	"Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)"
en-US	Male	"Microsoft Server Speech Text to Speech Voice (en-US, BenjaminRUS)"
es-ES	Female	"Microsoft Server Speech Text to Speech Voice (es-ES, Laura, Apollo)"
es-ES	Male	"Microsoft Server Speech Text to Speech Voice (es-ES, Pablo, Apollo)"
es-MX	Male	"Microsoft Server Speech Text to Speech Voice (es-MX, Raul, Apollo)"
fr-CA	Female	"Microsoft Server Speech Text to Speech Voice (fr-CA, Caroline)"
fr-FR	Female	"Microsoft Server Speech Text to Speech Voice (fr-FR, Julie, Apollo)"
fr-FR	Male	"Microsoft Server Speech Text to Speech Voice (fr-FR, Paul, Apollo)"
it-IT	Male	"Microsoft Server Speech Text to Speech Voice (it-IT, Cosimo, Apollo)"
ja-JP	Female	"Microsoft Server Speech Text to Speech Voice (ja-JP, Ayumi, Apollo)"
ja-JP	Male	"Microsoft Server Speech Text to Speech Voice (ja-JP, Ichiro, Apollo)"
pt-BR	Male	"Microsoft Server Speech Text to Speech Voice (pt-BR, Daniel, Apollo)"
ru-RU	Female	"Microsoft Server Speech Text to Speech Voice (ru-RU, Irina, Apollo)"
ru-RU	Male	"Microsoft Server Speech Text to Speech Voice (ru-RU, Pavel, Apollo)"
zh-CN	Female	"Microsoft Server Speech Text to Speech Voice (zh-CN, HuihuiRUS)"
zh-CN	Female	"Microsoft Server Speech Text to Speech Voice (zh-CN, Yaoyao, Apollo)"
zh-CN	Male	"Microsoft Server Speech Text to Speech Voice (zh-CN, Kangkang, Apollo)"
zh-HK	Female	"Microsoft Server Speech Text to Speech Voice (zh-HK, Tracy, Apollo)"
zh-HK	Male	"Microsoft Server Speech Text to Speech Voice (zh-HK, Danny, Apollo)"
zh-TW	Female	"Microsoft Server Speech Text to Speech Voice (zh-TW, Yating, Apollo)"
zh-TW	Male	"Microsoft Server Speech Text to Speech Voice (zh-TW, Zhiwei, Apollo)"
"""
