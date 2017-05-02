#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: Extend - https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
    import gpiodummy as GPIO

class EmeraldGPIO(object):
    #__metaclass__ = Singleton

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.__output_channels = [11, 12]
        GPIO.setup(self.__output_channels, GPIO.OUT)

        self.__input_channels = [8, 9]
        GPIO.setup(self.__input_channels, GPIO.IN)

        self.HIGH = GPIO.HIGH
        self.LOW = GPIO.LOW


    def output(self, channel, state):
        GPIO.output(channel, state)

    def input(self, channel):
        return GPIO.input(channel)

    def cleanup(self):
        GPIO.cleanup()


print EmeraldGPIO().input(5)
