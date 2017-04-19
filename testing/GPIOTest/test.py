#!/usr/bin/python
# -*- coding: utf-8 -*-

# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
    import gpiodummy as GPIO

GPIO.setmode(GPIO.BOARD)
print GPIO.getmode()
GPIO.setwarnings(False)

chan_list = [11,12]
GPIO.setup(chan_list, GPIO.OUT)

# GPIO.input(chan_list)

channel = 11
state = GPIO.HIGH
# State can be 0 / GPIO.LOW / False or 1 / GPIO.HIGH / True.
GPIO.output(channel, state)

"""
GPIO.output(chan_list, GPIO.LOW)                # sets all to GPIO.LOW
GPIO.output(chan_list, (GPIO.HIGH, GPIO.LOW))   # sets first HIGH and second LOW
"""

GPIO.cleanup()

