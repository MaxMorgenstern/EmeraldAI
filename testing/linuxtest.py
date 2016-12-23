#!/usr/bin/python
# -*- coding: utf-8 -*-
import itertools

cmd = """
iwlist scan
wlan0     Scan completed :
          Cell 01 - Address: 64:66:B3:4C:81:EC
                    ESSID:"Puschi"
                    Protocol:IEEE 802.11bgn
                    Mode:Master
                    Frequency:2.412 GHz (Channel 1)
                    Encryption key:on
                    Bit Rates:150 Mb/s
                    Extra:wpa_ie=dd1a0050f20101000050f20202000050f2040050f20201000050f202
                    IE: WPA Version 1
                        Group Cipher : TKIP
                        Pairwise Ciphers (2) : CCMP TKIP
                        Authentication Suites (1) : PSK
                    Extra:rsn_ie=30180100000fac020200000fac04000fac020100000fac020000
                    IE: IEEE 802.11i/WPA2 Version 1
                        Group Cipher : TKIP
                        Pairwise Ciphers (2) : CCMP TKIP
                        Authentication Suites (1) : PSK
                    IE: Unknown: DD990050F204104A0001101044000102103B00010310470010000000000000100000006466B34C81101021000754502D4C494E4B10230009544C2D57523734304E10240003342E3010420003312E301054000800060050F204000110110019576972656C65737320526F7574657220544C2D57523734304E100800020086103C000101104900140024E26002000101600000020001600100020001
                    Quality=20/100  Signal level=44/100
          Cell 02 - Address: F8:04:2E:A6:E4:F8
                    ESSID:"UPC244554972"
                    Protocol:IEEE 802.11bgn
                    Mode:Master
                    Frequency:2.437 GHz (Channel 6)
                    Encryption key:on
                    Bit Rates:144 Mb/s
                    Extra:rsn_ie=30180100000fac020200000fac02000fac040100000fac020000
                    IE: IEEE 802.11i/WPA2 Version 1
                        Group Cipher : TKIP
                        Pairwise Ciphers (2) : TKIP CCMP
                        Authentication Suites (1) : PSK
                    IE: Unknown: DDA70050F204104A0001101044000102103B00010310470010BC329E001DD811B28601F8042EA6E4F81021001A43656C656E6F20436F6D6D756E69636174696F6E2C20496E632E1023001743656C656E6F20576972656C65737320415020322E344710240006434C313830301042000831323334353637381054000800060050F20400011011000C43656C656E6F4150322E344710080002210C103C0001011049000600372A000120
                    Quality=77/100  Signal level=72/100
          Cell 03 - Address: 54:FA:3E:7C:29:67
                    ESSID:"Aperture Science Laboratories"
                    Protocol:IEEE 802.11bgn
                    Mode:Master
                    Frequency:2.467 GHz (Channel 12)
                    Encryption key:on
                    Bit Rates:144 Mb/s
                    Extra:rsn_ie=30180100000fac020200000fac02000fac040100000fac020000
                    IE: IEEE 802.11i/WPA2 Version 1
                        Group Cipher : TKIP
                        Pairwise Ciphers (2) : TKIP CCMP
                        Authentication Suites (1) : PSK
                    IE: Unknown: DDA70050F204104A0001101044000102103B00010310470010BC329E001DD811B2860154FA3E7C29671021001A43656C656E6F20436F6D6D756E69636174696F6E2C20496E632E1023001743656C656E6F20576972656C65737320415020322E344710240006434C313830301042000831323334353637381054000800060050F20400011011000C43656C656E6F4150322E3447100800024388103C0001011049000600372A000120
                    Quality=100/100  Signal level=100/100
          Cell 04 - Address: FA:8F:CA:93:9B:2D
                    ESSID:""
                    Protocol:IEEE 802.11bgn
                    Mode:Master
                    Frequency:2.467 GHz (Channel 12)
                    Encryption key:off
                    Bit Rates:72 Mb/s
                    Quality=20/100  Signal level=96/100
          Cell 05 - Address: 44:32:C8:A1:65:32
                    ESSID:"UPC1472707"
                    Protocol:IEEE 802.11bgn
                    Mode:Master
                    Frequency:2.462 GHz (Channel 11)
                    Encryption key:on
                    Bit Rates:144 Mb/s
                    Extra:wpa_ie=dd1a0050f20101000050f20202000050f2040050f20201000050f202
                    IE: WPA Version 1
                        Group Cipher : TKIP
                        Pairwise Ciphers (2) : CCMP TKIP
                        Authentication Suites (1) : PSK
                    Extra:rsn_ie=30180100000fac020200000fac04000fac020100000fac020c00
                    IE: IEEE 802.11i/WPA2 Version 1
                        Group Cipher : TKIP
                        Pairwise Ciphers (2) : CCMP TKIP
                        Authentication Suites (1) : PSK
                    Quality=100/100  Signal level=56/100
          Cell 06 - Address: 46:32:C8:A1:65:34
                    ESSID:"Unitymedia WifiSpot"
                    Protocol:IEEE 802.11bgn
                    Mode:Master
                    Frequency:2.462 GHz (Channel 11)
                    Encryption key:on
                    Bit Rates:144 Mb/s
                    Extra:rsn_ie=30180100000fac020200000fac04000fac020100000fac010c00
                    IE: IEEE 802.11i/WPA2 Version 1
                        Group Cipher : TKIP
                        Pairwise Ciphers (2) : CCMP TKIP
                        Authentication Suites (1) : 802.1x
                    Quality=82/100  Signal level=47/100
          Cell 07 - Address: BC:8C:CD:EB:51:98
                    ESSID:"UPC242839629"
                    Protocol:IEEE 802.11bgn
                    Mode:Master
                    Frequency:2.462 GHz (Channel 11)
                    Encryption key:on
                    Bit Rates:144 Mb/s
                    Extra:rsn_ie=30180100000fac020200000fac02000fac040100000fac020000
                    IE: IEEE 802.11i/WPA2 Version 1
                        Group Cipher : TKIP
                        Pairwise Ciphers (2) : TKIP CCMP
                        Authentication Suites (1) : PSK
                    IE: Unknown: DDA70050F204104A0001101044000102103B00010310470010BC329E001DD811B28601BC8CCDEB51981021001A43656C656E6F20436F6D6D756E69636174696F6E2C20496E632E1023001743656C656E6F20576972656C65737320415020322E344710240006434C313830301042000831323334353637381054000800060050F20400011011000C43656C656E6F4150322E344710080002210C103C0001011049000600372A000120
                    Quality=100/100  Signal level=44/100
          Cell 08 - Address: 88:25:2C:2C:9F:4A
                    ESSID:"WLAN-2C9F33"
                    Protocol:IEEE 802.11bgn
                    Mode:Master
                    Frequency:2.462 GHz (Channel 11)
                    Encryption key:on
                    Bit Rates:270 Mb/s
                    Extra:wpa_ie=dd1a0050f20101000050f20202000050f2020050f20401000050f202
                    IE: WPA Version 1
                        Group Cipher : TKIP
                        Pairwise Ciphers (2) : TKIP CCMP
                        Authentication Suites (1) : PSK
                    Extra:rsn_ie=30180100000fac020200000fac02000fac040100000fac020000
                    IE: IEEE 802.11i/WPA2 Version 1
                        Group Cipher : TKIP
                        Pairwise Ciphers (2) : TKIP CCMP
                        Authentication Suites (1) : PSK
                    IE: Unknown: DD130050F204104A0001101044000102103C000103
                    Quality=50/100  Signal level=23/100

lo        Interface doesn't support scanning.
"""


def group_separator(line):
    return line=='\n'

ssid = None
bssid = None
signal = None
for key, group in itertools.groupby(cmd, group_separator):
    line = ''.join(str(e) for e in group)
    line = line.strip()
    if(len(line) > 2):
        splitLine = line.split(":", 1)
        if line.startswith("Cell "):
            ssid = splitLine[1].strip()
            bssid = None
            signal = None

        if line.startswith("ESSID"):
            bssid = splitLine[1].strip()

        if line.startswith("Quality"):
            signalDetails = line.split("  ", 1)


            quality = (signalDetails[0].split("=", 1)[1].replace("/100", "")) # quality
            level = (signalDetails[1].split("=", 1)[1].replace("/100", "")) # signal level

            print "Quality: " + quality
            print "Level: " + level


        if(ssid != None and bssid != None and signal != None):
            print ssid + " - " + bssid + " - " + signal
            bssid = None
            signal = None
            #store data
