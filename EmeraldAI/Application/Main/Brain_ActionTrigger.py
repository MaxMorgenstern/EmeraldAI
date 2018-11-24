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
from EmeraldAI.Logic.Logger import *
from EmeraldAI.Logic.Memory.Brain import Brain as BrainMemory
from EmeraldAI.Pipelines.TriggerProcessing.ProcessTrigger import ProcessTrigger
from EmeraldAI.Entities.User import User


class BrainActionTrigger:
    def __init__(self):    	

        self.__UnknownUserTag = Config().Get("Application.Brain", "UnknownUserTag")

        rospy.init_node('emerald_brain_actiontrigger_node', anonymous=True)

    	#self.__TriggerPublisher = rospy.Publisher('/emerald_ai/action/trigger', String, queue_size=10)

        self.__ResponsePublisher = rospy.Publisher('/emerald_ai/io/text_to_speech', String, queue_size=10)

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
        if (dataParts[0] == "PERSON" and dataParts[1] != self.__UnknownUserTag):

            # TODO - check if we saw the user today
            print dataParts
            User().SetUserByCVTag(dataParts[1])
            print User()
            #user.LastSpokenTo
            #datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            response = ProcessTrigger().ProcessCategory("Greeting")

            lastAudioTimestamp = BrainMemory().GetString("Brain.Trigger.AudioTimestamp", 20)
            if(lastAudioTimestamp is None and len(response) > 1):
                FileLogger().Info("TTS, callback(), Audio: {0}".format(response))
                self.__ResponsePublisher.publish("TTS|{0}".format(response))



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
