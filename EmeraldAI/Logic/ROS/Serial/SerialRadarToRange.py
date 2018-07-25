#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.ROS.Helper import TFHelper
from EmeraldAI.Logic.ROS.Helper import GeometryHelper
from EmeraldAI.Config.HardwareConfig import *

import rospy
import os

import tf_conversions as tf_conv

from sensor_msgs.msg import Range

class SerialRadarToRange():
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

        self.__rangePublisherFront = rospy.Publisher('/emerald_ai/serial/radar/range/front', Range, queue_size=10)
        self.__rangePublisherBack = rospy.Publisher('/emerald_ai/serial/radar/range/back', Range, queue_size=10)

        self.__rangeMessage = Range()
        self.__rangeMessage.radiation_type = 0
        self.__rangeMessage.min_range = HardwareConfig().GetFloat("Ultrasonic", "RangeMin") / 100.0
        self.__rangeMessage.max_range = HardwareConfig().GetFloat("Ultrasonic", "RangeMax") / 100.0
        self.__rangeMessage.field_of_view = HardwareConfig().GetFloat("Ultrasonic", "FieldOfView")
        self.__rangeMessage.radiation_type = 0

    def Validate(self, data):
        if(data is None):
            return False
        if(len(data) != self.Length):
            return False
        if(data[0].lower() == "Ultrasonic".lower()):
            return True
        return False

    def Process(self, data, rangeFrameID="radar_ultrasonic", rangeParentFrameID="radar_mount", translation=(0, 0, 0), sendTF=True):
        moduleName = data[1].lower()
        modulePosition = int(data[2])
        moduleRange = int(data[3]) # range in cm

        calculatedRangeFrameID = "{0}_{1}".format(rangeFrameID, moduleName)

        moduleRangeInMeter = round(moduleRange / 100.0, 3)

        self.__rangeMessage.range = moduleRangeInMeter
        self.__rangeMessage.header.stamp = rospy.Time.now()
        self.__rangeMessage.header.frame_id = calculatedRangeFrameID
        rospy.loginfo(self.__rangeMessage)

        if moduleName == "front":
            self.__rangePublisherFront.publish(self.__rangeMessage)
        if moduleName == "back":
            self.__rangePublisherBack.publish(self.__rangeMessage)

        if (sendTF):
            quaternion = tf_conv.transformations.quaternion_from_euler(0, 0, GeometryHelper.DegreeToRadian(modulePosition))
            TFHelper.SendTF2Transform(
                translation,
                quaternion,
                self.__rangeMessage.header.stamp,
                calculatedRangeFrameID,
                rangeParentFrameID)

