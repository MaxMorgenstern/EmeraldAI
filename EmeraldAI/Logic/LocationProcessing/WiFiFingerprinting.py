#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import plistlib
import itertools
import json
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Entities.Hotspot import Hotspot
from EmeraldAI.Config.Config import *
if(Config().Get("Database", "WiFiFingerprintDatabaseType").lower() == "sqlite"):
    from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db
elif(Config().Get("Database", "WiFiFingerprintDatabaseType").lower() == "mysql"):
    from EmeraldAI.Logic.Database.MySQL import MySQL as db


class WiFiFingerprinting(object):
    __metaclass__ = Singleton

    __osxCall = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x"
    __windowsCall = "netsh wlan show network"
    __linuxCall = "sudo iwlist scan | egrep 'Cell |Quality|ESSID'"
    __OnionOmega2Call = """ubus call onion wifi-scan '{"device":"ra0"}' | egrep 'ssid|bssid|signalStrength'"""

    def GetWiFiList(self):
        if(Global.OS == Global.OperatingSystem.Windows):
            return self.GetWiFiListWindows()

        if(Global.OS == Global.OperatingSystem.Linux):
            return self.GetWiFiListLinux()

        if(Global.OS == Global.OperatingSystem.OSX):
            return self.GetWiFiListOSX()


    # This needs to be calles separately as the Onion Omega2 is a linux wihout iwlist option
    def GetWiFiListOnionOmega2(self):
        proc = subprocess.Popen([self.__OnionOmega2Call], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        returnList = []

        jObject =json.loads(out)
        for i in jObject['results']:
            returnList.append(Hotspot(i["bssid"], i["ssid"], i["signalStrength"]))

        return returnList


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
                    signal = (signalDetails[1].split("=", 1)[1].replace("/100", "").replace(" dBm", "")) # signal level

                if(ssid != None and bssid != None and signal != None):
                    returnList.append(Hotspot(bssid, ssid, abs(int(signal))))
                    ssid = None
                    signal = None

        return returnList


    def GetWiFiListOSX(self):
        proc = subprocess.Popen([self.__osxCall], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        returnList = []
        if len(out) > 1:
            wifilist = plistlib.readPlistFromString(out)
            for wifi in wifilist:
                returnList.append(Hotspot(wifi["BSSID"], wifi["SSID_STR"], (wifi["RSSI"] - wifi["NOISE"]), wifi["RSSI"], wifi["NOISE"]))

        return returnList


    def CreateLocation(self, name):
        returnID = self.GetLocationID(name)
        if (returnID is None):
            returnID = db().Execute("INSERT INTO Fingerprint_Position ('Name') Values ('{0}')".format(name))
        return returnID

    def GetLocationID(self, name):
        location = db().Fetchall("SELECT ID FROM Fingerprint_Position WHERE Name = '{0}'".format(name))
        if len(location) > 0:
            return location[0][0]
        return None

    def GetLocationName(self, id):
        location = db().Fetchall("SELECT Name FROM Fingerprint_Position WHERE ID = '{0}'".format(id))
        if len(location) > 0:
            return location[0][0]
        return None


    def CreateWiFi(self, wifi):
        return db().Execute("INSERT INTO Fingerprint_WiFi ('BSSID', 'SSID') Values ('{0}','{1}');".format(wifi.BSSID, wifi.SSID))
        
    def GetWiFiID(self, bssid):
        location = db().Fetchall("SELECT ID FROM Fingerprint_WiFi WHERE BSSID = '{0}'".format(bssid))
        if len(location) > 0:
            return location[0][0]
        return None

    def GetWiFiBSSID(self, id):
        location = db().Fetchall("SELECT BSSID FROM Fingerprint_WiFi WHERE ID = '{0}'".format(id))
        if len(location) > 0:
            return location[0][0]
        return None



    def PredictLocation(self):
        wifiList = self.GetWiFiList()
        prediction = {}

        for wifi in wifiList:
            query = """SELECT Fingerprint_Position_WiFi.Indicator, 
                ABS({1}-Fingerprint_Position_WiFi.Indicator) as diff, 
                Fingerprint_Position.ID
            FROM Fingerprint_WiFi, Fingerprint_Position_WiFi, Fingerprint_Position
            WHERE BSSID = '{0}'
            AND Fingerprint_WiFi.ID = Fingerprint_Position_WiFi.WiFiID
            AND Fingerprint_Position_WiFi.PositionID = Fingerprint_Position.ID
            ORDER BY ABS({1}-Indicator)
            LIMIT 5"""

            result = db().Fetchall(query.format(wifi.BSSID, wifi.Indicator))
            for r in result:
                distance = r[1]+1
                if r[2] in prediction:
                    prediction[r[2]] += (r[0]/distance)
                else:
                    prediction[r[2]] = (r[0]/distance)
                prediction[r[2]] += 10

        return prediction


    def AddWifiToLocation(self, location, wifi):
        if not isinstance( location, ( int, long ) ):
            location = self.GetLocationID(location)

        wifientry = self.GetWiFiID(wifi.BSSID)
        if(wifientry is None):
            query = "INSERT INTO Fingerprint_WiFi ('BSSID', 'SSID') Values ('{0}','{1}');".format(wifi.BSSID, wifi.SSID)
            wifientry = db().Execute(query)

        query = "INSERT INTO Fingerprint_Position_WiFi ('PositionID', 'WiFiID', 'RSSI', 'Noise', 'Indicator') VALUES ('{0}','{1}','{2}','{3}','{4}')".format(location, wifientry, wifi.RSSI, wifi.Noise, wifi.Indicator)
        db().Execute(query)


    def __groupSeparator(self, line):
        return line=='\n'

