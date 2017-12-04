#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.ROS.Serial.SerialFinder import SerialFinder
from EmeraldAI.Logic.ROS.Serial.SerialReader import SerialReader
from EmeraldAI.Logic.ROS.Serial.SerialWheelToOdometry import SerialWheelToOdometry



if __name__=="__main__":

    # TODO - determin portName

    portName = "/dev/ttyUSB0"
    baud = 230400

    finderResult = SerialFinder().Find()
    if(not finderResult or len(finderResult) == 0):
        # TODO
        exit()

    portName = finderResult[0]

    reader = SerialReader(portName, baud)

    radarToRange = SerialWheelToOdometry(318, 100, 20)

    while True:
        line = reader.Read()

        data = reader.Validate(line)

        if(not radarToRange.Validate(data)):
            continue


        rangeFrameID = "/base_link"
        rangeParentFrameID = "/odom"
        radarToRange.Process(data, rangeFrameID, rangeParentFrameID)


print "Bye!"
