#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')

from EmeraldAI.Config.Config import *

male =  Config().Get("DEFAULT", "FormalFormOfAddressMale")
female = Config().Get("DEFAULT", "FormalFormOfAddressFemale")

print male.format("Porzelt")
print female.format("Porzelt")
