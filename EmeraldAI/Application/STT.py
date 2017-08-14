#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Pipelines.SpeechToText.STT import STT
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
    pub = rospy.Publisher('to_brain', String, queue_size=10)

    rospy.Subscriber("trigger", String, callback)

    rospy.init_node('STT_node', anonymous=True)
    rospy.Rate(10) # 10hz

    useTrigger = Config().GetBoolean("Application.SpeechToText", "Trigger")
    triggerTime = Config().GetInt("Application.SpeechToText", "TriggerTime")

    while True:
        #rate.sleep()
        if(useTrigger and (STTMemory().GetFloat("TriggerTimestamp") + triggerTime) < time.time()):
            time.sleep(1)
            continue

        data = STT().Process(False)
        if(data is None):
            print "None"
            continue
        print "We got:", data

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
