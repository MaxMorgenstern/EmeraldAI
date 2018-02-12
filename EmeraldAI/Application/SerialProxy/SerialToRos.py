#!/usr/bin/env python
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import multiprocessing
import time

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Logic.ROS.Serial.SerialFinder import SerialFinder
from EmeraldAI.Logic.ROS.Serial.SerialConnector import SerialConnector
from EmeraldAI.Logic.ROS.Serial.SerialWheelToOdometry import SerialWheelToOdometry
from EmeraldAI.Logic.ROS.Serial.TwistToSerialWheel import TwistToSerialWheel
from EmeraldAI.Logic.ROS.Serial.SerialRadarToRange import SerialRadarToRange
from EmeraldAI.Logic.ROS.Serial.SerialRadarToLaser import SerialRadarToLaser
from EmeraldAI.Logic.ROS.Serial.SerialImuToImu import SerialImuToImu

# TODO: Add to config: UseRange ... UseLaser
UseRange = True
UseLaser = True

def Processing(port, baud):
    serialConnect = SerialConnector(port, baud)

    imuToImu = SerialImuToImu()
    radarToRange = SerialRadarToRange()
    radarToLaser = SerialRadarToLaser()
    wheelToOdom = SerialWheelToOdometry(318, 100, 20)
    twistToWheel = TwistToSerialWheel(318, 100, 20)

    wheelDataSendZeroTimestamp = int(round(time.time() * 1000))
    wheelDataSendZeroDelay = 100

    while True:
        try:
            line = serialConnect.Read()
        except IOError:
            return

        data = serialConnect.Validate(line)

        if(data is None):
            continue

        if(imuToImu.Validate(data)):
            imuToImu.Process(data)
            continue

        if(UseRange and radarToRange.Validate(data)):
            radarToRange.Process(data)
            continue

        if(UseLaser and radarToLaser.Validate(data)):
            radarToLaser.Process(data)
            continue

        if(wheelToOdom.Validate(data)):
            wheelToOdom.Process(data)

            twistToWheel.ProcessTwist()
            twistToWheel.ProcessPID(data)

            rightMotorValue, leftMotorValue = twistToWheel.GetMotorInstructions()
            currentTime = int(round(time.time() * 1000))
            if(rightMotorValue == 0 and leftMotorValue == 0 and
                wheelDataSendZeroTimestamp + wheelDataSendZeroDelay > currentTime):
                continue

            wheelDataSendZeroTimestamp = currentTime
            serialConnect.Write("{0}|{1}".format(leftMotorValue, rightMotorValue))


def mainLoop():
    baud = 115200
    timeToSleep = 5
    processList = {}

    while True:
        finderResult = SerialFinder().Find()

        tmpProcessList = list(processList)
        for process in tmpProcessList:
            if process not in finderResult or not processList[process].is_alive():
                print "Terminate", process
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



if __name__=="__main__":

    if(Pid.HasPid("SerialToRos")):
        print "Process is already runnung. Bye!"
        sys.exit()
    Pid.Create("SerialToRos")
    try:
        mainLoop()
    except KeyboardInterrupt:
        print "End"
    finally:
        Pid.Remove("SerialToRos")


