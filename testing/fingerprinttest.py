#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Logic.LocationProcessing.WiFiFingerprinting import *

fp = WiFiFingerprinting()

wfl = fp.GetWiFiList()

print len(wfl)

for w in wfl:
	print w.BSSID + " - " + w.SSID

while True:
	x = fp.PredictLocation()
	print x
	percent = 100 / sum(x.values())
	for key, value in x.iteritems():
	    print "{0}: {1:.2f}%".format(fp.GetLocationName(key), (value * percent))
