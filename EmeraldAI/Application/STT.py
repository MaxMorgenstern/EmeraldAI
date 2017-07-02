#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Pipelines.SpeechToText.STT import STT
from EmeraldAI.Logic.Modules import Pid

def RunSTT():
    pub = rospy.Publisher('to_brain', String, queue_size=10)
    rospy.init_node('STT_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    while True:
        #rate.sleep()
        data = STT().Process(False)
        if(data == None):
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
        RunSTT()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("STT")
