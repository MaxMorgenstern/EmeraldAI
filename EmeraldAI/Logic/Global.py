#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

class Global(object):
    #Path = os.path.dirname(os.path.abspath(__file__)).rstrip("/") + "/"
    Path = os.path.dirname(os.path.abspath(sys.argv[0])).rstrip("/") + "/"
