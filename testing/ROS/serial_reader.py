#!/usr/bin/env python

import serial

ser = serial.Serial('/dev/ttyUSB0', 38400)
while True:
	line = ser.readline().rstrip()
	if(len(line) <= 1):
		continue
	data = line.split("|")
	print data


print "Bye!"
