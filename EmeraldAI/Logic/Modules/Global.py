#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import platform

RootPath = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))).rstrip(os.sep) + os.sep
EmeraldPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).rstrip(os.sep) + os.sep
OS = platform.system().lower()  # darwin (=osx) - windows - linux

def ReadDataFile(foldername, filename):
    script_dir = EmeraldPath + \
        "Data" + os.set + foldername + os.sep + filename
    return [line.rstrip('\n').rstrip('\r') for line in open(script_dir)]
