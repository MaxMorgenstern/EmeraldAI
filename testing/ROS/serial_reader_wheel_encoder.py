#!/usr/bin/env python
from __future__ import division

import serial
import rospy
import os
import sys
import math

from nav_msgs.msg import Odometry


def RadianToDegree(rad):
    return (rad * 4068) / 71.0

def DegreeToRadian(deg):
    return (deg * 71) / 4068.0


if __name__=="__main__":

	uid = str(os.getpid())
	rospy.init_node("serial_reader_{0}".format(uid))
	rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))

	odomPub1 = rospy.Publisher('/odom/wheels/1', Odometry, queue_size=10)
	odomPub2 = rospy.Publisher('/odom/wheels/2', Odometry, queue_size=10)

	port_name = "/dev/ttyUSB0"
	#baud = 57600 # 230400
	baud = 230400

	if len(sys.argv) >= 2 :
		port_name  = sys.argv[1]

	if len(sys.argv) >= 3 :
		baud  = int(sys.argv[2])

	ser = serial.Serial(port_name, baud)

	odomParentFrameID = "/odom"
	odomFrameID = "/base_link"
	odomMsg = Odometry()
	odomMsg.header.frame_id = odomParentFrameID
	odom.child_frame_id = odomFrameID



	while True:
		line = ser.readline().rstrip()
		if(len(line) <= 1):
			continue

		data = line.split("|")
		if(len(data) <= 1):
			continue
		#print data

		# we expect 4 values from the ultrasonic node
		if(len(data) > 8):
			continue
		
		messageType = data[0]
		moduleID = int(data[1])
		timestamp = int(data[2])
		count = int(data[3])
		timestampDelta = int(data[4])
		countDelata = int(data[5])
		stepsPerRevelation = int(data[6])
		distanceInMMPerRevelation = int(data[7])

		odomMsg.header.stamp = rospy.Time.now()



		#rospy.loginfo(odomMsg)
		if moduleID == 1:
			odomPub1.publish(odomMsg)
		if moduleID == 2:	
			odomPub2.publish(odomMsg)

		

print "Bye!"
