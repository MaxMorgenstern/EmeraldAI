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

from EmeraldAI.Logic.SpeechProcessing.Google import *
from EmeraldAI.Logic.SpeechProcessing.Microsoft import *
from EmeraldAI.Logic.SpeechProcessing.Wit import *
from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Logic.Memory.STT import STT as STTMemory
from EmeraldAI.Config.Config import *

def InitSettings():
    STTMemory().Set("TriggerTimestamp", time.time())


def callback(data):
    dataParts = data.data.split("|")
    # TODO - check timestamp
    if(dataParts[1] is "STT"):
        STTMemory().Set("TriggerTimestamp", time.time())


def RunSTT():
    pub = rospy.Publisher('/emerald_ai/io/speech_to_text', String, queue_size=10)

    rospy.Subscriber("trigger", String, callback)

    rospy.init_node('STT_node', anonymous=True)
    rospy.Rate(10) # 10hz

    useTrigger = Config().GetBoolean("Application.SpeechToText", "Trigger")
    triggerTime = Config().GetInt("Application.SpeechToText", "TriggerTime")

    sttProvider = Config().Get("SpeechToText", "Provider") # Google
    if(sttProvider.lower() == "google"):
        provider = Google()

    if(sttProvider.lower() == "microsoft"):
        provider = Microsoft()

    if(sttProvider.lower() == "wit"):
        provider = Wit()    

    while True:
        #rate.sleep()
        if(useTrigger and (STTMemory().GetFloat("TriggerTimestamp") + triggerTime) < time.time()):
            time.sleep(1)
            continue

        data = provider.Listen()

        if(len(data) == 0):
            print "None"
            continue

        print "We got:", data

        FileLogger().Info("STT, RunSTT(), Input Data: {0}".format(data))

        rospy.loginfo("STT|{0}".format(data))
        pub.publish("STT|{0}".format(data))


if __name__ == "__main__":
    if(Pid.HasPid("STT")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("STT")

    try:
        InitSettings()
        RunSTT()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("STT")
