#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')


module_name = "EmeraldAI.Logic.LocationProcessing.WiFiFingerprinting"
class_name = "WiFiFingerprinting"
function_name = "PredictLocation"



from EmeraldAI.Logic.Conversation.Action import Action
a = Action()

x = a.CallFunction(module_name, class_name, function_name)

instance = a.CreateClass(module_name, class_name)

print x
percent = 100 / sum(x.values())
for key, value in x.iteritems():
    print "{0}: {1:.2f}%".format(instance.GetLocationName(key), (value * percent))


exit(1)

"""
module = __import__(module_name)
print module
class_ = getattr(module, class_name)
instance = class_()
"""

import importlib
module = importlib.import_module(module_name)
MyClass = getattr(module, class_name)
instance = MyClass()

method = getattr(instance, function_name)
x = method()
print x
percent = 100 / sum(x.values())
for key, value in x.iteritems():
    print "{0}: {1:.2f}%".format(instance.GetLocationName(key), (value * percent))



class Foo(object):
	def write(self):
		print "Hello Foo()"

my_cls = Foo()
method_name = "write"
method = None
try:
    method = getattr(my_cls, method_name)
except AttributeError:
    raise NotImplementedError("Class `{}` does not implement `{}`".format(my_cls.__class__.__name__, method_name))

method()

