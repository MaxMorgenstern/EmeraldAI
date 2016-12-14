#!/usr/bin/env python

from scapy.all import *

ap_list = []

def PacketHandler(pkt) :

  if pkt.haslayer(Dot11) :
		if pkt.type == 0 and pkt.subtype == 8 :
			if pkt.addr2 not in ap_list :
				ap_list.append(pkt.addr2)
				print "AP MAC: %s with SSID: %s " %(pkt.addr2, pkt.info)


sniff(iface="mon0", prn = PacketHandler)


"""
import socket
rawSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.htons(0x0003))
rawSocket.bind(("mon0", 0x0003))
ap_list = set()
while True :
	pkt = rawSocket.recvfrom(2048)[0]
	if pkt[26] == "\x80" :
		if pkt[36:42] not in ap_list  and ord(pkt[63]) > 0:
			ap_list.add(pkt[36:42])
			print "SSID: %s  AP MAC: %s" % (pkt[64:64 +ord(pkt[63])], pkt[36:42].encode('hex'))
"""


"""
import os
import sys
import nmap                         # import nmap.py
import time
import re

try:
    nm = nmap.PortScanner()         # instance of nmap.PortScanner
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(0)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(0)

hostList = []
gracePeriod = 7

def seek():                         # function to scan the network
    curHosts = []
    nm.scan(hosts = '192.168.1.0/24', arguments = '-n -sP -PE -T5')
    # executes a ping scan

    localtime = time.asctime(time.localtime(time.time()))
    print('============ {0} ============'.format(localtime))
    # system time

    for host in nm.all_hosts():
        try:
            mac = nm[host]['addresses']['mac']
            vendor = nm[host]['vendor'][mac]
        except:
            vendor = mac = 'unknown'

        curHosts.append((host,mac,vendor,gracePeriod))

    updateHostList(curHosts)

    for host in hostList:
        print('Scan report for %s\nMAC Address: %s (%s)' % (host[0], host[1], host[2]))

    print('Number of hosts: ' + str(len(hostList)))
    return len(hostList)                # returns count

def updateHostList(curHosts):
    global hostList
    if hostList == []:
        hostList = curHosts
    else:
        hostList = [(x[0],x[1],x[2],x[3]-1) for x in hostList]

        # only the hosts that were new in this iteration
        newList = [(x[0],x[1],x[2],x[3]) for x in curHosts if not (any(x[0]==y[0] for y in hostList))]

        for host in newList:
            hostList.append(host)

        for host in hostList:
            if any(host[0] == y[0] for y in curHosts):
                hostList[hostList.index(host)] = (host[0],host[1],host[2],gracePeriod)

        for host in hostList:
            if host[3] <= 0:
                hostList.remove(host)



def beep():                         # no sound dependency
    print('\a')

if __name__ == '__main__':
    old_count = new_count = seek()

    startCounter = gracePeriod

    # are there any new hosts?
    while (new_count <= old_count) or startCounter >= 0:
        startCounter -= 1
        time.sleep(1)               # increase to slow down the speed
        old_count = new_count
        new_count = seek()

    # DANGER!!!
    print('OHSHITOHSHITOHSHITOHSHITOHSHIT!')
    beep()
"""
