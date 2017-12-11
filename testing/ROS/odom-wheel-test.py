#!/usr/bin/env python
from __future__ import division

import math

wheelDiameter = 70 # mm
wheelRange = 220 # mm
wheelBaseline = 100 # distance between wheels in mm

encoderTicksPerRevelation = 20

wheelDistancePerTickLeft = math.pi * wheelDiameter / encoderTicksPerRevelation
wheelDistancePerTickRight = math.pi * wheelDiameter / encoderTicksPerRevelation

clicksLeft = 1
distanceLeft = clicksLeft * wheelDistancePerTickLeft

clicksRight = 2
distanceRight = clicksRight * wheelDistancePerTickRight



distance = (distanceRight + distanceLeft) / 2
rotation = (distanceLeft - distanceRight) / wheelBaseline

print wheelDistancePerTickLeft
print distanceLeft, distanceRight
print distance, rotation


