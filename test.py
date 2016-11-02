#!/usr/bin/python
# -*- coding: utf-8 -*-

from EmeraldAI.Entities.Word import *
from EmeraldAI.Logic.Global import *
from EmeraldAI.Logic.NLP import *


x = Word("hi")

print x.toJSON()


print Global().RootPath

print Global().EmeraldPath


print NLP().DetectLanguage("Hallo, dies ist ein nötiger Test!")
