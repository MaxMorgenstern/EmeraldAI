#!/usr/bin/env python
import os
import subprocess
import itertools


#command = "ll /sys/class/tty/ttyUSB*"
#command = "ls -al /sys/class/tty/ttyUSB*"
command = """ls -al /sys/class/tty/ttyUSB* | grep -o "/sys/class/tty/ttyUSB.*"| sed 's/ -> .*//'"""

proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

if len(out) < 2:
    print "no data"

# tmp
out = """/sys/class/tty/ttyUSB0 
/sys/class/tty/ttyUSB1
 """

def groupSeparator(line):
    return line=='\n'

def split(data):
    lines = []
    for key, group in itertools.groupby(data, groupSeparator):
        line = ''.join(str(e) for e in group)
        line = line.strip()
        if (len(line) > 1):
            lines.append(line)
    return lines


print "program output: ", split(out)

