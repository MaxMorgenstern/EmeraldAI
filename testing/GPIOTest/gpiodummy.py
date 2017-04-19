#!/usr/bin/python
BOARD = "board"
BCM = "bcm"
OUT = "out"
IN = "in"
HIGH = "1"
LOW = "0"

def output(pin,value):
  print pin, ":", value

def setmode(mode):
  print mode

def setwarnings(value):
  print value

def getmode():
  return "current mode - debug"

def setup(pin,value):
  print pin, ":", value

def cleanup():
  print "clean-up"

#End
