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

from EmeraldAI.Logic.SpeechProcessing.Google import Google
from EmeraldAI.Logic.SpeechProcessing.Microsoft import Microsoft
from EmeraldAI.Logic.SpeechProcessing.Wit import Wit
from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Logic.Memory.STT import STT as STTMemory
from EmeraldAI.Config.Config import Config
from EmeraldAI.Logic.Logger import FileLogger

def InitSettings():
    STTMemory().Set("TriggerTimestamp", time.time())


def callback(data):
    dataParts = data.data.split("|")
    if(dataParts[0] is "TRIGGER"):
        triggerType = Config().GetBoolean("Application.SpeechToText", "TriggerType") # KEY
        triggerKey = Config().GetBoolean("Application.SpeechToText", "TriggerKey") # ENTER
        if(dataParts[1] is triggerType and dataParts[2] is triggerKey):
            STTMemory().Set("TriggerTimestamp", time.time())


def RunSTT(printData):
    pub = rospy.Publisher('/emerald_ai/io/speech_to_text', String, queue_size=10)

    rospy.Subscriber("/emerald_ai/io/hardware_trigger", String, callback)

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

    if(sttProvider.lower() == "watson"):
        return  

    print sttProvider.lower()

    while True:
        #rate.sleep()
        if(useTrigger and (STTMemory().GetFloat("TriggerTimestamp") + triggerTime) < time.time()):
            time.sleep(1)
            continue

        data = provider.Listen()

        if(len(data) == 0):
            if(printData):
                print "None"
            continue
            
        if(printData):
            print "We got:", data

        FileLogger().Info("STT, RunSTT(), Input Data: {0}".format(data))

        rospy.loginfo("STT|{0}".format(data))
        pub.publish("STT|{0}".format(data))


if __name__ == "__main__":
    if(Pid.HasPid("STT")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("STT")

    printData = False
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if (arg.lower().startswith("-output")):
                printData = True

    try:
        InitSettings()
        RunSTT(printData)
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("STT")
