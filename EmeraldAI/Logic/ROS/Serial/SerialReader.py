#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton

class SerialReader():
    __metaclass__ = Singleton

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
