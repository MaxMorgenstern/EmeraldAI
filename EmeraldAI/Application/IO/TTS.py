#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from os.path import dirname, abspath
from mutagen.mp3 import MP3
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Logic.SpeechProcessing.Google import Google
from EmeraldAI.Logic.SpeechProcessing.Ivona import Ivona
from EmeraldAI.Logic.SpeechProcessing.Microsoft import Microsoft
from EmeraldAI.Logic.SpeechProcessing.Watson import Watson
from EmeraldAI.Config.Config import Config
from EmeraldAI.Logic.Logger import FileLogger
from EmeraldAI.Logic.Audio.SoundMixer import SoundMixer
from EmeraldAI.Logic.Memory.TTS import TTS as TTSMemory
from EmeraldAI.Entities.User import User


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
        if usePygame and data == "TRIGGER_STOP_AUDIO":
            SoundMixer().Stop()
            return

        if(ttsProvider.lower() == "google"):
            data = Google().Speak(dataParts[1])

        if(ttsProvider.lower() == "microsoft"):
            data = Microsoft().Speak(dataParts[1])

        if(ttsProvider.lower() == "ivona"):
            data = Ivona().Speak(dataParts[1])

        if(ttsProvider.lower() == "watson"):
            data = Watson().Speak(dataParts[1])


        try:
            audio = MP3(data)
            TTSMemory().Set("TTS.Until", (rospy.Time.now().to_sec() + int(round(audio.info.length))))
        except Exception as e:
            FileLogger().Warn("TTS, callback() - Error on getting audio duration: {0}".format(e))


        if usePygame:
            SoundMixer().Play(data)
        else:
            audioPlayer = Config().Get("TextToSpeech", "AudioPlayer") + " '{0}'"
            os.system(audioPlayer.format(data))


        FileLogger().Info("TTS, callback(), Play Audio: {0}".format(data))
        GLOBAL_FileNamePublisher.publish("TTS|{0}".format(data))

        user = User().LoadObject()
        if(user.GetName() is not None):
            user.UpdateSpokenTo()
            user.Update()

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
