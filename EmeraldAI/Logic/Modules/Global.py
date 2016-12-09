#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import platform

RootPath = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))).rstrip("/") + "/"
EmeraldPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).rstrip("/") + "/"
OS = platform.system().lower()  # darwin (=osx) - windows - linux

def ReadDataFile(foldername, filename):
    script_dir = EmeraldPath + \
        "Data/{0}/{1}".format(foldername, filename)
    return [line.rstrip('\n').rstrip('\r') for line in open(script_dir)]
