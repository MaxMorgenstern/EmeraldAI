#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from collections import namedtuple


class BaseObject(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def JSONtoObject(self):
		return json.loads(self, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    def toDict(self, prefix = ""):
    	return {(prefix+key).title():value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}

    def appendIfNotNone(self, parent, child):
        if child is not None:
            parent.append(child)
