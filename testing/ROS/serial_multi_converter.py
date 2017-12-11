#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')

import multiprocessing
import time

from EmeraldAI.Logic.ROS.Serial.SerialFinder import SerialFinder
from EmeraldAI.Logic.ROS.Serial.SerialReader import SerialReader
from EmeraldAI.Logic.ROS.Serial.SerialWheelToOdometry import SerialWheelToOdometry
from EmeraldAI.Logic.ROS.Serial.SerialRadarToRange import SerialRadarToRange
from EmeraldAI.Logic.ROS.Serial.SerialImuToImu import SerialImuToImu


def Processing(port, baud):
    reader = SerialReader(port, baud)

    wheelToOdom = SerialWheelToOdometry(318, 100, 20)
    imuToImu = SerialImuToImu()
    radarToRange = SerialRadarToRange()

    while True:
        line = reader.Read()

        data = reader.Validate(line)

        if(wheelToOdom.Validate(data)):
            wheelToOdom.Process(data)
            continue

        if(imuToImu.Validate(data)):
            imuToImu.Process(data)
            continue

        if(radarToRange.Validate(data)):
            radarToRange.Process(data)
            continue



if __name__=="__main__":

    portName = "/dev/ttyUSB0"
    baud = 230400

    processList = {}

    while True:
        finderResult = SerialFinder().Find()
        
        if(not finderResult or len(finderResult) == 0):
            time.sleep(10)
            continue

        for port in finderResult:
            if port in processList:
                continue
            else:
                print "Launching Process for", portName
                process = multiprocessing.Process(name=portName, target=Processing, args=(portName,baud,))
                process.start()
                processList[port] = process

        for process in processList:
            if process not in finderResult:
                # todo
                del processList[process]

        time.sleep(30)

print "Bye!"
