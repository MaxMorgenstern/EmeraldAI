#!/usr/bin/env python
from __future__ import division

import serial
import rospy
import os
import sys
import time

if __name__=="__main__":

	uid = str(os.getpid())
	rospy.init_node("serial_reader_{0}".format(uid))
	rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))


	port_name = "/dev/ttyUSB0"
	baud = 230400

	if len(sys.argv) >= 2 :
		port_name  = sys.argv[1]

	if len(sys.argv) >= 3 :
		baud  = int(sys.argv[2])

	ser = serial.Serial(port_name, baud, timeout=1)
	
	readTimestamp = time.time() + 10
	print readTimestamp
	while True:
		# if nothing to read, sleep for 10 milliseconds and check timeout
		while ser.inWaiting() == 0:
			time.sleep(0.01)
			if(readTimestamp + 5 < time.time()):
				print "reconnect..."
				ser.close()
				time.sleep(1)
				ser = serial.Serial(port_name, baud, timeout=1)
				readTimestamp = time.time() + 10
		
		line = ser.readline().rstrip()
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
