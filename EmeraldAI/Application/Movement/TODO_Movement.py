#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
import time
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import rospy
from std_msgs.msg import String

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Config.Config import *

def RunMovement():

    rospy.init_node('movement_node', anonymous=True)

    rospy.Subscriber("/emerald_ai/movement/commander", String, callback)

    rospy.spin()


def callback(data):
    dataParts = data.data.split("|")
    print dataParts



if __name__ == "__main__":

    if(Pid.HasPid("Movement")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("Movement")
    try:
        RunMovement()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("Movement")
