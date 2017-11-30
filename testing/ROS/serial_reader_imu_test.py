#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.ROS.Serial.SerialReader import SerialReader
from EmeraldAI.Logic.ROS.Serial.SerialImuToImu import SerialImuToImu



if __name__=="__main__":

	portName = "/dev/ttyUSB0"
	baud = 230400

	if len(sys.argv) >= 2 :
		portName  = sys.argv[1]

	if len(sys.argv) >= 3 :
		baud  = int(sys.argv[2])

	reader = SerialReader(portName, baud)

	while True:
		line = reader.Read()

		data = reader.Validate(line)

		if(not SerialImuToImu().Validate(data)):
			continue


		imuFrameID = "/imu_sensor"
		imuParentFrameID = "/odom"
		translation = (0, 0, 0.5)
		SerialImuToImu().Process(data, imuFrameID, imuParentFrameID, translation)



		exit()