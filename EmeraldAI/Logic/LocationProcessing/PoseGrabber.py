#!/usr/bin/env python
import rospy

from nav_msgs.msg import Odometry
from EmeraldAI.Logic.Singleton import Singleton

class PoseGrabber(object):
    __metaclass__ = Singleton

    __timeout = 3

    def __init__(self):
        rospy.init_node("pose_grabber", anonymous=True)


    def GetPose(self): 
        try:
            msg = rospy.wait_for_message("/odometry/filtered", Odometry, self.__timeout)
        except Exception:
            return None
        return msg.pose.pose

