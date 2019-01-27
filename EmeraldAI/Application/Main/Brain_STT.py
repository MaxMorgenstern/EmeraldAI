#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Pipelines.ScopeAnalyzer.AnalyzeScope import AnalyzeScope
from EmeraldAI.Pipelines.ResponseProcessing.ProcessResponse import ProcessResponse
from EmeraldAI.Pipelines.Trainer.Trainer import Trainer
from EmeraldAI.Entities.ContextParameter import ContextParameter
from EmeraldAI.Entities.PipelineArgs import PipelineArgs
from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import Config
from EmeraldAI.Logic.Memory.Brain import Brain as BrainMemory
from EmeraldAI.Logic.Memory.TTS import TTS as TTSMemory
from EmeraldAI.Entities.Word import Word
from EmeraldAI.Logic.Logger import FileLogger

class BrainSTT:
    def __init__(self):
        if(not BrainMemory().Has("Listen")):
            BrainMemory().Set("Listen", True)

        if(not BrainMemory().Has("Mute")):
            BrainMemory().Set("Mute", False)

        rospy.init_node('emerald_brain_stt_node', anonymous=True)

        rospy.Subscriber("/emerald_ai/io/speech_to_text", String, self.sentenceCallback)
        rospy.Subscriber("/emerald_ai/io/speech_to_text/word", String, self.wordCallback)

        self.__FaceappPublisher = rospy.Publisher('/emerald_ai/app/face', String, queue_size=10)

        self.__ResponsePublisher = rospy.Publisher('/emerald_ai/io/text_to_speech', String, queue_size=10)

        self.Pipeline = None

        rospy.spin()


    def sentenceCallback(self, data):
        dataParts = data.data.split("|")

        if dataParts[0] == "STT":
            self.ProcessSpeech(dataParts[1])
            return

    def wordCallback(self, data):
        dataParts = data.data.split("|")

        if dataParts[0] == "STT":
            self.ProcessWord(dataParts[1])
            return


    ##### STT #####

    def ProcessWord(self, word):
        if(not BrainMemory().GetBoolean("Listen") or self.__TTSActive()):
            return

        if self.Pipeline is None:
            self.Pipeline = PipelineArgs()

        if self.Pipeline.HasWord(word):
            return

        BrainMemory().Set("Brain.AudioTimestamp", rospy.Time.now().to_sec())
        word = Word(word)
        self.Pipeline.AddWord(word)


    def ProcessSpeech(self, sentence):
        if(not BrainMemory().GetBoolean("Listen") or self.__TTSActive()):
            return

        cancelSpeech = False
        stopwordList = Config().GetList("Bot", "StoppwordList")
        if(sentence in stopwordList):
            cancelSpeech = True
            self.__ResponsePublisher.publish("TTS|TRIGGER_STOP_AUDIO")

        if self.Pipeline is None:
            self.Pipeline = PipelineArgs()

        BrainMemory().Set("Brain.AudioTimestamp", rospy.Time.now().to_sec())

        self.Pipeline.AddSentence(sentence)

        self.Pipeline = AnalyzeScope().Process(self.Pipeline)

        self.Pipeline = ProcessResponse().Process(self.Pipeline)
        if(not cancelSpeech and not BrainMemory().GetBoolean("Mute")):
            self.ProcessAnimation(self.Pipeline.Animation)
            if(self.Pipeline.ResponseFound):

                FileLogger().Info("Brain STT, ProcessSpeech(): {0}".format(self.Pipeline.Response))
                self.__ResponsePublisher.publish("TTS|{0}".format(self.Pipeline.Response))

        trainerResult = Trainer().Process(self.Pipeline)

        contextParameter = ContextParameter().LoadObject(240)
        contextParameter.AppendHistory(self.Pipeline)
        contextParameter.SaveObject()

        print "Pipeline Args", self.Pipeline.toJSON()
        print "Trainer Result: ", trainerResult
        print "Input: ", sentence
        print "Response: ", self.Pipeline.Response

        self.Pipeline = None


    def ProcessAnimation(self, animation):
        if animation is not None and len(animation) > 0:
            print animation, "TODO"
            animationData = "FACEMASTER|{0}".format(animation)
            rospy.loginfo(animationData)
            self.__FaceappPublisher.publish(animationData)


    def __TTSActive(self):
        storedTimestamp = TTSMemory().GetFloat("TTS.Until")
        if(storedTimestamp >= rospy.Time.now().to_sec()):
            return True
        return False


##### MAIN #####

if __name__ == "__main__":
    if(Pid.HasPid("Brain.STT")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Brain.STT")
    try:
        BrainSTT()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Brain.STT")
