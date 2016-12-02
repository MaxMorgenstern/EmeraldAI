#!/usr/bin/python
# -*- coding: utf-8 -*-
import wikipedia
import re
from EmeraldAI.Logic.Singleton import Singleton


class Wikipedia(object):
    __metaclass__ = Singleton

    def __init__(self):
        wikipedia.set_lang("de")

    def GetSummary(self, term, trimBrackets=True):
        summary = wikipedia.summary(term)
        if(trimBrackets):
            summary = re.sub("[\(\[].*?[\)\]] ", "", summary)
        return summary

    def GetImages(self, term):
        page = wikipedia.WikipediaPage(term)
        return page.images
