#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This Class is based on the work of:

Pyvona : an IVONA python library
Author: Zachary Bears
Contact Email: bears.zachary@gmail.com
Note: Full operation of this library requires the requests and pygame libraries

https://github.com/zbears/pyvona/

---
The MIT License (MIT)

Copyright (c) 2015 Zachary Bears

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
"""

import os
import re
import json
import datetime
import hashlib
import hmac
import requests
requests.packages.urllib3.disable_warnings()

from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Config.Config import *


class Ivona(object):

    __language_2letter_cc = 'de'
    __language_4letter_cc = 'de-DE'
    __audioPlayer = "afplay '{0}'"

    __voiceGender = 'Male'
    __voiceName = 'Hans'
    __accessKey = None
    __secretKey = None
    __speechRate = None
    __sentenceBreak = None
    __paragraphBreak = None

    __session = None

    __host = None
    __region = None
    __region_options = {
        'us-east': 'us-east-1',
        'us-west': 'us-west-2',
        'eu-west': 'eu-west-1',
    }

    def __setRegion(self, region_name):
        self.__region = self.__region_options.get(region_name, 'eu-west-1')
        self.__host = 'tts.{}.ivonacloud.com'.format(self.__region)

    __codec = None
    __codec_options = {
        'mp3': 'mp3',
        'ogg': 'ogg',
        'mp4': 'mp4',
    }

    def __setCodec(self, codec_name):
        self.__codec = self.__codec_options.get(codec_name, 'mp3')

    def __init__(self):
        self.__language_2letter_cc = Config().Get("TextToSpeech", "CountryCode2Letter")
        self.__language_4letter_cc = Config().Get("TextToSpeech", "CountryCode4Letter")
        self.__audioPlayer = Config().Get(
            "TextToSpeech", "AudioPlayer") + " '{0}'"

        self.__voiceGender = Config().Get("TextToSpeech", "IvonaVoiceGender")
        self.__voiceName = Config().Get("TextToSpeech", "IvonaVoiceName")
        self.__accessKey = Config().Get("TextToSpeech", "IvonaAccessKey")
        self.__secretKey = Config().Get("TextToSpeech", "IvonaSecretKey")

        self.__speechRate = 'medium'  # x-slow - slow - medium - fast - x-fast
        self.__sentenceBreak = 400
        self.__paragraphBreak = 650
        self.__setRegion('eu-west')
        self.__setCodec('mp3')

    def Speak(self, audioString, playAudio=False):
        if(len(audioString) == 0):
            return
        tmpAudioFile = Global.EmeraldPath + "Data/TTS/Ivona_" + \
            self.__language_2letter_cc + "_" + \
            self.CleanString(audioString) + ".mp3"

        if not os.path.isfile(tmpAudioFile):
            with open(tmpAudioFile, "wb") as f:
                r = self._send_amazon_auth_packet_v4(
                    'POST', 'tts', 'application/json', '/CreateSpeech', '',
                    self._generate_payload(audioString
                                           ), self.__region, self.__host)
                if r.content.startswith(b'{'):
                    raise Exception(
                        'Error fetching voice: {}'.format(r.content))
                else:
                    f.write(r.content)

        if(playAudio):
            os.system(self.__audioPlayer.format(tmpAudioFile))
        return tmpAudioFile

    def GetVoices(self):
        """Returns all the possible voices
        """
        r = self._send_amazon_auth_packet_v4(
            'POST', 'tts', 'application/json', '/ListVoices', '', '',
            self.__region, self.__host)
        return r.json()

    def CleanString(self, string):
        data = re.sub(r'\W+', '', string)
        return (data[:75] + '_TRIMMED') if len(data) > 75 else data

    def _generate_payload(self, text_to_speak):
        return json.dumps({
            'Input': {
                "Type": "application/ssml+xml",
                'Data': text_to_speak
            },
            'OutputFormat': {
                'Codec': self.__codec.upper()
            },
            'Parameters': {
                'Rate': self.__speechRate,
                'SentenceBreak': self.__sentenceBreak,
                'ParagraphBreak': self.__paragraphBreak
            },
            'Voice': {
                'Name': self.__voiceName,
                'Language': self.__language_4letter_cc,
                'Gender': self.__voiceGender
            }
        })

    def _send_amazon_auth_packet_v4(self, method, service, content_type,
                                    canonical_uri, canonical_querystring,
                                    request_parameters, region, host):
        """Send a packet to a given amazon server using Amazon's signature Version 4,
        Returns the resulting response object
        """

        algorithm = 'AWS4-HMAC-SHA256'
        signed_headers = 'content-type;host;x-amz-content-sha256;x-amz-date'

        # Create date for headers and the credential string
        t = datetime.datetime.utcnow()
        amazon_date = t.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = t.strftime('%Y%m%d')

        # Step 1: Create canonical request
        payload_hash = self._sha_hash(request_parameters)

        canonical_headers = 'content-type:{}\n'.format(content_type)
        canonical_headers += 'host:{}\n'.format(host)
        canonical_headers += 'x-amz-content-sha256:{}\n'.format(payload_hash)
        canonical_headers += 'x-amz-date:{}\n'.format(amazon_date)

        canonical_request = '\n'.join([
            method, canonical_uri, canonical_querystring, canonical_headers,
            signed_headers, payload_hash])

        # Step 2: Create the string to sign
        credential_scope = '{}/{}/{}/aws4_request'.format(
            date_stamp, region, service)
        string_to_sign = '\n'.join([
            algorithm, amazon_date, credential_scope,
            self._sha_hash(canonical_request)])

        # Step 3: Calculate the signature
        signing_key = self._get_signature_key(
            self.__secretKey, date_stamp, region, service)
        signature = hmac.new(
            signing_key, string_to_sign.encode('utf-8'),
            hashlib.sha256).hexdigest()

        # Step 4: Create the signed packet
        endpoint = 'https://{}{}'.format(host, canonical_uri)
        authorization_header = '{} Credential={}/{}, ' +\
            'SignedHeaders={}, Signature={}'
        authorization_header = authorization_header.format(
            algorithm, self.__accessKey, credential_scope,
            signed_headers, signature)
        headers = {
            'Host': host,
            'Content-type': content_type,
            'X-Amz-Date': amazon_date,
            'Authorization': authorization_header,
            'x-amz-content-sha256': payload_hash,
            'Content-Length': str(len(request_parameters))
        }

        # Send the packet and return the response
        # Use requests.Session() for HTTP keep-alive
        if self.__session is None:
            self.__session = requests.Session()

        return self.__session.post(endpoint, data=request_parameters, headers=headers)

    def _sha_hash(self, to_hash):
        return hashlib.sha256(to_hash.encode('utf-8')).hexdigest()

    def _sign(self, key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def _get_signature_key(self, key, date_stamp, region_name, service_name):
        k_date = self._sign(('AWS4{}'.format(key)).encode('utf-8'), date_stamp)
        k_region = self._sign(k_date, region_name)
        k_service = self._sign(k_region, service_name)
        k_signing = self._sign(k_service, 'aws4_request')
        return k_signing
