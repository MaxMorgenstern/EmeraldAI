#!/usr/bin/env python
from __future__ import division

import serial
import rospy
import os
import sys
import math

from sensor_msgs.msg import Range

if __name__=="__main__":

	uid = str(os.getpid())
	rospy.init_node("serial_reader_{0}".format(uid))
	rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))

	ultasonicPubFront = rospy.Publisher('/radar/Ultrasonic/Front', Range, queue_size=10)
	ultasonicPubBack = rospy.Publisher('/radar/Ultrasonic/Back', Range, queue_size=10)


	port_name = "/dev/ttyUSB0"
	#baud = 57600 # 230400
	baud = 230400

	if len(sys.argv) >= 2 :
		port_name  = sys.argv[1]

	if len(sys.argv) >= 3 :
		baud  = int(sys.argv[2])

	ser = serial.Serial(port_name, baud)

	rangeFrameID = "/radar_ultrasonic_{0}"
	rangeMsg = Range()
	rangeMsg.radiation_type = 0
	rangeMsg.min_range = 0.05
	rangeMsg.max_range = 2.50
	rangeMsg.field_of_view = (math.pi/4/45*10) # 10deg
	rangeMsg.radiation_type = 0


	while True:
		line = ser.readline().rstrip()
		if(len(line) <= 1):
			continue

		data = line.split("|")
		if(len(data) <= 1):
			continue
		print data

		# we expect 4 values from the ultrasonic node
		if(len(data) > 4):
			continue
		

		messageType = data[0]
		moduleName = data[1].lower()
		modulePosition = data[2]
		moduleRange = int(data[3])

		rangeMsg.header.frame_id = rangeFrameID.format(moduleName)
		rangeMsg.range = moduleRange / 100.0
		rangeMsg.header.stamp = rospy.Time.now()


		rospy.loginfo(rangeMsg)
		if moduleName == "front":
			ultasonicPubFront.publish(rangeMsg)
		if moduleName == "back":	
			ultasonicPubBack.publish(rangeMsg)

		

print "Bye!"
