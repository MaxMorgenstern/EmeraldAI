#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import platform

def GetFileCreationDate(filePath):
    if platform.system() == 'Windows':
        return os.path.getctime(filePath)
    else:
        stat = os.stat(filePath)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime
