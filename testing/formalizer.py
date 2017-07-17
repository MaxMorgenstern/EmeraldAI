#!/usr/bin/python
# -*- coding: utf-8 -*-

def replaceablePart(data):
	output = data.lower().replace("du", "sie")

	return output

print "Tippe 'ende' oder 'beenden' zum beenden!"

loop = True
while(loop):
    data = raw_input("Input: ")
    if(len(data) == 0):
    	continue
    if(data.lower() == 'ende' or data.lower() == 'beenden'):
        loop = False
        continue

    print replaceablePart(data)



"""



"""

