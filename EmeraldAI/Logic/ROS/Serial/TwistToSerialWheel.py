#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.ROS.Helper.PIDController import PIDController

import rospy
import os
import math

from geometry_msgs.msg import Twist


class TwistToSerialWheel():
    __metaclass__ = Singleton

    Length = 10

    def __init__(self, wheelDiameter, wheelBaseline, encoderTicksPerRevelation, topic="/cmd_vel"):
        uid = str(os.getpid())
        try:
            print "Initialize: serial_converter_{0}".format(uid)
            rospy.init_node("serial_converter_{0}".format(uid), log_level=rospy.WARN)
        except:
            print "Node already initialized: ".format(rospy.get_caller_id())
        rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))

        self.__timeoutTicks = 5
        self.__ticksSinceLastTwistInstruction = self.__timeoutTicks
        self.__left = 0
        self.__right = 0

        self.__wheelBaseline = wheelBaseline # distance between wheels in mm

        self.__currentTime = rospy.Time.now()
        self.__lastTime = rospy.Time.now()

        self.__leftPidController = PIDController(rospy.Time.now())
        self.__rightPidController = PIDController(rospy.Time.now())

        rospy.Subscriber(topic, Twist, self.__twistCallback)


    def __twistCallback(self, msg):
        self.__ticksSinceLastTwistInstruction = 0
        self.__dx = msg.linear.x
        self.__dr = msg.angular.z
        self.__dy = msg.linear.y



    def Validate(self, data):
        if(data is None):
            return False
        if(len(data) != self.Length):
            return False
        if(data[0].lower() == "Wheel".lower()):
            return True
        return False


    def ProcessTwist(self):
        if (self.__ticksSinceLastTwistInstruction < self.__timeoutTicks):
            if(self.__ticksSinceLastTwistInstruction == 0):
                self.__right = 1.0 * self.__dx + self.__dr * self.__wheelBaseline / 2
                self.__rightPidController.SetTarget(self.__right)
                self.__left = 1.0 * self.__dx - self.__dr * self.__wheelBaseline / 2
                self.__leftPidController.SetTarget(self.__left)

            self.__ticksSinceLastTwistInstruction += 1


    def ProcessPID(self, data):
        clicksLeft = int(data[4])
        clicksLeftDelta = int(data[5])

        clicksRight = int(data[8])
        clicksRightDelata = int(data[9])

        self.__rightPidController.SetWheel(clicksRight)
        self.__leftPidController.SetWheel(clicksLeft)

        self.__rightVel = self.__rightPidController.MainLoop(rospy.Time.now())
        self.__leftVel = self.__leftPidController.MainLoop(rospy.Time.now())


    def GetMotorInstructions(self):
        return (self.__rightVel, self.__leftVel)


