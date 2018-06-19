#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

def RadianToDegree(rad):
    return (rad * 4068) / 71.0

def DegreeToRadian(deg):
    return (deg * 71) / 4068.0

def Cast(targetType, val, default=None):
    try:
        return targetType(val)
    except (ValueError, TypeError):
        return default