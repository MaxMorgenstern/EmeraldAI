#!/usr/bin/env python
from __future__ import division

import serial
import rospy
import os
import sys
import math
import tf

from sensor_msgs.msg import Imu


def RadianToDegree(rad):
    return (rad * 4068) / 71.0

def DegreeToRadian(deg):
    return (deg * 71) / 4068.0


if __name__=="__main__":

	uid = str(os.getpid())
	rospy.init_node("serial_reader_{0}".format(uid))
	rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))

	imuPub = rospy.Publisher('/imu', Imu, queue_size=10)
	transformBroadcaster = tf.TransformBroadcaster()

	port_name = "/dev/ttyUSB0"
	#baud = 57600 # 230400
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
		
		#print data

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
		quaternion = tf.transformations.quaternion_from_euler(Y, P, R, 'rzyx')
		
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
		transformBroadcaster.sendTransform((0, 0, 1),
			tf.transformations.quaternion_from_euler(0, 0, 0),
			rospy.Time.now(),
			imuMessage.header.frame_id,
			imuParentFrameID)

		

print "Bye!"
