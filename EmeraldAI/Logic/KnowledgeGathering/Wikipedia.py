#!/usr/bin/python
# -*- coding: utf-8 -*-
import wikipedia
import re
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import *
from EmeraldAI.Logic.Logger import *

class Wikipedia(object):
    __metaclass__ = Singleton

    def __init__(self):
        wikipedia.set_lang(Config().Get("DEFAULT", "CountryCode2Letter"))


    def GetSummary(self, term, fallback = True, trimBrackets=True):
        summary = None
        try:
            try:
                #wikipedia.summary(query, sentences=0, chars=0, auto_suggest=True, redirect=True)
                summary = wikipedia.summary(term.title(), 0, 0, False, True)
            except wikipedia.exceptions.DisambiguationError as e:
                FileLogger().Error("Wikipedia Line 22: DisambiguationError: {0}".format(e))
                if fallback:
                    topics = wikipedia.search(e.options[0])
                    for i, topic in enumerate(topics):
                        summary = wikipedia.summary(topic)
                        break

            if summary is None or len(summary) < 5:
                return None

            if(trimBrackets):
                summary = re.sub("[\(\[].*?[\)\]][,.;\s]", "", summary)
            return summary
        except Exception as e:
            FileLogger().Error("Wikipedia Line 36: Exception: {0}".format(e))
            return None


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

        if page is None:
            return None

        return page.images
