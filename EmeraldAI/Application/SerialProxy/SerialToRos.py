#!/usr/bin/env python
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(dirname(dirname(abspath(__file__))))))
reload(sys)
sys.setdefaultencoding('utf-8')

import multiprocessing
import time
import signal

from EmeraldAI.Logic.Modules import Pid
from EmeraldAI.Logic.ROS.Serial.SerialFinder import SerialFinder
from EmeraldAI.Logic.ROS.Serial.SerialConnector import SerialConnector
from EmeraldAI.Logic.ROS.Serial.SerialWheelToOdometry import SerialWheelToOdometry
from EmeraldAI.Logic.ROS.Serial.TwistToSerialWheel import TwistToSerialWheel
from EmeraldAI.Logic.ROS.Serial.SerialRadarToRange import SerialRadarToRange
from EmeraldAI.Logic.ROS.Serial.SerialLaserToLaser import SerialLaserToLaser
from EmeraldAI.Logic.ROS.Serial.SerialImuToImu import SerialImuToImu
from EmeraldAI.Config.HardwareConfig import *

UseUltrasonic = HardwareConfig().GetBoolean("Sensor", "UseUltrasonic")
UseLaser = HardwareConfig().GetBoolean("Sensor", "UseLaser")

def ProcessHandler(signal, frame):
    sys.exit(0)

def Processing(port, baud):
    serialConnect = SerialConnector(port, baud)

    imuToImu = SerialImuToImu()
    radarToRange = SerialRadarToRange()
    laserToLaser = SerialLaserToLaser()
    wheelToOdom = SerialWheelToOdometry()
    twistToWheel = TwistToSerialWheel()

    try:
        signal.signal(signal.SIGINT, ProcessHandler)

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

            if(UseUltrasonic and radarToRange.Validate(data)):
                radarToRange.Process(data)
                continue

            if(UseLaser and laserToLaser.Validate(data)):
                laserToLaser.Process(data)
                continue

            if(wheelToOdom.Validate(data)):
                wheelToOdom.Process(data)

                twistToWheel.ProcessTwist()
                twistToWheel.ProcessPID(data)

                rightMotorValue, leftMotorValue = twistToWheel.GetMotorInstructions()            
                serialConnect.Write("{0}|{1}".format(leftMotorValue, rightMotorValue))
    
    finally:
        print "Disconnect serial connection for", port
        serialConnect.Disconnect()


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
                print "Launching process for", port
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
        print "End SerialToRos"
    finally:
        Pid.Remove("SerialToRos")
