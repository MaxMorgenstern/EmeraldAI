#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import itertools

cmd = """
Zusammenfassung der Drahtlossysteminformationen
(Zeit: 20.12.2016 07:42:33 Mitteleurop„ische Zeit)


=======================================================================
============================ TREIBER ANZEIGEN =========================
=======================================================================


Schnittstellenname: WLAN

    Treiber                   : Intel(R) Dual Band Wireless-AC 7260
    Hersteller                : Intel Corporation
    Anbieter                  : Intel
    Datum                     : 03.05.2016
    Version                   : 18.33.3.2
    INF-Datei                 : C:\Windows\INF\oem28.inf
    Dateien                   : 2 insgesamt
                                C:\Windows\system32\DRIVERS\Netwbw02.sys
                                C:\Windows\system32\DRIVERS\Netwfw02.dat
    Typ                       : Wi-Fi-Treiber (Ursprungsversion)
    Untersttzte Funktypen    : 802.11b 802.11g 802.11n 802.11a 802.11ac
    FIPS 140-2-Modus wird untersttzt: Ja
    802.11w Management Frame Protection wird untersttzt: Ja
    Untersttzte gehostete Netzwerke  : Ja
    Im Infrastrukturmodus untersttzte Authentifizierung und untersttztes Verschlsselungsverfahren:
                                Offen           Keine
                                Offen           WEP-40bit
                                Offen           WEP-104bit
                                Offen           WEP
                                Firmenweiter WPATKIP
                                Firmenweiter WPACCMP
                                WPA-Personal    TKIP
                                WPA-Personal    CCMP
                                WPA2-Enterprise TKIP
                                WPA2-Enterprise CCMP
                                WPA2-Personal   TKIP
                                WPA2-Personal   CCMP
                                Offen           Herstellerdefiniert
                                HerstellerdefiniertHerstellerdefiniert
    Im Ad-hoc-Modus untersttzte Authentifizierung und untersttztes Verschlsselungsverfahren:
                                Offen           Keine
                                Offen           WEP-40bit
                                Offen           WEP-104bit
                                Offen           WEP
                                WPA2-Personal   CCMP
    IHV-Dienst vorhanden      : Ja
    IHV-Adapter-OUI           : [00 80 86], Typ: [00]
    IHV-Erweiterbarkeits-DLL-Pfad: C:\Windows\System32\IWMSSvc.dll
    IHV UI-Erweiterbarkeits-ClSID: {1bf6cb2d-2ae0-4879-a7aa-a75834fbd0e3}
    IHV-Diagnose-CLSID     : {00000000-0000-0000-0000-000000000000}
    Untersttzte drahtlose Anzeige: Ja (Grafiktreiber: Ja, Wi-Fi-Treiber: Ja)


=======================================================================
========================= SCHNITTSTELLEN ANZEIGEN =====================
=======================================================================


Es ist 1 Schnittstelle auf dem System vorhanden:

    Name                   : WLAN
    Beschreibung           : Intel(R) Dual Band Wireless-AC 7260
    GUID                   : 129f3750-dcc9-462b-bc46-dd3ff1ded1c0
    Physische Adresse      : 28:b2:bd:89:f2:9c
    Status                 : getrennt
    Funkstatus           : Hardware Ein
                             Software Ein

    Status des gehosteten Netzwerks  : Nicht gestartet


=======================================================================
=========================== SHOW HOSTED NETWORK =======================
=======================================================================


Einstellungen fr das gehostete Netzwerk
-----------------------
    Modus                   : Zugelassen
    SSID-Name              : "lenovo"
    Maximale Clientanzahl  : 100
    Authentifizierung         : WPA2-Personal
    Verschlsselung                 : CCMP

Status des gehosteten Netzwerks
---------------------
    Status                 : Nicht gestartet


=======================================================================
========================== EINSTELLUNGEN ANZEIGEN =====================
=======================================================================


Drahtlos-LAN-Einstellungen
---------------------
    Blockierte Netzwerke in sichtbarer Netzwerkliste anzeigen: Nein
    Nur Gruppenrichtlinienprofile fr Netzwerke verwenden, die mit Gruppenrichtlinien konfiguriert werden: Nein
    Modus fr das gehostete Netzwerk im WLAN-Dienst zugelassen: Ja

    Freigegebene Benutzeranmeldeinformationen fr die Netzwerkauthentifizierung zulassen: Ja
    Blockierungszeitraum: Nicht konfiguriert.

    Die Logik fr die automatische Konfiguration ist an der Schnittstelle "WLAN" aktiviert.
    Zuf„llige MAC-Adressen auf Schnittstelle WLAN nicht verfgbar


=======================================================================
============================= FILTER ANZEIGEN =========================
=======================================================================


Zulassungsliste auf dem System (Gruppenrichtlinie)
---------------------------------------------------
    <Kein>

Zulassungsliste auf dem System (Benutzer)
------------------------------------------
    <Kein>

Blockierungsliste auf dem System (Gruppenrichtlinie)
----------------------------------------------------
    <Kein>

Blockierungsliste auf dem System (Benutzer)
-------------------------------------------
    <Kein>


=======================================================================
================== ERSTELLEN ALLER BENUTZER ANZEIGEN ==================
=======================================================================


Jeder Benutzer kann alle Benutzerprofile erstellen.


=======================================================================
============================ PROFILE ANZEIGEN =========================
=======================================================================


Profile auf Schnittstelle WLAN:

Gruppenrichtlinienprofile (schreibgeschtzt)
---------------------------------
    <Kein>

Benutzerprofile
---------------
    Profil fr alle Benutzer : bpa_intern


=======================================================================
========================== PROFILNAMEN ANZEIGEN =======================
=======================================================================


Das Profil "bpa_intern" auf Schnittstelle WLAN:
=======================================================================

Angewendet: Profil fr alle Benutzer

Profilinformationen
-------------------
    Version                : 1
    Typ                    : Drahtlos-LAN
    Name                   : bpa_intern
    Steuerungsoptionen     :
        Verbindungsmodus   : Automatisch verbinden
        Netzwerkbertragung  : Verbinden, nur wenn dieses Netzwerk bertr„gt
        Automatisch wechseln         : Nicht zu anderen Netzwerken wechseln.
        MAC-Randomisierung  : Deaktiviert

Konnektivit„tseinstellungen
---------------------
    Anzahl von SSIDs        : 1
    SSID-Name              : "bpa_intern"
    Netzwerktyp            : Infrastruktur
    Funktyp                : [ Beliebiger Funktyp ]
    Herstellererweiterung          : Nicht vorhanden

Sicherheitseinstellungen
------------------------
    Authentifizierung         : WPA2-Enterprise
    Verschlsselung                 : CCMP
    Sicherheitsschlssel   : Nicht vorhanden
    802.1X                 : Aktiviert
    EAP-Typ                : Microsoft: Geschtztes EAP (PEAP)
    802.1X Anmeldeinformationen zur Auth. : Benutzeranmeldeinformationen
    Anmeldeinformationen konfiguriert : Nein
    Benutzerinformationen zwischenspeichern : Ja

Kosteneinstellungen
-------------------
    Kosten                 : Uneingeschr„nkt
    šberlastet              : Nein
    Datenlimit bald erreicht: Nein
    šber Datenlimit         : Nein
    Roaming                : Nein
    Kostenquelle            : Standard


=======================================================================
===================== NETZEORKMODUS=BSSID ANZEIGEN ====================
=======================================================================


Schnittstellenname : WLAN
Momentan sind 3 Netzwerke sichtbar.

SSID 1 : bpa_intern
    Netzwerktyp             : Infrastruktur
    Authentifizierung       : WPA2-Enterprise
    Verschlsselung         : CCMP
    BSSIDD 1                 : 00:1a:8c:7e:a1:e2
         Signal             : 70%
         Funktyp         : 802.11n
         Kanal           : 6
         Basisraten (MBit/s)   : 6.5 16 19.5 117
         Andere Raten (MBit/s) : 18 19.5 24 36 39 48 54 156
    BSSIDD 2                 : 00:1a:8c:7e:a1:ac
         Signal             : 83%
         Funktyp         : 802.11n
         Kanal           : 1
         Basisraten (MBit/s)   : 6.5 16 19.5 117
         Andere Raten (MBit/s) : 18 19.5 24 36 39 48 54 156

SSID 2 : BPA_Chromecast
    Netzwerktyp             : Infrastruktur
    Authentifizierung       : WPA2-Personal
    Verschlsselung         : CCMP
    BSSIDD 1                 : 00:1a:8c:7e:a1:e3
         Signal             : 68%
         Funktyp         : 802.11n
         Kanal           : 6
         Basisraten (MBit/s)   : 6.5 16 19.5 117
         Andere Raten (MBit/s) : 18 19.5 24 36 39 48 54 156
    BSSIDD 2                 : 00:1a:8c:7e:a1:ad
         Signal             : 85%
         Funktyp         : 802.11n
         Kanal           : 1
         Basisraten (MBit/s)   : 6.5 16 19.5 117
         Andere Raten (MBit/s) : 18 19.5 24 36 39 48 54 156
    BSSIDD 3                 : 00:1a:8c:98:e7:6f
         Signal             : 33%
         Funktyp         : 802.11n
         Kanal           : 6
         Basisraten (MBit/s)   : 6.5 16 19.5 117
         Andere Raten (MBit/s) : 18 19.5 24 36 39 48 54 156

SSID 3 : bpa_guest
    Netzwerktyp             : Infrastruktur
    Authentifizierung       : WPA2-Personal
    Verschlsselung         : CCMP
    BSSIDD 1                 : 00:1a:8c:7e:a1:e1
         Signal             : 70%
         Funktyp         : 802.11n
         Kanal           : 6
         Basisraten (MBit/s)   : 6.5 16 19.5 117
         Andere Raten (MBit/s) : 18 19.5 24 36 39 48 54 156
    BSSIDD 2                 : 00:1a:8c:7e:a1:ab
         Signal             : 83%
         Funktyp         : 802.11n
         Kanal           : 1
         Basisraten (MBit/s)   : 6.5 16 19.5 117
         Andere Raten (MBit/s) : 18 19.5 24 36 39 48 54 156
    BSSIDD 3                 : 00:1a:8c:98:e7:6d
         Signal             : 33%
         Funktyp         : 802.11n
         Kanal           : 6
         Basisraten (MBit/s)   : 6.5 16 19.5 117
         Andere Raten (MBit/s) : 18 19.5 24 36 39 48 54 156


=======================================================================
======================= SCHNITTSTELLENFUNKTIONEN ANZEIGEN ===================
=======================================================================


Funktionen des Drahtlossystems
----------------------------
    Die Anzahl der Antennen fr die 802.11-Drahtlosverbindung (Wert nicht verfgbar)

    Max. Anzahl von Kan„len, die das Ger„t gleichzeitig untersttzt (kein Wert verfgbar)

    Koexistenzuntersttzung                        : Unbekannt


Eigenschaften von Drahtlosger„ten
----------------------------

Schnittstellenname: WLAN

    WDI-Version (Windows)                       : 0.0.0.0

    WDI-Version (IHV)                           : 0.0.0.0

    Firmwareversion                            :

    Station                                     : Untersttzt

    Softwarezugriffspunkt                                    : Untersttzt

    Netzwerkberwachungsmodus                        : Untersttzt

    Wi-Fi Direct-Ger„t                         : Untersttzt

    Wi-Fi Direct-GO                             : Untersttzt

    Wi-Fi Direct-Client                         : Untersttzt

    Geschtzte Management Frames                 : Untersttzt

    DOT11k-Nachbarbericht                      : Unbekannt

    Ermittlung von ANQP-Dienstinformationen          : Nicht untersttzt

    Aktionsrahmen                                : Nicht untersttzt

    Antennendiversit„t                           : Unbekannt

    IBSS                                        : Untersttzt

    Promiscuous Mode                            : Untersttzt

    P2P-Ger„teermittlung                        : Nicht untersttzt

    Ermittlung von P2P-Dienstnamen                  : Nicht untersttzt

    Ermittlung von P2P-Dienstinformationen                  : Nicht untersttzt

    P2P-Hintergrundermittlung                    : Nicht untersttzt

    P2P GO fr 5 GHz                             : Unbekannt

    FIPS                                        : Untersttzt

    Direktverbindung                             : Untersttzt

    Dx-Standby-NLO                              : Untersttzt

    Erweiterte Channel-Switch-Ankndigung        : Unbekannt

    Zurcksetzen der Funktionsebene                      : Nicht untersttzt

    Zurcksetzung der Plattformebene                        : Nicht untersttzt

    Zurcksetzen auf Busebene                             : Nicht untersttzt

    MAC-Randomisierung                           : Nicht untersttzt

    Schnellbergang                             : Nicht untersttzt

    MU-MIMO                                     : Unbekannt

    Miracast-Senke                               : Unbekannt

    BSS-šbergang (802.11v)                    : Unbekannt

    IHV-Erweiterbarkeitsmodul konfiguriert         : Untersttzt

    Anzahl der Tx-Signalstr”me                : 0

    Anzahl der Rx-Signalstr”me                : 0

    Anzahl der gleichzeitig untersttzten Kan„le     : 2

    Anzahl von P2P-GO-Ports                          : 1

    Anzahl der P2P-Clientports                      : 1

    Maximale P2P-Mobile-AP-Clients                   : 10

    Maximal untersttzte ANQP-Dienstankndigungen   : 0

    Koexistenzuntersttzung                        : Unbekannt
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
        if line.startswith("SSID "):
            ssid = splitLine[1].strip()
            bssid = None
            signal = None

        if line.startswith("BSSIDD "):
            bssid = splitLine[1].strip()

        if line.startswith("Signal "):
            signal = splitLine[1].strip()

        if(ssid != None and bssid != None and signal != None):
            print ssid + " - " + bssid + " - " + signal
            bssid = None
            signal = None
            #store data


# SSID
# BSSIDD
# Signal
