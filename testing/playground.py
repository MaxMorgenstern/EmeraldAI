#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

import subprocess
import plistlib
from EmeraldAI.Logic.Database.SQlite3 import SQlite3 as db

while True:
    locationInput = raw_input("Enter Location: ")
    if(len(locationInput) < 2):
        break

    positionID = db().Execute("INSERT INTO Fingerprint_Position ('Name') Values ('{0}');".format(locationInput))

    locationLoop = 0
    while locationLoop < 5:
        print "Loop #{0} in progress...".format((locationLoop+1))
        proc = subprocess.Popen(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        wifilist = plistlib.readPlistFromString(out)
        for wifi in wifilist:

            query = "INSERT INTO Fingerprint_WiFi ('BSSID', 'SSID', 'RSSI', 'Noise', 'Indicator') Values ('{0}','{1}','{2}','{3}','{4}');".format(wifi["BSSID"], wifi["SSID_STR"], wifi["RSSI"], wifi["NOISE"], (wifi["RSSI"] - wifi["NOISE"]))
            wifientry = db().Execute(query)

            query = "INSERT INTO Fingerprint_Position_WiFi ('PositionID', 'WiFiID') VALUES ('{0}','{1}');".format(positionID, wifientry)
            db().Execute(query)

        time.sleep( 5 )
        locationLoop += 1

    print "Location Scan Complete!"





print "Determine where we are..."

while True:
    prediction = {}

    proc = subprocess.Popen(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s -x"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    wifilist = plistlib.readPlistFromString(out)
    for wifi in wifilist:
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

            print r
        print "---"
    print prediction

    percent = 100 / sum(prediction.values())

    for key, value in prediction.iteritems():
        print "{0}: {1:.2f}%".format(key, (value * percent))



