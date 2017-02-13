#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import *
from EmeraldAI.Entities.User import User
from EmeraldAI.Logic.Trainer.DialogTrainer import *


class Trainer(object):
    __metaclass__ = Singleton


    def __init__(self):
        self.__trainData = Config().GetBoolean("Trainer", "Enabled") # True

    def Process(self, PipelineArgs):
    	if not self.__trainData or not PipelineArgs.TrainConversation:
    		return False

    	if len(PipelineArgs.History) == 0
    		return False

    	DialogTrainer().TrainSentence(PipelineArgs.History[-1].Response, PipelineArgs.Normalized, PipelineArgs.Language, User().Name):

    	# TODO

    	return True


