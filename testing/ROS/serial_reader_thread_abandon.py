#!/usr/bin/env python
from __future__ import division

import serial
import rospy
import os
import sys
import math
import tf
import time

from threading import Thread

from sensor_msgs.msg import Imu

class SerialReader:
	def __init__(self, port, baud):
		self.port = port_name
		self.baud = baud

		self.data = None

		self.stopped = True

	def start(self):
		self.stopped = False
		self.serial = serial.Serial(self.port, self.baud, timeout=1)
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		while True:
			if self.stopped:
				return
			self.data = self.serial.readline().rstrip()

	def read(self):
		returnValue = self.data
		self.data = None
		return returnValue

	def stop(self):
		self.stopped = True
		self.serial.close()





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
	baud = 230400
	#baud = 57600

	if len(sys.argv) >= 2 :
		port_name  = sys.argv[1]

	if len(sys.argv) >= 3 :
		baud  = int(sys.argv[2])

	ser2 = SerialReader(port_name, baud).start()

	#ser = serial.Serial(port_name, baud, timeout=1)
	
	readTimestamp = time.time()

	while True:
		line = ser2.read()
		if line == None:
			if (readTimestamp + 5 < time.time()):
				print "timeout"
				ser2.stop()
				ser2.start()
			continue

		#line = ser.readline().rstrip()
		if(len(line) <= 1):
			continue

		data = line.split("|")
		if(len(data) <= 1):
			continue

		readTimestamp = time.time()
		print data

		# we expect 14 values from the ultrasonic node
		#if(len(data) != 14):
		#	continue
		
		#print "working"
		

print "Bye!"
