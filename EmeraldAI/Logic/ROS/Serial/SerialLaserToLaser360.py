#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.ROS.Helper import GeometryHelper
from EmeraldAI.Config.HardwareConfig import *

import rospy
import os

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

        self.__laserPublisher360One = rospy.Publisher('/radar/laser/360/one', LaserScan, queue_size=20)
        self.__laserPublisher360Two = rospy.Publisher('/radar/laser/360/two', LaserScan, queue_size=20)

        self.__laserMessage = LaserScan()
        self.__laserMessage.range_min = round(HardwareConfig().GetFloat("Laser.FullRange", "RangeMin") / 100.0, 2)
        self.__laserMessage.range_max = round(HardwareConfig().GetFloat("Laser.FullRange", "RangeMax") / 100.0, 2)

        self.__laserScannerCount = HardwareConfig().GetInt("Laser.FullRange", "LaserScannerCount")

        self.__laserDictionary = {}
        self.__laserDictionary["one"] = {}
        self.__laserDictionary["two"] = {}

        self.__laserScanStartTime = {}
        self.__laserScanStartTime["one"] = rospy.Time.now()
        self.__laserScanStartTime["two"] = rospy.Time.now()

        self.__laserScanStartAngle = {}
        self.__laserScanStartAngle["one"] = None
        self.__laserScanStartAngle["two"] = None

    def Validate(self, data):
        if(data is None):
            return False
        if(len(data) != self.Length):
            return False
        if(data[0].lower() == "Laser360".lower()):
            return True
        return False

    def Process(self, data, rangeFrameID="radar_laser_360", rangeParentFrameID="radar_mount", translation=(0, 0, 0), sendTF=True):
        moduleName = data[1].lower()
        modulePosition = int(data[2])
        moduleRange = int(data[3]) # range in mm
        moduleStepInDegree = int(data[4])

        maxValueCount = 360 / self.__laserScannerCount / moduleStepInDegree

        moduleRangeInMeter = round(moduleRange / 1000.0, 3)
        if(moduleRangeInMeter >= self.__laserMessage.range_max):
            moduleRangeInMeter = float('inf')

        self.__setLaserDict(moduleName, modulePosition, moduleRangeInMeter)

        dictReference = self.__getDict(moduleName)
        if(len(dictReference) == maxValueCount):
            scanTime = (rospy.Time.now() - self.__laserScanStartTime[moduleName]).nsecs/100000000
            self.__laserScanStartTime[moduleName] = rospy.Time.now()

            #print moduleName
            #print sorted(dictReference)
            #print dictReference


            if(self.__laserScanStartAngle[moduleName] > modulePosition):
                sortedDictReference = sorted(dictReference)
                minScanAngle = max(sorted(dictReference))
                maxScanAngle = min(sorted(dictReference))
            else:
                sortedDictReference = list(reversed(sorted(dictReference)))
                minScanAngle = min(sorted(dictReference))
                maxScanAngle = max(sorted(dictReference))
            


            rangeArray = []
            for key in sortedDictReference:
                #print key, dictReference[key]
                rangeArray.append(dictReference[key])


            self.__laserMessage.ranges = rangeArray
            self.__laserMessage.header.stamp = rospy.Time.now()
            self.__laserMessage.header.frame_id = rangeFrameID

            self.__laserMessage.time_increment = scanTime / maxValueCount
            self.__laserMessage.scan_time = scanTime

            self.__laserMessage.angle_min = GeometryHelper.DegreeToRadian(minScanAngle) # start angle
            self.__laserMessage.angle_max = GeometryHelper.DegreeToRadian(maxScanAngle) # end angle
            self.__laserMessage.angle_increment = (self.__laserMessage.angle_max - self.__laserMessage.angle_min) / maxValueCount


            rospy.loginfo(self.__laserMessage)
            if moduleName == "one":
                self.__laserPublisher360One.publish(self.__laserMessage)
            if moduleName == "two":
                self.__laserPublisher360Two.publish(self.__laserMessage)

            #print rangeArray
            #print "Last: ", modulePosition,  moduleRangeInMeter
            #print "Scan duration", scanTime
            #print "------"

            self.__clearLaserDict(moduleName)



    def __getDict(self, name):
        return self.__laserDictionary[name]

    def __clearLaserDict(self, name):
        self.__laserDictionary[name] = {}
        self.__laserScanStartAngle[name] = None

    def __setLaserDict(self, name, position, rangeInMeter):
        self.__laserDictionary[name][position] = rangeInMeter
        if(self.__laserScanStartAngle[name] is None):
            self.__laserScanStartAngle[name] = position
