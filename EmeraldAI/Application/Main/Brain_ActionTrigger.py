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


class BrainActionTrigger:
    def __init__(self):
    	print "todo"

    	self.__TriggerPublisher = rospy.Publisher('/emerald_ai/io/action_trigger', String, queue_size=10)

    	# in order to check if someone says something
        #rospy.Subscriber("/emerald_ai/io/speech_to_text/word", String, self.wordCallback)


    	# in order to check if someone is present
        #rospy.Subscriber("/emerald_ai/io/person", String, self.personCallback)


        rospy.spin()


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
