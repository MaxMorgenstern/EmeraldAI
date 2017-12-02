#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.ROS.Helper import TFHelper
from EmeraldAI.Logic.ROS.Helper import GeometryHelper

import rospy
import os

import tf_conversions as tf_conv

from sensor_msgs.msg import Imu

class SerialImuToImu():
    __metaclass__ = Singleton

    Length = 14

    def __init__(self):
        uid = str(os.getpid())
        rospy.init_node("serial_reader_imu_{0}".format(uid))
        rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))

        self.__imuPublisher = rospy.Publisher('/imu', Imu, queue_size=10)

    def Validate(self, data):
        if(data is None):
            return False
        if(len(data) != self.Length):
            return False
        if(data[0].lower() == "MPU6050".lower() || 
            data[0].lower() == "MPU6500".lower() || 
            data[0].lower() == "MPU9150".lower() || 
            data[0].lower() == "MPU9250".lower()):
            return True
        return False

    def Process(self, data, imuFrameID, imuParentFrameID, translation):
        Y = GeometryHelper.DegreeToRadian(float(data[2]))
        P = GeometryHelper.DegreeToRadian(float(data[3]))
        R = GeometryHelper.DegreeToRadian(float(data[4]))

        GyroX = float(data[5])
        GyroY = float(data[6])
        GyroZ = float(data[7])

        AccelX = float(data[8])
        AccelY = float(data[9])
        AccelZ = float(data[10])

        MagnetX = float(data[11])
        MagnetY = float(data[12])
        MagnetZ = float(data[13])


        imuMessage = Imu()
        imuMessage.header.frame_id = imuFrameID
        imuMessage.header.stamp = rospy.Time.now()
        quaternion = tf_conv.transformations.quaternion_from_euler(Y, P, R, 'rzyx')
        
        imuMessage.orientation.x = quaternion[0]
        imuMessage.orientation.y = quaternion[1]
        imuMessage.orientation.z = quaternion[2]
        imuMessage.orientation.w = quaternion[3]
        imuMessage.orientation_covariance = [0.0025, 0, 0, 0, 0.0025, 0, 0, 0, 0.0025]
        
        imuMessage.linear_acceleration.x = AccelX
        imuMessage.linear_acceleration.y = AccelY
        imuMessage.linear_acceleration.z = AccelZ
        imuMessage.linear_acceleration_covariance = [0.02, 0, 0, 0, 0.02, 0, 0, 0, 0.02]
        
        imuMessage.angular_velocity.x = GyroX
        imuMessage.angular_velocity.y = GyroY
        imuMessage.angular_velocity.z = GyroZ
        imuMessage.angular_velocity_covariance = [0.04, 0, 0, 0, 0.04, 0, 0, 0, 0.04]


        rospy.loginfo(imuMessage)

        self.__imuPublisher.publish(imuMessage)
        
        TFHelper.SendTF2Transform(
            translation,
            quaternion,
            imuMessage.header.stamp,
            imuFrameID,
            imuParentFrameID)
