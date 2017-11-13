#!/usr/bin/env python
import os
import subprocess

#command = "ll /sys/class/tty/ttyUSB*"
#command = "ls -al /sys/class/tty/ttyUSB*"
command = """ls -al /sys/class/tty/ttyUSB* | grep -o "/sys/class/tty/ttyUSB.*"| sed 's/ -> .*//'"""

#data = os.system(command)

data = os.popen(command).read()

print data
