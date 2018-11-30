#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import datetime

from EmeraldAI.Logic.Memory.Entity import Entity as EntityMemory

class BaseObject(object):
    def toJSON(self):
        return json.dumps(self, default=self.toJSONDefault, sort_keys=True, indent=4)
    
    def toJSONDefault(self, value):
        if isinstance(value, datetime.date):
            return dict(year=value.year, month=value.month, day=value.day, hour=value.hour, minute=value.minute, second=value.second)
        else:
            return value.__dict__

    def toDict(self, prefix = ""):
        return {(prefix+key).title():value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}

    def appendIfNotNone(self, parent, child):
        if child is not None:
            parent.append(child)

    def Init(self, dict):
        vars(self).update(dict)

    def SaveObject(self):
        EntityMemory().Set(self.__class__.__name__, self.toJSON())

    # maxAge in seconds - default = 60 seconds
    def LoadObject(self, maxAge=60):
        obj = type(self)()
        dataString = EntityMemory().GetString(self.__class__.__name__, maxAge)
        if dataString is None:
            return obj

        obj.Init(json.loads(dataString))
        return obj
