#!/usr/bin/env python
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
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
        try:
            line = reader.Read()
        except IOError:
            return

        data = reader.Validate(line)

        if(data is None):
            continue

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

    timeToSleep = 5

    processList = {}

    while True:
        finderResult = SerialFinder().Find()

        tmpProcessList = list(processList)
        for process in tmpProcessList:
            if process not in finderResult or not processList[process].is_alive():
                print "Terminste", process
                processList[process].terminate()
                del processList[process]

        if(len(finderResult) == 0):
            time.sleep(timeToSleep)
            continue

        for port in finderResult:
            if port in processList:
                continue
            else:
                print "Launching Process for", portName
                process = multiprocessing.Process(name=portName, target=Processing, args=(portName,baud,))
                process.start()
                processList[port] = process

        time.sleep(timeToSleep)

print "Bye!"
