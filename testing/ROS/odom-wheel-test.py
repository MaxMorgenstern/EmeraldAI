#!/usr/bin/env python
from __future__ import division

import math

wheelDiameter = 5
wheelBaseline = 20 # distance between wheels

encoderTicksPerRevelation = 20

wheelDistancePerTickLeft = math.pi * wheelDiameter / encoderTicksPerRevelation
wheelDistancePerTickRight = math.pi * wheelDiameter / encoderTicksPerRevelation

clicksLeft = 10
distanceLeft = clicksLeft * wheelDistancePerTickLeft

clicksRight = 10
distanceRight = clicksLeft * wheelDistancePerTickRight



distance = (distanceRight + distanceLeft) / 2
rotation = (distanceLeft - distanceRight) / wheelBaseline



