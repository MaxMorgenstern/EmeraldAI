#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import platform
import codecs
from os.path import dirname, abspath

from cachetools import cached

RootPath = dirname(dirname(dirname(dirname(abspath(__file__))))).rstrip(os.sep) + os.sep
EmeraldPath = dirname(dirname(dirname(abspath(__file__)))).rstrip(os.sep) + os.sep
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
