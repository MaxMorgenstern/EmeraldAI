#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

pidfileFormat = "{0}.pid"

def Create(name):
	pid = str(os.getpid())
	filePath = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), pidfileFormat.format(name))
	file(filePath, 'w').write(pid)

def Remove(name):
	filePath = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), pidfileFormat.format(name))
	os.unlink(filePath)

def HasPid(name):
	filePath = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), pidfileFormat.format(name))

	if os.path.isfile(filePath):
	    return True
	return False
