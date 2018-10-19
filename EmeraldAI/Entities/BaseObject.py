#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from EmeraldAI.Logic.Memory.Entity import Entity as EntityMemory

class BaseObject(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def toDict(self, prefix = ""):
        return {(prefix+key).title():value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}

    def appendIfNotNone(self, parent, child):
        if child is not None:
            parent.append(child)

    def SaveObject(self):
        EntityMemory().Set(self.__class__.__name__, self.toJSON())

    def LoadObject(self, maxAge=None):
        dataString = EntityMemory().GetString(self.__class__.__name__, maxAge)
        if dataString is None:
            return None
        #return json.loads(dataString, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        return json.loads(dataString, object_hook=type(self))
