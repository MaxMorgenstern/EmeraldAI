#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

wheel1 = 150
wheel2 = 270
wheel3 = 30


def GetSpeed(wheel, angle):
    return -round(math.cos(math.radians(wheel - angle)), 4)

def Map(speed):
    return int(round(speed * 255))


a = 0
print GetSpeed(wheel1, a), Map(GetSpeed(wheel1, a))
print GetSpeed(wheel2, a), Map(GetSpeed(wheel2, a))
print GetSpeed(wheel3, a), Map(GetSpeed(wheel3, a))



print "OR"

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from EmeraldAI.Logic.Movement.Omniwheel import Omniwheel

for x in range(360):
    print x, Omniwheel().Move(x)

print Omniwheel().Rotate(False, 0.5)
