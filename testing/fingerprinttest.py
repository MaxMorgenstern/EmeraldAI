#!/usr/bin/python
# -*- coding: utf-8 -*-
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
