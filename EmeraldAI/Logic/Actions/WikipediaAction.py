#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.KnowledgeGathering.Wikipedia import Wikipedia as wiki
import textwrap

class WikipediaAction(object):
    __metaclass__ = Singleton

    # TODO - move to config
    __minCharBeforeTrim = 200
    __maxCharBeforeTrim = 300


    def ProcessArticle(self, PipelineArgs):
        result = wiki().GetSummary(PipelineArgs.InputWithoutBasewords)

        dotIndex = result.find('.', self.__minCharBeforeTrim)
        newLineIndex = result.find('n\\', self.__minCharBeforeTrim)

        if(newLineIndex > 0 and newLineIndex <= self.__maxCharBeforeTrim):
            trimmedResult = result[:newLineIndex+1]
        elif(dotIndex > 0):
            trimmedResult = result[:dotIndex+1]
        else:
            trimmedResult = result

        return {'Input':PipelineArgs.InputWithoutBasewords, 'Result':trimmedResult, 'ResultType':'string'}

    def ProcessImages(self, PipelineArgs):
        result = wiki().GetImages(PipelineArgs.InputWithoutBasewords)
        return {'Input':PipelineArgs.InputWithoutBasewords, 'Result':result, 'ResultType':'image'}
