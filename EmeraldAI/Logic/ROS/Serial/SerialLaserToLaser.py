#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.ROS.Helper import TFHelper
from EmeraldAI.Logic.ROS.Helper import GeometryHelper
from EmeraldAI.Config.HardwareConfig import *

import rospy
import os

import tf_conversions as tf_conv

from sensor_msgs.msg import LaserScan

class SerialLaserToLaser():
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

        self.__laserMessage = LaserScan()
        self.__laserMessage.angle_min = HardwareConfig().GetFloat("Laser.SinglePoint", "AngleMin")
        self.__laserMessage.angle_max = HardwareConfig().GetFloat("Laser.SinglePoint", "AngleMax")
        self.__laserMessage.angle_increment = HardwareConfig().GetFloat("Laser.SinglePoint", "AngleIncrement")
        self.__laserMessage.time_increment = HardwareConfig().GetFloat("Laser.SinglePoint", "TimeIncrement")
        self.__laserMessage.range_min = round(HardwareConfig().GetFloat("Laser.SinglePoint", "RangeMin") / 100.0, 2)
        self.__laserMessage.range_max = round(HardwareConfig().GetFloat("Laser.SinglePoint", "RangeMax") / 100.0, 2)

    def Validate(self, data):
        if(data is None):
            return False
        if(len(data) != self.Length):
            return False
        if(data[0].lower() == "Laser".lower()):
            return True
        return False

    def Process(self, data, rangeFrameID="radar_laser", rangeParentFrameID="radar_mount", translation=(0, 0, 0), sendTF=True):
        moduleName = data[1].lower()
        modulePosition = int(data[2])
        moduleRange = int(data[3]) # range in mm

        calculatedLaserFrameID = "{0}_{1}".format(rangeFrameID, moduleName)

        moduleRangeInMeter = round(moduleRange / 1000.0, 3)

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
