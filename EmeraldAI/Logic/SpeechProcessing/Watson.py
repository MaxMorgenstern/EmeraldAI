#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import pyaudio
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
from threading import Thread
from sets import Set

import rospy
from std_msgs.msg import String

try:
    from Queue import Queue, Full
except ImportError:
    from queue import Queue, Full

from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Logger import *

class Watson():
    __metaclass__ = Singleton

    def __init__(self):
        self.CHUNK = 1024
        self.BUF_MAX_SIZE = self.CHUNK * 10
        self.q = Queue(maxsize=int(round(self.BUF_MAX_SIZE / self.CHUNK)))
        self.audio_source = AudioSource(self.q, True, True)
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

        self.__username = Config().Get("SpeechToText", "WatsonSTTUsername")
        self.__password = Config().Get("SpeechToText", "WatsonSTTPassword")
        self.__language = Config().Get("SpeechToText", "CountryCode4Letter")


        self.speech_to_text = SpeechToTextV1(
            username=self.__username,
            password=self.__password,
            url='https://stream.watsonplatform.net/speech-to-text/api')

        self.audio = pyaudio.PyAudio()

        # open stream using callback
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.pyaudio_callback,
            start=False
        )
        rospy.init_node('STT_watson_node', anonymous=True)


    def Listen(self):
        self.stream.start_stream()

        try:
            while True:
                recognize_thread = Thread(target=self.recognize_using_weboscket, args=())
                recognize_thread.start()

                recognize_thread.join()

        except KeyboardInterrupt:
            # stop recording
            self.audio_source.completed_recording()
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

    def recognize_using_weboscket(self, *args):
        mycallback = MyRecognizeCallback()
        self.speech_to_text.recognize_using_websocket(audio=self.audio_source,
                                                      content_type='audio/l16; rate=44100',
                                                      recognize_callback=mycallback,
                                                      interim_results=True,
                                                      model='{0}_BroadbandModel'.format(self.__language),
                                                      smart_formatting=True)

    def pyaudio_callback(self, in_data, frame_count, time_info, status):
        try:
            self.q.put(in_data)
        except Full:
            pass
        return (None, pyaudio.paContinue)


# define callback for the speech to text service
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)
        self.dataString = ""
        self.dataList = []

        self.__WatsonSentencePublisher = rospy.Publisher('/emerald_ai/io/speech_to_text', String, queue_size=10)
        self.__WatsonWordPublisher = rospy.Publisher('/emerald_ai/io/speech_to_text/word', String, queue_size=10)


    #def on_transcription(self, transcript):
    #    print(transcript)

    def on_connected(self):
        FileLogger().Info('Connection was successful')

    def on_error(self, error):
        FileLogger().Error('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        FileLogger().Error('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        FileLogger().Info('Service is listening')

    #def on_hypothesis(self, hypothesis):
    #    if(self.dataString != hypothesis):

    #        s1 = Set(hypothesis.split())
    #        s2 = Set(self.dataList)
    #        t = list(s1.difference(s2))
    #        print(t)
    #        self.dataList.extend(t)

    #        self.dataString = hypothesis
    #        print(self.data)

    def on_data(self, data):
        hypothesis = data["results"][0]["alternatives"][0]["transcript"]

        if (data["results"][0]["final"]):
            self.__WatsonSentencePublisher.publish("STT|{0}".format(self.dataString))

            self.dataString = ""
            self.dataList = []
        else:
            if(self.dataString != hypothesis):
                s1 = Set(hypothesis.split())
                s2 = Set(self.dataList)
                t = list(s1.difference(s2))
                for w in t:
                    self.__WatsonWordPublisher.publish("STT|{0}".format(w))
                self.dataList.extend(t)

                self.dataString = hypothesis

    def on_close(self):
        FileLogger().Warn("Connection closed")

