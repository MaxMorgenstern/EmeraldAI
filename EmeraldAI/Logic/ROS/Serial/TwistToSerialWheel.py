#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from EmeraldAI.Logic.Singleton import Singleton

import rospy
import os
import math

from geometry_msgs.msg import Twist


class TwistToSerialWheel():
    __metaclass__ = Singleton

    Length = 10

    def __init__(self, wheelDiameter, wheelBaseline, encoderTicksPerRevelation):
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

        #self.__wheelDiameter = wheelDiameter # mm
        self.__wheelBaseline = wheelBaseline # distance between wheels in mm
        #self.__encoderTicksPerRevelation = encoderTicksPerRevelation

        #self.__wheelDistancePerTickLeft = math.pi * self.__wheelDiameter / self.__encoderTicksPerRevelation
        #self.__wheelDistancePerTickRight = math.pi * self.__wheelDiameter / self.__encoderTicksPerRevelation

        self.__currentTime = rospy.Time.now()
        self.__lastTime = rospy.Time.now()

        rospy.Subscriber('/navigation/twist', Twist, self.__twistCallback)


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
                self.__left = 1.0 * self.__dx - self.__dr * self.__wheelBaseline / 2
            self.__ticksSinceLastTwistInstruction += 1


    def ProcessPID(self, data):
        clicksLeft = int(data[4])
        clicksLeftDelta = int(data[5])

        clicksRight = int(data[8])
        clicksRightDelata = int(data[9])

        #self.__currentTime = rospy.Time.now()












    def spinOnce(self):
        self.previous_error = 0.0
        self.prev_vel = [0.0] * self.rolling_pts
        self.integral = 0.0
        self.error = 0.0
        self.derivative = 0.0
        self.vel = 0.0

        # only do the loop if we've recently recieved a target velocity message
        while not rospy.is_shutdown() and self.ticks_since_target < self.timeout_ticks:
            self.calcVelocity()
            self.doPid()
            self.pub_motor.publish(self.motor)
            self.r.sleep()
            self.ticks_since_target += 1
            if self.ticks_since_target == self.timeout_ticks:
                self.pub_motor.publish(0)



    def doPid(self):
    #####################################################
        pid_dt_duration = rospy.Time.now() - self.prev_pid_time
        pid_dt = pid_dt_duration.to_sec()
        self.prev_pid_time = rospy.Time.now()

        self.error = self.target - self.vel
        self.integral = self.integral + (self.error * pid_dt)
        # rospy.loginfo("i = i + (e * dt):  %0.3f = %0.3f + (%0.3f * %0.3f)" % (self.integral, self.integral, self.error, pid_dt))
        self.derivative = (self.error - self.previous_error) / pid_dt
        self.previous_error = self.error

        self.motor = (self.Kp * self.error) + (self.Ki * self.integral) + (self.Kd * self.derivative)

        if self.motor > self.out_max:
            self.motor = self.out_max
            self.integral = self.integral - (self.error * pid_dt)
        if self.motor < self.out_min:
            self.motor = self.out_min
            self.integral = self.integral - (self.error * pid_dt)

        if (self.target == 0):
            self.motor = 0

        rospy.logdebug("vel:%0.2f tar:%0.2f err:%0.2f int:%0.2f der:%0.2f ## motor:%d " %
                      (self.vel, self.target, self.error, self.integral, self.derivative, self.motor))



