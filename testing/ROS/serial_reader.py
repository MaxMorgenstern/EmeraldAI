#!/usr/bin/env python

import serial
import rospy
import os
import sys

from sensor_msgs.msg import LaserScan, Range

if __name__=="__main__":

	uid = str(os.getpid())
	rospy.init_node("serial_reader_{0}".format(uid))
	rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))

	laserPub = rospy.Publisher('/radar/Laser', LaserScan, queue_size=10)
	ultasonicPub = rospy.Publisher('/radar/Ultrasonic', Range, queue_size=10)


	port_name = "/dev/ttyUSB0"
	baud = 57600 # 230400

	if len(sys.argv) >= 2 :
		port_name  = sys.argv[1]

	if len(sys.argv) >= 3 :
		baud  = int(sys.argv[2])

	ser = serial.Serial(port_name, baud)


	laserFrameID = "/radar_laser/{0}"
	laserScan = LaserScan()
	laserScan.angle_min = math.pi/4 - 0.05
	laserScan.angle_max = math.pi/4 + 0.05
	laserScan.angle_increment = 0.1
	laserScan.time_increment = 0.0
	laserScan.range_min = 0.05
	laserScan.range_max = 2.50
	laserScan.header.stamp = rospy.Time.now()


	rangeFrameID = "radar_ultrasonic/{0}"
	rangeMsg = Range()
	rangeMsg.radiation_type = 0
	rangeMsg.min_range = 0.05
	rangeMsg.max_range = 2.50
	rangeMsg.field_of_view = 0.17 # 10deg
	rangeMsg.radiation_type = 0


	while True:
		line = ser.readline().rstrip()
		if(len(line) <= 1):
			continue

		data = line.split("|")
		if(len(data) <= 1):
			continue

		messageType = data[0]
		moduleName = data[1]
		modulePosition = data[2]
		moduleRange = data[3]

		laserScan.header.frame_id = laserFrameID.format(moduleName)
		laserScan.ranges = moduleRange/100
		laserScan.header.stamp = rospy.Time.now()

		rangeMsg.header.frame_id = rangeFrameID.format(moduleName)
		rangeMsg.range = moduleRange / 100
		rangeMsg.header.stamp = rospy.Time.now()



		"""
		sensor = data[0]
		timestamp = data[1]

		Y = data[2]
		P = data[3]
		R = data[4]

		GyroX = data[5]
		GyroY = data[6]
		GyroZ = data[7]

		AccelX = data[8]
		AccelY = data[9]
		AccelZ = data[10]

		MagnetX = data[11]
		MagnetY = data[12]
		MagnetZ = data[13]
		"""
		print data
		laserPub.loginfo(laserScan)
		laserPub.publish(laserScan)
		ultasonicPub.loginfo(rangeMsg)
		ultasonicPub.publish(rangeMsg)

		

print "Bye!"
