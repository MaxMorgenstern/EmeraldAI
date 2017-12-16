#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.ROS.Helper import TFHelper
from EmeraldAI.Logic.ROS.Helper import GeometryHelper

import rospy
import os
import math

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

        self.__rangePublisherFront = rospy.Publisher('/range/radar/front', Range, queue_size=10)
        self.__rangePublisherBack = rospy.Publisher('/range/radar/back', Range, queue_size=10)

    def Validate(self, data):
        if(data is None):
            return False
        if(len(data) != self.Length):
            return False
        if(data[0].lower() == "Ultrasonic".lower()):
            return True
        return False

    def Process(self, data, rangeFrameID="/radar_ultrasonic", rangeParentFrameID="/radar_ultrasonic_mount", translation=(0, 0, 0), sendTF=False):
        moduleName = data[1].lower()
        modulePosition = int(data[2])
        moduleRange = int(data[3])

        rangeFrameIDTemplate = "{0}_{1}"
        calculatedRangeFrameID = rangeFrameIDTemplate.format(rangeFrameID, moduleName)


        rangeMessage = Range()
        rangeMessage.radiation_type = 0
        rangeMessage.min_range = 0.05
        rangeMessage.max_range = 2.50
        rangeMessage.field_of_view = (math.pi/4/45*20) # 20deg
        rangeMessage.radiation_type = 0

        rangeMessage.header.frame_id = calculatedRangeFrameID
        rangeMessage.range = moduleRange / 100.0
        rangeMessage.header.stamp = rospy.Time.now()


        rospy.loginfo(rangeMessage)

        if moduleName == "front":
            self.__rangePublisherFront.publish(rangeMessage)
        if moduleName == "back":
            self.__rangePublisherBack.publish(rangeMessage)

        if (sendTF):
            quaternion = tf_conv.transformations.quaternion_from_euler(0, 0, GeometryHelper.DegreeToRadian(modulePosition))
            TFHelper.SendTF2Transform(
                translation,
                quaternion,
                rangeMessage.header.stamp,
                calculatedRangeFrameID,
                rangeParentFrameID)
