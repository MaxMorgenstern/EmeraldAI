#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import time
from mutagen.mp3 import MP3
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import Config
from EmeraldAI.Logic.Audio.SoundMixer import SoundMixer
from EmeraldAI.Logic.Memory.Brain import Brain as BrainMemory
from EmeraldAI.Logic.Logger import FileLogger


class BrainTTS:
    def __init__(self):
        
        self.__audioPlayer = Config().Get("TextToSpeech", "AudioPlayer") + " '{0}'"
        self.__usePygame = Config().GetBoolean("TextToSpeech", "UsePygame")

        rospy.init_node("emerald_brain_tts_node", anonymous=True)

        rospy.Subscriber("/emerald_ai/io/text_to_speech/file", String, self.playAudio)
    
        rospy.spin()

    def playAudio(self, data):
        dataParts = data.data.split("|")

        if dataParts[0] != "TTS":
            return
        try:
            audio = MP3(dataParts[1])
            BrainMemory().Set("TTS.Until", (rospy.Time.now().to_sec() + int(round(audio.info.length))))
        except Exception as e:
            FileLogger().Warn("Brain TTS, playAudio() - Error on getting audio duration: {0}".format(e))

        try:
            if self.__usePygame:
                SoundMixer().Play(dataParts[1])
                return
            
            os.system(self.__audioPlayer.format(dataParts[1]))
        except Exception as e:
            FileLogger().Warn("Brain TTS, playAudio() - Error on playing audio: {0}".format(e))


##### MAIN #####

if __name__ == "__main__":
    if(Pid.HasPid("Brain.TTS")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Brain.TTS")
    try:
        BrainTTS()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Brain.TTS")
