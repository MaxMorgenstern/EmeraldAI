#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import Config

class Omniwheel(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.wheel = [None]*6

        for i in range(6):
            angle = Config().GetInt("Robot.Movement", "Wheel{0}Degree".format(i+1))
            if(angle>=0):
                self.wheel[i] = angle

        self.MappingRange = Config().GetInt("Robot.Movement", "MappingRange")
        self.FrontDegree = 0
        self.LeftFrontAngleID = 0
        self.RightFrontAngleID = 1
        self.MaxMoveAngle = 45


    def Rotate(self, cw=True, velocity=1):
        result = ""
        for wheel in self.wheel:
            if wheel is None:
                continue
            if(cw):
                result += "|{0}".format(self.Map(velocity))
            else:
                result += "|-{0}".format(self.Map(velocity))
        return result.strip('|')


    def Move(self, angle, velocity=1, straveOnly=False):
        result = []

        for wheel in self.wheel:
            if wheel is None:
                continue
            result.append(self.Map(self.CalculatePower(wheel, angle, velocity)))

        if (not straveOnly and abs(angle) - self.FrontDegree) < self.MaxMoveAngle:
            percent = 100 * ((self.MaxMoveAngle * 2) - abs(angle)) / (self.MaxMoveAngle * 2)

            if (angle>0):
                result[self.RightFrontAngleID] = int(round(result[0] * percent / 100))
            else:
                result[self.LeftFrontAngleID] = int(round(result[1] * percent / 100))

        return "|".join(str(x) for x in result)


    def CalculatePower(self, wheelAngle, angle, velocity=1):
        return -round(velocity * math.cos(math.radians(wheelAngle - angle)), 4)

    def Map(self, speed):
        return int(round(speed * self.MappingRange))
