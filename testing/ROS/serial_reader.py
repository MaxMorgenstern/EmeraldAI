#!/usr/bin/env python
from __future__ import division

import serial
import rospy
import os
import sys
import time

class SerialHelper():
	SerialPointer = None
	ReadTimestamp = None
	InitialTimestampDelay = 10

	def __init__ (self, port_name, baud, timeout=1):
		self._port_name = port_name
		self._baud = baud
		self._timeout = timeout

		self.SerialPointer = serial.Serial(port_name, baud, timeout=timeout)
		self.ReadTimestamp = time.time() + self.InitialTimestampDelay

	def Read(self):
		# if nothing to read, sleep for 10 milliseconds and check timeout
		while self.SerialPointer.inWaiting() == 0:
			time.sleep(0.01)
			if(self.ReadTimestamp + 5 < time.time()):
				print "reconnect..."
				self.SerialPointer.close()
				time.sleep(1)
				self.SerialPointer = serial.Serial(self._port_name, self._baud, timeout=self._timeout)
				self.ReadTimestamp = time.time() + self.InitialTimestampDelay
		return self.SerialPointer.readline().rstrip()

	def ValidateAndProcess(self, line, length):
		if(len(line) <= 1):
			return None

		data = line.split("|")
		if(len(data) <= 1):
			return None

		if(len(data) != length):
			return None

		self.ReadTimestamp = time.time()
		return data



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

	sh = SerialHelper(port_name, baud, timeout=1)
	
	while True:
		line = sh.Read()
		
		data = sh.ValidateAndProcess(line, 14)

		if(data == None):
			continue

		print data
		

print "Bye!"
