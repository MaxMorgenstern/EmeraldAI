#!/usr/bin/python
# -*- coding: utf-8 -*-
import json


class BaseObject(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def toDict(self):
    	return {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}
