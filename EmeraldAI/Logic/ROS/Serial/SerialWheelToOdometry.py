#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.ROS.Helper import TFHelper
from EmeraldAI.Logic.ROS.Helper import GeometryHelper

import rospy
import os
import sys
import math

import tf2_ros as tf
import tf_conversions as tf_conv

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

class SerialWheelToOdometry():
    __metaclass__ = Singleton

    Length = 10

    def __init__(self, wheelDiameter, wheelBaseline, encoderTicksPerRevelation):
        uid = str(os.getpid())
        rospy.init_node("serial_reader_odometry_{0}".format(uid))
        rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))

        self.__odomPublisher = rospy.Publisher('/odom', Odometry, queue_size=10)

        self.__wheelDiameter = wheelDiameter # mm
        self.__wheelBaseline = wheelBaseline # distance between wheels in mm
        self.__encoderTicksPerRevelation = encoderTicksPerRevelation

        self.__wheelDistancePerTickLeft = math.pi * self.__wheelDiameter / self.__encoderTicksPerRevelation
        self.__wheelDistancePerTickRight = math.pi * self.__wheelDiameter / self.__encoderTicksPerRevelation

        # start position
        self.__x = 0.0
        self.__y = 0.0
        self.__th = 0.0

        self.__currentTime = rospy.Time.now()
        self.__lastTime = rospy.Time.now()


    def Validate(self, data):
        if(data is None):
            return False
        if(len(data) != self.Length):
            return False
        if(data[0].lower() == "Wheel".lower()):
            return True
        return False


    def Process(self, data, odomFrameID, odomParentFrameID):
        clicksLeft = int(data[4])
        clicksLeftDelta = int(data[5])

        clicksRight = int(data[8])
        clicksRightDelata = int(data[9])

        self.__currentTime = rospy.Time.now()

        distanceLeftDelta = clicksLeftDelta * self.__wheelDistancePerTickLeft
        distanceRightDelata = clicksRightDelata * self.__wheelDistancePerTickRight

        estimatedDistance = (distanceRightDelata + distanceLeftDelta) / 2  / 1000 # mm to m
        estimatedRotation = (distanceRightDelata - distanceLeftDelta) / self.__wheelBaseline

        dt = (self.__currentTime - self.__lastTime).to_sec()
        self.__lastTime = self.__currentTime

        if (estimatedDistance != 0): 
            # calculate distance traveled in x and y
            xTmp = math.cos(estimatedRotation) * estimatedDistance
            yTmp = -math.sin(estimatedRotation) * estimatedDistance
            # calculate the final position of the robot
            self.__x += (math.cos(self.__th) * xTmp - math.sin(self.__th) * yTmp) * dt
            self.__y += (math.sin(self.__th) * xTmp + math.cos(self.__th) * yTmp) * dt

        if (estimatedRotation != 0):
            self.__th += estimatedRotation * dt
        
        # create the quaternion
        quaternion = Quaternion()
        quaternion.x = 0.0
        quaternion.y = 0.0
        quaternion.z = math.sin(self.__th / 2)
        quaternion.w = math.cos(self.__th / 2)


        odomMessage = Odometry()
        odomMessage.header.frame_id = odomParentFrameID
        odomMessage.child_frame_id = odomFrameID

        odomMessage.header.stamp = self.__currentTime

        # set the position
        odomMessage.pose.pose = Pose(Point(self.__x, self.__y, 0.), quaternion)

        # set the velocity
        odomMessage.twist.twist = Twist(Vector3(estimatedDistance, 0, 0), Vector3(0, 0, estimatedRotation))

        rospy.loginfo(odomMessage)
        
        self.__odomPublisher.publish(odomMessage)

        TFHelper.SendTF2Transform(
            (self.__x, self.__y, 0.),
            (quaternion.x, quaternion.y, quaternion.z, quaternion.w),
            odomMessage.header.stamp,
            odomFrameID,
            odomParentFrameID)
