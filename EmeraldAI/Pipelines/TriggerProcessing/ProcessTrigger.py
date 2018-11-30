#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.NLP.SentenceResolver import SentenceResolver
from EmeraldAI.Entities.User import User
from EmeraldAI.Entities.ContextParameter import ContextParameter
from EmeraldAI.Config.Config import *

import random
import re

class ProcessTrigger(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.__DefaultLanguage = Config().Get("DEFAULT", "Language")


    def ProcessCategory(self, category, language=None):
        if language is None:
            language = self.__DefaultLanguage

        user = User().LoadObject()
        # TODO - add language to user...

        sentenceList = SentenceResolver().GetSentenceByCategory(category, language, (user.Admin or user.Trainer))

        contextParameter = ContextParameter().LoadObject(240)
        contextParameterDict = contextParameter.GetParameterDictionary()

        calculationResult = SentenceResolver().CalculateRequirement(sentenceList, contextParameterDict)
        sentenceList = calculationResult["sentenceList"]

        responseID = random.choice(sentenceList.keys())

        responseString = sentenceList[responseID].GetSentenceString(user.Formal)

        keywords = re.findall(r"\{(.*?)\}", responseString)
        for keyword in keywords:
            if keyword.title() in contextParameterDict:
                replaceword = contextParameterDict[keyword.title()]
                if replaceword is None or replaceword == "Unknown":
                    replaceword = ""
                responseString = responseString.replace("{{{0}}}".format(keyword.lower()), str(replaceword))
            else:
                responseString = responseString.replace("{{{0}}}".format(keyword.lower()), "")

        return responseString


