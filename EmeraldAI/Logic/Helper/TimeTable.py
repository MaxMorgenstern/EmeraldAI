#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta

class TimeTable(object):

    def __init__(self, name):
        self.__Timetable = []
    
    def IsActive(self):
        today = datetime.now()
        todayName = today.strftime('%a')

        yesterday = datetime.today() - timedelta(1)
        yesterdayName = yesterday.strftime('%a')

        if (self.__Timetable[todayName] is not None):
            yesterdayFrom = self.__Timetable[yesterdayName].From
            yesterdayDuration = self.__Timetable[yesterdayName].Duration
            yesterdayTo = (yesterdayFrom + yesterdayDuration) % 24

            if (self.__inBetweenTime(0, yesterdayTo, datetime.now().hour)):
                return True

        if (self.__Timetable[todayName] is not None):
            todayFrom = self.__Timetable[todayName].From
            todayDuration = self.__Timetable[todayName].Duration
            todayTo = (todayFrom + todayDuration) % 24

            if (self.__inBetweenTime(todayFrom, todayTo, datetime.now().hour)):
                return True

        return False


    def __inBetweenTime(self, fromHour, toHour, current):
        if fromHour < toHour:
            return current >= fromHour and current <= toHour
        else: #Over midnight
            return current >= fromHour or current <= toHour         
