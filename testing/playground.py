#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')


"""
from subprocess import *
print "-----"
y = call("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x")
print y
print "-----2"
"""


import subprocess
import plistlib

proc = subprocess.Popen(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
#print "program output:", out


wifilist = plistlib.readPlistFromString(out)

print len(wifilist)
for wifi in wifilist:
	print wifi["SSID_STR"]
	print wifi["RSSI"]
	print wifi["NOISE"]
	print (wifi["RSSI"] - wifi["NOISE"])
	print "---"

