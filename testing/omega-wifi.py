#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

data = """{
        "results": [
                {
                        "channel": "6",
                        "ssid": "bpa_guest",
                        "bssid": "00:1a:8c:7e:a1:e1",
                        "authentication": "AES",
                        "encryption": "WPA2PSK",
                        "signalStrength": "42",
                        "wirelessMode": "11b\/g\/n",
                        "ext-ch": "NONE"
                },
                {
                        "channel": "6",
                        "ssid": "bpa_intern",
                        "bssid": "00:1a:8c:7e:a1:e2",
                        "authentication": "AES",
                        "encryption": "WPA2",
                        "signalStrength": "42",
                        "wirelessMode": "11b\/g\/n",
                        "ext-ch": "NONE"
                },
                {
                        "channel": "6",
                        "ssid": "BPA_Chromecast",
                        "bssid": "00:1a:8c:7e:a1:e3",
                        "authentication": "TKIPAES",
                        "encryption": "WPA1PSKWPA2PSK",
                        "signalStrength": "42",
                        "wirelessMode": "11b\/g\/n",
                        "ext-ch": "NONE"
                },
                {
                        "channel": "6",
                        "ssid": "bpa_guest",
                        "bssid": "00:1a:8c:98:e7:6d",
                        "authentication": "AES",
                        "encryption": "WPA2PSK",
                        "signalStrength": "0",
                        "wirelessMode": "11b\/g\/n",
                        "ext-ch": "NONE"
                },
                {
                        "channel": "6",
                        "ssid": "bpa_intern",
                        "bssid": "00:1a:8c:98:e7:6e",
                        "authentication": "AES",
                        "encryption": "WPA2",
                        "signalStrength": "0",
                        "wirelessMode": "11b\/g\/n",
                        "ext-ch": "NONE"
                },
                {
                        "channel": "6",
                        "ssid": "BPA_Chromecast",
                        "bssid": "00:1a:8c:98:e7:6f",
                        "authentication": "TKIPAES",
                        "encryption": "WPA1PSKWPA2PSK",
                        "signalStrength": "0",
                        "wirelessMode": "11b\/g\/n",
                        "ext-ch": "NONE"
                },
                {
                        "channel": "11",
                        "ssid": "bpa_intern",
                        "bssid": "00:1a:8c:7e:a1:ac",
                        "authentication": "AES",
                        "encryption": "WPA2",
                        "signalStrength": "42",
                        "wirelessMode": "11b\/g\/n",
                        "ext-ch": "NONE"
                },
                {
                        "channel": "11",
                        "ssid": "BPA_Chromecast",
                        "bssid": "00:1a:8c:7e:a1:ad",
                        "authentication": "TKIPAES",
                        "encryption": "WPA1PSKWPA2PSK",
                        "signalStrength": "42",
                        "wirelessMode": "11b\/g\/n",
                        "ext-ch": "NONE"
                },
                {
                        "channel": "11",
                        "ssid": "bpa_guest",
                        "bssid": "00:1a:8c:7e:a1:ab",
                        "authentication": "AES",
                        "encryption": "WPA2PSK",
                        "signalStrength": "42",
                        "wirelessMode": "11b\/g\/n",
                        "ext-ch": "NONE"
                }
        ]
}"""

jObject =json.loads(data)
print jObject

for i in jObject['results']:
    print i["bssid"], " - ", i["signalStrength"], " - ",  i["ssid"]
