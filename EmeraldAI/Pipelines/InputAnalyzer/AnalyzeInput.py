#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton


class AnalyzeInput(object):
    __metaclass__ = Singleton


    def Process(self, PipelineArgs):
        return PipelineArgs
