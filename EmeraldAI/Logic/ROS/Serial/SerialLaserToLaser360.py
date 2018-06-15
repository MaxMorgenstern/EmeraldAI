#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.ROS.Helper import TFHelper
from EmeraldAI.Logic.ROS.Helper import GeometryHelper
from EmeraldAI.Config.HardwareConfig import *

from Queue import Queue

import rospy
import os

import tf_conversions as tf_conv

from sensor_msgs.msg import LaserScan

class SerialLaserToLaser360():
    __metaclass__ = Singleton

    Length = 5

    def __init__(self):
        uid = str(os.getpid())
        try:
            print "Initialize: serial_converter_{0}".format(uid)
            rospy.init_node("serial_converter_{0}".format(uid), log_level=rospy.WARN)
        except:
            print "Node already initialized: ".format(rospy.get_caller_id())
        rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))

        self.__laserPublisher360 = rospy.Publisher('/radar/laser/360', LaserScan, queue_size=20)

        self.__laserMessage = LaserScan()
        self.__laserMessage.range_min = round(HardwareConfig().GetFloat("Laser.FullRange", "RangeMin") / 100.0, 2)
        self.__laserMessage.range_max = round(HardwareConfig().GetFloat("Laser.FullRange", "RangeMax") / 100.0, 2)
        
        self.__laserScannerCount = HardwareConfig().GetInt("Laser.FullRange", "LaserScannerCount")
        self.__laserPointQueue = Queue(self.__laserScannerCount)

        self.__laserDictionary = {}


    def __clearLaserArray(self):
        self.__laserDictionary = {}
        while not self.__laserPointQueue.empty():
            queueItem = self.__laserPointQueue.get()
            for key in queueItem:
                self.__laserDictionary[key] = queueItem[key]


    def __addToQueue(self, item):
        if self.__laserPointQueue.full():
            self.__laserPointQueue.get()
        self.__laserPointQueue.put(item)

    
    def Validate(self, data):
        if(data is None):
            return False
        if(len(data) != self.Length):
            return False
        if(data[0].lower() == "Laser360".lower()):
            return True
        return False

    def Process(self, data, rangeFrameID="radar_laser_360", rangeParentFrameID="radar_mount", translation=(0, 0, 0), sendTF=True):
        #moduleName = data[1].lower()
        modulePosition = int(data[2])
        moduleRange = int(data[3]) # range in mm
        moduleStepInDegree = int(data[4])

        maxValueCount = 360 / moduleStepInDegree

        moduleRangeInMeter = round(moduleRange / 1000.0, 3)
        if(moduleRangeInMeter >= self.__laserMessage.range_max):
            moduleRangeInMeter = float('inf')

        self.__laserDictionary[modulePosition] = moduleRangeInMeter
        self.__addToQueue({modulePosition:moduleRangeInMeter})

        print len(self.__laserDictionary)
        print self.__laserDictionary
        print "-----"

        if(len(self.__laserDictionary) == maxValueCount):
            self.__laserMessage.ranges = [moduleRangeInMeter, moduleRangeInMeter, moduleRangeInMeter]
            self.__laserMessage.header.stamp = rospy.Time.now()
            self.__laserMessage.header.frame_id = rangeFrameID
            rospy.loginfo(self.__laserMessage)

            self.__laserPublisher360.publish(self.__laserMessage)

            """
            # TODO: PArameter in method call
            if (sendTF):
                quaternion = tf_conv.transformations.quaternion_from_euler(0, 0, GeometryHelper.DegreeToRadian(modulePosition))
                TFHelper.SendTF2Transform(
                    translation,
                    quaternion,
                    self.__laserMessage.header.stamp,
                    rangeFrameID,
                    rangeParentFrameID)
            """

            self.__clearLaserArray()
