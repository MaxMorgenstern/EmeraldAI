#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import platform

RootPath = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))).rstrip("/") + "/"
EmeraldPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).rstrip("/") + "/"
OS = platform.system().lower() # darwin (=osx) - windows - linux
