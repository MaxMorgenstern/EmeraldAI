#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.ROS.Helper.TFLooper import TFLooper
from EmeraldAI.Logic.Modules import Pid

import rospy
import tf2_ros as tf

from geometry_msgs.msg import TransformStamped
from tf2_msgs.msg import TFMessage

nodeName = 'serial_tf_repeater'
nodeNameToRepeat = 'serial_converter_'

def callback(data):
    if not data._connection_header['callerid'].strip('/').startswith(nodeNameToRepeat):
        return

    for t in data.transforms:
        TFLooper().add(t)


def mainLoop():
    rateInHz = 20 # in Hz
    rospy.init_node(nodeName)
    rospy.Subscriber('tf', TFMessage, callback)

    rate = rospy.Rate(rateInHz) # hz
    while not rospy.is_shutdown():
        TFLooper().loop()
        rate.sleep()


if __name__=='__main__':
    if(Pid.HasPid("SerialTFRepeater")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("SerialTFRepeater")
    try:
        mainLoop()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("SerialTFRepeater")
   