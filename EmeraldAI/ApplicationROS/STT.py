#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Pipelines.SpeechToText.STT import STT

def RunTTS():
    pub = rospy.Publisher('to_brain', String, queue_size=10)
    rospy.init_node('STT_node', anonymous=True)
    #rate = rospy.Rate(10) # 10hz

    while True:
        #rate.sleep()
        data = STT().Process(False)
        if(data == None):
            continue

        rospy.loginfo("STT|{0}".format(data))
        pub.publish("STT|{0}".format(data))


if __name__ == "__main__":
    try:
        RunTTS()
    except KeyboardInterrupt:
        print "End"
