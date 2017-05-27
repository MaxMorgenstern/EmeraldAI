#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
    import RPi.GPIO as GPIO
except ImportError:
    print "Error importing RPi.GPIO! Dummy class is used."
    import gpiodummy as GPIO

from EmeraldAI.Logic.Singleton import Singleton


class GPIOProxy(object):
    __metaclass__ = Singleton

    def __init__(self, outputChannels, inputChannels):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.__output_channels = outputChannels #[11, 12]
        GPIO.setup(self.__output_channels, GPIO.OUT)

        self.__input_channels = inputChannels #[8, 9]
        GPIO.setup(self.__input_channels, GPIO.IN)

        self.HIGH = GPIO.HIGH
        self.LOW = GPIO.LOW


    def output(self, channel, state):
        GPIO.output(channel, state)

    def input(self, channel):
        return GPIO.input(channel)

    def cleanup(self):
        GPIO.cleanup()
