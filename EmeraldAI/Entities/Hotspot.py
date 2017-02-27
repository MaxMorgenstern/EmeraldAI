#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Entities.BaseObject import BaseObject
from EmeraldAI.Logic.Modules import Global


class Hotspot(BaseObject):
    BSSID = None
    SSID = None
    RSSI = None
    Noise = None
    Indicator = None
    ScanningOS = None

    def __init__(self, BSSID, SSID, Indicator, RSSI=None, Noise=None, ScanningOS=None):
        self.BSSID = BSSID
        self.SSID = SSID
        self.RSSI = RSSI
        self.Noise = Noise
        self.Indicator = Indicator
        if(ScanningOS == None):
            ScanningOS = Global.OS
        self.ScanningOS = ScanningOS

    def __repr__(self):
         return "{0} {1}".format(self.BSSID, self.SSID)

    def __str__(self):
         return "{0} {1}".format(self.BSSID, self.SSID)
