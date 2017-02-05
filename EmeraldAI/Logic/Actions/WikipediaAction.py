#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.KnowledgeGathering.Wikipedia import Wikipedia as wiki
from EmeraldAI.Config.Config import *

class WikipediaAction(object):
    __metaclass__ = Singleton

    __minCharBeforeTrim = 200
    __maxCharToNewLine = 300

    def __init__(self):
        self.__minCharBeforeTrim = Config().GetInt("Action.Wikipedia", "MinCharBeforeTrim") # 200
        self.__maxCharToNewLine = Config().GetInt("Action.Wikipedia", "MaxCharToNewLine") # 300


    def ProcessArticle(self, PipelineArgs):
        result = wiki().GetSummary(PipelineArgs.InputWithoutBasewords)

        # TODO - on no result trim stopwords and try again
        # TODO - no result at all response

        dotIndex = result.find('.', self.__minCharBeforeTrim)
        newLineIndex = result.find('n\\', self.__minCharBeforeTrim)

        if(newLineIndex > 0 and newLineIndex <= self.__maxCharToNewLine):
            trimmedResult = result[:newLineIndex+1]
        elif(dotIndex > 0):
            trimmedResult = result[:dotIndex+1]
        else:
            trimmedResult = result

        return {'Input':PipelineArgs.InputWithoutBasewords, 'Result':trimmedResult, 'ResultType':'string'}

    def ProcessImages(self, PipelineArgs):
        result = wiki().GetImages(PipelineArgs.InputWithoutBasewords)
        return {'Input':PipelineArgs.InputWithoutBasewords, 'Result':result, 'ResultType':'image'}
