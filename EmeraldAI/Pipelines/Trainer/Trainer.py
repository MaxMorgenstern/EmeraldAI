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

        context = Context().LoadObject()
        if len(context.History) == 0:
            return False

        FileLogger().Info("Trainer, Process(), Train Sentence")
        user = User().LoadObject()
        try:
            DialogTrainer().TrainSentence(context.History[-1]["Response"], PipelineArgs.Normalized, PipelineArgs.Language, user.Name)
        except Exception as e:
            FileLogger().Error("Trainer, Process(), Error on training sentence: {0}".format(e))

        return True
