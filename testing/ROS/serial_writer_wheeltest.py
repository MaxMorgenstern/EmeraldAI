#!/usr/bin/env python
import serial
import os
import sys
import time


if __name__=="__main__":

    portName = "/dev/ttyUSB0"
    baud = 115200

    SerialPointer = serial.Serial(portName, baud)
    
    count = 0;
    while count < 20:
        SerialPointer.write("255|255;")
        SerialPointer.flush()
        time.sleep(0.1)
        count+=1
        if SerialPointer.inWaiting() != 0:
            print SerialPointer.readline()

    print "-----"
    time.sleep(2)
    
    count = 0;
    while count < 20:
        SerialPointer.write("-255|-255;")
        SerialPointer.flush()
        time.sleep(0.1)
        count+=1
        if SerialPointer.inWaiting() != 0:
            print SerialPointer.readline()
        
