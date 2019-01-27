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
from EmeraldAI.Logic.ROS.Serial.SerialLaserToLaser360 import SerialLaserToLaser360
from EmeraldAI.Logic.ROS.Serial.SerialImuToImu import SerialImuToImu
from EmeraldAI.Config.HardwareConfig import HardwareConfig

UseUltrasonic = HardwareConfig().GetBoolean("Sensor", "UseUltrasonic")
UseLaser = HardwareConfig().GetBoolean("Sensor", "UseLaser")

def ProcessHandler(signal, frame):
    sys.exit(0)

def Processing(port, baud):
    serialConnect = SerialConnector(port, baud)

    imuToImu = SerialImuToImu()
    isImu = True
    radarToRange = SerialRadarToRange()
    isRadarRange = True
    laserToLaser = SerialLaserToLaser()
    isLaserRange = True
    laserToLaser360 = SerialLaserToLaser360()
    isLaserRange360 = True
    wheelToOdom = SerialWheelToOdometry()
    isWheel = True
    twistToWheel = TwistToSerialWheel()

    firstRun = True

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

            if(firstRun):
                if(not imuToImu.Validate(data)):
                    isImu = False

                if(UseUltrasonic and not radarToRange.Validate(data)):
                    isRadarRange = False

                if(UseLaser and not laserToLaser.Validate(data)):
                    isLaserRange = False

                if(UseLaser and not laserToLaser360.Validate(data)):
                    isLaserRange360 = False

                if(not wheelToOdom.Validate(data)):
                    isWheel = False

                if(isImu or isRadarRange or isLaserRange or isLaserRange360 or isWheel):
                    firstRun = False
                else:
                    isImu = True
                    isRadarRange = True
                    isLaserRange = True
                    isLaserRange360 = True
                    isWheel = True


            if(isImu and imuToImu.Validate(data)):
                imuToImu.Process(data)
                continue

            if(isRadarRange and radarToRange.Validate(data)):
                radarToRange.Process(data)
                continue

            if(isLaserRange and laserToLaser.Validate(data)):
                laserToLaser.Process(data)
                continue

            if(isLaserRange360 and laserToLaser360.Validate(data)):
                laserToLaser360.Process(data)
                continue

            if(isWheel and wheelToOdom.Validate(data)):
                wheelToOdom.Process(data)

                twistToWheel.ProcessTwist()
                twistToWheel.ProcessPID(data)

                rightMotorValue, leftMotorValue = twistToWheel.GetMotorInstructions()            
                serialConnect.Write("{0}|{1}".format(leftMotorValue, rightMotorValue))
                continue

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
