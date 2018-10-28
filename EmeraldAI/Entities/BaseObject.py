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

    def Init(self, dict):
        vars(self).update(dict)

    def SaveObject(self):
        EntityMemory().Set(self.__class__.__name__, self.toJSON())

    # maxAge in seconds - default = 60 seconds
    def LoadObject(self, maxAge=60):
        dataString = EntityMemory().GetString(self.__class__.__name__, maxAge)
        if dataString is None:
            return None

        obj = type(self)()
        obj.Init(json.loads(dataString))
