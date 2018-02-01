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

        self.__laserPublisherFront = rospy.Publisher('/radar/laser/front', LaserScan, queue_size=20)
        self.__laserPublisherBack = rospy.Publisher('/radar/laser/back', LaserScan, queue_size=20)

        # TODO - hardcoded values - min and max range to config
        self.__laserMessage = LaserScan()
        self.__laserMessage.angle_min = -0.025
        self.__laserMessage.angle_max = 0.025
        self.__laserMessage.angle_increment = 0.025
        self.__laserMessage.time_increment = 0.01
        self.__laserMessage.range_min = 0.05
        self.__laserMessage.range_max = 2.00

    def Validate(self, data):
        if(data is None):
            return False
        if(len(data) != self.Length):
            return False
        if(data[0].lower() == "Ultrasonic".lower()):
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

        if moduleName == "front":
            self.__laserPublisherFront.publish(self.__laserMessage)
        if moduleName == "back":
            self.__laserPublisherBack.publish(self.__laserMessage)

        if (sendTF):
            quaternion = tf_conv.transformations.quaternion_from_euler(0, 0, GeometryHelper.DegreeToRadian(modulePosition))
            TFHelper.SendTF2Transform(
                translation,
                quaternion,
                self.__laserMessage.header.stamp,
                calculatedLaserFrameID,
                rangeParentFrameID)
