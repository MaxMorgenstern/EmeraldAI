#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import plistlib
import itertools
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
        proc = subprocess.Popen([self.__windowsCall], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        returnList = []

        ssid = None
        bssid = None
        signal = None
        for key, group in itertools.groupby(out, self.__groupSeparator):
            line = ''.join(str(e) for e in group)
            line = line.strip()
            if(len(line) > 2):
                splitLine = line.split(":", 1)
                if line.startswith("SSID "):
                    ssid = splitLine[1].strip()
                    bssid = None
                    signal = None

                if line.startswith("BSSIDD "):
                    bssid = splitLine[1].strip()

                if line.startswith("Signal "):
                    signal = splitLine[1].strip()

                if(ssid != None and bssid != None and signal != None):
                    returnList.append(Hotspot(bssid, ssid, signal))
                    bssid = None
                    signal = None

        return returnList

    def GetWiFiListLinux(self):
        proc = subprocess.Popen([self.__linuxCall], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        returnList = []

        ssid = None
        bssid = None
        signal = None
        for key, group in itertools.groupby(out, self.__groupSeparator):
            line = ''.join(str(e) for e in group)
            line = line.strip()
            if(len(line) > 2):
                splitLine = line.split(":", 1)
                if line.startswith("Cell "):
                    bssid = splitLine[1].strip()
                    ssid = None
                    signal = None

                if line.startswith("ESSID"):
                    ssid = splitLine[1].strip()

                if line.startswith("Quality"):
                    signalDetails = line.split("  ", 1)
                    #signal = (signalDetails[0].split("=", 1)[1].replace("/100", "")) # quality
                    signal = (signalDetails[1].split("=", 1)[1].replace("/100", "")) # signal level

                if(ssid != None and bssid != None and signal != None):
                    returnList.append(Hotspot(bssid, ssid, signal))
                    ssid = None
                    signal = None

        return returnList

    def GetWiFiListOSX(self):
        proc = subprocess.Popen([self.__osxCall], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        returnList = []
        wifilist = plistlib.readPlistFromString(out)
        for wifi in wifilist:
            returnList.append(Hotspot(wifi["BSSID"], wifi["SSID_STR"], (wifi["RSSI"] - wifi["NOISE"]), wifi["RSSI"], wifi["NOISE"]))

        return returnList

    def __groupSeparator(self, line):
        return line=='\n'

