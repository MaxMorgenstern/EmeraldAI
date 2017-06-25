#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Logic.KnowledgeGathering.Math import Math as m


class MathAction(object):
    __metaclass__ = Singleton


    def ProcessEquation(self, PipelineArgs):

    	returnInput = m().CleanTerm(PipelineArgs.Input)
    	returnResult = m().Calculate(PipelineArgs.Input)

        return {'Input':returnInput, 'Result':returnResult, 'ResultType':'string'}
