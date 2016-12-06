#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom import minidom
xmldoc = minidom.parse('German-standalone.aiml')
category = xmldoc.getElementsByTagName('category')
print(len(category))

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

f = open('myfile.txt','w')

def printfile(file, quantifyer, text):
	file.write("{0} {1}\n".format(quantifyer, text))

for group in category:
    printfile(f, "Q:", getText(group.getElementsByTagName('pattern')[0].childNodes))

    randomNode = group.getElementsByTagName('template')[0].getElementsByTagName('random')
    if(len(randomNode) > 0):
    	liNode = randomNode[0].getElementsByTagName('li')
        for node in liNode:
        	printfile(f, "A:", getText(node.childNodes))
    else:
        printfile(f, "A:", getText(group.getElementsByTagName('template')[0].childNodes))
    printfile(f, "", "")
f.close()

# s.attributes['name'].value
