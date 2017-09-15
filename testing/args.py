#!/usr/bin/env python

import sys


print len(sys.argv)
print sys.argv

if len(sys.argv) >= 2 :
	print "Arg 1: ", sys.argv[1]
