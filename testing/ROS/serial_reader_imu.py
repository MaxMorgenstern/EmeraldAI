#!/usr/bin/env python
from __future__ import division

import serial
import rospy
import os
import sys
import math

import tf2_ros as tf
import tf_conversions as tf_conv

from sensor_msgs.msg import Imu
from geometry_msgs.msg import TransformStamped


def RadianToDegree(rad):
    return (rad * 4068) / 71.0

def DegreeToRadian(deg):
    return (deg * 71) / 4068.0

def SendTF2Transform(transformBroadcaster, translation, rotation, time, child_frame_id, frame_id):
    t = TransformStamped()
 
    t.header.stamp = time
    t.header.frame_id = frame_id
    t.child_frame_id = child_frame_id
    t.transform.translation.x = translation[0]
    t.transform.translation.y = translation[1]
    t.transform.translation.z = translation[2]
    #t.transform.rotation = rotation

    t.transform.rotation.x = rotation[0]
    t.transform.rotation.y = rotation[1]
    t.transform.rotation.z = rotation[2]
    t.transform.rotation.w = rotation[3]

    transformBroadcaster.sendTransform(t)

if __name__=="__main__":

	uid = str(os.getpid())
	rospy.init_node("serial_reader_{0}".format(uid))
	rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))

	imuPub = rospy.Publisher('/imu', Imu, queue_size=10)
	transformBroadcaster = tf.TransformBroadcaster()

	port_name = "/dev/ttyUSB0"
	baud = 230400

	if len(sys.argv) >= 2 :
		port_name  = sys.argv[1]

	if len(sys.argv) >= 3 :
		baud  = int(sys.argv[2])

	ser = serial.Serial(port_name, baud)

	imuParentFrameID = "/odom"
	imuFrameID = "/imu_sensor"
	imuMessage = Imu()
	imuMessage.header.frame_id = imuFrameID

	while True:
		line = ser.readline().rstrip()
		if(len(line) <= 1):
			continue

		data = line.split("|")
		if(len(data) <= 1):
			continue
		
		print data

		# we expect 14 values from the ultrasonic node
		if(len(data) != 14):
			continue
		sensor = data[0]
		timestamp = data[1]

		Y = DegreeToRadian(float(data[2]))
		P = DegreeToRadian(float(data[3]))
		R = DegreeToRadian(float(data[4]))

		GyroX = float(data[5])
		GyroY = float(data[6])
		GyroZ = float(data[7])

		AccelX = float(data[8])
		AccelY = float(data[9])
		AccelZ = float(data[10])

		MagnetX = float(data[11])
		MagnetY = float(data[12])
		MagnetZ = float(data[13])



		imuMessage.header.stamp = rospy.Time.now()
		quaternion = tf_conv.transformations.quaternion_from_euler(Y, P, R, 'rzyx')
		#quaternion = tf_conv.transformations.quaternion_from_euler(R, P, Y)
		
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
		

		#rospy.loginfo(imuMessage)
		imuPub.publish(imuMessage)

		# translation (x,y,z), rotation(yaw-pitch-roll (ZYX) ), time, child, parent
		#transformBroadcaster.sendTransform((0, 0, 1),
		#	quaternion,
		#	rospy.Time.now(),
		#	imuMessage.header.frame_id,
		#	imuParentFrameID)
		SendTF2Transform(transformBroadcaster,
			(0, 0, 0.5),
			quaternion,
			rospy.Time.now(),
			imuMessage.header.frame_id,
			imuParentFrameID)

		

print "Bye!"
