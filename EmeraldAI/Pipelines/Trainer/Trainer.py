#!/usr/bin/python
# -*- coding: utf-8 -*-
from EmeraldAI.Logic.Singleton import Singleton
from EmeraldAI.Config.Config import Config
from EmeraldAI.Entities.User import User
from EmeraldAI.Logic.Trainer.DialogTrainer import DialogTrainer
from EmeraldAI.Entities.ContextParameter import ContextParameter
from EmeraldAI.Logic.Logger import FileLogger


class Trainer(object):
    __metaclass__ = Singleton


    def __init__(self):
        self.__trainData = Config().GetBoolean("Trainer", "Enabled") # True

    def Process(self, PipelineArgs):
        if not self.__trainData or not PipelineArgs.TrainConversation:
            return False

        context = ContextParameter().LoadObject()
        if len(context.History) == 0:
            return False

        FileLogger().Info("Trainer, Process(), Train Sentence")
        user = User().LoadObject()
        try:
            DialogTrainer().TrainSentence(context.History[-1]["Response"], PipelineArgs.Normalized, PipelineArgs.Language, user.Name)
        except Exception as e:
            FileLogger().Error("Trainer, Process(), Error on training sentence: {0}".format(e))

        return True
