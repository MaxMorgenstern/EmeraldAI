#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Logic.SpeechProcessing.Google import *
from EmeraldAI.Logic.SpeechProcessing.Ivona import *
from EmeraldAI.Logic.SpeechProcessing.Microsoft import *
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Logger import *
from EmeraldAI.Logic.Audio.SoundMixer import *
from EmeraldAI.Logic.Memory.TTS import TTS as TTSMemory

GLOBAL_FileNamePublisher = None

def InitSettings():
    TTSMemory().Set("TTSProvider", Config().Get("TextToSpeech", "Provider"))
    TTSMemory().Set("UsePygame", Config().Get("TextToSpeech", "UsePygame"))


def RunTTS():
    global GLOBAL_FileNamePublisher
    
    rospy.init_node('TTS_node', anonymous=True)

    rospy.Subscriber("/emerald_ai/io/text_to_speech", String, callback)

    GLOBAL_FileNamePublisher = rospy.Publisher('/emerald_ai/io/text_to_speech/file', String, queue_size=10)

    rospy.spin()


def callback(data):
    global GLOBAL_FileNamePublisher

    dataParts = data.data.split("|")

    if dataParts[0] != "TTS":
        return

    ttsProvider = TTSMemory().GetString("TTSProvider")
    usePygame = TTSMemory().GetBoolean("UsePygame")

    FileLogger().Info("TTS, callback(), Provider: {0}".format(ttsProvider))

    try:
        if(ttsProvider.lower() == "google"):
            data = Google().Speak(dataParts[1], not usePygame)

        if(ttsProvider.lower() == "microsoft"):
            data = Microsoft().Speak(dataParts[1], not usePygame)

        if(ttsProvider.lower() == "ivona"):
            data = Ivona().Speak(dataParts[1], not usePygame)


        if usePygame:
            SoundMixer().Play(data)

        FileLogger().Info("TTS, callback(), Audio: {0}".format(data))
        GLOBAL_FileNamePublisher.publish("TTS|{0}".format(data))

    except Exception as e:
        FileLogger().Error("TTS, callback(), Error on processing TTS data: {0}".format(e))


if __name__ == "__main__":
    if(Pid.HasPid("TTS")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("TTS")

    try:
        InitSettings()
        RunTTS()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("TTS")
