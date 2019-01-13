#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import Config

class ParallelWheels(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.MappingRange = Config().GetInt("Robot.Movement", "MappingRange")


    def Rotate(self, cw=True, velocity=1):
        result = "{0}|{1}|0"
        value = int(round(velocity * self.MappingRange))
        if(cw):
            return result.format(value, value * -1)
        return result.format(value * -1, value)


    def Move(self, angle, velocity=1):
        if (abs(angle) > 90 and abs(angle) != 180):
            return ""

        if (abs(angle) == 180):
            result = "-{0}|-{1}|0"
            angle = 0
        else:
            result = "{0}|{1}|0"

        cw = True if (angle > 0) else False
        percent = 100 * (90 - abs(angle)) / 90

        reducedValue = int(round(velocity * self.MappingRange * percent / 100))
        value = int(round(velocity * self.MappingRange))

        if(cw):
            return result.format(value, reducedValue)
        return result.format(reducedValue, value)
