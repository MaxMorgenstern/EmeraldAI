#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
from os.path import dirname, abspath, join, isfile

pidfileFormat = "{0}.pid"

def Create(name):
    pid = str(os.getpid())
    filePath = join(abspath(dirname(sys.argv[0])), pidfileFormat.format(name))
    file(filePath, 'w').write(pid)

def Remove(name):
    filePath = join(abspath(dirname(sys.argv[0])), pidfileFormat.format(name))
    os.unlink(filePath)

def HasPid(name):
    filePath = join(abspath(dirname(sys.argv[0])), pidfileFormat.format(name))

    if isfile(filePath):
        return True
    return False
