#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import *
from EmeraldAI.Entities.User import User
from EmeraldAI.Logic.Trainer.DialogTrainer import *
from EmeraldAI.Entities.Context import Context
from EmeraldAI.Logic.Logger import *


class Trainer(object):
    __metaclass__ = Singleton


    def __init__(self):
        self.__trainData = Config().GetBoolean("Trainer", "Enabled") # True

    def Process(self, PipelineArgs):
    	if not self.__trainData or not PipelineArgs.TrainConversation:
    		return False

    	if len(Context().History) == 0:
    		return False

        FileLogger().Info("Trainer, Process(), Train Sentence")
    	DialogTrainer().TrainSentence(Context().History[-1].Response, PipelineArgs.Normalized, PipelineArgs.Language, User().Name)

    	return True
