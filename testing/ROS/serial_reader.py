#!/usr/bin/env python
from __future__ import division

import serial
import rospy
import os
import sys
import time
import subprocess


class SerialHelper():
    SerialPointer = None
    ReadTimestamp = None
    InitialTimestampDelay = 10

    def __init__(self, port_name, baud, timeout=1):
        self._port_name = port_name
        self._baud = baud
        self._timeout = timeout

        self.SerialPointer = serial.Serial(port_name, baud, timeout=timeout)
        self.ReadTimestamp = time.time() + self.InitialTimestampDelay

    def Read(self):
        # if nothing to read, sleep for 10 milliseconds and check timeout
        while self.SerialPointer.inWaiting() == 0:
            time.sleep(0.01)
            if(self.ReadTimestamp + 5 < time.time()):
                print "reconnect..."
                self.SerialPointer.close()
                time.sleep(1)
                self.SerialPointer = serial.Serial(self._port_name, self._baud, timeout=self._timeout)
                self.ReadTimestamp = time.time() + self.InitialTimestampDelay
        return self.SerialPointer.readline().rstrip()

    def Validate(self, line):
        if(len(line) <= 1):
            return None

        data = line.split("|")
        if(len(data) <= 1):
            return None

        self.ReadTimestamp = time.time()
        return data


class SerialFinder():
    _command = """ls -al /sys/class/tty/ttyUSB* | grep -o "/sys/class/tty/ttyUSB.*"| sed 's/ -> .*//'"""

    def Find(self):

        proc = subprocess.Popen(
            [self._command], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        if len(out) < 2:
            return None

        print out


class SerialWheelToOdometry():

    def Process(self, data):
        return


if __name__ == "__main__":

    uid = str(os.getpid())
    rospy.init_node("serial_reader_{0}".format(uid))
    rospy.loginfo("ROS Serial Python Node '{0}'".format(uid))

    port_name = "/dev/ttyUSB0"
    baud = 230400

    if len(sys.argv) >= 2:
        port_name = sys.argv[1]

    if len(sys.argv) >= 3:
        baud = int(sys.argv[2])

    sh = SerialHelper(port_name, baud, timeout=1)

    while True:
        line = sh.Read()

        data = sh.Validate(line)

        if(data == None):
            continue

        # check for type - data[0]
        # ultrasonic - length: 10 -- multiple messageTypes depending on MPU
        # wheel - length 10
        # radar - length: 4

        if(len(data) != 14):
            continue

        # if(data[0].lower() == "wheel")
        #             SerialWheelToOdometry().Process(data)
        # if(data[0].lower() == "MPU6050".lower()) # MPU9150 - MPU6500 - MPU9250
        #             SerialImuToImu().Process(data)
        # if(data[0].lower() == "ultrasonic")
        #             SerialRadarToRange().Process(data)

        print data


print "Bye!"
