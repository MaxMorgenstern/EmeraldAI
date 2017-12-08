#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.ROS.Serial.SerialFinder import SerialFinder
from EmeraldAI.Logic.ROS.Serial.SerialReader import SerialReader
from EmeraldAI.Logic.ROS.Serial.SerialImuToImu import SerialImuToImu



if __name__=="__main__":

    # TODO - determin portName

    portName = "/dev/ttyUSB1"
    baud = 230400

    finderResult = SerialFinder().Find()
    if(not finderResult or len(finderResult) == 0):
        # TODO
        exit()

    #portName = finderResult[0]

    reader = SerialReader(portName, baud)

    imuToImu = SerialImuToImu()

    while True:
        line = reader.Read()
        #print line

        data = reader.Validate(line)

        if(not imuToImu.Validate(data)):
            continue


        imuFrameID = "/imu_sensor"
        imuParentFrameID = "/odom"
        translation = (0, 0, 0.5)
        imuToImu.Process(data)



        #exit()