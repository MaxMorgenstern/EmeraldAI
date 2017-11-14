#!/usr/bin/env python
import os
import subprocess

#command = "ll /sys/class/tty/ttyUSB*"
#command = "ls -al /sys/class/tty/ttyUSB*"
command = """ls -al /sys/class/tty/ttyUSB* | grep -o "/sys/class/tty/ttyUSB.*"| sed 's/ -> .*//'"""

proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

if len(out) < 2:
	print "no data"

print "program output:", out

