#!/usr/bin/env python
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import multiprocessing
import time

from EmeraldAI.Logic.ROS.Serial.SerialFinder import SerialFinder
from EmeraldAI.Logic.ROS.Serial.SerialConnector import SerialConnector
from EmeraldAI.Logic.ROS.Serial.SerialWheelToOdometry import SerialWheelToOdometry
from EmeraldAI.Logic.ROS.Serial.TwistToSerialWheel import TwistToSerialWheel
from EmeraldAI.Logic.ROS.Serial.SerialRadarToRange import SerialRadarToRange
from EmeraldAI.Logic.ROS.Serial.SerialImuToImu import SerialImuToImu


def Processing(port, baud):
    serialConnect = SerialConnector(port, baud)

    imuToImu = SerialImuToImu()
    radarToRange = SerialRadarToRange()
    wheelToOdom = SerialWheelToOdometry(318, 100, 20)
    twistToWheel = TwistToSerialWheel(318, 100, 20)
    wheelData = False

    while True:
        try:
            line = serialConnect.Read()
        except IOError:
            return

        data = serialConnect.Validate(line)

        if(data is None):
            continue

        try:
            if(imuToImu.Validate(data)):
                imuToImu.Process(data)
                continue

            if(radarToRange.Validate(data)):
                radarToRange.Process(data)
                continue

            if(wheelToOdom.Validate(data)):
                wheelToOdom.Process(data)
                wheelData = True

            if(wheelData):
                twistToWheel.ProcessTwist()
                if(twistToWheel.Validate(data)):
                    twistToWheel.ProcessPID(data)

                rightMotorValue, leftMotorValue = twistToWheel.GetMotorInstructions()
                serialConnect.Write("{0}|{1}".format(leftMotorValue, rightMotorValue))
        except Exception as ex:
            # TODO for debugging
            print "Data", data
            print "Error", ex
            raise Exception(ex)

if __name__=="__main__":

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
                print "Launching Process for", port
                process = multiprocessing.Process(name=port, target=Processing, args=(port,baud,))
                process.start()
                processList[port] = process

        time.sleep(timeToSleep)

print "Bye!"
