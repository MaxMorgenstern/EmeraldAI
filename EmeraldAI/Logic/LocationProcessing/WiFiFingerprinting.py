#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import plistlib
import itertools
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Entities.Hotspot import Hotspot
from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db


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






    def CreateLocation(self, name):
        return db().Execute("INSERT INTO Fingerprint_Position ('Name') Values ('{0}');".format(name))

    def GetLocationID(self, name):
        location = db().Fetchall("SELECT * FROM Fingerprint_Position WHERE Name = '{0}'".format(name))
        #TODO
        return ""

    def PredictLocation(self):
        wifiList = self.GetWiFiList()
        prediction = {}


        for wifi in wifiList:
            query = """SELECT Fingerprint_WiFi.Indicator, ABS({1}-Fingerprint_WiFi.Indicator) as diff, Fingerprint_Position.Name
            FROM Fingerprint_WiFi, Fingerprint_Position_WiFi, Fingerprint_Position
            WHERE BSSID = '{0}'
            AND Fingerprint_WiFi.ID = Fingerprint_Position_WiFi.WiFiID
            AND Fingerprint_Position_WiFi.PositionID = Fingerprint_Position.ID
            ORDER BY ABS({1}-Indicator)
            LIMIT 5"""

            result = db().Fetchall(query.format(wifi['BSSID'], (wifi["RSSI"] - wifi["NOISE"])))
            for r in result:
                print r
                distance = r[1]+1
                if r[2] in prediction:
                    prediction[r[2]] += (r[0]/distance)
                else:
                    prediction[r[2]] = (r[0]/distance)
                prediction[r[2]] += 10

        # TODO: maybe ID as well
        return prediction


    def AddWifiToLocation(self, location, wifi):
        if not isinstance( location, ( int, long ) ):
            location = self.GetLocationID(location)

        query = "INSERT INTO Fingerprint_WiFi ('BSSID', 'SSID', 'RSSI', 'Noise', 'Indicator') Values ('{0}','{1}','{2}','{3}','{4}');".format(wifi.BSSID, wifi.SSID, wifi.RSSI, wifi.NOISE, wifi.Indicator)
        wifientry = db().Execute(query)

        query = "INSERT INTO Fingerprint_Position_WiFi ('PositionID', 'WiFiID') VALUES ('{0}','{1}');".format(location, wifientry)
        db().Execute(query)


