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

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Memory.Brain import Brain as BrainMemory


class BrainActionTrigger:
    def __init__(self):    	

        self.__UnknownUserTag = Config().Get("Application.Brain", "UnknownUserTag")

        rospy.init_node('emerald_brain_actiontrigger_node', anonymous=True)

    	self.__TriggerPublisher = rospy.Publisher('/emerald_ai/io/action_trigger', String, queue_size=10)

    	# in order to check if someone says something
        rospy.Subscriber("/emerald_ai/io/speech_to_text/word", String, self.ioCallback)

    	# in order to check if someone is present
        rospy.Subscriber("/emerald_ai/io/person", String, self.personCallback)

        rospy.spin()


    def ioCallback(self, data):
        dataParts = data.data.split("|")
        if dataParts[0] == "STT":
            BrainMemory().Set("Brain.Trigger.AudioTimestamp", time.time())


    def personCallback(self, data):
        dataParts = data.data.split("|")
        if dataParts[0] == "PERSON":
            lastAudioTimestamp = BrainMemory().GetString("Brain.Trigger.AudioTimestamp", 20)
            if (lastAudioTimestamp is None and dataParts[1] != self.__UnknownUserTag):
                # TODO Trigger
                print ""



if __name__ == "__main__":
    if(Pid.HasPid("Brain.Trigger")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Brain.Trigger")
    try:
        BrainActionTrigger()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Brain.Trigger")
