#!/usr/bin/env python

import serial

ser = serial.Serial('/dev/ttyUSB1', 38400)
while True:
	line = ser.readline().rstrip()
	if(len(line) <= 1):
		continue
	data = line.split("|")
	if(len(data) <= 1):
		continue

	senstor = data[0]
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

	print data


print "Bye!"
