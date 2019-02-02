#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta

from EmeraldAI.Config.Config import Config

class TimeTable(object):

    def __init__(self, name):
        self.__Timetable = {}

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        for day in days:
            conf = Config().GetList(name, "TimeFrom{0}".format(day))
            self.__Timetable[day] = [int(conf[0]), int(conf[1])]


    def IsActive(self):
        today = datetime.now()
        todayName = today.strftime('%a')

        yesterday = datetime.today() - timedelta(1)
        yesterdayName = yesterday.strftime('%a')

        if (self.__Timetable[yesterdayName] is not None):
            yesterdayFrom = self.__Timetable[yesterdayName][0]
            yesterdayDuration = self.__Timetable[yesterdayName][1]
            yesterdayTo = (yesterdayFrom + yesterdayDuration) % 24

            if (self.__inBetweenTime(0, yesterdayTo, datetime.now().hour)):
                return True

        if (self.__Timetable[todayName] is not None):
            todayFrom = self.__Timetable[todayName][0]
            todayDuration = self.__Timetable[todayName][1]
            todayTo = (todayFrom + todayDuration) % 24

            if (self.__inBetweenTime(todayFrom, todayTo, datetime.now().hour)):
                return True

        return False


    def __inBetweenTime(self, fromHour, toHour, current):
        if fromHour < toHour:
            return current >= fromHour and current < toHour
        else: #Over midnight
            return current >= fromHour or current < toHour         
