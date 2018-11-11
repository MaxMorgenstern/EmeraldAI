#!/usr/bin/python

# https://sourceforge.net/p/raspberry-gpio-python/wiki/Examples/

BOARD = "board"
BCM = "bcm"
OUT = "out"
IN = "in"
HIGH = 1
LOW = 0
RPI_INFO = "dummy"
RPI_REVISION = "dummy"
VERSION = "dummy"
RISING = 1
FALLING = 0
BOTH = 2

def setmode(mode):
	print "setmode()", mode

def output(pin, value):
	print "output()", pin, ":", value

def input(channel):
	print "input()"
	return LOW

def setwarnings(value):
	print "setwarnings()", value

def getmode():
	print "getmode()"
	return BOARD

def setup(pin, value):
	print "setup()", pin, ":", value

def cleanup(channel=None):
	print "cleanup()"

def wait_for_edge(channel, value, timeput=None):
	return 1

def add_event_detect(channel, type, callback, bouncetime):
	print "add_event_detect()"
