#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.KnowledgeGathering.Wikipedia import Wikipedia as wiki
from EmeraldAI.Config.Config import Config

class WikipediaAction(object):
    __metaclass__ = Singleton

    __minCharBeforeTrim = 200
    __maxCharToNewLine = 300

    def __init__(self):
        self.__minCharBeforeTrim = Config().GetInt("Action.Wikipedia", "MinCharBeforeTrim") # 200
        self.__maxCharToNewLine = Config().GetInt("Action.Wikipedia", "MaxCharToNewLine") # 300


    def ProcessArticle(self, PipelineArgs):
        result = wiki().GetSummary(PipelineArgs.BasewordTrimmedInput)
        inputString = PipelineArgs.BasewordTrimmedInput

        if result is None or len(result) == 0:
            result = wiki().GetSummary(PipelineArgs.FullyTrimmedInput)
            inputString = PipelineArgs.FullyTrimmedInput

        if result is None or len(result) == 0:
            return {'Input':inputString, 'Result':None, 'ResultType':'Error'}

        dotIndex = result.find('.', self.__minCharBeforeTrim)
        newLineIndex = result.find('\n', self.__minCharBeforeTrim)

        if(newLineIndex > 0 and newLineIndex <= self.__maxCharToNewLine):
            trimmedResult = result[:newLineIndex+1]
        elif(dotIndex > 0):
            trimmedResult = result[:dotIndex+1]
        else:
            trimmedResult = result

        return {'Input':inputString, 'Result':trimmedResult, 'ResultType':'string'}

    def ProcessImages(self, PipelineArgs):
        result = wiki().GetImages(PipelineArgs.BasewordTrimmedInput)
        return {'Input':PipelineArgs.BasewordTrimmedInput, 'Result':result, 'ResultType':'image'}
