#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.ROS.Serial.SerialFinder import SerialFinder
from EmeraldAI.Logic.ROS.Serial.SerialReader import SerialReader
from EmeraldAI.Logic.ROS.Serial.SerialRadarToRange import SerialRadarToRange



if __name__=="__main__":

	# TODO - determin portName

	portName = "/dev/ttyUSB0"
	baud = 230400

	finderResult = SerialFinder().Find()
	if(len(finderResult) == 0):
		# TODO
		exit()

	portName = finderResult[0]

	reader = SerialReader(portName, baud)

	while True:
		line = reader.Read()

		data = reader.Validate(line)

		if(not SerialRadarToRange().Validate(data)):
			continue


		rangeFrameID = "/radar_ultrasonic"
		rangeParentFrameID = "/radar_ultrasonic_mount"
		translation = (0, 0, 0)
		SerialRadarToRange().Process(data, rangeFrameID, rangeParentFrameID, translation)


		exit()