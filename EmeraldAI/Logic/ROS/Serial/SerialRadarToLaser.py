#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.ROS.Helper import TFHelper
from EmeraldAI.Logic.ROS.Helper import GeometryHelper

import rospy
import os
import math

import tf_conversions as tf_conv

from sensor_msgs.msg import LaserScan

class SerialRadarToLaser():
    __metaclass__ = Singleton

    Length = 4

    def __init__(self):
        uid = str(os.getpid())
        try:
            print "Initialize: serial_converter_{0}".format(uid)
            rospy.init_node("serial_converter_{0}".format(uid), log_level=rospy.WARN)
        except:
            print "Node already initialized: ".format(rospy.get_caller_id())
        rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))

        self.__laserPublisherOne = rospy.Publisher('/radar/laser/one', LaserScan, queue_size=20)
        self.__laserPublisherTwo = rospy.Publisher('/radar/laser/two', LaserScan, queue_size=20)
        self.__laserPublisherThree = rospy.Publisher('/radar/laser/three', LaserScan, queue_size=20)
        self.__laserPublisherFour = rospy.Publisher('/radar/laser/four', LaserScan, queue_size=20)

        # TODO - hardcoded values - min and max range to config
        self.__laserMessage = LaserScan()
        self.__laserMessage.angle_min = -0.0058 # 0.332 degree
        self.__laserMessage.angle_max = 0.0058 # 0.332 degree
        self.__laserMessage.angle_increment = 0.0058 # 0.332 degree
        self.__laserMessage.time_increment = 0.01
        self.__laserMessage.range_min = 0.05
        self.__laserMessage.range_max = 2.00

    def Validate(self, data):
        if(data is None):
            return False
        if(len(data) != self.Length):
            return False
        if(data[0].lower() == "Laser".lower()):
            return True
        return False

    def Process(self, data, rangeFrameID="/radar_laser", rangeParentFrameID="/radar_mount", translation=(0, 0, 0), sendTF=True):
        moduleName = data[1].lower()
        modulePosition = int(data[2])
        moduleRange = int(data[3])

        calculatedLaserFrameID = "{0}_{1}".format(rangeFrameID, moduleName)

        moduleRangeInMeter = moduleRange / 100.0

        self.__laserMessage.ranges = [moduleRangeInMeter, moduleRangeInMeter, moduleRangeInMeter]
        self.__laserMessage.header.stamp = rospy.Time.now()
        self.__laserMessage.header.frame_id = calculatedLaserFrameID
        rospy.loginfo(self.__laserMessage)

        if moduleName == "one":
            self.__laserPublisherOne.publish(self.__laserMessage)
        if moduleName == "two":
            self.__laserPublisherTwo.publish(self.__laserMessage)
        if moduleName == "three":
            self.__laserPublisherThree.publish(self.__laserMessage)
        if moduleName == "four":
            self.__laserPublisherFour.publish(self.__laserMessage)

        if (sendTF):
            quaternion = tf_conv.transformations.quaternion_from_euler(0, 0, GeometryHelper.DegreeToRadian(modulePosition))
            TFHelper.SendTF2Transform(
                translation,
                quaternion,
                self.__laserMessage.header.stamp,
                calculatedLaserFrameID,
                rangeParentFrameID)
