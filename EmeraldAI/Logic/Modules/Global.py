#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import platform
import codecs

from cachetools import cached

RootPath = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))).rstrip(os.sep) + os.sep
EmeraldPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).rstrip(os.sep) + os.sep
OS = platform.system().lower()  # darwin (=osx) - windows - linux

class OperatingSystem():
    Linux = "linux"
    Windows = "windows"
    OSX = "darwin"

@cached(cache={})
def ReadDataFile(foldername, filename, utf8=True):
    script_dir = os.path.join(EmeraldPath, "Data", foldername, filename)
    if utf8:
        return [line.rstrip('\n').rstrip('\r') for line in codecs.open(script_dir, encoding='utf-8')]
    else:
        return [line.rstrip('\n').rstrip('\r') for line in open(script_dir)]

def EnsureDirectoryExists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
