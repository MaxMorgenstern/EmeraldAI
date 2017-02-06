#!/usr/bin/python
# -*- coding: utf-8 -*-
import wikipedia
import re
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import *

class Wikipedia(object):
    __metaclass__ = Singleton

    def __init__(self):
        wikipedia.set_lang(Config().Get("DEFAULT", "CountryCode2Letter"))

    def GetSummary(self, term, fallback = False, trimBrackets=True):
        summary = None
        try:
            #wikipedia.summary(query, sentences=0, chars=0, auto_suggest=True, redirect=True)
            summary = wikipedia.summary(term, 0, 0, False, True)
        except:
            if fallback:
                topics = wikipedia.search(term)
                for i, topic in enumerate(topics):
                    summary = wikipedia.summary(topic)
                    break

        if summary == None or len(summary) < 5:
            return None

        if(trimBrackets):
            summary = re.sub("[\(\[].*?[\)\]] ", "", summary)
        return summary


    def GetImages(self, term, fallback = False):
        page = None
        try:
            page = wikipedia.WikipediaPage(term)
        except:
            if fallback:
                topics = wikipedia.search(term)
                for i, topic in enumerate(topics):
                    page = wikipedia.WikipediaPage(topic)
                    break

        if page == None:
            return None

        return page.images
