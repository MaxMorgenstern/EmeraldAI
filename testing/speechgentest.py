#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
#Copyright (c) Microsoft Corporation
#All rights reserved.
#MIT License
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ""Software""), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###

#import http.client, urllib.parse, json

import httplib
from urlparse import urlparse
import json
import os

#Note: The way to get api key:
#Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
#Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0
apiKey = "62a761e7e88f4274b912796a7c4c97c7"

params = ""
headers = {"Ocp-Apim-Subscription-Key": apiKey}

#AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
AccessTokenHost = "api.cognitive.microsoft.com"
path = "/sts/v1.0/issueToken"

# Connect to server to get the Access Token
print ("Connect to server to get the Access Token")
conn = httplib.HTTPSConnection(AccessTokenHost)
conn.request("POST", path, params, headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
conn.close()

accesstoken = data.decode("UTF-8")
print ("Access Token: " + accesstoken)

ssml = """<speak version='1.0' xml:lang='de-DE'>
				<voice xml:lang='de-DE' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (de-DE, Hedda)'>
					Hi Max, was kann ich für dich tun?
				</voice>
			</speak>"""


ssml = """<speak version='1.0' xml:lang='en-US'>
				<voice xml:lang='en-US' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'>
					<prosody pitch="low"> This is low pitch. </prosody><prosody pitch="medium"> This is medium pitch. </prosody><prosody pitch="high"> This is high pitch. </prosody><prosody rate="slow"> This is slow speech. </prosody><prosody rate="1"> This is medium speech. </prosody><prosody rate="fast"> This is fast speech. </prosody><prosody volume="x-soft"> This is extra soft volume. </prosody><prosody volume="medium"> This is medium volume. </prosody><prosody volume="x-loud"> This is extra loud volume. </prosody>
				</voice>
			</speak>"""

ssml = """<speak version='1.0' xml:lang='de-DE'>
				<voice xml:lang='de-DE' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (de-DE, Hedda)'>
					<prosody pitch="low"> This is low pitch. </prosody><prosody pitch="medium"> This is medium pitch. </prosody><prosody pitch="high"> This is high pitch. </prosody><prosody rate="slow"> This is slow speech. </prosody><prosody rate="1"> This is medium speech. </prosody><prosody rate="fast"> This is fast speech. </prosody><prosody volume="x-soft"> This is extra soft volume. </prosody><prosody volume="medium"> This is medium volume. </prosody><prosody volume="x-loud"> This is extra loud volume. </prosody>
				</voice>
			</speak>"""

# Max: !!! NEW !!!
body = ssml #.encode('utf8')

headers = {"Content-type": "application/ssml+xml",
			"X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
			"Authorization": "Bearer " + accesstoken,
			"X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
			"X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
			"User-Agent": "TTSForPython"}

#Connect to server to synthesize the wave
print ("\nConnect to server to synthesize the wave")
conn = httplib.HTTPSConnection("speech.platform.bing.com")
conn.request("POST", "/synthesize", body, headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
conn.close()
print("The synthesized wave length: %d" %(len(data)))

#data.save("TMPAudioBing.wav")
#os.system("afplay TMPAudioBing.wav")

with open("TMPAudioBing.wav", "wb") as f:
    f.write(data)

os.system("afplay TMPAudioBing.wav")


"""

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


