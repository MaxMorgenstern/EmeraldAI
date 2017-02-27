#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')
from itertools import repeat
from EmeraldAI.Logic.LocationProcessing.WiFiFingerprinting import *

wifiFP = WiFiFingerprinting()

locationName = raw_input('Please enter the location name: ')

locationID = wifiFP.CreateLocation(locationName)


for i in repeat(None, 5):
    wifiList = wifiFP.GetWiFiList()
    for wifi in wifiList:
        wifiFP.AddWifiToLocation(locationID, wifi)
