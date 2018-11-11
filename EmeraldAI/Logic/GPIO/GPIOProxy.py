#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
    import RPi.GPIO as GPIO
except ImportError:
    print "Error importing RPi.GPIO! Dummy class is used."
    import EmeraldAI.Logic.GPIO.GPIODummy as GPIO


class GPIOProxy(object):

    def __init__(self, outputChannels=None, inputChannels=None):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        if outputChannels is not None:
            self.__output_channels = outputChannels #[11, 12]
            GPIO.setup(self.__output_channels, GPIO.OUT)

        if inputChannels is not None:
            self.__input_channels = inputChannels #[8, 9]
            GPIO.setup(self.__input_channels, GPIO.IN)

        self.HIGH = GPIO.HIGH
        self.LOW = GPIO.LOW

        self.RISING = GPIO.RISING
        self.FALLING = GPIO.FALLING
        self.BOTH = GPIO.BOTH

        self.IN = GPIO.IN
        self.OUT = GPIO.OUT

    def setmode(self, mode):
        GPIO.setmode(mode)

    def output(self, channel, state):
        GPIO.output(channel, state)

    def input(self, channel):
        return GPIO.input(channel)

    def cleanup(self):
        GPIO.cleanup()

    def setwarnings(self, value):
        GPIO.setwarnings(value)

    def getmode(self):
        GPIO.getmode()

    def setup(self, pin, value):
        GPIO.setup(pin, value)

    def wait_for_edge(self, channel, value, timeout=None):
        GPIO.wait_for_edge(channel, value, timeout)

    def add_event_detect(self, channel, GPIOType, callback=None, bouncetime=100):
        GPIO.add_event_detect(channel, GPIOType, callback=callback, bouncetime=bouncetime)
