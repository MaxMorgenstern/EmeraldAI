#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import plistlib
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.Modules import Global

# TODO: move hotspot into entities - inherit from base object
class Hotspot(object):
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


class WiFiFingerprinting(object):
    __metaclass__ = Singleton

    __osxCall = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x"
    __windowsCall = "netsh wlan show network"
    __linuxCall = "iwlist scan | egrep 'Cell |Quality|ESSID'"

    def GetWiFiList(self):
        if(Global.OS == Global.OperatingSystem.Windows):
            return self.GetWiFiListWindows()

        if(Global.OS == Global.OperatingSystem.Linux):
            return self.GetWiFiListLinux()

        if(Global.OS == Global.OperatingSystem.OSX):
            return self.GetWiFiListOSX()

    def GetWiFiListWindows(self):
        return ""

    def GetWiFiListLinux(self):
        return ""

    def GetWiFiListOSX(self):
        proc = subprocess.Popen([self.__osxCall], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        returnList = []
        wifilist = plistlib.readPlistFromString(out)
        for wifi in wifilist:
            returnList.append(Hotspot(wifi["BSSID"], wifi["SSID_STR"], (wifi["RSSI"] - wifi["NOISE"]), wifi["RSSI"], wifi["NOISE"]))

        return returnList


