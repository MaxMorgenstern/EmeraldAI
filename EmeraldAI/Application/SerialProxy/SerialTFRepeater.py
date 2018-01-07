#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.ROS.Helper.TFLooper import TFLooper

import rospy
import tf2_ros as tf

from geometry_msgs.msg import TransformStamped
from tf2_msgs.msg import TFMessage

nodeName = 'serial_tf_repeater'

def callback(data):
    if data._connection_header['callerid'].strip("/") == nodeName:
        return

    for t in data.transforms:
        TFLooper().add(t)


def listener():
    rateInHz = 20 # in Hz
    rospy.init_node(nodeName)
    rospy.Subscriber("tf", TFMessage, callback)

    rate = rospy.Rate(rateInHz) # hz
    while not rospy.is_shutdown():
        TFLooper().loop()
        rate.sleep()


if __name__=="__main__":
    listener()
